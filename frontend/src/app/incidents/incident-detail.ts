import { DatePipe } from '@angular/common';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Subscription } from 'rxjs';
import { Incident, IncidentStatusHistory, Status } from './incident.models';
import { IncidentService } from './incident.service';
import { apiErrorMessage } from './api-error';

@Component({
  selector: 'app-incident-detail',
  imports: [DatePipe, ReactiveFormsModule, RouterLink],
  templateUrl: './incident-detail.html',
  styleUrl: './incident-detail.scss',
})
export class IncidentDetail {
  private readonly service = inject(IncidentService);
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  private requests = new Subscription();
  private historyRequest?: Subscription;
  protected readonly incident = signal<Incident | null>(null);
  protected readonly loading = signal(true);
  protected readonly error = signal('');
  protected readonly history = signal<IncidentStatusHistory[]>([]);
  protected readonly historyLoading = signal(false);
  protected readonly historyError = signal('');
  protected readonly saving = signal(false);
  protected readonly statusError = signal('');
  protected readonly statusMessage = signal('');
  protected readonly status = new FormControl<Status>('Open', { nonNullable: true });
  protected readonly statusForm = new FormGroup({ status: this.status });

  constructor() {
    this.route.paramMap.pipe(takeUntilDestroyed()).subscribe((params) => {
      this.requests.unsubscribe();
      this.requests = new Subscription();
      this.historyRequest?.unsubscribe();
      this.incident.set(null);
      this.error.set('');
      this.statusError.set('');
      this.statusMessage.set('');
      this.saving.set(false);
      this.loading.set(true);
      const id = Number(params.get('id'));
      if (!Number.isSafeInteger(id) || id <= 0) {
        this.error.set('Incidente não encontrado.');
        this.loading.set(false);
        return;
      }
      this.requests.add(this.service.getIncident(id).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
        next: (incident) => {
          this.incident.set(incident);
          this.status.setValue(incident.status);
          this.loading.set(false);
          this.loadHistory();
        },
        error: (error: unknown) => { this.error.set(apiErrorMessage(error)); this.loading.set(false); },
      }));
    });
  }

  protected loadHistory(): void {
    const incident = this.incident();
    if (!incident) return;
    this.historyRequest?.unsubscribe();
    this.historyLoading.set(true);
    this.historyError.set('');
    this.history.set([]);
    this.historyRequest = this.service.getIncidentHistory(incident.id).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (history) => { this.history.set(history); this.historyLoading.set(false); },
      error: (error: unknown) => { this.historyError.set(apiErrorMessage(error)); this.historyLoading.set(false); },
    });
  }

  protected changeStatus(): void {
    const incident = this.incident();
    if (!incident || this.saving()) return;
    this.saving.set(true);
    this.statusError.set('');
    this.statusMessage.set('');
    this.requests.add(this.service.changeIncidentStatus(incident.id, { status: this.status.value })
      .pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
        next: (updated) => {
          this.incident.set(updated);
          this.status.setValue(updated.status);
          this.saving.set(false);
          this.statusMessage.set('Status salvo com sucesso.');
          this.loadHistory();
        },
        error: (error: unknown) => { this.statusError.set(apiErrorMessage(error)); this.saving.set(false); },
      }));
  }
}
