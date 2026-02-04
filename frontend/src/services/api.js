import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  sendMessage: async (message, sessionId = null) => {
    const response = await api.post('/chat', {
      message,
      session_id: sessionId,
    });
    return response.data;
  },

  getSessionHistory: async (sessionId) => {
    const response = await api.get(`/chat/sessions/${sessionId}`);
    return response.data;
  },
};

export const knowledgeAPI = {
  addDocument: async (content, title = null, metadata = {}) => {
    const response = await api.post('/knowledge', {
      content,
      title,
      metadata,
    });
    return response.data;
  },

  deleteDocument: async (documentId) => {
    const response = await api.delete(`/knowledge/${documentId}`);
    return response.data;
  },

  searchDocuments: async (query, topK = 5) => {
    const response = await api.get('/knowledge/search', {
      params: { query, top_k: topK },
    });
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/knowledge/stats');
    return response.data;
  },
};

export default api;
