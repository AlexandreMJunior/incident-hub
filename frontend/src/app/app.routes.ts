import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'incidents',
    title: 'Incidentes | Incident Hub',
    loadComponent: () => import('./incidents/incident-list').then((m) => m.IncidentList),
  },
  {
    path: 'incidents/new',
    title: 'Novo incidente | Incident Hub',
    loadComponent: () => import('./incidents/incident-create').then((m) => m.IncidentCreate),
  },
  {
    path: 'incidents/:id',
    title: 'Detalhes | Incident Hub',
    loadComponent: () => import('./incidents/incident-detail').then((m) => m.IncidentDetail),
  },
  {
    path: '',
    pathMatch: 'full',
    title: 'Dashboard | Incident Hub',
    loadComponent: () => import('./dashboard/dashboard').then((m) => m.Dashboard),
  },
];
