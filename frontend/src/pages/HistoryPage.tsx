// export default function HistoryPage() {
//   return (
//     <div>
//       <h1>History Page Placeholder</h1>
//       <p>Page lịch sử phân tích: để thành viên khác implement danh sách phiên trước.</p>
//     </div>
//   );
// }

// BÊN DƯỚI LÀ ĐKHOA CẬP NHẬT 19/07

import { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { Link } from 'react-router-dom';

interface HistoryItem {
  analysis_id: string;
  cv_name: string;
  overall_score: number;
  created_at: string;
  status: string;
}

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [accessLevel, setAccessLevel] = useState<'free' | 'premium'>('free');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const result = await apiService.getHistory(10);
        setHistory(result.data);
        setAccessLevel(result.access_level);
      } catch (error) {
        console.error("Lỗi khi tải lịch sử:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (loading) return <div className="text-center mt-20 text-gray-500">Đang tải dữ liệu...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Lịch sử phân tích</h1>
        {accessLevel === 'free' && (
          <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-medium border border-purple-200">
            Giới hạn: 3 CV gần nhất
          </span>
        )}
      </div>

      <div className="grid gap-4">
        {history.length === 0 ? (
          <div className="text-center p-10 bg-white rounded-xl border border-gray-100">
            <p className="text-gray-500">Bạn chưa có kết quả phân tích nào.</p>
          </div>
        ) : (
          history.map((item) => (
            <div key={item.analysis_id} className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-lg text-gray-800 truncate">{item.cv_name}</h3>
                <p className="text-sm text-gray-500 mt-1">
                  Phân tích ngày: {new Date(item.created_at).toLocaleDateString('vi-VN')}
                </p>
              </div>
              <div className="flex items-center gap-6">
                <div className="text-center">
                  <p className="text-xs text-gray-500 uppercase tracking-wide">Điểm ATS</p>
                  <p className={`font-bold text-2xl ${item.overall_score >= 70 ? 'text-green-500' : 'text-orange-500'}`}>
                    {item.overall_score}/100
                  </p>
                </div>
                {/* Nút Xem chi tiết sẽ chuyển hướng tới trang Gợi ý của chính CV đó */}
                <Link 
                  to={`/analysis/${item.analysis_id}`}
                  className="bg-gray-50 hover:bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Xem chi tiết
                </Link>
              </div>
            </div>
          ))
        )}

        {accessLevel === 'free' && (
          <div className="bg-gradient-to-r from-purple-50 to-indigo-50 p-6 rounded-xl border border-purple-100 text-center mt-4">
            <h3 className="font-bold text-purple-900 mb-2">Xem toàn bộ lịch sử phân tích?</h3>
            <p className="text-purple-700 text-sm mb-4">Nâng cấp Premium để lưu trữ không giới hạn và xem lại các phân tích cũ.</p>
            <Link to="/plans" className="inline-block bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium shadow-sm transition-colors">
              Nâng cấp Premium
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}