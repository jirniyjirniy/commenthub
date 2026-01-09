<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import type { Comment } from "../types/comments";
import { useAuthStore } from "../stores/authStore";
import CommentForm from "./CommentForm.vue";
import { filesApi } from "../api/files";

interface Props {
  comment: Comment;
  isDetail?: boolean;
}

const props = defineProps<Props>();

const router = useRouter();
const authStore = useAuthStore();
const showReplyForm = ref(false);
const isHovered = ref(false);

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString();
};

const goToDetail = () => {
  if (!props.isDetail) {
    router.push(`/comments/${props.comment.id}`);
  }
};

const toggleReplyForm = () => {
  showReplyForm.value = !showReplyForm.value;
};

const handleReplySuccess = () => {
  showReplyForm.value = false;
};

const selectedImage = ref<string | null>(null);

const openImage = (url: string) => {
  selectedImage.value = url;
};

const closeImage = () => {
  selectedImage.value = null;
};

const selectedText = ref<string | null>(null);
const isTextLoading = ref(false);

const openText = async (url: string) => {
  isTextLoading.value = true;
  selectedText.value = "";
  try {
    const text = await filesApi.getTextFile(url);
    selectedText.value = text;
  } catch (e) {
    console.error(e);
    selectedText.value = "Failed to load text content.";
  } finally {
    isTextLoading.value = false;
  }
};

const closeText = () => {
  selectedText.value = null;
};

// Random gradient for avatar
const avatarGradients = [
  "from-purple-400 to-pink-500",
  "from-blue-400 to-indigo-500",
  "from-green-400 to-teal-500",
  "from-orange-400 to-red-500",
  "from-pink-400 to-rose-500",
  "from-indigo-400 to-purple-500",
];

const getAvatarGradient = (username: string) => {
  const index = username.charCodeAt(0) % avatarGradients.length;
  return avatarGradients[index];
};
</script>

<template>
  <div class="flex flex-col gap-4">
    <div
      class="group relative bg-gradient-to-br from-gray-50 to-white dark:from-gray-800 dark:to-gray-900 rounded-2xl shadow-lg border border-gray-200/50 dark:border-gray-700/50 transition-all duration-300 overflow-hidden"
      :class="{ 'cursor-pointer hover:shadow-2xl hover:-translate-y-1': !isDetail }"
      @click="goToDetail"
      @mouseenter="isHovered = true"
      @mouseleave="isHovered = false"
    >
      <!-- Gradient accent bar -->
      <div
        class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 transition-all duration-300"
        :class="{ 'h-1.5': isHovered }"
      ></div>

      <!-- Glowing effect on hover -->
      <div
        class="absolute inset-0 bg-gradient-to-br from-purple-500/0 to-pink-500/0 transition-all duration-500 group-hover:from-purple-500/5 group-hover:to-pink-500/5"
      ></div>

      <div class="relative p-6">
        <!-- Header -->
        <div class="flex justify-between items-start mb-4">
          <div class="flex items-start gap-4">
            <!-- Avatar with gradient -->
            <div
              class="relative w-12 h-12 rounded-xl bg-gradient-to-br shadow-lg transition-transform duration-300 group-hover:scale-110 group-hover:shadow-xl flex-shrink-0"
              :class="getAvatarGradient(comment.user.username)"
            >
              <div
                class="absolute inset-0 rounded-xl flex items-center justify-center text-white font-bold text-lg"
              >
                {{ comment.user.username.charAt(0).toUpperCase() }}
              </div>
              <!-- Online indicator -->
              <div
                class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white dark:border-gray-800 animate-pulse"
              ></div>
            </div>

            <!-- User info -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <h3
                  class="font-bold text-gray-900 dark:text-white text-lg truncate"
                >
                  {{ comment.user.username }}
                </h3>
                <span
                  class="px-2 py-0.5 rounded-full bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-purple-700 dark:text-purple-300 text-xs font-semibold"
                >
                  Member
                </span>
              </div>
              <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                {{ comment.user.email }}
              </p>
            </div>
          </div>

          <!-- Timestamp -->
          <div
            class="flex items-center gap-2 text-xs text-gray-400 dark:text-gray-500 bg-gray-100/50 dark:bg-gray-800/50 px-3 py-1.5 rounded-lg"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                clip-rule="evenodd"
              />
            </svg>
            {{ formatDate(comment.created_at) }}
          </div>
        </div>

        <!-- Content -->
        <div
          class="prose dark:prose-invert max-w-none mb-4 text-gray-700 dark:text-gray-200 leading-relaxed comment-content"
          v-html="comment.text"
        ></div>

        <!-- Attachments -->
        <div
          v-if="comment.attachments && comment.attachments.length > 0"
          class="mt-4 mb-4 flex flex-wrap gap-3"
          @click.stop
        >
          <div v-for="attachment in comment.attachments" :key="attachment.id">
            <!-- Image -->
            <div
              v-if="attachment.media_type === 'image'"
              @click="openImage(attachment.file)"
              class="group/img relative w-28 h-28 rounded-xl overflow-hidden border-2 border-gray-200 dark:border-gray-700 hover:border-purple-400 dark:hover:border-purple-500 transition-all duration-300 cursor-pointer shadow-md hover:shadow-xl"
            >
              <img
                :src="attachment.file"
                class="w-full h-full object-cover transition-transform duration-300 group-hover/img:scale-110"
                alt="Attachment"
              />
              <div
                class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover/img:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-2"
              >
                <span class="text-white text-xs font-medium">Click to view</span>
              </div>
            </div>

            <!-- Text File -->
            <button
              v-else-if="attachment.file.toLowerCase().endsWith('.txt')"
              @click="openText(attachment.file)"
              class="group/file flex items-center gap-3 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 px-4 py-3 rounded-xl border-2 border-purple-200 dark:border-purple-800 hover:border-purple-400 dark:hover:border-purple-600 transition-all duration-300 shadow-md hover:shadow-lg hover:-translate-y-0.5"
            >
              <div
                class="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center shadow-md"
              >
                <svg
                  class="w-5 h-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <div class="text-left">
                <p
                  class="text-sm font-semibold text-purple-700 dark:text-purple-300"
                >
                  Text File
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  Click to read
                </p>
              </div>
            </button>

            <!-- Other File -->
            <a
              v-else
              :href="attachment.file"
              target="_blank"
              class="group/file flex items-center gap-3 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 px-4 py-3 rounded-xl border-2 border-blue-200 dark:border-blue-800 hover:border-blue-400 dark:hover:border-blue-600 transition-all duration-300 shadow-md hover:shadow-lg hover:-translate-y-0.5"
            >
              <div
                class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-400 to-indigo-500 flex items-center justify-center shadow-md"
              >
                <svg
                  class="w-5 h-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <div class="text-left">
                <p class="text-sm font-semibold text-blue-700 dark:text-blue-300">
                  Download
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Open file</p>
              </div>
            </a>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-between mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div
            v-if="!isDetail"
            class="flex items-center gap-2 text-purple-600 dark:text-purple-400 font-medium text-sm group-hover:gap-3 transition-all duration-300"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z"
              />
              <path
                d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z"
              />
            </svg>
            <span>View Thread</span>
            <svg
              class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>

          <button
            v-if="isDetail && authStore.isAuthenticated"
            @click.stop="toggleReplyForm"
            class="px-4 py-2 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium text-sm transition-all duration-300 shadow-md hover:shadow-lg hover:-translate-y-0.5 flex items-center gap-2"
          >
            <svg
              class="w-4 h-4 transition-transform duration-300"
              :class="{ 'rotate-45': showReplyForm }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!showReplyForm"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            {{ showReplyForm ? "Cancel" : "Reply" }}
          </button>
        </div>

        <!-- Reply Form -->
        <Transition
          enter-active-class="transition-all duration-300 ease-out"
          enter-from-class="opacity-0 -translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition-all duration-200 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-4"
        >
          <div v-if="showReplyForm" class="mt-6" @click.stop>
            <CommentForm :reply-to="comment.id" :on-success="handleReplySuccess" />
          </div>
        </Transition>
      </div>
    </div>

    <!-- Nested Replies -->
    <div
      v-if="isDetail && comment.replies && comment.replies.length > 0"
      class="pl-6 border-l-2 border-gradient-to-b from-purple-300 to-pink-300 dark:from-purple-700 dark:to-pink-700 ml-6 space-y-4"
    >
      <CommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :is-detail="true"
      />
    </div>

    <!-- Image Modal -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="selectedImage"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
        @click="closeImage"
      >
        <button
          @click="closeImage"
          class="absolute top-6 right-6 w-12 h-12 rounded-full bg-white/10 backdrop-blur-lg border border-white/20 text-white hover:bg-white/20 transition-all duration-300 flex items-center justify-center hover:rotate-90"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
        <img
          :src="selectedImage"
          class="max-w-full max-h-full object-contain rounded-2xl shadow-2xl"
          @click.stop
        />
      </div>
    </Transition>

    <!-- Text Modal -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="selectedText !== null || isTextLoading"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
        @click="closeText"
      >
        <div
          class="bg-white dark:bg-gray-900 rounded-2xl max-w-3xl w-full max-h-[80vh] flex flex-col shadow-2xl border border-gray-200 dark:border-gray-700"
          @click.stop
        >
          <div
            class="flex justify-between items-center p-6 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20"
          >
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center shadow-md"
              >
                <svg
                  class="w-5 h-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <h3 class="text-xl font-bold text-gray-900 dark:text-white">
                Text Content
              </h3>
            </div>
            <button
              @click="closeText"
              class="w-10 h-10 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-300 flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <div class="p-6 overflow-auto flex-1">
            <div
              v-if="isTextLoading"
              class="flex flex-col justify-center items-center h-32 gap-3"
            >
              <svg
                class="animate-spin h-10 w-10 text-purple-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              <p class="text-sm text-gray-500 dark:text-gray-400">Loading...</p>
            </div>
            <pre
              v-else
              class="whitespace-pre-wrap font-mono text-sm text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800 p-4 rounded-xl"
              >{{ selectedText }}</pre
            >
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.comment-content :deep(a) {
  color: #9333ea;
  background-color: #faf5ff;
  border-radius: 0.25rem;
  padding: 0.125rem 0.375rem;
  text-decoration: none;
  transition: all 0.2s;
}

.dark .comment-content :deep(a) {
  color: #c084fc;
  background-color: rgba(88, 28, 135, 0.2);
}

.comment-content :deep(a):hover {
  text-decoration: underline;
  background-color: #f3e8ff;
}

.dark .comment-content :deep(a):hover {
  background-color: rgba(88, 28, 135, 0.4);
}

.comment-content :deep(strong) {
  font-weight: 700;
  color: #111827;
}

.dark .comment-content :deep(strong) {
  color: #ffffff;
}

.comment-content :deep(em) {
  font-style: italic;
}

.comment-content :deep(code) {
  background-color: #f3f4f6;
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
  font-family: ui-monospace, monospace;
  font-size: 0.875rem;
}

.dark .comment-content :deep(code) {
  background-color: #1f2937;
}
</style>