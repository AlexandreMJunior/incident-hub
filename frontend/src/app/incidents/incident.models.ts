export type Severity = 'Low' | 'Medium' | 'High' | 'Critical';

export type Status = 'Open' | 'In Progress' | 'Resolved';

export interface Incident {
  id: number;
  title: string;
  description: string;
  severity: Severity;
  owner: string;
  status: Status;
  created_at: string;
  updated_at: string;
}

export interface IncidentStatusHistory {
  previous_status: Status;
  new_status: Status;
  changed_at: string;
}

export interface Dashboard {
  open_count: number;
  critical_unresolved_count: number;
  resolved_count: number;
}

export type CreateIncident = Pick<Incident, 'title' | 'description' | 'severity' | 'owner'>;

export interface ChangeIncidentStatus {
  status: Status;
}

export interface IncidentFilters {
  status?: Status;
  severity?: Severity;
}

export interface IncidentComment {
  id: number;
  author: string;
  content: string;
  created_at: string;
}

export type CreateIncidentComment = Pick<IncidentComment, 'author' | 'content'>;

export type IncidentTimelineEvent = { id: number; occurred_at: string } & (
  | { type: 'status_change'; previous_status: Status; new_status: Status }
  | { type: 'comment'; author: string; content: string }
);
