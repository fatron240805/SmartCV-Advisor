import { useEffect, useMemo, useState } from 'react';
import AdminLayout from '../components/AdminLayout';
import { apiService, getApiErrorMessage } from '../services/api';
import type { AdminCareerRole } from '../types';

type RoleFormState = {
  name: string;
  description: string;
  status: 'active' | 'inactive';
};

function formatDate(value: string | null) {
  if (!value) return '—';
  return new Date(value).toLocaleDateString('vi-VN');
}

function StatusPill({ status }: { status: 'active' | 'inactive' }) {
  const active = status === 'active';
  return (
    <span
      className={[
        'inline-flex min-w-20 justify-center rounded-full border px-3 py-1 text-xs font-semibold',
        active ? 'border-green-200 bg-green-50 text-green-700' : 'border-orange-200 bg-orange-50 text-orange-700',
      ].join(' ')}
    >
      {active ? 'Đang hoạt động' : 'Ngưng hoạt động'}
    </span>
  );
}

export default function AdminCareerRolesPage() {
  const [roles, setRoles] = useState<AdminCareerRole[]>([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [toast, setToast] = useState('');
  const [editingRole, setEditingRole] = useState<AdminCareerRole | null>(null);
  const [roleModalOpen, setRoleModalOpen] = useState(false);
  const [statusRole, setStatusRole] = useState<AdminCareerRole | null>(null);
  const [form, setForm] = useState<RoleFormState>({ name: '', description: '', status: 'active' });
  const [saving, setSaving] = useState(false);

  const formIsValid = useMemo(() => form.name.trim().length > 0 && form.description.trim().length > 0, [form]);

  useEffect(() => {
    let active = true;
    async function loadRoles() {
      setLoading(true);
      setErrorMessage('');
      try {
        const result = await apiService.getAdminCareerRoles({ search, status: statusFilter });
        if (active) setRoles(result.data);
      } catch (error) {
        if (active) setErrorMessage(getApiErrorMessage(error));
      } finally {
        if (active) setLoading(false);
      }
    }
    void loadRoles();
    return () => {
      active = false;
    };
  }, [search, statusFilter]);

  async function reloadRoles() {
    const result = await apiService.getAdminCareerRoles({ search, status: statusFilter });
    setRoles(result.data);
  }

  function openCreateModal() {
    setEditingRole(null);
    setForm({ name: '', description: '', status: 'active' });
    setRoleModalOpen(true);
  }

  function openEditModal(role: AdminCareerRole) {
    setEditingRole(role);
    setForm({ name: role.name, description: role.description, status: role.status });
    setRoleModalOpen(true);
  }

  async function saveRole() {
    if (!formIsValid) return;
    setSaving(true);
    setErrorMessage('');
    try {
      const result = editingRole
        ? await apiService.updateAdminCareerRole(editingRole.role_id, form)
        : await apiService.createAdminCareerRole(form);
      setToast(result.meta.message);
      setRoleModalOpen(false);
      setEditingRole(null);
      setForm({ name: '', description: '', status: 'active' });
      await reloadRoles();
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error));
    } finally {
      setSaving(false);
    }
  }

  async function confirmStatusChange() {
    if (!statusRole) return;
    setSaving(true);
    try {
      const nextStatus = statusRole.status === 'active' ? 'inactive' : 'active';
      const result = await apiService.updateAdminCareerRoleStatus(statusRole.role_id, nextStatus);
      setToast(result.meta.message);
      setStatusRole(null);
      await reloadRoles();
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error));
    } finally {
      setSaving(false);
    }
  }

  return (
    <AdminLayout
      breadcrumb="Vị trí IT"
      title="Quản lý vị trí IT"
      actions={
        <button
          className="inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 text-sm font-bold text-white shadow-sm hover:bg-blue-700"
          type="button"
          onClick={openCreateModal}
        >
          <span className="text-lg leading-none">+</span>
          Thêm vị trí IT
        </button>
      }
    >
      <div className="mb-5 grid gap-3 md:grid-cols-[1fr_180px]">
        <input
          className="h-11 rounded-xl border border-slate-200 bg-white px-4 text-sm outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          placeholder="Tìm theo tên vị trí..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <select
          className="h-11 rounded-xl border border-slate-200 bg-white px-4 text-sm text-slate-600 outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          value={statusFilter}
          onChange={(event) => setStatusFilter(event.target.value as 'all' | 'active' | 'inactive')}
        >
          <option value="all">Tất cả trạng thái</option>
          <option value="active">Đang hoạt động</option>
          <option value="inactive">Ngưng hoạt động</option>
        </select>
      </div>

      {toast && <div className="mb-4 rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm font-semibold text-green-700">{toast}</div>}
      {errorMessage && <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-600">{errorMessage}</div>}

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <table className="w-full min-w-[820px] border-collapse text-left text-sm">
          <thead className="bg-slate-50 text-xs font-bold uppercase text-slate-500">
            <tr>
              <th className="px-5 py-4">Tên vị trí</th>
              <th className="px-5 py-4">Mô tả</th>
              <th className="px-5 py-4">Trạng thái</th>
              <th className="px-5 py-4">Ngày tạo</th>
              <th className="px-5 py-4">Cập nhật</th>
              <th className="px-5 py-4 text-right">Thao tác</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading && (
              <tr>
                <td className="px-5 py-8 text-center text-slate-500" colSpan={6}>
                  Đang tải danh sách vị trí IT...
                </td>
              </tr>
            )}
            {!loading && roles.length === 0 && (
              <tr>
                <td className="px-5 py-8 text-center text-slate-500" colSpan={6}>
                  Không tìm thấy vị trí IT phù hợp.
                </td>
              </tr>
            )}
            {!loading &&
              roles.map((role) => (
                <tr key={role.role_id} className="hover:bg-slate-50/70">
                  <td className="px-5 py-4 font-bold text-slate-800">{role.name}</td>
                  <td className="max-w-xs truncate px-5 py-4 text-slate-500">{role.description}</td>
                  <td className="px-5 py-4">
                    <StatusPill status={role.status} />
                  </td>
                  <td className="px-5 py-4 text-slate-500">{formatDate(role.created_at)}</td>
                  <td className="px-5 py-4 text-slate-500">{formatDate(role.updated_at)}</td>
                  <td className="px-5 py-4 text-right">
                    <button className="font-semibold text-blue-600 hover:text-blue-700" type="button" onClick={() => openEditModal(role)}>
                      Sửa
                    </button>
                    <span className="mx-3 text-slate-200">|</span>
                    <button className="font-semibold text-orange-600 hover:text-orange-700" type="button" onClick={() => setStatusRole(role)}>
                      {role.status === 'active' ? 'Ngưng' : 'Kích hoạt'}
                    </button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {roleModalOpen && (
        <div className="fixed inset-0 z-40 grid place-items-center bg-slate-900/40 px-4">
          <div className="w-full max-w-xl rounded-2xl bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-100 px-6 py-5">
              <h2 className="text-xl font-bold">{editingRole ? 'Chỉnh sửa vị trí IT' : 'Thêm vị trí IT'}</h2>
              <button className="text-2xl text-slate-400 hover:text-slate-600" type="button" onClick={() => setRoleModalOpen(false)}>
                ×
              </button>
            </div>
            <div className="space-y-4 px-6 py-5">
              <label className="block">
                <span className="mb-2 block text-sm font-semibold text-slate-600">Tên vị trí</span>
                <input
                  className="h-11 w-full rounded-xl border border-slate-200 px-4 outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={form.name}
                  onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
                />
              </label>
              <label className="block">
                <span className="mb-2 block text-sm font-semibold text-slate-600">Mô tả tổng quan</span>
                <textarea
                  className="min-h-24 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={form.description}
                  onChange={(event) => setForm((current) => ({ ...current, description: event.target.value }))}
                />
              </label>
              <label className="block">
                <span className="mb-2 block text-sm font-semibold text-slate-600">Trạng thái</span>
                <select
                  className="h-11 w-full rounded-xl border border-slate-200 px-4 outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={form.status}
                  onChange={(event) => setForm((current) => ({ ...current, status: event.target.value as 'active' | 'inactive' }))}
                >
                  <option value="active">Đang hoạt động</option>
                  <option value="inactive">Ngưng hoạt động</option>
                </select>
              </label>
            </div>
            <div className="grid gap-3 border-t border-slate-100 px-6 py-5 sm:grid-cols-2">
              <button className="h-11 rounded-xl border border-slate-200 font-semibold text-slate-600 hover:border-slate-300" type="button" onClick={() => setRoleModalOpen(false)}>
                Hủy
              </button>
              <button
                className="h-11 rounded-xl bg-blue-600 font-bold text-white hover:bg-blue-700 disabled:bg-blue-300"
                disabled={!formIsValid || saving}
                type="button"
                onClick={saveRole}
              >
                {saving ? 'Đang lưu...' : editingRole ? 'Lưu thay đổi' : 'Thêm vị trí IT'}
              </button>
            </div>
          </div>
        </div>
      )}

      {statusRole && (
        <div className="fixed inset-0 z-40 grid place-items-center bg-slate-900/40 px-4">
          <div className="w-full max-w-md rounded-2xl bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-100 px-6 py-5">
              <h2 className="text-xl font-bold">Xác nhận thay đổi trạng thái</h2>
              <button className="text-2xl text-slate-400 hover:text-slate-600" type="button" onClick={() => setStatusRole(null)}>
                ×
              </button>
            </div>
            <div className="px-6 py-6 text-slate-600">
              Bạn có chắc chắn muốn <strong>{statusRole.status === 'active' ? 'ngưng hoạt động' : 'kích hoạt'}</strong> vị trí{' '}
              <strong>"{statusRole.name}"</strong> không? Dữ liệu đánh giá CV trước đây sẽ được giữ nguyên.
            </div>
            <div className="grid gap-3 px-6 pb-6 sm:grid-cols-2">
              <button className="h-11 rounded-xl border border-slate-200 font-semibold text-slate-600" type="button" onClick={() => setStatusRole(null)}>
                Hủy
              </button>
              <button className="h-11 rounded-xl bg-orange-500 font-bold text-white hover:bg-orange-600 disabled:bg-orange-300" disabled={saving} type="button" onClick={confirmStatusChange}>
                Xác nhận
              </button>
            </div>
          </div>
        </div>
      )}
    </AdminLayout>
  );
}
