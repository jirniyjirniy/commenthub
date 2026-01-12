<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue";
import { useCommentsStore } from "../stores/commentsStore";
import { useAuthStore } from "../stores/authStore";
import { commentsApi } from "../api/comments";
import { useEditor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Link from "@tiptap/extension-link";
import ReCaptcha from "./ReCaptcha.vue";
import { type RecaptchaExposed } from "./ReCaptcha.vue";

const props = defineProps<{
  replyTo?: number;
  onSuccess?: () => void;
}>();

const store = useCommentsStore();
const authStore = useAuthStore();
const error = ref("");
const previewHtml = ref("");
const showPreview = ref(false);
const isPreviewLoading = ref(false);
const files = ref<File[]>([]);
const fileInput = ref<HTMLInputElement | null>(null);
const recaptchaToken = ref("");
const recaptchaRef = ref<RecaptchaExposed | null>(null);

const editor = useEditor({
  content: "",
  extensions: [
    StarterKit,
    Link.configure({
      openOnClick: false,
      HTMLAttributes: {
        class: "text-purple-600 dark:text-purple-400 hover:underline",
      },
    }),
  ],
  editorProps: {
    attributes: {
      class:
        "prose prose-sm dark:prose-invert max-w-none focus:outline-none min-h-[120px] p-4 text-gray-900 dark:text-gray-100",
    },
  },
});

const setLink = () => {
  const previousUrl = editor.value?.getAttributes("link").href;
  const url = window.prompt("URL", previousUrl);

  if (url === null) return;

  if (url === "") {
    editor.value?.chain().focus().extendMarkRange("link").unsetLink().run();
    return;
  }

  editor.value
    ?.chain()
    .focus()
    .extendMarkRange("link")
    .setLink({ href: url })
    .run();
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files) {
    const newFiles = Array.from(target.files);
    const allowedTypes = ["text/plain", "image/jpeg", "image/png", "image/gif"];

    const validFiles = newFiles.filter((file) => {
      const isSizeValid = file.name.endsWith(".txt")
        ? file.size <= 100 * 1024
        : file.size <= 5 * 1024 * 1024;
      const isTypeValid =
        allowedTypes.includes(file.type) || file.name.endsWith(".txt");
      return isSizeValid && isTypeValid;
    });

    if (validFiles.length !== newFiles.length) {
      alert(
        "Some files were skipped. Max TXT size: 100KB. Max JPG, PNG, GIF size: 5MB. Allowed types: TXT, JPG, PNG, GIF."
      );
    }

    if (files.value.length + validFiles.length > 5) {
      alert("You can only attach up to 5 files.");
      return;
    }

    files.value = [...files.value, ...validFiles];
  }
  if (target.value) target.value = "";
};

const getFilePreview = (file: File) => {
  if (file.type.startsWith("image/")) {
    return URL.createObjectURL(file);
  }
  return null;
};

const removeFile = (index: number) => {
  files.value.splice(index, 1);
};

// Функция для получения превью
const fetchPreview = async () => {
  // 1. Проверяем наличие текста
  if (!editor.value || editor.value.isEmpty) {
    error.value = "Comment cannot be empty";
    return;
  }

  // 2. УБРАЛИ ПРОВЕРКУ КАПЧИ ЗДЕСЬ
  // Теперь превью доступно всем и не тратит токен

  isPreviewLoading.value = true;
  showPreview.value = true;
  try {
    const rawText = editor.value.getHTML();

    // Передаем пустую строку вместо токена!
    const data = await commentsApi.preview(rawText, "");

    previewHtml.value = data.text;
    error.value = "";
  } catch (e) {
    error.value = "Failed to load preview";
  } finally {
    isPreviewLoading.value = false;
  }
};

const handleSubmit = async () => {
  if (!editor.value || editor.value.isEmpty) {
    error.value = "Comment cannot be empty";
    return;
  }

  // Здесь проверка капчи ОСТАЕТСЯ обязательной
  if (!recaptchaToken.value) {
    error.value = "Please complete the CAPTCHA verification";
    return;
  }

  try {
    const content = editor.value.getHTML();
    await store.addComment(
      content,
      props.replyTo,
      files.value,
      recaptchaToken.value
    );
    editor.value.commands.clearContent();
    files.value = [];
    error.value = "";
    showPreview.value = false;
    previewHtml.value = "";
    recaptchaToken.value = "";
    if (props.onSuccess) {
      props.onSuccess();
    }
    recaptchaRef.value?.reset();
  } catch (e: any) {
    error.value = e.message || "Failed to post comment";
    recaptchaToken.value = "";
  }
};

const onCaptchaVerify = (token: string) => {
  recaptchaToken.value = token;
  error.value = "";
};

const onCaptchaExpired = () => {
  recaptchaToken.value = "";
  error.value = "CAPTCHA expired. Please verify again.";
};

const onCaptchaError = () => {
  recaptchaToken.value = "";
  error.value = "CAPTCHA error. Please try again.";
};

onBeforeUnmount(() => {
  editor.value?.destroy();
});
</script>

<template>
  <div class="w-full">
    <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl dark:shadow-purple-900/50 overflow-hidden ring-1 ring-gray-200/20 dark:ring-purple-500/20">
      <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500"></div>

      <div class="absolute -top-20 -right-20 w-40 h-40 bg-purple-500/10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-20 -left-20 w-40 h-40 bg-pink-500/10 rounded-full blur-3xl"></div>

      <div class="relative p-6">
        <div class="mb-6">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                {{ replyTo ? "Leave a Reply" : "Post a Comment" }}
              </h3>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                as <span class="font-semibold text-purple-600 dark:text-purple-400">{{ authStore.user?.username }}</span>
              </p>
            </div>
          </div>
        </div>

        <div class="mb-4 bg-gray-50 dark:bg-gray-900/50 rounded-xl border-2 border-transparent dark:border-transparent overflow-hidden focus-within:border-purple-500 focus-within:ring-4 focus-within:ring-purple-500/20 transition-all duration-300 shadow-inner dark:shadow-none">
          <div
            v-if="editor"
            class="flex items-center gap-1 p-3 border-b-2 border-gray-200/50 dark:border-gray-700/30 bg-white/50 dark:bg-gray-800/50"
          >
            <button
              type="button"
              @click="editor.chain().focus().toggleBold().run()"
              :class="{ 'bg-purple-100 dark:bg-purple-900/50 text-purple-600 dark:text-purple-400': editor.isActive('bold') }"
              class="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-all duration-200 font-bold"
              title="Bold"
            >
              B
            </button>
            <button
              type="button"
              @click="editor.chain().focus().toggleItalic().run()"
              :class="{ 'bg-purple-100 dark:bg-purple-900/50 text-purple-600 dark:text-purple-400': editor.isActive('italic') }"
              class="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 italic transition-all duration-200"
              title="Italic"
            >
              I
            </button>
            <button
              type="button"
              @click="editor.chain().focus().toggleCode().run()"
              :class="{ 'bg-purple-100 dark:bg-purple-900/50 text-purple-600 dark:text-purple-400': editor.isActive('code') }"
              class="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-mono text-sm transition-all duration-200"
              title="Code"
            >
              &lt;/&gt;
            </button>
            <button
              type="button"
              @click="setLink"
              :class="{ 'bg-purple-100 dark:bg-purple-900/50 text-purple-600 dark:text-purple-400': editor.isActive('link') }"
              class="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-all duration-200"
              title="Link"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
            </button>

            <div class="w-px h-6 bg-gray-300 dark:bg-gray-600 mx-1"></div>

            <button
              type="button"
              @click="triggerFileInput"
              class="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-all duration-200 flex items-center gap-1"
              title="Attach File"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
              </svg>
              <span v-if="files.length > 0" class="text-xs font-semibold">{{ files.length }}</span>
            </button>

            <input
              type="file"
              ref="fileInput"
              multiple
              class="hidden"
              accept="image/jpeg, image/png, image/gif, .txt"
              @change="handleFileChange"
            />
          </div>

          <editor-content :editor="editor" />

          <Transition
            enter-active-class="transition-all duration-300"
            enter-from-class="opacity-0 max-h-0"
            enter-to-class="opacity-100 max-h-96"
            leave-active-class="transition-all duration-200"
            leave-from-class="opacity-100 max-h-96"
            leave-to-class="opacity-0 max-h-0"
          >
            <div
              v-if="files.length > 0"
              class="p-4 border-t-2 border-gray-200/50 dark:border-gray-700/30 bg-white/50 dark:bg-gray-800/50 flex flex-wrap gap-3"
            >
              <div v-for="(file, index) in files" :key="index" class="relative group">
                <div
                  v-if="getFilePreview(file)"
                  class="w-20 h-20 rounded-xl overflow-hidden border-2 border-purple-200/50 dark:border-purple-500/30 shadow-md hover:shadow-lg hover:border-purple-400 dark:hover:border-purple-400 transition-all duration-200"
                >
                  <img
                    :src="getFilePreview(file)!"
                    class="w-full h-full object-cover"
                    :alt="file.name"
                  />
                </div>
                <div
                  v-else
                  class="w-20 h-20 rounded-xl border-2 border-purple-200/50 dark:border-purple-500/30 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-gray-800 dark:to-gray-700 flex items-center justify-center text-xs font-semibold text-gray-600 dark:text-gray-300 text-center p-2 break-all shadow-md hover:shadow-lg hover:border-purple-400 dark:hover:border-purple-400 transition-all duration-200"
                >
                  {{ file.name.split(".").pop()?.toUpperCase() }}
                </div>

                <button
                  type="button"
                  @click="removeFile(index)"
                  class="absolute -top-2 -right-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-full p-1 shadow-lg hover:shadow-xl hover:scale-110 transition-all duration-200"
                >
                  <svg class="w-3 h-3" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </Transition>
        </div>

        <Transition
          enter-active-class="transition-all duration-300 ease-out"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition-all duration-200 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2"
        >
          <div v-if="error" class="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border-2 border-red-200/50 dark:border-red-800/50 rounded-xl flex items-start gap-3">
            <svg class="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
            <p class="text-sm text-red-600 dark:text-red-400 font-medium">{{ error }}</p>
          </div>
        </Transition>

        <div class="mb-4">
          <ReCaptcha
            ref="recaptchaRef"
            @verify="onCaptchaVerify"
            @expired="onCaptchaExpired"
            @error="onCaptchaError"
          />
        </div>

        <Transition
          enter-active-class="transition-all duration-300"
          enter-from-class="opacity-0 max-h-0"
          enter-to-class="opacity-100 max-h-96"
          leave-active-class="transition-all duration-200"
          leave-from-class="opacity-100 max-h-96"
          leave-to-class="opacity-0 max-h-0"
        >
          <div
            v-if="showPreview"
            class="mb-4 p-4 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-gray-900 dark:to-purple-900/20 rounded-xl border-2 border-purple-200/50 dark:border-purple-800/50"
          >
            <div class="flex items-center gap-2 mb-3">
              <svg class="w-4 h-4 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <h4 class="text-sm font-bold text-purple-700 dark:text-purple-300 uppercase tracking-wide">Preview</h4>
            </div>

            <div v-if="isPreviewLoading" class="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-2">
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading preview...
            </div>

            <div v-else>
               <div
                class="preview-content prose prose-sm dark:prose-invert max-w-none text-gray-900 dark:text-gray-100"
                v-html="previewHtml"
              ></div>

              <div v-if="files.length > 0" class="mt-4 pt-4 border-t border-gray-200/50 dark:border-gray-700/50">
                <p class="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-2">Attached files:</p>
                <div class="flex flex-wrap gap-3">
                  <div v-for="(file, index) in files" :key="index" class="relative">
                    <div v-if="getFilePreview(file)" class="w-20 h-20 rounded-xl overflow-hidden border border-purple-200/30 dark:border-purple-700/30 shadow-sm">
                      <img :src="getFilePreview(file)!" class="w-full h-full object-cover" />
                    </div>
                    <div v-else class="w-20 h-20 rounded-xl border border-purple-200/30 dark:border-purple-700/30 bg-purple-50 dark:bg-purple-900/20 flex items-center justify-center text-xs p-1 text-center font-medium text-gray-600 dark:text-gray-300 break-all">
                      {{ file.name.split('.').pop()?.toUpperCase() || 'FILE' }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </Transition>

        <div class="flex justify-end gap-3">
          <button
            type="button"
            @click="fetchPreview"
            class="px-5 py-2.5 bg-white/10 dark:bg-gray-700/50 backdrop-blur-sm border-2 border-white/20 dark:border-purple-500/30 hover:border-purple-500 dark:hover:border-purple-400 text-gray-700 dark:text-gray-200 rounded-xl font-semibold text-sm transition-all duration-300 hover:shadow-lg hover:bg-white/20 dark:hover:bg-gray-600/50 flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            Preview
          </button>

          <button
            type="button"
            @click="handleSubmit"
            :disabled="store.loading"
            class="px-6 py-2.5 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:from-purple-600 hover:via-pink-600 hover:to-blue-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-lg flex items-center gap-2 group"
          >
            <span v-if="store.loading">
              <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            <span>{{ store.loading ? "Posting..." : (replyTo ? "Post Reply" : "Post Comment") }}</span>
            <svg class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.preview-content :deep(a) {
  color: #7c3aed; /* purple-600 */
  background-color: rgba(124, 58, 237, 0.05);
  border-radius: 4px;
  padding: 2px 4px;
  text-decoration: none;
  transition: all 0.2s;
}

.dark .preview-content :deep(a) {
  color: #a78bfa; /* purple-400 */
  background-color: rgba(167, 139, 250, 0.1);
}

.preview-content :deep(a):hover {
  text-decoration: underline;
  background-color: rgba(124, 58, 237, 0.1);
}

.dark .preview-content :deep(a):hover {
  background-color: rgba(167, 139, 250, 0.15);
}
</style>