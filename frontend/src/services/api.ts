// export async function fetchPlaceholder() {
//   // Placeholder API call. Replace with axios/fetch implementation.
//   return Promise.resolve({ message: "API placeholder" });
// }

// BÊN DƯỚI LÀ ĐĂNG KHOA CẬP NHẬT NGÀY 19/07/2026

import axios from 'axios';

// Khởi tạo một instance của axios với base URL là địa chỉ của Backend
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Lấy lịch sử phân tích (UC-024)
  getHistory: async (limit: number = 10) => {
    const response = await apiClient.get(`/analyses?limit=${limit}`);
    return response.data;
  },
  
  // Lấy gợi ý cải thiện của một CV cụ thể (UC-016)
  getSuggestions: async (analysisId: string) => {
    const response = await apiClient.get(`/analyses/${analysisId}/suggestions`);
    return response.data;
  },

  // Lấy danh sách gói dịch vụ (UC-026)
  getPlans: async () => {
    const response = await apiClient.get('/service-plans');
    return response.data;
  }
};