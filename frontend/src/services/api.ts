import axios from 'axios';
import type { AnalysisResult, CareerRole, UploadedCv } from '../types';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
});

export const apiService = {
  getCareerRoles: async (): Promise<{ data: CareerRole[] }> => {
    const response = await apiClient.get('/career-roles');
    return response.data;
  },

  uploadCv: async (payload: {
    file: File;
    consentAccepted: boolean;
    policyVersion?: string;
  }): Promise<{ data: UploadedCv }> => {
    const formData = new FormData();
    formData.append('file', payload.file);
    formData.append('consent_accepted', String(payload.consentAccepted));
    formData.append('policy_version', payload.policyVersion ?? 'cv-processing-policy-v1');

    const response = await apiClient.post('/cvs', formData);
    return response.data;
  },

  createAnalysis: async (
    cvId: string,
    careerRoleId: string,
  ): Promise<{ data: AnalysisResult }> => {
    const response = await apiClient.post(`/cvs/${cvId}/analyses`, {
      career_role_id: careerRoleId,
    });
    return response.data;
  },

  getAnalysisResult: async (analysisId: string): Promise<{ data: AnalysisResult; access_level: string }> => {
    const response = await apiClient.get(`/analyses/${analysisId}`);
    return response.data;
  },

  getHistory: async (limit: number = 10) => {
    const response = await apiClient.get(`/analyses?limit=${limit}`);
    return response.data;
  },

  getSuggestions: async (analysisId: string) => {
    const response = await apiClient.get(`/analyses/${analysisId}/suggestions`);
    return response.data;
  },

  getPlans: async () => {
    const response = await apiClient.get('/service-plans');
    return response.data;
  },
};

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail?.message === 'string') {
      return detail.message;
    }
    if (typeof detail === 'string') {
      return detail;
    }
    return 'Không thể kết nối máy chủ. Vui lòng thử lại.';
  }
  return 'Đã có lỗi xảy ra. Vui lòng thử lại.';
}
