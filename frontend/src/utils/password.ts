export function passwordChecks(password: string) {
  return {
    length: password.length >= 8,
    letter: /[A-Za-zÀ-ỹ]/.test(password),
    digit: /\d/.test(password),
  };
}

export function isStrongPassword(password: string) {
  const checks = passwordChecks(password);
  return checks.length && checks.letter && checks.digit;
}
