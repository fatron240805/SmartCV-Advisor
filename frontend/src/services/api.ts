import axios from 'axios';
import type {
  AdminCareerRole,
  AdminSkillConfig,
  AdminUserDetail,
  AdminUserSummary,
  AnalysisResult,
  AuthSession,
  AuthUser,
  CareerRole,
  UserProfile,
  UploadedCv,
} from '../types';

const AUTH_STORAGE_KEY = 'smartcv_auth_session';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
});

export function getStoredAuthSession(): AuthSession | null {
  const raw = window.sessionStorage.getItem(AUTH_STORAGE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as AuthSession;
  } catch {
    window.sessionStorage.removeItem(AUTH_STORAGE_KEY);
    return null;
  }
}

export function getStoredAuthUser(): AuthUser | null {
  return getStoredAuthSession()?.user ?? null;
}

export function saveAuthSession(session: AuthSession) {
  window.sessionStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
}

export function clearAuthSession() {
  window.sessionStorage.removeItem(AUTH_STORAGE_KEY);
}

apiClient.interceptors.request.use((config) => {
  const session = getStoredAuthSession();
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`;
  }
  return config;
});

export const apiService = {
  register: async (payload: {
    fullName: string;
    email: string;
    password: string;
    passwordConfirmation: string;
    termsAccepted: boolean;
  }): Promise<{ data: AuthUser; meta: { next_step: string } }> => {
    const response = await apiClient.post('/auth/register', {
      full_name: payload.fullName,
      email: payload.email,
      password: payload.password,
      password_confirmation: payload.passwordConfirmation,
      terms_accepted: payload.termsAccepted,
    });
    return response.data;
  },

  login: async (payload: {
    email: string;
    password: string;
    rememberMe: boolean;
  }): Promise<{ data: AuthSession }> => {
    const response = await apiClient.post('/auth/login', {
      email: payload.email,
      password: payload.password,
      remember_me: payload.rememberMe,
    });
    return response.data;
  },

  logout: async (refreshToken?: string | null): Promise<{ data: { message: string } }> => {
    const response = await apiClient.post('/auth/logout', { refresh_token: refreshToken ?? null });
    return response.data;
  },

  checkEmail: async (email: string): Promise<{ data: { exists: boolean } }> => {
    const response = await apiClient.post('/auth/check-email', { email });
    return response.data;
  },

  forgotPassword: async (email: string): Promise<{ data: { message: string; demo_reset_token?: string | null; email_masked: string } }> => {
    const response = await apiClient.post('/auth/forgot-password', { email });
    return response.data;
  },

  resetPassword: async (payload: {
    token: string;
    password: string;
    passwordConfirmation: string;
  }): Promise<{ data: { message: string } }> => {
    const response = await apiClient.post('/auth/reset-password', {
      token: payload.token,
      password: payload.password,
      password_confirmation: payload.passwordConfirmation,
    });
    return response.data;
  },

  getProfile: async (): Promise<{ data: UserProfile }> => {
    const response = await apiClient.get('/users/me');
    return response.data;
  },

  getQuota: async (): Promise<{
    data: {
      account_type: string;
      current_plan_id: string;
      unlimited: boolean;
      used: number | null;
      limit: number | null;
      remaining: number | null;
      label: string;
    };
  }> => {
    const response = await apiClient.get('/users/me/quota');
    return response.data;
  },

  updateProfile: async (payload: {
    fullName: string;
    email: string;
    industryInterest: string;
    targetRole: string;
    currentLevel: string;
    avatarUrl?: string | null;
  }): Promise<{ data: UserProfile; meta: { message: string } }> => {
    const response = await apiClient.patch('/users/me', {
      full_name: payload.fullName,
      email: payload.email,
      industry_interest: payload.industryInterest,
      target_role: payload.targetRole,
      current_level: payload.currentLevel,
      avatar_url: payload.avatarUrl ?? null,
    });
    return response.data;
  },

  requestDataDeletion: async (payload: {
    scope: 'cv_data' | 'all_personal_data';
    reason?: string;
  }): Promise<{ data: UserProfile['data_deletion_requests'][number]; meta: { message: string } }> => {
    const response = await apiClient.post('/users/me/data-deletion-request', {
      scope: payload.scope,
      reason: payload.reason ?? '',
    });
    return response.data;
  },

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

  getAdminCareerRoles: async (params?: {
    search?: string;
    status?: 'all' | 'active' | 'inactive';
  }): Promise<{ data: AdminCareerRole[]; meta: { count: number } }> => {
    const response = await apiClient.get('/admin/career-roles', { params });
    return response.data;
  },

  createAdminCareerRole: async (payload: {
    name: string;
    description: string;
    status: 'active' | 'inactive';
  }): Promise<{ data: AdminCareerRole; meta: { message: string } }> => {
    const response = await apiClient.post('/admin/career-roles', payload);
    return response.data;
  },

  updateAdminCareerRole: async (
    roleId: string,
    payload: { name?: string; description?: string; status?: 'active' | 'inactive' },
  ): Promise<{ data: AdminCareerRole; meta: { message: string } }> => {
    const response = await apiClient.patch(`/admin/career-roles/${roleId}`, payload);
    return response.data;
  },

  updateAdminCareerRoleStatus: async (
    roleId: string,
    status: 'active' | 'inactive',
  ): Promise<{ data: AdminCareerRole; meta: { message: string } }> => {
    const response = await apiClient.patch(`/admin/career-roles/${roleId}/status`, { status });
    return response.data;
  },

  getAdminRoleSkills: async (
    roleId: string,
  ): Promise<{ data: AdminSkillConfig[]; meta: { total_weight: number; count: number; role: AdminCareerRole } }> => {
    const response = await apiClient.get(`/admin/career-roles/${roleId}/skills`);
    return response.data;
  },

  createAdminRoleSkill: async (
    roleId: string,
    payload: {
      skill_name: string;
      skill_group: string;
      required_score: number;
      weight: number;
      importance: number;
      criteria_description: string;
    },
  ): Promise<{ data: AdminSkillConfig; meta: { message: string } }> => {
    const response = await apiClient.post(`/admin/career-roles/${roleId}/skills`, payload);
    return response.data;
  },

  updateAdminRoleSkill: async (
    roleId: string,
    configId: string,
    payload: {
      required_score?: number;
      weight?: number;
      importance?: number;
      criteria_description?: string;
      status?: 'active' | 'inactive';
      skill_group?: string;
    },
  ): Promise<{ data: AdminSkillConfig; meta: { message: string } }> => {
    const response = await apiClient.patch(`/admin/career-roles/${roleId}/skills/${configId}`, payload);
    return response.data;
  },

  bulkUpdateAdminRoleSkills: async (
    roleId: string,
    payload: {
      config_ids: string[];
      required_score?: number;
      weight?: number;
      importance?: number;
      status?: 'active' | 'inactive';
    },
  ): Promise<{ data: AdminSkillConfig[]; meta: { message: string } }> => {
    const response = await apiClient.patch(`/admin/career-roles/${roleId}/skills/bulk`, payload);
    return response.data;
  },

  getAdminUsers: async (params?: {
    search?: string;
    account_type?: 'all' | 'registered' | 'premium' | 'admin';
    status?: 'all' | 'active' | 'locked';
    date_from?: string;
    date_to?: string;
    page?: number;
    limit?: number;
  }): Promise<{
    data: AdminUserSummary[];
    meta: { total: number; page: number; limit: number; has_next: boolean };
  }> => {
    const response = await apiClient.get('/admin/users', { params });
    return response.data;
  },

  getAdminUser: async (userId: string): Promise<{ data: AdminUserDetail }> => {
    const response = await apiClient.get(`/admin/users/${userId}`);
    return response.data;
  },

  updateAdminUser: async (
    userId: string,
    payload: Partial<{
      full_name: string;
      email: string;
      phone: string;
      address: string;
      account_type: 'registered' | 'premium' | 'admin';
      industry_interest: string;
      target_role: string;
      current_level: string;
    }>,
  ): Promise<{ data: AdminUserSummary; meta: { message: string } }> => {
    const response = await apiClient.patch(`/admin/users/${userId}`, payload);
    return response.data;
  },

  lockAdminUser: async (userId: string, reason: string): Promise<{ data: AdminUserSummary; meta: { message: string } }> => {
    const response = await apiClient.post(`/admin/users/${userId}/lock`, { reason });
    return response.data;
  },

  unlockAdminUser: async (userId: string): Promise<{ data: AdminUserSummary; meta: { message: string } }> => {
    const response = await apiClient.post(`/admin/users/${userId}/unlock`);
    return response.data;
  },
};

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail?.message === 'string') {
      return typeof detail?.hint === 'string' ? `${detail.message} ${detail.hint}` : detail.message;
    }
    if (typeof detail === 'string') {
      return detail;
    }
    return 'Không thể kết nối backend tại http://127.0.0.1:8000. Kiểm tra backend đang chạy, mở /api/health, hoặc restart backend để nhận cấu hình CORS mới.';
  }
  return 'Đã có lỗi xảy ra. Vui lòng thử lại.';
}
