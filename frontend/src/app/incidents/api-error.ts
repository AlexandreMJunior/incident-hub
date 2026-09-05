import { HttpErrorResponse } from '@angular/common/http';

export function apiErrorMessage(error: unknown): string {
  if (!(error instanceof HttpErrorResponse)) return 'Não foi possível concluir a operação.';
  if (error.status === 0) return 'Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.';
  if (error.status === 404) return 'Incidente não encontrado.';
  if (error.status >= 500) return 'O servidor não conseguiu concluir a operação. Tente novamente em instantes.';
  const labels: Record<string, string> = {
    title: 'Título', description: 'Descrição', severity: 'Severidade', owner: 'Responsável', status: 'Status',
  };
  const body: unknown = error.error;
  if (body && typeof body === 'object' && !Array.isArray(body)) {
    const messages = Object.entries(body).flatMap(([field, value]) => {
      const items: unknown[] = Array.isArray(value) ? value : [value];
      return items.filter((item): item is string => typeof item === 'string')
        .map((message) => `${labels[field] ? labels[field] + ': ' : ''}${message}`);
    });
    if (messages.length) return messages.join(' ');
  }
  return 'Não foi possível concluir a operação. Verifique os dados e tente novamente.';
}
