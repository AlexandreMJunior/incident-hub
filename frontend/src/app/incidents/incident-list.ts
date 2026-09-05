import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Subscription } from 'rxjs';
import { Incident, Severity, Status } from './incident.models';
import { IncidentService } from './incident.service';
import { apiErrorMessage } from './api-error';

@Component({
  selector: 'app-incident-list',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './incident-list.html',
  styleUrl: './incident-list.scss',
})
export class IncidentList {
  private readonly service = inject(IncidentService);
  private readonly destroyRef = inject(DestroyRef);
  private request?: Subscription;
  protected readonly incidents = signal<Incident[]>([]);
  protected readonly loading = signal(false);
  protected readonly error = signal('');
  protected readonly filters = new FormGroup({
    status: new FormControl<Status | ''>('', { nonNullable: true }),
    severity: new FormControl<Severity | ''>('', { nonNullable: true }),
  });

  constructor() { this.load(); }

  protected load(): void {
    this.request?.unsubscribe();
    this.loading.set(true);
    this.error.set('');
    const { status, severity } = this.filters.getRawValue();
    this.request = this.service.listIncidents({
      ...(status ? { status } : {}), ...(severity ? { severity } : {}),
    }).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (data) => { this.incidents.set(data); this.loading.set(false); },
      error: (error: unknown) => { this.error.set(apiErrorMessage(error)); this.loading.set(false); },
    });
  }

  protected clearFilters(): void {
    this.filters.reset();
    this.load();
  }
}
