import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './authStore'
import { commentsApi } from '../api/comments'
import type { Comment } from '../types/comments'

// Используем текущий host браузера для WebSocket
const WS_PROTOCOL = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
const WS_HOST = window.location.host

export const useCommentsStore = defineStore('comments', () => {
  const comments = ref<Comment[]>([])
  const totalComments = ref(0)
  const currentPage = ref(1)
  const currentSort = ref('-created_at')
  const currentSearch = ref('')
  const currentComment = ref<Comment | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const socket = ref<WebSocket | null>(null)

  const authStore = useAuthStore()

  const findAndAddReply = (node: Comment, parentId: number, newReply: Comment): boolean => {
    if (node.id === parentId) {
      if (!node.replies) node.replies = []
      if (!node.replies.find(r => r.id === newReply.id)) {
        node.replies.unshift(newReply)
      }
      return true
    }

    if (node.replies && node.replies.length > 0) {
      for (const child of node.replies) {
        if (findAndAddReply(child, parentId, newReply)) {
          return true
        }
      }
    }
    return false
  }

  const fetchComments = async (page = 1, ordering?: string, search?: string) => {
    loading.value = true
    error.value = null

    if (ordering !== undefined) currentSort.value = ordering
    if (search !== undefined) currentSearch.value = search
    currentPage.value = page

    try {
      const response = await commentsApi.getAll({
        page,
        ordering: currentSort.value,
        search: currentSearch.value
      })

      if (page === 1) {
        comments.value = response.results
      } else {
        comments.value = [...comments.value, ...response.results]
      }

      totalComments.value = response.count
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const fetchCommentDetail = async (id: number) => {
    loading.value = true
    error.value = null
    currentComment.value = null

    try {
      const data = await commentsApi.getById(id)
      currentComment.value = data
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const addComment = async (text: string, replyTo: number | null = null, files: File[] = [], recaptchaToken: string) => {
    loading.value = true
    error.value = null

    try {
      const formData = new FormData()
      formData.append('text', text)
      formData.append('recaptcha_token', recaptchaToken)

      if (replyTo) {
        formData.append('reply', replyTo.toString())
      }

      files.forEach((file) => {
        formData.append('files', file)
      })

      const newComment = await commentsApi.create(formData)

      if (!replyTo) {
        comments.value.unshift(newComment)
      } else {
        let added = false

        if (currentComment.value) {
          added = findAndAddReply(currentComment.value, replyTo, newComment)
        }

        if (!added && comments.value.length > 0) {
          for (const rootComment of comments.value) {
            if (findAndAddReply(rootComment, replyTo, newComment)) {
              break
            }
          }
        }
      }

      return newComment
    } catch (err: any) {
      error.value = err.message || "Failed to post comment"
      throw err
    } finally {
      loading.value = false
    }
  }

  const connectWebSocket = (commentId: number) => {
    if (socket.value) {
      socket.value.close()
    }

    let wsUrl = `${WS_PROTOCOL}//${WS_HOST}/ws/comments/${commentId}/`
    if (authStore.accessToken) {
      wsUrl += `?token=${authStore.accessToken}`
    }

    console.log('🔌 Connecting to WebSocket:', wsUrl)

    socket.value = new WebSocket(wsUrl)

    socket.value.onopen = () => {
      console.log('✅ WebSocket connected')
    }

    socket.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('📨 WebSocket message received:', data)

        if (data.type === 'new_reply') {
          const newReply = data.data

          if (!newReply || !newReply.reply) return

          let added = false

          if (currentComment.value) {
            added = findAndAddReply(currentComment.value, newReply.reply, newReply)
          }

          if (!added && comments.value.length > 0) {
            for (const rootComment of comments.value) {
              if (findAndAddReply(rootComment, newReply.reply, newReply)) {
                break
              }
            }
          }
        }
      } catch (e) {
        console.error("❌ WebSocket parse error:", e)
      }
    }

    socket.value.onerror = (err) => {
      console.error('❌ WebSocket error:', err)
    }

    socket.value.onclose = (event) => {
      console.log('🔌 WebSocket disconnected. Code:', event.code, 'Reason:', event.reason)
    }
  }

  const disconnectWebSocket = () => {
    if (socket.value) {
      socket.value.close()
      socket.value = null
    }
  }

  return {
    comments,
    totalComments,
    currentPage,
    currentSort,
    currentSearch,
    currentComment,
    loading,
    error,
    fetchComments,
    fetchCommentDetail,
    addComment,
    connectWebSocket,
    disconnectWebSocket
  }
})
