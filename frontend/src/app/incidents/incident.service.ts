import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import {
  ChangeIncidentStatus,
  CreateIncidentComment,
  IncidentComment,
  IncidentTimelineEvent,
  CreateIncident,
  Dashboard,
  Incident,
  IncidentFilters,
  IncidentStatusHistory,
} from './incident.models';

@Injectable({ providedIn: 'root' })
export class IncidentService {
  private readonly http = inject(HttpClient);
  private readonly incidentsUrl = `${environment.apiBaseUrl}incidents/`;

  listIncidents(filters: IncidentFilters = {}): Observable<Incident[]> {
    let params = new HttpParams();
    if (filters.status !== undefined) {
      params = params.set('status', filters.status);
    }
    if (filters.severity !== undefined) {
      params = params.set('severity', filters.severity);
    }
    return this.http.get<Incident[]>(this.incidentsUrl, { params });
  }

  createIncident(data: CreateIncident): Observable<Incident> {
    return this.http.post<Incident>(this.incidentsUrl, data);
  }

  getIncident(id: number): Observable<Incident> {
    return this.http.get<Incident>(this.incidentUrl(id));
  }

  changeIncidentStatus(id: number, data: ChangeIncidentStatus): Observable<Incident> {
    return this.http.patch<Incident>(`${this.incidentUrl(id)}status/`, data);
  }

  getIncidentHistory(id: number): Observable<IncidentStatusHistory[]> {
    return this.http.get<IncidentStatusHistory[]>(`${this.incidentUrl(id)}history/`);
  }

  createIncidentComment(id: number, data: CreateIncidentComment): Observable<IncidentComment> {
    return this.http.post<IncidentComment>(`${this.incidentUrl(id)}comments/`, data);
  }

  getIncidentTimeline(id: number): Observable<IncidentTimelineEvent[]> {
    return this.http.get<IncidentTimelineEvent[]>(`${this.incidentUrl(id)}timeline/`);
  }

  getDashboard(): Observable<Dashboard> {
    return this.http.get<Dashboard>(`${environment.apiBaseUrl}dashboard/`);
  }

  private incidentUrl(id: number): string {
    return `${this.incidentsUrl}${id}/`;
  }
}
