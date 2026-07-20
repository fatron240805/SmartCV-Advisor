export interface User {
  id: string;
  name: string;
  email: string;
}

export interface CareerRole {
  role_id: string;
  name: string;
  description: string;
  status: 'active' | 'inactive';
  icon_label?: string;
}

export interface UploadedCv {
  cv_id: string;
  filename: string;
  file_type: string;
  size_bytes: number;
  size_label: string;
  status: string;
  uploaded_at: string;
  target_role_id: string | null;
  extraction: {
    text_length: number;
    page_count: number | null;
    method: string;
    language_hints: string[];
    warnings: string[];
    quality_score: number;
  };
}

export interface CriteriaScore {
  key: 'layout' | 'content' | 'keywords' | 'style' | 'ats';
  label: string;
  score: number;
  color: 'green' | 'orange' | 'blue';
}

export interface SectionScore {
  section: string;
  score: number;
  max_score: number;
  word_count: number | null;
  comment: string;
}

export interface AnalysisIssue {
  issue_id: string;
  criterion: string;
  severity: 'high' | 'medium' | 'positive';
  severity_label: string;
  title: string;
  description: string;
  impact: string;
}

export interface AnalysisResult {
  analysis_id: string;
  cv_id: string;
  cv_name: string;
  file_type: string;
  file_size_label: string;
  role_id: string | null;
  role_name: string | null;
  role_description: string | null;
  created_at: string;
  status: string;
  total_score: number;
  classification: string;
  summary: string;
  criteria_scores: CriteriaScore[];
  section_scores: SectionScore[];
  issues: AnalysisIssue[];
  strengths: string[];
  weaknesses: string[];
  priority_actions: string[];
  scoring_config_version: string;
}

export interface HistoryItem {
  analysis_id: string;
  cv_name: string;
  overall_score: number;
  classification?: string;
  role_id?: string | null;
  role_name?: string | null;
  created_at: string;
  status: string;
}
