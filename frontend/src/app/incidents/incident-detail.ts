import { DatePipe } from '@angular/common';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Subscription } from 'rxjs';
import { Incident, IncidentTimelineEvent, Status } from './incident.models';
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
  private timelineRequest?: Subscription;
  protected readonly incident = signal<Incident | null>(null);
  protected readonly loading = signal(true);
  protected readonly error = signal('');
  protected readonly timeline = signal<IncidentTimelineEvent[]>([]);
  protected readonly timelineLoading = signal(false);
  protected readonly timelineError = signal('');
  protected readonly saving = signal(false);
  protected readonly statusError = signal('');
  protected readonly statusMessage = signal('');
  protected readonly status = new FormControl<Status>('Open', { nonNullable: true });
  protected readonly statusForm = new FormGroup({ status: this.status });

  protected readonly commentSaving = signal(false);
  protected readonly commentError = signal('');
  protected readonly commentMessage = signal('');
  protected readonly commentForm = new FormGroup({
    author: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.pattern(/\S/), Validators.maxLength(255)] }),
    content: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.pattern(/\S/)] }),
  });

  protected addComment(): void {
    const incident = this.incident();
    if (!incident || this.commentSaving()) return;
    this.commentForm.markAllAsTouched();
    this.commentError.set('');
    this.commentMessage.set('');
    if (this.commentForm.invalid) return;
    const data = this.commentForm.getRawValue();
    this.commentSaving.set(true);
    this.requests.add(this.service.createIncidentComment(incident.id, {
      author: data.author.trim(), content: data.content.trim(),
    }).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: () => {
        this.commentSaving.set(false);
        this.commentForm.reset();
        this.commentMessage.set('Comentário adicionado com sucesso.');
        this.loadTimeline();
      },
      error: (error: unknown) => { this.commentError.set(apiErrorMessage(error)); this.commentSaving.set(false); },
    }));
  }

  constructor() {
    this.route.paramMap.pipe(takeUntilDestroyed()).subscribe((params) => {
      this.requests.unsubscribe();
      this.requests = new Subscription();
      this.timelineRequest?.unsubscribe();
      this.incident.set(null);
      this.commentForm.reset();
      this.commentSaving.set(false);
      this.commentError.set('');
      this.commentMessage.set('');
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
          this.loadTimeline();
        },
        error: (error: unknown) => { this.error.set(apiErrorMessage(error)); this.loading.set(false); },
      }));
    });
  }

  protected loadTimeline(): void {
    const incident = this.incident();
    if (!incident) return;
    this.timelineRequest?.unsubscribe();
    this.timelineLoading.set(true);
    this.timelineError.set('');
    this.timeline.set([]);
    this.timelineRequest = this.service.getIncidentTimeline(incident.id).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (timeline) => { this.timeline.set(timeline); this.timelineLoading.set(false); },
      error: (error: unknown) => { this.timelineError.set(apiErrorMessage(error)); this.timelineLoading.set(false); },
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
          this.loadTimeline();
        },
        error: (error: unknown) => { this.statusError.set(apiErrorMessage(error)); this.saving.set(false); },
      }));
  }
}
