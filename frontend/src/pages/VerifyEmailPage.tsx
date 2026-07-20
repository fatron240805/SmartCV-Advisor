import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import AuthLayout from '../components/AuthLayout';
import { apiService, getApiErrorMessage } from '../services/api';

export default function VerifyEmailPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [email, setEmail] = useState(searchParams.get('email') ?? '');
  const [token, setToken] = useState(searchParams.get('token') ?? '');
  const [statusMessage, setStatusMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function handleVerify() {
    setStatusMessage('');
    setErrorMessage('');
    if (!token) {
      setErrorMessage('Liên kết xác thực không hợp lệ hoặc đã hết hạn.');
      return;
    }

    try {
      setSubmitting(true);
      await apiService.verifyEmail(token);
      setStatusMessage('Tài khoản đã được kích hoạt.');
      window.setTimeout(() => navigate('/login'), 900);
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error));
    } finally {
      setSubmitting(false);
    }
  }

  async function handleResend(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatusMessage('');
    setErrorMessage('');
    try {
      setSubmitting(true);
      const result = await apiService.resendVerification(email);
      const nextToken = result.data.demo_verification_token ?? '';
      setToken(nextToken);
      setSearchParams({ email, token: nextToken });
      setStatusMessage(result.data.already_verified ? 'Tài khoản đã được xác thực.' : 'Email xác thực đã được gửi lại.');
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthLayout title="Kiểm tra email của bạn" subtitle="Chúng tôi đã gửi liên kết xác thực đến email đăng ký">
      <div className="mb-6 rounded-3xl border border-blue-100 bg-blue-50 p-5 text-center">
        <div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-white text-blue-600 shadow-sm">
          <svg viewBox="0 0 24 24" aria-hidden="true" className="h-7 w-7">
            <path d="M4 6h16v12H4z" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
            <path d="m4 7 8 6 8-6" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
        <p className="mt-4 font-semibold text-slate-800">{email || 'Email đăng ký của bạn'}</p>
        <p className="mt-2 text-sm leading-6 text-slate-500">Liên kết xác thực đang chờ được xác nhận.</p>
      </div>

      {statusMessage && (
        <div className="mb-4 rounded-2xl border border-green-200 bg-green-50 px-4 py-3 text-sm font-medium text-green-700">
          {statusMessage}
        </div>
      )}
      {errorMessage && (
        <div className="mb-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          {errorMessage}
        </div>
      )}

      <button
        className="h-12 w-full rounded-2xl bg-blue-600 px-5 font-bold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
        disabled={!token || submitting}
        type="button"
        onClick={handleVerify}
      >
        {submitting ? 'Đang xác thực...' : 'Xác thực tài khoản'}
      </button>

      <form className="mt-6 border-t border-slate-100 pt-5" onSubmit={handleResend}>
        <label className="block">
          <span className="mb-2 block font-medium text-slate-700">Gửi lại email xác thực</span>
          <input
            className="h-12 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-100"
            placeholder="email@example.com"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </label>
        <button
          className="mt-4 h-12 w-full rounded-2xl border border-slate-200 bg-white px-5 font-bold text-slate-700 transition hover:border-blue-200 hover:text-blue-600 disabled:cursor-not-allowed disabled:text-slate-400"
          disabled={!email || submitting}
          type="submit"
        >
          Gửi lại email xác thực
        </button>
      </form>

      <div className="mt-6 text-center">
        <Link className="font-bold text-blue-600 hover:text-blue-700" to="/login">
          Quay lại đăng nhập
        </Link>
      </div>
    </AuthLayout>
  );
}
