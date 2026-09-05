import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Severity } from './incident.models';
import { IncidentService } from './incident.service';
import { apiErrorMessage } from './api-error';

@Component({
  selector: 'app-incident-create',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './incident-create.html',
  styleUrl: './incident-create.scss',
})
export class IncidentCreate {
  private readonly service = inject(IncidentService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);
  protected readonly saving = signal(false);
  protected readonly error = signal('');
  protected readonly form = new FormGroup({
    title: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.pattern(/\S/), Validators.maxLength(255)] }),
    description: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.pattern(/\S/)] }),
    severity: new FormControl<Severity | ''>('', { nonNullable: true, validators: [Validators.required] }),
    owner: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.pattern(/\S/), Validators.maxLength(255)] }),
  });

  protected submit(): void {
    if (this.saving()) return;
    this.form.markAllAsTouched();
    this.error.set('');
    const data = this.form.getRawValue();
    if (this.form.invalid || !data.severity) return;
    this.saving.set(true);
    this.service.createIncident({
      title: data.title.trim(), description: data.description.trim(),
      severity: data.severity, owner: data.owner.trim(),
    }).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (incident) => { void this.router.navigate(['/incidents', incident.id]); },
      error: (error: unknown) => { this.error.set(apiErrorMessage(error)); this.saving.set(false); },
    });
  }
}
