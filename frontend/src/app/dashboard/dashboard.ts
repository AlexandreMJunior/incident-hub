import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { Dashboard as DashboardData } from '../incidents/incident.models';
import { IncidentService } from '../incidents/incident.service';

type DashboardState =
  { status: 'loading' } | { status: 'error' } | { status: 'success'; data: DashboardData };

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard {
  private readonly incidentService = inject(IncidentService);
  protected readonly state = signal<DashboardState>({ status: 'loading' });

  constructor() {
    this.incidentService
      .getDashboard()
      .pipe(takeUntilDestroyed())
      .subscribe({
        next: (data) => this.state.set({ status: 'success', data }),
        error: () => this.state.set({ status: 'error' }),
      });
  }
}
