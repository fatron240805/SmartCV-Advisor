import { Link } from 'react-router-dom';
import type { ReactNode } from 'react';

interface AuthLayoutProps {
  title: string;
  subtitle: string;
  children: ReactNode;
}

export default function AuthLayout({ title, subtitle, children }: AuthLayoutProps) {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50/70 via-white to-slate-50 px-5 py-8 text-slate-900">
      <div className="mx-auto flex w-full max-w-[520px] flex-col items-center">
        <Link to="/" className="mb-7 flex items-center gap-3">
          <span className="grid h-10 w-10 place-items-center rounded-2xl bg-blue-600 text-white shadow-sm">
            <svg viewBox="0 0 24 24" aria-hidden="true" className="h-5 w-5">
              <path d="M8 3h6l4 4v14H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Z" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
              <path d="M14 3v5h4M10 13h4M10 17h6" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
            </svg>
          </span>
          <span className="text-xl font-bold">
            SmartCV <span className="text-blue-600">Advisor</span>
          </span>
        </Link>

        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold tracking-normal">{title}</h1>
          <p className="mt-3 text-slate-500">{subtitle}</p>
        </div>

        <section className="w-full rounded-3xl border border-slate-200 bg-white p-8 shadow-xl shadow-slate-200/70">
          {children}
        </section>
      </div>
    </main>
  );
}
