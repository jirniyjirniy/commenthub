<script setup lang="ts">
import { ref, computed } from 'vue'
import { useQuery, useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'

// ============================================
// QUERIES
// ============================================
const COMMENTS_QUERY = gql`
  query GetComments($limit: Int, $offset: Int) {
    comments(limit: $limit, offset: $offset) {
      id
      text
      shortText
      createdAt
      replyCount
      hasAttachments
      user {
        id
        username
      }
      replyList {
        id
        text
        createdAt
        user {
          username
        }
      }
      attachmentsList {
        id
        file
        mediaType
      }
    }
    commentCount
    topLevelCommentCount
  }
`

const ME_QUERY = gql`
  query GetMe {
    me {
      id
      username
      email
    }
  }
`

// ============================================
// MUTATIONS
// ============================================
const CREATE_COMMENT = gql`
  mutation CreateComment($text: String!, $replyId: Int) {
    createComment(text: $text, replyId: $replyId) {
      id
      text
      createdAt
      user {
        username
      }
    }
  }
`

const UPDATE_COMMENT = gql`
  mutation UpdateComment($commentId: Int!, $text: String!) {
    updateComment(commentId: $commentId, text: $text) {
      id
      text
      updatedAt
    }
  }
`

const DELETE_COMMENT = gql`
  mutation DeleteComment($commentId: Int!) {
    deleteComment(commentId: $commentId)
  }
`

// ============================================
// COMPOSABLES
// ============================================
const page = ref(0)
const perPage = 10

const { result: commentsResult, loading, error, refetch } = useQuery(
  COMMENTS_QUERY,
  () => ({
    limit: perPage,
    offset: page.value * perPage
  })
)

const { result: meResult } = useQuery(ME_QUERY)

const { mutate: createComment, loading: creating, error: createError } = useMutation(CREATE_COMMENT)
const { mutate: updateComment, loading: updating } = useMutation(UPDATE_COMMENT)
const { mutate: deleteComment, loading: deleting } = useMutation(DELETE_COMMENT)

// ============================================
// STATE
// ============================================
const newCommentText = ref('')
const editingCommentId = ref<number | null>(null)
const editingText = ref('')
const replyingTo = ref<number | null>(null)
const expandedComments = ref<Set<number>>(new Set())

// ============================================
// COMPUTED
// ============================================
const comments = computed(() => commentsResult.value?.comments || [])
const totalComments = computed(() => commentsResult.value?.commentCount || 0)
const currentUser = computed(() => meResult.value?.me)

const canLoadMore = computed(() => {
  const total = commentsResult.value?.topLevelCommentCount || 0
  return (page.value + 1) * perPage < total
})

// ============================================
// METHODS
// ============================================
const handleCreate = async () => {
  if (!newCommentText.value.trim()) {
    alert('Введите текст комментария!')
    return
  }

  try {
    await createComment({
      text: newCommentText.value,
      replyId: replyingTo.value
    })

    newCommentText.value = ''
    replyingTo.value = null

    await refetch()
  } catch (err: any) {
    console.error('Ошибка создания:', err)
    alert(`Ошибка: ${err.message}`)
  }
}

const handleUpdate = async (commentId: number) => {
  if (!editingText.value.trim()) {
    alert('Введите текст!')
    return
  }

  try {
    await updateComment({
      commentId,
      text: editingText.value
    })

    editingCommentId.value = null
    editingText.value = ''

    await refetch()
  } catch (err: any) {
    console.error('Ошибка обновления:', err)
    alert(`Ошибка: ${err.message}`)
  }
}

const handleDelete = async (commentId: number) => {
  if (!confirm('Удалить комментарий?')) {
    return
  }

  try {
    await deleteComment({ commentId })
    await refetch()
  } catch (err: any) {
    console.error('Ошибка удаления:', err)
    alert(`Ошибка: ${err.message}`)
  }
}

const startEditing = (commentId: number, currentText: string) => {
  editingCommentId.value = commentId
  editingText.value = currentText
}

const cancelEditing = () => {
  editingCommentId.value = null
  editingText.value = ''
}

const startReplying = (commentId: number) => {
  replyingTo.value = commentId
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const cancelReplying = () => {
  replyingTo.value = null
}

const toggleReplies = (commentId: number) => {
  if (expandedComments.value.has(commentId)) {
    expandedComments.value.delete(commentId)
  } else {
    expandedComments.value.add(commentId)
  }
}

const loadMore = () => {
  page.value++
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="min-h-screen p-4 md:p-8" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="max-w-4xl mx-auto">

      <!-- HEADER -->
      <div class="mb-8 text-center text-white">
        <h1 class="text-5xl font-bold mb-2">
          🔮 GraphQL Feed
        </h1>
        <p class="text-lg opacity-90">
          Powered by Strawberry & Apollo
        </p>

        <!-- Stats -->
        <div v-if="commentsResult" class="mt-4 flex gap-4 justify-center flex-wrap">
          <div class="px-4 py-2 bg-white bg-opacity-20 backdrop-blur-sm rounded-full">
            <span class="text-sm">Комментариев: <strong>{{ totalComments }}</strong></span>
          </div>
          <div class="px-4 py-2 bg-white bg-opacity-20 backdrop-blur-sm rounded-full">
            <span class="text-sm">Верхнего уровня: <strong>{{ commentsResult.topLevelCommentCount }}</strong></span>
          </div>
        </div>
      </div>

      <!-- USER INFO -->
      <div v-if="currentUser" class="mb-6 p-4 bg-white rounded-xl shadow-lg">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold" style="background: linear-gradient(135deg, #667eea, #764ba2);">
            {{ currentUser.username[0].toUpperCase() }}
          </div>
          <div>
            <p class="font-bold text-gray-800">{{ currentUser.username }}</p>
            <p class="text-sm text-gray-500">{{ currentUser.email }}</p>
          </div>
        </div>
      </div>

      <!-- CREATE FORM -->
      <div class="mb-8 p-6 bg-white rounded-xl shadow-xl">
        <h2 class="text-xl font-bold mb-4 text-gray-800">
          <span v-if="replyingTo">💬 Ответить #{{ replyingTo }}</span>
          <span v-else>✍️ Написать комментарий</span>
        </h2>

        <textarea
          v-model="newCommentText"
          placeholder="Ваш комментарий..."
          class="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none resize-none"
          rows="3"
          :disabled="creating"
        ></textarea>

        <div v-if="createError" class="mt-2 p-2 bg-red-50 text-red-600 rounded text-sm">
          ❌ {{ createError.message }}
        </div>

        <div class="mt-3 flex gap-2">
          <button
            @click="handleCreate"
            :disabled="creating || !newCommentText.trim() || !currentUser"
            class="px-5 py-2 text-white rounded-lg font-medium hover:opacity-90 disabled:opacity-50 transition"
            style="background: linear-gradient(135deg, #667eea, #764ba2);"
          >
            {{ creating ? '⏳ Отправка...' : '📤 Отправить' }}
          </button>

          <button
            v-if="replyingTo"
            @click="cancelReplying"
            class="px-5 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300"
          >
            Отмена
          </button>

          <p v-if="!currentUser" class="text-sm text-gray-600 self-center">
            🔒 Войдите чтобы комментировать
          </p>
        </div>
      </div>

      <!-- LOADING -->
      <div v-if="loading && !comments.length" class="text-center py-12 text-white">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-white border-t-transparent"></div>
        <p class="mt-3 text-lg">Загрузка...</p>
      </div>

      <!-- ERROR -->
      <div v-else-if="error" class="p-6 bg-red-100 text-red-700 rounded-xl">
        <h3 class="font-bold mb-2">❌ Ошибка</h3>
        <p class="text-sm">{{ error.message }}</p>
        <button @click="refetch()" class="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg">
          🔄 Повторить
        </button>
      </div>

      <!-- COMMENTS -->
      <div v-else-if="comments.length" class="space-y-4">
        <div
          v-for="comment in comments"
          :key="comment.id"
          class="p-5 bg-white rounded-xl shadow-lg hover:shadow-xl transition"
        >
          <!-- Header -->
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center gap-2">
              <div class="w-9 h-9 rounded-full flex items-center justify-center text-white font-bold text-sm" style="background: linear-gradient(135deg, #667eea, #764ba2);">
                {{ comment.user.username[0].toUpperCase() }}
              </div>
              <div>
                <p class="font-bold text-gray-800 text-sm">{{ comment.user.username }}</p>
                <p class="text-xs text-gray-500">{{ formatDate(comment.createdAt) }}</p>
              </div>
            </div>

            <!-- Actions -->
            <div v-if="currentUser?.id === comment.user.id" class="flex gap-2">
              <button
                @click="startEditing(comment.id, comment.text)"
                class="px-2 py-1 text-xs bg-blue-50 text-blue-600 rounded hover:bg-blue-100"
              >
                ✏️
              </button>
              <button
                @click="handleDelete(comment.id)"
                :disabled="deleting"
                class="px-2 py-1 text-xs bg-red-50 text-red-600 rounded hover:bg-red-100 disabled:opacity-50"
              >
                🗑️
              </button>
            </div>
          </div>

          <!-- Edit Mode -->
          <div v-if="editingCommentId === comment.id" class="mb-3">
            <textarea
              v-model="editingText"
              class="w-full p-2 border border-gray-200 rounded"
              rows="3"
            ></textarea>
            <div class="mt-2 flex gap-2">
              <button
                @click="handleUpdate(comment.id)"
                :disabled="updating"
                class="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700"
              >
                💾 Сохранить
              </button>
              <button
                @click="cancelEditing"
                class="px-3 py-1 text-sm bg-gray-200 rounded hover:bg-gray-300"
              >
                Отмена
              </button>
            </div>
          </div>

          <!-- Text -->
          <div v-else class="mb-3 text-gray-700" v-html="comment.text"></div>

          <!-- Attachments -->
          <div v-if="comment.hasAttachments && comment.attachmentsList?.length" class="mb-3">
            <div class="flex gap-2 flex-wrap">
              <template v-for="att in comment.attachmentsList" :key="att.id">
                <img
                  v-if="att.media_type === 'image'"
                  :src="att.file"
                  class="w-24 h-24 object-cover rounded shadow"
                />
              </template>
            </div>
          </div>

          <!-- Footer -->
          <div class="flex items-center gap-3 text-sm">
            <button
              @click="startReplying(comment.id)"
              class="text-purple-600 hover:underline font-medium"
            >
              💬 Ответить
            </button>

            <button
              v-if="comment.replyCount > 0"
              @click="toggleReplies(comment.id)"
              class="text-gray-600 hover:underline"
            >
              {{ expandedComments.has(comment.id) ? '⬆️' : '⬇️' }}
              {{ comment.replyCount }}
            </button>
          </div>

          <!-- Replies -->
          <div v-if="expandedComments.has(comment.id) && comment.replyList?.length" class="mt-4 ml-6 space-y-3 border-l-2 border-purple-200 pl-4">
            <div
              v-for="reply in comment.replyList"
              :key="reply.id"
              class="p-3 bg-purple-50 rounded-lg"
            >
              <div class="flex items-center gap-2 mb-2">
                <div class="w-7 h-7 rounded-full flex items-center justify-center text-white font-bold text-xs" style="background: linear-gradient(135deg, #667eea, #764ba2);">
                  {{ reply.user.username[0].toUpperCase() }}
                </div>
                <span class="font-bold text-sm">{{ reply.user.username }}</span>
                <span class="text-xs text-gray-500">{{ formatDate(reply.createdAt) }}</span>
              </div>
              <div class="text-sm text-gray-700" v-html="reply.text"></div>
            </div>
          </div>
        </div>

        <!-- Load More -->
        <div v-if="canLoadMore" class="text-center mt-6">
          <button
            @click="loadMore"
            :disabled="loading"
            class="px-6 py-2 text-white rounded-lg font-medium hover:opacity-90 disabled:opacity-50"
            style="background: linear-gradient(135deg, #667eea, #764ba2);"
          >
            {{ loading ? '⏳ Загрузка...' : '📥 Загрузить еще' }}
          </button>
        </div>
      </div>

      <!-- EMPTY -->
      <div v-else class="text-center py-16 text-white">
        <p class="text-6xl mb-4">💬</p>
        <p class="text-xl font-bold mb-2">Нет комментариев</p>
        <p class="opacity-80">Будьте первым!</p>
      </div>

    </div>
  </div>
</template>