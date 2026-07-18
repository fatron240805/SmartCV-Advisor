export interface User {
  id: string;
  name: string;
  email: string;
}

export interface Cv {
  id: string;
  title: string;
  createdAt: string;
}

export interface AnalysisResult {
  id: string;
  summary: string;
  score: number;
}
