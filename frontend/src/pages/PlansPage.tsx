import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface Plan {
  plan_id: string;
  name: string;
  price: number;
  features: string[];
}

export default function PlansPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [currentPlan] = useState<'free' | 'premium'>('free'); // Sẽ lấy từ context/auth sau

  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const result = await apiService.getPlans();
        setPlans(result.data);
      } catch (error) {
        console.error("Lỗi khi tải gói dịch vụ:", error);
      }
    };
    fetchPlans();
  }, []);

  return (
    <div className="max-w-6xl mx-auto p-6 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-4">Nâng tầm CV của bạn với SmartCV</h1>
        <p className="text-lg text-gray-500">Mở khóa sức mạnh AI để tạo CV chuẩn ATS, chinh phục nhà tuyển dụng.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        {plans.map((plan) => {
          const isPopular = plan.plan_id === 'DV_PREMIUM_30';
          
          return (
            <div key={plan.plan_id} className={`relative bg-white rounded-2xl shadow-sm border-2 ${isPopular ? 'border-purple-500' : 'border-gray-200'} p-8 flex flex-col`}>
              {isPopular && (
                <span className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-4 py-1 rounded-full text-sm font-bold shadow-md">
                  ĐƯỢC ĐỀ XUẤT
                </span>
              )}
              
              <h3 className="text-2xl font-bold text-gray-800">{plan.name}</h3>
              <div className="mt-4 flex items-baseline text-gray-900">
                <span className="text-4xl font-extrabold tracking-tight">
                  {plan.price === 0 ? 'Miễn phí' : `${plan.price.toLocaleString('vi-VN')}đ`}
                </span>
                {plan.price > 0 && <span className="ml-1 text-xl font-medium text-gray-500">/ 30 ngày</span>}
              </div>

              <ul className="mt-8 space-y-4 flex-1">
                {plan.features.map((feature, idx) => (
                  <li key={idx} className="flex items-start">
                    <svg className="h-6 w-6 text-green-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="ml-3 text-gray-600">{feature}</span>
                  </li>
                ))}
              </ul>

              <div className="mt-8">
                {currentPlan === 'free' && plan.plan_id === 'DV_FREE' ? (
                  <button disabled className="w-full bg-gray-100 text-gray-500 py-3 rounded-xl font-bold cursor-not-allowed">
                    Gói hiện tại
                  </button>
                ) : plan.plan_id === 'DV_PREMIUM_30' && currentPlan === 'premium' ? (
                  <button className="w-full bg-purple-100 text-purple-700 hover:bg-purple-200 py-3 rounded-xl font-bold transition-colors">
                    Gia hạn ngay
                  </button>
                ) : (
                  <button className={`w-full py-3 rounded-xl font-bold transition-all shadow-sm hover:shadow-md ${isPopular ? 'bg-purple-600 hover:bg-purple-700 text-white' : 'bg-gray-800 hover:bg-gray-900 text-white'}`}>
                    Nâng cấp Premium
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}