<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { useCommentsStore } from "../stores/commentsStore";
import CommentItem from "../components/CommentItem.vue";
import CommentForm from "../components/CommentForm.vue";
import { useAuthStore } from "../stores/authStore";

const store = useCommentsStore();
const authStore = useAuthStore();

const localSearch = ref("");
const localSort = ref<"newest" | "oldest">("newest");

const totalPages = computed(() => Math.ceil(store.totalComments / 25));

const applyFilters = () => {
  const sortValue = localSort.value === "newest" ? "-created_at" : "created_at";
  store.fetchComments(1, sortValue, localSearch.value);
};

const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    const sortValue = localSort.value === "newest" ? "-created_at" : "created_at";
    store.fetchComments(page, sortValue, localSearch.value);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};

onMounted(() => {
  store.fetchComments();
});
</script>

<template>
  <!-- Фиксированный градиентный фон на всю страницу -->
  <div class="fixed inset-0 -z-10 bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-purple-900/20 dark:to-blue-900/20"></div>

  <div class="min-h-screen">
    <div class="max-w-4xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl dark:shadow-purple-900/50 overflow-hidden ring-1 ring-gray-200/20 dark:ring-purple-500/20">
          <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500"></div>

          <div class="absolute -top-20 -right-20 w-40 h-40 bg-purple-500/10 rounded-full blur-3xl"></div>

          <div class="relative p-6 flex justify-between items-center">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div>
                <h1 class="text-3xl font-black bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                  Comments Feed
                </h1>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  Share your thoughts with the community
                </p>
              </div>
            </div>

            <button
              @click="store.fetchComments()"
              class="p-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white transition-all duration-300 hover:shadow-lg group"
              title="Refresh"
            >
              <svg
                class="h-6 w-6 transition-transform duration-500 group-hover:rotate-180"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="mb-8">
        <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl dark:shadow-purple-900/50 overflow-hidden ring-1 ring-gray-200/20 dark:ring-purple-500/20">
          <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500"></div>
          <div class="absolute -top-20 -right-20 w-40 h-40 bg-purple-500/10 rounded-full blur-3xl"></div>
          <div class="absolute -bottom-20 -left-20 w-40 h-40 bg-pink-500/10 rounded-full blur-3xl"></div>

          <div class="relative p-6">
            <div class="grid grid-cols-1 md:grid-cols-[1fr,300px,auto] gap-4 items-end">
              <!-- Search -->
              <div class="space-y-2">
                <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Search User
                </label>
                <div class="relative group">
                  <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                  <input
                    v-model="localSearch"
                    type="text"
                    placeholder="Search by name or email..."
                    @keyup.enter="applyFilters"
                    class="w-full pl-12 pr-4 py-3 bg-gray-50 dark:bg-gray-900/50 border-2 border-transparent rounded-xl focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-500/20 transition-all duration-300 text-gray-900 dark:text-white placeholder-gray-400 shadow-inner dark:shadow-none"
                  />
                </div>
              </div>

              <!-- Sort -->
              <div class="space-y-2">
                <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Sort By
                </label>
                <div class="relative group">
                  <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                    </svg>
                  </div>
                  <select
                    v-model="localSort"
                    @change="applyFilters"
                    class="w-full pl-12 pr-10 py-3 bg-gray-50 dark:bg-gray-900/50 border-2 border-transparent rounded-xl focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-500/20 transition-all duration-300 text-gray-900 dark:text-white appearance-none cursor-pointer shadow-inner dark:shadow-none"
                  >
                    <option value="newest">Newest First</option>
                    <option value="oldest">Oldest First</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              <!-- Apply Button -->
              <button
                @click="applyFilters"
                class="px-8 py-3 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:from-purple-600 hover:via-pink-600 hover:to-blue-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center gap-2 group h-[50px]"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
                <span>Apply</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Comment Form or Auth Required -->
      <div class="mb-8">
        <CommentForm v-if="authStore.isAuthenticated" />

        <!-- Auth Required -->
        <div v-else class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl dark:shadow-red-900/50 overflow-hidden ring-1 ring-gray-200/20 dark:ring-red-500/20">
          <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-red-500 via-pink-500 to-orange-500"></div>
          <div class="absolute -top-20 -right-20 w-40 h-40 bg-red-500/10 rounded-full blur-3xl"></div>
          <div class="absolute -bottom-20 -left-20 w-40 h-40 bg-pink-500/10 rounded-full blur-3xl"></div>

          <div class="relative p-8 text-center">
            <div class="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-red-500 to-pink-500 shadow-lg mb-6 animate-pulse">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>

            <h3 class="text-2xl font-black bg-gradient-to-r from-red-600 via-pink-600 to-orange-600 bg-clip-text text-transparent mb-3">
              Authentication Required
            </h3>

            <p class="text-gray-600 dark:text-gray-400 mb-6 max-w-md mx-auto">
              You need to be logged in to post comments. Please sign in to your account or create a new one to continue.
            </p>

            <div class="flex flex-col sm:flex-row gap-3 justify-center">
              <router-link
                to="/login"
                class="px-8 py-3.5 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 hover:from-purple-600 hover:via-pink-600 hover:to-blue-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center gap-2 group"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                <span>Sign In</span>
              </router-link>

              <router-link
                to="/register"
                class="px-8 py-3.5 bg-white/10 dark:bg-gray-700/50 backdrop-blur-sm border-2 border-white/20 dark:border-purple-500/30 hover:border-purple-500 text-gray-700 dark:text-gray-200 rounded-xl font-semibold transition-all duration-300 hover:shadow-lg flex items-center justify-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
                <span>Create Account</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="store.loading && store.comments.length === 0" class="flex justify-center py-12">
        <div class="relative">
          <div class="w-16 h-16 rounded-full border-4 border-purple-200 dark:border-purple-900"></div>
          <div class="w-16 h-16 rounded-full border-4 border-purple-600 border-t-transparent animate-spin absolute top-0"></div>
        </div>
      </div>

      <!-- Comments -->
      <div v-else-if="!store.error" class="space-y-6 pb-8">
        <CommentItem
          v-for="comment in store.comments"
          :key="comment.id"
          :comment="comment"
        />

        <!-- Empty State -->
        <div v-if="store.comments && store.comments.length === 0" class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl dark:shadow-purple-900/50 overflow-hidden ring-1 ring-gray-200/20 dark:ring-purple-500/20">
          <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500"></div>
          <div class="relative p-12 text-center">
            <div class="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900/30 dark:to-pink-900/30 mb-6">
              <svg class="w-10 h-10 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-700 dark:text-gray-300 mb-2">No comments yet</h3>
            <p class="text-gray-500 dark:text-gray-400">Be the first to share your thoughts!</p>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1 && !store.error" class="mt-8 pb-8">
        <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl dark:shadow-purple-900/50 overflow-hidden ring-1 ring-gray-200/20 dark:ring-purple-500/20">
          <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500"></div>
          <div class="relative p-4 flex justify-between items-center">
            <button
              @click="changePage(store.currentPage - 1)"
              :disabled="store.currentPage === 1"
              class="px-6 py-2.5 bg-white/10 dark:bg-gray-700/50 backdrop-blur-sm border-2 border-white/20 dark:border-purple-500/30 hover:border-purple-500 text-gray-700 dark:text-gray-200 rounded-xl font-semibold text-sm transition-all duration-300 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
              Previous
            </button>

            <span class="text-sm font-semibold text-gray-700 dark:text-gray-300 px-4">
              Page <span class="text-purple-600 dark:text-purple-400">{{ store.currentPage }}</span> of <span class="text-purple-600 dark:text-purple-400">{{ totalPages }}</span>
            </span>

            <button
              @click="changePage(store.currentPage + 1)"
              :disabled="store.currentPage === totalPages"
              class="px-6 py-2.5 bg-white/10 dark:bg-gray-700/50 backdrop-blur-sm border-2 border-white/20 dark:border-purple-500/30 hover:border-purple-500 text-gray-700 dark:text-gray-200 rounded-xl font-semibold text-sm transition-all duration-300 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              Next
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>