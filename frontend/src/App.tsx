import { BrowserRouter, Link, Route, Routes, useLocation } from 'react-router-dom';
import AnalysisResultPage from './pages/AnalysisResultPage';
import HistoryPage from './pages/HistoryPage';
import PlansPage from './pages/PlansPage';
import UploadCvPage from './pages/UploadCvPage';

const navigationItems = [
  { label: 'Tổng quan', path: '/', icon: 'grid' },
  { label: 'Phân tích CV', path: '/upload', icon: 'upload' },
  { label: 'Lịch sử phân tích', path: '/', icon: 'clock' },
  { label: 'Gói dịch vụ', path: '/plans', icon: 'card' },
  { label: 'Hồ sơ cá nhân', path: '/profile', icon: 'user' },
];

function NavIcon({ icon }: { icon: string }) {
  if (icon === 'upload') {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" className="h-5 w-5">
        <path d="M12 16V5m0 0 4 4m-4-4-4 4M5 16v3h14v-3" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }
  if (icon === 'clock') {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" className="h-5 w-5">
        <path d="M12 7v5l3 2M5 5v5h5M5.6 14a7 7 0 1 0 1.8-6.6L5 10" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }
  if (icon === 'card') {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" className="h-5 w-5">
        <path d="M4 7h16v10H4zM4 10h16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }
  if (icon === 'user') {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" className="h-5 w-5">
        <path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm7 8a7 7 0 0 0-14 0" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" className="h-5 w-5">
      <path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
    </svg>
  );
}

function AppShell() {
  const location = useLocation();
  const isAnalysisFlow = location.pathname.startsWith('/upload') || location.pathname.startsWith('/analysis');

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-slate-200 bg-white lg:flex lg:flex-col">
        <Link to="/" className="flex h-20 items-center gap-3 border-b border-slate-200 px-7">
          <span className="grid h-9 w-9 place-items-center rounded-xl bg-blue-600 text-sm font-bold text-white">CV</span>
          <span className="text-xl font-bold">
            SmartCV <span className="text-blue-600">Advisor</span>
          </span>
        </Link>

        <nav className="flex-1 space-y-2 px-4 py-6">
          {navigationItems.map((item) => {
            const active =
              item.path === '/upload'
                ? isAnalysisFlow
                : item.label === 'Gói dịch vụ' && location.pathname === item.path;
            const historyActive = item.label === 'Lịch sử phân tích' && location.pathname === '/';
            return (
              <Link
                key={`${item.label}-${item.path}`}
                to={item.path}
                className={[
                  'flex min-h-12 items-center gap-3 rounded-2xl px-4 font-medium transition',
                  active || historyActive
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700',
                ].join(' ')}
              >
                <NavIcon icon={item.icon} />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="space-y-4 border-t border-slate-200 p-4">
          <div className="rounded-2xl border border-purple-100 bg-purple-50 p-4 text-sm">
            <p className="font-bold text-purple-700">Premium — Job Search Pass</p>
            <p className="mt-1 text-purple-500">Hết hạn: 09/08/2026</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded-full bg-blue-100 font-bold text-blue-600">T</span>
            <div>
              <p className="font-semibold text-slate-900">Trần Minh An</p>
              <p className="text-sm text-slate-400">Gói Premium</p>
            </div>
          </div>
        </div>
      </aside>

      <div className="lg:pl-72">
        <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-5 backdrop-blur">
          <div className="flex items-center gap-3 text-sm font-medium text-slate-500">
            <Link to="/" className="hover:text-blue-600">
              Trang chủ
            </Link>
            <span>/</span>
            <span className="text-slate-700">
              {isAnalysisFlow ? 'Phân tích CV' : location.pathname === '/plans' ? 'Gói dịch vụ' : 'Tổng quan'}
            </span>
          </div>
          <div className="flex items-center gap-3">
            <span className="relative grid h-10 w-10 place-items-center rounded-full text-slate-500">
              <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-blue-600" />
              <svg viewBox="0 0 24 24" aria-hidden="true" className="h-5 w-5">
                <path d="M18 16v-5a6 6 0 0 0-12 0v5l-2 2h16zM10 20h4" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </span>
            <span className="grid h-10 w-10 place-items-center rounded-full bg-blue-100 font-bold text-blue-600">T</span>
          </div>
        </header>

        <Routes>
          <Route path="/" element={<HistoryPage />} />
          <Route path="/upload" element={<UploadCvPage />} />
          <Route path="/analysis/:id" element={<AnalysisResultPage />} />
          <Route path="/plans" element={<PlansPage />} />
          <Route path="*" element={<UploadCvPage />} />
        </Routes>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppShell />
    </BrowserRouter>
  );
}

export default App;
