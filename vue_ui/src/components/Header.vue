<script setup lang="ts">
import { RouterLink } from "vue-router";
import { useAuthStore } from "../stores/authStore";
import { ref } from "vue";

const authStore = useAuthStore();
const showUserMenu = ref(false);
</script>

<template>
  <header class="relative bg-gradient-to-r from-purple-900 via-indigo-900 to-blue-900 text-white shadow-2xl">
    <!-- Animated background pattern - ТЕПЕРЬ С OVERFLOW HIDDEN ТОЛЬКО НА ДЕКОРАЦИЯХ -->
    <div class="absolute inset-0 overflow-hidden">
      <div
        class="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')]"
      ></div>

      <!-- Gradient overlay -->
      <div
        class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-purple-600/20 to-blue-600/20 animate-gradient-shift"
      ></div>
    </div>

    <div class="relative container mx-auto px-4 py-4 flex justify-between items-center">
      <!-- Logo/Brand -->
      <RouterLink
        to="/"
        class="flex items-center gap-3 group transition-all duration-300 hover:scale-105"
      >
        <div
          class="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400 to-blue-500 flex items-center justify-center shadow-lg group-hover:shadow-purple-500/50 transition-all duration-300 group-hover:rotate-6"
        >
          <svg
            class="w-7 h-7 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
        </div>
        <div>
          <h1
            class="text-2xl font-black bg-gradient-to-r from-purple-300 via-pink-300 to-blue-300 bg-clip-text text-transparent group-hover:from-pink-300 group-hover:via-purple-300 group-hover:to-blue-300 transition-all duration-500"
          >
            CommentsHub
          </h1>
          <p class="text-xs text-purple-200/70 font-medium">Real-time discussions</p>
        </div>
      </RouterLink>

      <!-- Navigation -->
      <nav class="flex items-center gap-6">
        <div v-if="authStore.isAuthenticated" class="flex items-center gap-4">
          <!-- User Info with dropdown -->
          <div class="relative">
            <button
              @click="showUserMenu = !showUserMenu"
              class="flex items-center gap-3 px-4 py-2.5 rounded-xl bg-white/10 backdrop-blur-lg border border-white/20 hover:bg-white/20 transition-all duration-300 group"
            >
              <div
                class="w-9 h-9 rounded-lg bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center font-bold text-sm shadow-lg group-hover:shadow-purple-500/50 transition-all duration-300"
              >
                {{ authStore.user?.username.charAt(0).toUpperCase() }}
              </div>
              <div class="text-left hidden md:block">
                <p class="font-semibold text-sm">{{ authStore.user?.username }}</p>
                <p class="text-xs text-purple-200/70">Online</p>
              </div>
              <svg
                class="w-4 h-4 transition-transform duration-300"
                :class="{ 'rotate-180': showUserMenu }"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            <!-- Dropdown Menu - ТЕПЕРЬ НЕ ОБРЕЗАЕТСЯ -->
            <Transition
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="transform scale-95 opacity-0"
              enter-to-class="transform scale-100 opacity-100"
              leave-active-class="transition duration-150 ease-in"
              leave-from-class="transform scale-100 opacity-100"
              leave-to-class="transform scale-95 opacity-0"
            >
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-56 rounded-xl bg-white/10 backdrop-blur-xl border border-white/20 shadow-2xl overflow-hidden z-50"
              >
                <div class="py-2">
                  <div
                    class="px-4 py-3 border-b border-white/10 bg-gradient-to-r from-purple-500/20 to-pink-500/20"
                  >
                    <p class="text-sm font-semibold">
                      {{ authStore.user?.username }}
                    </p>
                    <p class="text-xs text-purple-200/70">
                      {{ authStore.user?.email }}
                    </p>
                  </div>
                  <button
                    @click="
                      authStore.logout();
                      showUserMenu = false;
                    "
                    class="w-full text-left px-4 py-3 text-sm hover:bg-white/10 transition-colors duration-200 flex items-center gap-3 text-red-300 hover:text-red-200"
                  >
                    <svg
                      class="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                      />
                    </svg>
                    <span class="font-medium">Logout</span>
                  </button>
                </div>
              </div>
            </Transition>
          </div>
        </div>

        <!-- Auth Links -->
        <div v-else class="flex gap-3">
          <RouterLink
            to="/login"
            class="px-5 py-2.5 rounded-xl bg-white/10 backdrop-blur-lg border border-white/20 hover:bg-white/20 transition-all duration-300 font-medium text-sm hover:scale-105 hover:shadow-lg hover:shadow-purple-500/30"
          >
            Login
          </RouterLink>
          <RouterLink
            to="/register"
            class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 transition-all duration-300 font-semibold text-sm hover:scale-105 shadow-lg hover:shadow-purple-500/50"
          >
            Sign Up
          </RouterLink>
        </div>
      </nav>
    </div>

    <!-- Loading indicator -->
    <Transition
      enter-active-class="transition-all duration-300"
      enter-from-class="opacity-0 h-0"
      enter-to-class="opacity-100 h-1"
      leave-active-class="transition-all duration-300"
      leave-from-class="opacity-100 h-1"
      leave-to-class="opacity-0 h-0"
    >
      <div
        v-if="authStore.isLoading"
        class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 animate-pulse overflow-hidden"
      >
        <div
          class="h-full w-full bg-gradient-to-r from-transparent via-white/50 to-transparent animate-shimmer"
        ></div>
      </div>
    </Transition>

    <!-- Error notification -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="transform translate-y-full opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform translate-y-full opacity-0"
    >
      <div
        v-if="authStore.error"
        class="absolute top-full left-0 right-0 bg-gradient-to-r from-red-500 to-pink-500 text-white px-4 py-3 shadow-2xl z-50"
      >
        <div class="container mx-auto flex items-center justify-between">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
            <span class="font-medium">{{ authStore.error }}</span>
          </div>
          <button
            @click="authStore.error = ''"
            class="text-white/80 hover:text-white transition-colors"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </header>
</template>

<style scoped>
@keyframes gradient-shift {
  0%,
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.1) rotate(180deg);
    opacity: 0.3;
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.animate-gradient-shift {
  animation: gradient-shift 10s ease-in-out infinite;
}

.animate-shimmer {
  animation: shimmer 2s linear infinite;
}
</style>