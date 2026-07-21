import { passwordChecks } from '../utils/password';

interface PasswordChecklistProps {
  password: string;
}

function CheckItem({ valid, label }: { valid: boolean; label: string }) {
  return (
    <li className={['flex items-center gap-2 text-sm', valid ? 'text-green-600' : 'text-slate-400'].join(' ')}>
      <span className={['grid h-4 w-4 place-items-center rounded-full text-[10px]', valid ? 'bg-green-100' : 'bg-slate-100'].join(' ')}>
        {valid ? '✓' : '•'}
      </span>
      {label}
    </li>
  );
}

export default function PasswordChecklist({ password }: PasswordChecklistProps) {
  const checks = passwordChecks(password);
  return (
    <ul className="mt-3 grid gap-1.5">
      <CheckItem valid={checks.length} label="Tối thiểu 8 ký tự" />
      <CheckItem valid={checks.letter} label="Có ít nhất một chữ cái" />
      <CheckItem valid={checks.digit} label="Có ít nhất một chữ số" />
    </ul>
  );
}
