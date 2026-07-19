// export default function AnalysisResultPage() {
//   return (
//     <div>
//       <h1>Analysis Result Page Placeholder</h1>
//       <p>Page hiển thị kết quả phân tích CV và matching JD.</p>
//     </div>
//   );
// }

// BÊN DƯỚI LÀ ĐKHOA CẬP NHẬT 19/07

import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiService } from '../services/api';

interface Suggestion {
  suggestion_id: string;
  category: string;
  issue: string;
  basic_fix: string;
  premium_rewrite: string | null;
  is_premium: boolean;
}

export default function AnalysisResultPage() {
  const { id } = useParams<{ id: string }>(); // Lấy ID kết quả phân tích từ URL
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [accessLevel, setAccessLevel] = useState<'free' | 'premium'>('free');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (!id) return;
      try {
        const result = await apiService.getSuggestions(id);
        setSuggestions(result.data);
        setAccessLevel(result.access_level);
      } catch (error) {
        console.error("Lỗi tải gợi ý:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchSuggestions();
  }, [id]);

  if (loading) return <div className="text-center mt-20 text-gray-500">Đang phân tích dữ liệu...</div>;

  return (
    <div className="max-w-5xl mx-auto p-6">
      <div className="flex items-center gap-4 mb-2">
        <Link to="/" className="text-gray-400 hover:text-gray-600">← Quay lại</Link>
        <h1 className="text-3xl font-bold text-gray-800">Kết quả phân tích CV ({id})</h1>
      </div>
      <p className="text-gray-500 mb-8 ml-10">Dưới đây là các gợi ý tối ưu từ SmartCV Advisor giúp hồ sơ của bạn lọt qua hệ thống ATS.</p>

      {suggestions.length === 0 ? (
        <div className="text-center p-8 bg-white rounded-xl border border-gray-200 text-gray-500">
          Không tìm thấy dữ liệu gợi ý cho lần phân tích này.
        </div>
      ) : (
        <div className="space-y-6">
          {suggestions.map((sug) => (
            <div key={sug.suggestion_id} className="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
              <div className="p-5 border-b border-gray-100 bg-gray-50 flex items-start justify-between">
                <div>
                  <span className="inline-block px-2.5 py-1 bg-red-100 text-red-700 text-xs font-bold uppercase rounded tracking-wider mb-2">
                    Lỗi {sug.category}
                  </span>
                  <h3 className="text-lg font-semibold text-gray-800">{sug.issue}</h3>
                </div>
              </div>
              
              <div className="p-5 space-y-4">
                <div>
                  <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wide mb-1">Gợi ý cơ bản</h4>
                  <p className="text-gray-700">{sug.basic_fix}</p>
                </div>

                {sug.is_premium && (
                  <div className="bg-purple-50 p-4 rounded-lg border border-purple-100 relative overflow-hidden">
                    <h4 className="text-sm font-bold text-purple-700 uppercase tracking-wide mb-1 flex items-center gap-2">
                      ✨ Câu mẫu AI viết lại (Chuẩn STAR)
                    </h4>
                    
                    {accessLevel === 'free' ? (
                      <div className="mt-2">
                        <p className="blur-[4px] select-none text-gray-500 font-mono">
                          "Đã thiết kế và tối ưu hóa hệ thống API bằng Python, giúp giảm 30% thời gian phản hồi hệ thống."
                        </p>
                        <div className="absolute inset-0 flex items-center justify-center bg-white/40">
                          <Link to="/plans" className="bg-gray-900 text-white px-4 py-2 rounded-md shadow-lg font-medium text-sm hover:bg-gray-800 transition-colors">
                            Mở khóa Premium
                          </Link>
                        </div>
                      </div>
                    ) : (
                      <div className="mt-2 flex justify-between items-start">
                        <p className="text-purple-900 font-medium italic">"{sug.premium_rewrite}"</p>
                        <button 
                          className="text-purple-600 hover:bg-purple-100 px-3 py-1 rounded text-sm transition-colors"
                          onClick={() => navigator.clipboard.writeText(sug.premium_rewrite || "")}
                        >
                          Copy
                        </button>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}