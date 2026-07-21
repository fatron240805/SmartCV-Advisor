import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link } from 'react-router-dom';
import AuthLayout from '../components/AuthLayout';
import { apiService, getApiErrorMessage } from '../services/api';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [resetToken, setResetToken] = useState('');
  const [statusMessage, setStatusMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatusMessage('');
    setErrorMessage('');
    try {
      setSubmitting(true);
      const result = await apiService.forgotPassword(email);
      setStatusMessage(result.data.message);
      setResetToken(result.data.demo_reset_token ?? '');
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error));
    } finally {
      setSubmitting(false);
    }
  }

  const resetSearch = new URLSearchParams({ email, token: resetToken }).toString();

  return (
    <AuthLayout title="Đặt lại mật khẩu" subtitle="Nhập email tài khoản để nhận liên kết đặt lại mật khẩu">
      <form className="space-y-5" onSubmit={handleSubmit}>
        <label className="block">
          <span className="mb-2 block font-medium text-slate-700">Email</span>
          <input
            className="h-12 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
            placeholder="email@example.com"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </label>

        {statusMessage && (
          <div className="rounded-2xl border border-green-200 bg-green-50 px-4 py-3 text-sm font-medium text-green-700">
            {statusMessage}
          </div>
        )}
        {errorMessage && (
          <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
            {errorMessage}
          </div>
        )}

        <button
          className="h-12 w-full rounded-2xl bg-blue-600 px-5 font-bold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
          disabled={!email || submitting}
          type="submit"
        >
          {submitting ? 'Đang gửi liên kết...' : 'Gửi liên kết đặt lại mật khẩu'}
        </button>
      </form>

      {resetToken && (
        <Link
          className="mt-4 flex h-12 items-center justify-center rounded-2xl border border-blue-200 bg-blue-50 px-5 font-bold text-blue-600 hover:bg-blue-100"
          to={`/reset-password?${resetSearch}`}
        >
          Mở liên kết đặt lại mật khẩu
        </Link>
      )}

      <div className="mt-6 text-center">
        <Link className="font-bold text-blue-600 hover:text-blue-700" to="/login">
          Quay lại đăng nhập
        </Link>
      </div>
    </AuthLayout>
  );
}
