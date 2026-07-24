import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export default function PlansPage() {
  const [billingCycle, setBillingCycle] = useState<'30' | '90'>('30');
  const [currentPlanId, setCurrentPlanId] = useState<string>('DV_FREE');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchQuota = async () => {
      try {
        const result = await apiService.getQuota();
        setCurrentPlanId(result.data.current_plan_id || 'DV_FREE');
      } catch {
        setCurrentPlanId('DV_FREE');
      } finally {
        setIsLoading(false);
      }
    };
    fetchQuota();
  }, []);

  const renderPremiumCard = (cycle: '30' | '90', isCurrent: boolean) => {
    return (
      <div className={`relative flex flex-col rounded-3xl p-8 ${isCurrent ? 'bg-white border border-slate-200 shadow-sm' : 'bg-blue-600 shadow-xl shadow-blue-600/20'}`}>
        {cycle === '90' && !isCurrent && (
          <div className="absolute right-6 top-6 rounded-full bg-white/20 px-3 py-1 text-xs font-semibold text-white">
            Đề xuất
          </div>
        )}
        {isCurrent && (
          <div className="absolute right-6 top-6 rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-600">
            Gói hiện tại
          </div>
        )}
        <h3 className={`pr-20 text-xl font-bold ${isCurrent ? 'text-slate-900' : 'text-white'}`}>Premium — Job Search Pass</h3>
        <div className="mt-4 flex items-baseline">
          <span className={`text-5xl font-extrabold tracking-tight ${isCurrent ? 'text-slate-900' : 'text-white'}`}>
            đ{cycle === '30' ? '199.000' : '389.000'}
          </span>
        </div>
        <p className={`mt-2 text-sm font-medium ${isCurrent ? 'text-slate-400' : 'text-blue-200'}`}>
          {cycle === '30' ? '30 ngày' : '90 ngày'}
        </p>

        <ul className={`mt-8 flex-1 space-y-4 text-sm font-medium ${isCurrent ? 'text-slate-700' : 'text-white'}`}>
          {[
            'Không giới hạn lượt phân tích',
            'Gợi ý chi tiết chuyên sâu',
            'Câu mẫu viết lại theo STAR',
            'Sao chép nhanh từng câu mẫu',
            'Tất cả quyền lợi Free',
          ].map((feature, idx) => (
            <li key={idx} className="flex items-start gap-3">
              <svg className={`mt-0.5 h-5 w-5 shrink-0 ${isCurrent ? 'text-green-500' : 'text-white'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
              <span>{feature}</span>
            </li>
          ))}

          <li className={`my-6 border-t ${isCurrent ? 'border-slate-200' : 'border-blue-500/50'}`}></li>

          {[
            cycle === '30' ? 'Matching Score với JD (10 lượt)' : 'Matching Score với JD (20 lượt)',
            cycle === '30' ? 'AI Assistant (20 lượt)' : 'AI Assistant (40 lượt)',
            'Tải xuống CV đã chỉnh sửa',
          ].map((feature, idx) => (
            <li key={idx} className={`flex items-center gap-3 ${isCurrent ? 'text-slate-500' : 'text-blue-200'}`}>
              <svg className={`h-5 w-5 shrink-0 ${isCurrent ? 'text-slate-400' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="flex-1">{feature}</span>
              <span className={`rounded-full border px-2.5 py-0.5 text-[10px] font-semibold ${isCurrent ? 'border-slate-200 bg-slate-100 text-slate-500' : 'border-blue-400/30 bg-blue-500/30 text-blue-100'}`}>
                Sắp ra mắt
              </span>
            </li>
          ))}
        </ul>

        <button
          disabled={isCurrent}
          className={`mt-8 w-full rounded-2xl py-3.5 font-bold transition-all ${
            isCurrent
              ? 'bg-slate-50 text-slate-400 cursor-not-allowed opacity-80'
              : 'bg-white text-blue-600 hover:bg-slate-50 hover:shadow-lg active:scale-95'
          }`}
        >
          {isCurrent ? 'Đang sử dụng' : 'Nâng cấp Premium'}
        </button>
      </div>
    );
  };

  const renderFreeCard = () => (
    <div className="relative flex flex-col rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <div className="absolute right-6 top-6 rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-600">
        Gói hiện tại
      </div>
      <h3 className="text-xl font-bold text-slate-900">Free</h3>
      <div className="mt-4 flex items-baseline">
        <span className="text-5xl font-extrabold tracking-tight text-slate-900">đ0</span>
      </div>
      <p className="mt-2 text-sm font-medium text-slate-400">Mãi mãi miễn phí</p>

      <ul className="mb-8 mt-8 flex-1 space-y-4 text-sm font-medium text-slate-700">
        {[
          '3 lượt phân tích/tháng',
          'Điểm tổng quan và 5 tiêu chí',
          'Danh sách lỗi phổ biến',
          'Gợi ý cải thiện tổng quan',
          'Lịch sử phân tích',
        ].map((feature, idx) => (
          <li key={idx} className="flex items-start gap-3">
            <svg className="mt-0.5 h-5 w-5 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
            </svg>
            <span>{feature}</span>
          </li>
        ))}
      </ul>

      <button
        disabled
        className="w-full rounded-2xl bg-slate-50 py-3.5 font-bold text-slate-400 transition cursor-not-allowed opacity-80"
      >
        Gói hiện tại của bạn
      </button>
    </div>
  );

  if (isLoading) {
    return <div className="flex justify-center py-20 text-slate-400">Đang tải gói dịch vụ...</div>;
  }

  return (
    <div className="mx-auto max-w-5xl px-5 py-12">
      <div className="mb-12 text-center">
        <h1 className="mb-8 text-2xl font-medium text-slate-500">
          {currentPlanId === 'DV_FREE'
            ? 'Bắt đầu miễn phí, nâng cấp khi bạn cần thêm sức mạnh'
            : 'Sử dụng công cụ AI mạnh mẽ nhất để nâng tầm CV của bạn'}
        </h1>
        
        {/* Toggle Billing Cycle for Free users */}
        {currentPlanId === 'DV_FREE' && (
          <div className="mx-auto inline-flex items-center gap-1 rounded-full bg-slate-100 p-1">
            <button
              onClick={() => setBillingCycle('30')}
              className={`rounded-full px-6 py-2.5 text-sm font-semibold transition-all ${billingCycle === '30'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
                }`}
            >
              30 ngày
            </button>
            <button
              onClick={() => setBillingCycle('90')}
              className={`relative flex items-center gap-1.5 rounded-full px-6 py-2.5 text-sm font-semibold transition-all ${billingCycle === '90'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
                }`}
            >
              90 ngày
              <span className="font-bold text-emerald-500">-35%</span>
              <span className="absolute -top-2.5 -right-2 rounded-md bg-blue-600 px-1.5 py-0.5 text-[10px] font-bold text-white shadow-sm ring-1 ring-white">
                Đề xuất
              </span>
            </button>
          </div>
        )}
      </div>

      <div className={`mx-auto grid max-w-4xl gap-6 ${currentPlanId === 'DV_PREMIUM_90' ? 'md:grid-cols-1 max-w-md' : 'md:grid-cols-2'}`}>
        {currentPlanId === 'DV_FREE' && (
          <>
            {renderFreeCard()}
            {renderPremiumCard(billingCycle, false)}
          </>
        )}

        {currentPlanId === 'DV_PREMIUM_30' && (
          <>
            {renderPremiumCard('30', true)}
            {renderPremiumCard('90', false)}
          </>
        )}

        {currentPlanId === 'DV_PREMIUM_90' && (
          <>
            {renderPremiumCard('90', true)}
          </>
        )}
      </div>
    </div>
  );
}