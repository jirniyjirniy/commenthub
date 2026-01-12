<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import CommentItem from "../components/CommentItem.vue";
import CommentForm from "../components/CommentForm.vue";
import { useAuthStore } from "../stores/authStore";

const authStore = useAuthStore();
const localSearch = ref("");
const currentPage = ref(1);

const perPage = 25;

const COMMENTS_QUERY = gql`
  query GetFeed($limit: Int, $offset: Int) {
    comments(limit: $limit, offset: $offset) {
      id
      text
      created_at: createdAt
      user {
        username
        email
      }
      attachments: attachmentsList {
        id
        file
        media_type: mediaType
      }
      replies: replyList {
        id
      }
    }
    topLevelCommentCount
  }
`;

const { result, loading, error, refetch } = useQuery(
  COMMENTS_QUERY,
  () => ({
    limit: perPage,
    offset: (currentPage.value - 1) * perPage
  }),
  {
    pollInterval: 0,
    fetchPolicy: 'network-only'
  }
);

const comments = computed(() => result.value?.comments || []);
const totalComments = computed(() => result.value?.topLevelCommentCount || 0);

const totalPages = computed(() => {
  return Math.ceil(totalComments.value / perPage);
});

const canGoPrevious = computed(() => currentPage.value > 1);

const canGoNext = computed(() => currentPage.value < totalPages.value);

const pageNumbers = computed(() => {
  const pages = [];
  const total = totalPages.value;
  const current = currentPage.value;

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
  } else {
    if (current <= 3) {
      pages.push(1, 2, 3, 4, 5, '...', total);
    } else if (current >= total - 2) {
      pages.push(1, '...', total - 4, total - 3, total - 2, total - 1, total);
    } else {
      pages.push(1, '...', current - 1, current, current + 1, '...', total);
    }
  }

  return pages;
});

const filteredComments = computed(() => {
  if (!localSearch.value) return comments.value;
  const q = localSearch.value.toLowerCase();
  return comments.value.filter((c: any) =>
    c.user.username.toLowerCase().includes(q) ||
    c.text.toLowerCase().includes(q)
  );
});

const goToPage = (page: number) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const nextPage = () => {
  if (canGoNext.value) {
    goToPage(currentPage.value + 1);
  }
};

const previousPage = () => {
  if (canGoPrevious.value) {
    goToPage(currentPage.value - 1);
  }
};

const handleSuccess = () => {
  currentPage.value = 1;
  refetch();
};
</script>

<template>
  <div class="fixed inset-0 -z-10 bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-purple-900/20 dark:to-blue-900/20"></div>

  <div class="min-h-screen">
    <div class="max-w-4xl mx-auto px-4 py-8">

      <!-- HEADER -->
      <div class="mb-8">
        <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl dark:shadow-purple-900/50 overflow-hidden ring-1 ring-gray-200/20 dark:ring-purple-500/20">
          <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500"></div>
          <div class="relative p-6 flex justify-between items-center">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div>
                <h1 class="text-3xl font-black bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                  GraphQL Feed
                </h1>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  Powered by Strawberry & Apollo
                </p>
              </div>
            </div>

            <!-- Stats Badge -->
            <div class="flex items-center gap-3">
              <div class="px-4 py-2 bg-purple-100 dark:bg-purple-900/30 rounded-full">
                <span class="text-sm font-bold text-purple-600 dark:text-purple-400">
                  Page {{ currentPage }} / {{ totalPages }}
                </span>
              </div>
              <button
                @click="refetch()"
                class="p-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:shadow-lg transition-all"
                title="Refresh"
              >
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- SEARCH -->
      <div class="mb-8">
        <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-6">
           <input
              v-model="localSearch"
              type="text"
              placeholder="Search comments..."
              class="w-full pl-4 pr-4 py-3 bg-gray-50 dark:bg-gray-900/50 border-2 border-transparent rounded-xl focus:border-purple-500 focus:outline-none"
            />
        </div>
      </div>

      <!-- FORM -->
      <div class="mb-8">
        <CommentForm v-if="authStore.isAuthenticated" :on-success="handleSuccess" />
        <div v-else class="p-8 text-center bg-white dark:bg-gray-800 rounded-3xl shadow-xl">
          <p class="text-gray-500">Please <router-link to="/login" class="text-purple-600 font-bold">login</router-link> to post.</p>
        </div>
      </div>

      <!-- LOADING -->
      <div v-if="loading" class="text-center py-12 text-gray-500">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent"></div>
        <p class="mt-4">Loading page {{ currentPage }}...</p>
      </div>

      <!-- ERROR -->
      <div v-else-if="error" class="text-center py-12">
        <div class="p-6 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-3xl shadow-xl inline-block">
          <p class="font-bold mb-2">❌ Error</p>
          <p class="text-sm">{{ error.message }}</p>
        </div>
      </div>

      <!-- COMMENTS LIST -->
      <div v-else class="space-y-6">
        <CommentItem
          v-for="comment in filteredComments"
          :key="comment.id"
          :comment="comment"
        />

        <!-- EMPTY STATE -->
        <div v-if="filteredComments.length === 0" class="text-center py-12">
          <p class="text-6xl mb-4">💬</p>
          <p class="text-xl font-bold text-gray-800 dark:text-white mb-2">No comments found</p>
          <p class="text-gray-500 dark:text-gray-400">Be the first to comment!</p>
        </div>
      </div>

      <!-- PAGINATION -->
      <div v-if="totalPages > 1 && !localSearch" class="mt-8 pb-8">
        <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-6">
          <div class="flex items-center justify-center gap-2 flex-wrap">

            <!-- Previous Button -->
            <button
              @click="previousPage"
              :disabled="!canGoPrevious"
              class="px-4 py-2 rounded-xl font-medium transition-all disabled:opacity-30 disabled:cursor-not-allowed"
              :class="canGoPrevious
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:shadow-lg'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-400'"
            >
              ← Previous
            </button>

            <!-- Page Numbers -->
            <template v-for="(page, index) in pageNumbers" :key="index">
              <!-- Ellipsis -->
              <span
                v-if="page === '...'"
                class="px-3 py-2 text-gray-400"
              >
                ...
              </span>

              <!-- Page Number Button -->
              <button
                v-else
                @click="goToPage(page as number)"
                class="px-4 py-2 rounded-xl font-medium transition-all min-w-[44px]"
                :class="currentPage === page
                  ? 'bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 text-white shadow-lg scale-110'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'"
              >
                {{ page }}
              </button>
            </template>

            <!-- Next Button -->
            <button
              @click="nextPage"
              :disabled="!canGoNext"
              class="px-4 py-2 rounded-xl font-medium transition-all disabled:opacity-30 disabled:cursor-not-allowed"
              :class="canGoNext
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:shadow-lg'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-400'"
            >
              Next →
            </button>
          </div>

          <!-- Page Info -->
          <div class="mt-4 text-center text-sm text-gray-500 dark:text-gray-400">
            Showing {{ (currentPage - 1) * perPage + 1 }} - {{ Math.min(currentPage * perPage, totalComments) }} of {{ totalComments }} comments
          </div>
        </div>
      </div>

    </div>
  </div>
</template>