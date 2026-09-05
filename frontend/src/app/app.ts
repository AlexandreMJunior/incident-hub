import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterLink, RouterLinkActive, RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  private readonly router = inject(Router);
  protected get isDetail(): boolean {
    return /^\/incidents\/(?!new(?:[/?#]|$))[^/?#]+/.test(this.router.url);
  }
  protected get breadcrumb(): string {
    const path = this.router.url.split(/[?#]/)[0];
    if (path === '/incidents/new') return 'Novo incidente';
    if (this.isDetail) return 'Detalhes do incidente';
    return path === '/incidents' ? 'Incidentes' : 'Dashboard';
  }
}
