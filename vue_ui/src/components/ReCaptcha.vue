<script setup lang="ts">
import { ref } from "vue";
import VueRecaptcha from "vue3-recaptcha2";
import { RECAPTCHA_SITE_KEY } from "../config/captcha";

export interface RecaptchaExposed {
  reset: () => void;
}

const emit = defineEmits<{
  verify: [token: string];
  error: [];
  expired: [];
}>();

const loadingTimeout = ref(30000);
const showRecaptcha = ref(true);
const recaptchaRef = ref<InstanceType<typeof VueRecaptcha> | null>(null);
const isVerified = ref(false);

const onVerify = (response: string) => {
  isVerified.value = true;
  emit("verify", response);
};

const onExpired = () => {
  isVerified.value = false;
  emit("expired");
};

const onError = () => {
  isVerified.value = false;
  emit("error");
};

defineExpose({
  reset: () => {
    isVerified.value = false;
    recaptchaRef.value?.reset();
  },
});
</script>

<template>
  <div class="my-4">
    <div class="flex items-start gap-3 p-4 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/10 dark:to-pink-900/10 rounded-xl border-2 border-purple-200 dark:border-purple-800 transition-all duration-300" :class="{ 'border-green-400 dark:border-green-600': isVerified }">
      <div class="flex-shrink-0 mt-1">
        <Transition
          enter-active-class="transition-all duration-300"
          enter-from-class="scale-0 rotate-180"
          enter-to-class="scale-100 rotate-0"
          leave-active-class="transition-all duration-200"
          leave-from-class="scale-100 rotate-0"
          leave-to-class="scale-0 -rotate-180"
        >
          <div v-if="isVerified" class="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div v-else class="w-6 h-6 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
        </Transition>
      </div>

      <div class="flex-1 min-w-0">
        <div class="flex items-center justify-between mb-2">
          <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300">
            Security Verification
          </h4>
          <Transition
            enter-active-class="transition-all duration-300"
            enter-from-class="opacity-0 scale-0"
            enter-to-class="opacity-100 scale-100"
          >
            <span v-if="isVerified" class="px-2 py-0.5 rounded-full bg-green-500 text-white text-xs font-semibold">
              Verified ✓
            </span>
          </Transition>
        </div>

        <vue-recaptcha
          ref="recaptchaRef"
          v-show="showRecaptcha"
          :sitekey="RECAPTCHA_SITE_KEY"
          size="normal"
          theme="light"
          hl="en"
          :loading-timeout="loadingTimeout"
          @verify="onVerify"
          @expire="onExpired"
          @fail="onError"
          @error="onError"
          class="recaptcha-custom"
        >
        </vue-recaptcha>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recaptcha-custom {
  transform: scale(0.95);
  transform-origin: left center;
  transition: transform 0.3s ease;
}

.recaptcha-custom:hover {
  transform: scale(0.97);
}

@media (max-width: 640px) {
  .recaptcha-custom {
    transform: scale(0.85);
  }

  .recaptcha-custom:hover {
    transform: scale(0.87);
  }
}
</style>