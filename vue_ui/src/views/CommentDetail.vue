<script setup lang="ts">
import { onMounted, onUnmounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useCommentsStore } from "../stores/commentsStore";
import CommentItem from "../components/CommentItem.vue";

const route = useRoute();
const store = useCommentsStore();
const commentId = computed(() => Number(route.params.id));

onMounted(() => {
  store.fetchCommentDetail(commentId.value);
  store.connectWebSocket(commentId.value);
});

onUnmounted(() => {
  store.disconnectWebSocket();
});
</script>

<template>
  <!-- Фиксированный градиентный фон на всю страницу -->
  <div class="fixed inset-0 -z-10 bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-purple-900/20 dark:to-blue-900/20"></div>

  <div class="min-h-screen">
    <div class="max-w-4xl mx-auto px-4 py-8">
      <!-- Loading State -->
      <div
        v-if="store.loading && !store.currentComment"
        class="flex justify-center items-center min-h-[60vh]"
      >
        <div class="text-center">
          <div class="relative inline-block mb-4">
            <div class="w-20 h-20 rounded-full border-4 border-purple-200 dark:border-purple-900"></div>
            <div class="w-20 h-20 rounded-full border-4 border-purple-600 border-t-transparent animate-spin absolute top-0 left-0"></div>
          </div>
          <p class="text-gray-600 dark:text-gray-400 font-medium">Loading comment...</p>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-else-if="store.error"
        class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl dark:shadow-red-900/50 overflow-hidden ring-1 ring-red-200/50 dark:ring-red-500/30"
      >
        <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-red-500 to-pink-500"></div>
        <div class="relative p-8 text-center">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-red-500 to-pink-500 shadow-lg mb-4">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Error Loading Comment</h3>
          <p class="text-red-600 dark:text-red-400 font-medium mb-6">{{ store.error }}</p>
          <router-link
            to="/"
            class="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:from-purple-600 hover:via-pink-600 hover:to-blue-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Comments
          </router-link>
        </div>
      </div>

      <!-- Comment Detail -->
      <div v-else-if="store.currentComment">
        <!-- Back Button Card -->
        <div class="mb-6">
          <div class="relative bg-white dark:bg-gray-800 rounded-2xl shadow-lg dark:shadow-purple-900/30 overflow-hidden ring-1 ring-gray-200/20 dark:ring-purple-500/20 hover:shadow-xl transition-shadow duration-300">
            <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500"></div>
            <div class="relative p-4">
              <router-link
                to="/"
                class="flex items-center gap-2 text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 font-semibold transition-colors group"
              >
                <svg
                  class="h-5 w-5 transition-transform group-hover:-translate-x-1"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10 19l-7-7m0 0l7-7m-7 7h18"
                  />
                </svg>
                <span>Back to Comments Feed</span>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Main Comment -->
        <div class="mb-6">
          <CommentItem :comment="store.currentComment" :is-detail="true" />
        </div>

        <!-- WebSocket Status Indicator (optional) -->
        <div class="relative bg-white dark:bg-gray-800 rounded-2xl shadow-lg dark:shadow-green-900/30 overflow-hidden ring-1 ring-gray-200/20 dark:ring-green-500/20">
          <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-green-500 to-emerald-500"></div>
          <div class="relative p-4">
            <div class="flex items-center gap-3">
              <div class="relative">
                <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <div class="absolute inset-0 w-3 h-3 bg-green-500 rounded-full animate-ping"></div>
              </div>
              <div>
                <p class="text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Live Updates Active
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  This comment updates in real-time via WebSocket
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>