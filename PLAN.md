# PLAN.md

# Incident Hub — Plano de Engenharia e Estratégia de Implementação

## 1. Resumo executivo

Este documento descreve o planejamento, a decomposição, as decisões técnicas e a estratégia de execução utilizados para construir o **Incident Hub** em um hackathon de um único dia, com geração de código orientada por IA sob supervisão humana constante.

A prioridade definida desde o início foi:

**Correção → Completude → Simplicidade → Confiabilidade → Extras**

O plano cobre: entendimento do problema, escopo, arquitetura, decisões e trade-offs, decomposição em etapas com gates de qualidade, estratégia de testes, gestão de riscos, uso controlado de IA, controle de regressão e escopo, critérios de aceite verificáveis, matriz de rastreabilidade e a evolução do plano durante a execução.

## 2. Entendimento do problema

O desafio consiste em construir uma aplicação web para que uma pequena equipe de operações registre, acompanhe e resolva incidentes operacionais.

Cada incidente possui: `id`, `title`, `description`, `severity`, `owner`, `status`, `created_at`, `updated_at`.

Severidades: `Low`, `Medium`, `High`, `Critical`.
Status: `Open`, `In Progress`, `Resolved`.

Regra de negócio crítica: um incidente `Critical` não pode realizar a transição direta `Open → Resolved`. O fluxo obrigatório é `Open → In Progress → Resolved`. Uma tentativa inválida deve ser bloqueada e apresentar feedback compreensível.

A aplicação precisa manter histórico de alterações de status, apresentar um dashboard resumido, persistir dados entre reinicializações e ser reproduzível localmente a partir da documentação.

Todo código, configuração técnica e lógica são produzidos por IA a partir de instruções em linguagem natural. Meu papel é entender o problema, planejar, decidir, decompor, orientar a IA, executar comandos, revisar, testar, validar, identificar erros, pedir correções, evitar regressões e controlar o escopo.

## 3. Objetivos da solução

- Implementar integralmente os requisitos funcionais obrigatórios do desafio.
- Centralizar a regra crítica no backend, como única fonte de verdade.
- Garantir persistência real dos dados entre reinicializações.
- Cobrir com testes automatizados as regras de negócio críticas.
- Entregar uma solução reproduzível por terceiros a partir do `README.md`.
- Utilizar IA de forma controlada, com validação humana em cada etapa.
- Evitar escopo não solicitado e evitar regressões em funcionalidades já estabilizadas.

## 4. Princípios de execução

- Nenhuma etapa avança sem que a etapa anterior esteja validada (gates de qualidade).
- Saída de IA nunca é aceita automaticamente; toda saída é revisada, executada e testada antes de ser considerada válida.
- Regras de negócio residem no backend; o frontend consome e exibe o resultado, sem duplicar lógica.
- Escopo obrigatório tem prioridade absoluta sobre qualquer melhoria desejável, incluindo aparência visual.
- Toda mudança relevante é seguida de reexecução dos testes automatizados e dos fluxos manuais críticos, para conter regressões.
- Decisões técnicas consideram a familiaridade prévia da equipe como fator legítimo de redução de risco, não apenas preferência pessoal.

## 5. Escopo

### 5.1 Obrigatório

- Criar incidentes, com `title`, `description`, `severity` e `owner` obrigatórios.
- Definir automaticamente `status = Open` e `created_at`/`updated_at` na criação.
- Listar incidentes com título, severidade, responsável e status.
- Filtrar por `status` e por `severity`.
- Visualizar todos os campos de um incidente em uma tela de detalhes.
- Alterar o status de um incidente.
- Bloquear a transição `Critical: Open → Resolved`, com feedback compreensível.
- Persistir histórico de cada alteração válida de status (status anterior, novo status, timestamp, vínculo com o incidente).
- Implementar dashboard com: incidentes `Open`, `Critical` ainda não `Resolved`, e incidentes `Resolved`.
- Persistir dados após refresh e após reinicialização da aplicação.
- Disponibilizar os três incidentes iniciais obrigatórios via comando de seed.
- Tratar entradas inválidas com feedback compreensível.
- Cobrir com testes automatizados as regras de negócio críticas.
- Documentar instalação, execução, dados iniciais e testes, permitindo reprodução local.

### 5.2 Desejável

Somente após o escopo obrigatório estar implementado, testado e documentado:

- Melhorar organização visual da interface (redesign).
- Melhorar mensagens de feedback.
- Melhorar experiência de uso dos filtros.
- Adicionar indicadores visuais para severidade e status (badges).
- Adicionar estados de carregamento ou vazio, quando fizer sentido.

### 5.3 Fora de escopo

Autenticação, cadastro de usuários, recuperação de senha, permissões, organizações/multi-tenant, comentários, anexos, notificações, atualização em tempo real, gráficos, busca textual, paginação sem necessidade, deploy público, infraestrutura complexa, bibliotecas pesadas, abstrações sem benefício claro e qualquer regra de negócio não solicitada.

Controlar o escopo é uma decisão de engenharia, não uma omissão. Cada item excluído reduz superfície de risco, reduz tempo de configuração e testes, e mantém o foco no requisito obrigatório, preservando a confiabilidade da entrega dentro do tempo disponível de um hackathon de um dia.

## 6. Arquitetura proposta

### Fluxo

```
Angular (frontend)
      ↓
IncidentService (HttpClient)
      ↓
API REST (HTTP)
      ↓
Django REST Framework
      ↓
Services / regras de negócio
      ↓
Models
      ↓
SQLite
```

### Frontend

Angular é responsável por: dashboard, listagem, filtros, formulário de criação, detalhes, alteração de status, histórico e feedback de erros. O acesso à API é centralizado em um `IncidentService`. A interface prioriza clareza e comportamento correto sobre sofisticação visual na primeira versão.

### Backend

Django é responsável por: persistência, validação, regras de negócio, API REST, histórico de status e dashboard. A regra crítica de transição de status é centralizada em uma função equivalente a `change_incident_status(incident, new_status)`, responsável por validar o novo status, impedir `Critical: Open → Resolved`, atualizar o incidente e o `updated_at`, criar histórico, evitar histórico duplicado quando o status não muda, e operar de forma transacional.

O frontend não replica essa regra: apenas envia a solicitação e apresenta o feedback retornado pelo backend. Isso garante única fonte de verdade, consistência, testabilidade, menor duplicação e menor risco de divergência entre clientes diferentes.

### Persistência

SQLite foi escolhido conscientemente, não por limitação. Motivos: simplicidade, ausência de servidor adicional, execução local, facilidade de reprodução pelo avaliador, baixo overhead operacional e adequação ao volume e à duração do desafio. SQLite não é tratado como solução inferior neste contexto.

## 7. Decisões técnicas e trade-offs

### Angular + Django vs. stack sugerida por IA (Node.js)

- **Escolha:** Angular + Django.
- **Alternativa considerada:** durante a análise inicial, uma IA sugeriu Node.js.
- **Motivo da rejeição:** ausência de experiência prática suficiente com Node.js para assumir esse risco em um desafio de poucas horas. A familiaridade prévia com Angular e Django foi tratada como fator legítimo de decisão arquitetural, reduzindo risco técnico e tempo de adaptação.
- **Trade-off:** duas aplicações/processos separados para executar (frontend e backend).
- **Mitigação:** estrutura simples em ambos os lados e documentação clara de execução.

### SQLite vs. banco com servidor

- **Escolha:** SQLite.
- **Benefício:** simplicidade e reprodução local imediata.
- **Limitação:** não projetado para grande escala ou múltiplos usuários concorrentes.
- **Aceitável porque:** o escopo do desafio é local, de pequena escala e de curta duração.

### Regra crítica no backend vs. no frontend

- **Escolha:** backend.
- **Motivo:** fonte única de verdade, testabilidade e proteção contra divergência entre clientes diferentes.

### Cobertura de testes: backend priorizado vs. cobertura extensa no frontend

- **Escolha:** concentrar testes automatizados no backend, especialmente na regra crítica.
- **Motivo:** é onde reside a regra de negócio e o maior risco de regressão silenciosa.
- **Mitigação no frontend:** build da aplicação e validação manual integrada com o backend.

### Funcionalidade antes de design

- **Escolha:** estabilizar o core funcional antes de investir em aparência.
- **Depois:** com o core validado e havendo tempo restante, promover o redesign a uma etapa real de trabalho.

## 8. Estratégia de implementação

A implementação seguiu a lógica de fases dependentes, sem inventar horários não fornecidos:

**Fase 1** — compreender o problema e planejar.
**Fase 2** — garantir backend base e regra crítica.
**Fase 3** — testar o backend.
**Fase 4** — construir frontend funcional.
**Fase 5** — validar integração real entre frontend e backend.
**Fase 6** — documentar.
**Fase 7** — somente com o core estável, investir em aparência (redesign).
**Fase 8** — revisão final, testes, Git e code freeze.

A dependência entre fases é explícita: não faz sentido investir pesado no frontend antes de a API estar minimamente estável; não faz sentido investir em redesign antes de os fluxos obrigatórios estarem validados; não faz sentido adicionar extras enquanto um critério obrigatório estiver incompleto.

## 9. Decomposição por etapas

### Etapa 1 — Preparação inicial

- **Objetivo:** estabelecer marco inicial e plano de trabalho.
- **Dependências:** nenhuma.
- **Atividades:** criar `START.md`; criar primeira versão do `PLAN.md`; definir estrutura inicial do repositório.
- **Saída:** repositório inicializado com plano registrado.
- **Validação:** documentos presentes e coerentes com o desafio.
- **Gate:** não iniciar implementação de código sem plano registrado.

### Etapa 2 — Backend base

- **Objetivo:** disponibilizar fundação Django funcional.
- **Dependências:** Etapa 1 concluída.
- **Atividades:** criar projeto Django; criar app principal; configurar Django REST Framework e `django-cors-headers`; criar `requirements.txt` e `.gitignore`; criar modelos `Incident` e `IncidentStatusHistory` (histórico); gerar migrations; configurar SQLite.
- **Saída:** projeto Django executável, com modelos migrados.
- **Validação:** `python manage.py check` sem erros; `python manage.py migrate` executado com sucesso.
- **Gate:** não avançar para regras de negócio sem modelos migrados.

### Etapa 3 — Regra crítica de transição de status

- **Objetivo:** centralizar e proteger a transição `Critical: Open → Resolved`.
- **Dependências:** modelos criados (Etapa 2).
- **Atividades:** implementar serviço de alteração de status contendo validação de transição, bloqueio da transição inválida, atualização de `updated_at`, criação de histórico, prevenção de histórico duplicado e execução transacional.
- **Saída:** função de alteração de status testável isoladamente.
- **Validação:** testes automatizados cobrindo transição válida, transição inválida e ausência de histórico duplicado.
- **Gate:** não avançar para os endpoints de status enquanto a regra não estiver testada.

### Etapa 4 — API e endpoints

- **Objetivo:** expor as operações do domínio via API REST.
- **Dependências:** Etapa 3 concluída.
- **Atividades:** implementar `GET/POST /api/incidents/`, `GET /api/incidents/<id>/`, `PATCH /api/incidents/<id>/status/`, `GET /api/incidents/<id>/history/`, `GET /api/dashboard/`; implementar filtros por `status` e `severity`; implementar comando de seed com os três incidentes obrigatórios.
- **Saída:** API funcional e navegável localmente.
- **Validação:** testes automatizados de endpoints e execução real com `runserver`.
- **Gate:** não avançar para o frontend sem endpoints testados.

### Etapa 5 — Testes do backend

- **Objetivo:** consolidar cobertura das regras críticas antes de seguir para o frontend.
- **Dependências:** Etapa 4 concluída.
- **Atividades:** revisão da suíte de testes cobrindo criação, validação de campos obrigatórios, status inicial `Open`, timestamps, listagem, filtros, detalhes, transições válidas, bloqueio da regra `Critical`, mensagens de erro, histórico, ausência de histórico duplicado, rollback/transação, dashboard, atualização do dashboard e seed reproduzível.
- **Saída:** 26 testes automatizados passando.
- **Validação:** `python manage.py test` e `python manage.py check` sem falhas.
- **Gate:** não iniciar o frontend com testes de backend falhando.

### Etapa 6 — Frontend base

- **Objetivo:** disponibilizar fundação Angular integrada à API.
- **Dependências:** Etapa 5 concluída (API estável e testada).
- **Atividades:** scaffold Angular; configurar routing; configurar `HttpClient` e URL base da API; criar models/interfaces; criar `IncidentService` centralizando as chamadas HTTP.
- **Saída:** projeto Angular capaz de se comunicar com a API.
- **Validação:** requisição de teste bem-sucedida entre Angular e Django (CORS funcionando).
- **Gate:** não construir telas de negócio sem comunicação básica validada.

### Etapa 7 — Interface funcional

- **Objetivo:** implementar as telas necessárias ao fluxo completo do desafio.
- **Dependências:** Etapa 6 concluída.
- **Atividades:** dashboard; listagem; filtros; criação de incidente; detalhes; alteração de status; histórico; tratamento de erros e feedback ao usuário.
- **Saída:** aplicação Angular funcional, cobrindo todas as rotas (`/`, `/incidents`, `/incidents/new`, `/incidents/:id`).
- **Validação:** `npm run build` sem erros; navegação manual pelas telas.
- **Gate:** não avançar para validação integrada sem build limpo.

### Etapa 8 — Validação integrada

- **Objetivo:** confirmar o comportamento real do sistema com frontend e backend em execução simultânea.
- **Dependências:** Etapa 7 concluída.
- **Atividades:** validar manualmente dashboard, listagem, filtros (isolados e combinados), criação, detalhes, alteração válida de status, tentativa inválida `Critical: Open → Resolved`, mensagem de erro, histórico, atualização das métricas do dashboard e persistência após reinicialização do backend.
- **Saída:** evidência de que os fluxos obrigatórios funcionam de ponta a ponta.
- **Validação:** checklist manual executado sem falhas.
- **Gate:** não iniciar o redesign visual sem os fluxos obrigatórios validados.

### Etapa 9 — Redesign visual (etapa promovida)

- **Objetivo:** melhorar a aparência da interface preservando o comportamento existente.
- **Dependências:** Etapa 8 concluída (core estável e validado).
- **Atividades:** produção de referência visual (Lovable) a partir de screenshots das quatro telas; aplicação do redesign na codebase Angular existente (Codex), alterando majoritariamente HTML e SCSS; planejamento e refinamento das instruções (ChatGPT).
- **Saída:** interface com sidebar, header, cards, badges, tabelas, formulário mais estruturado e histórico com apresentação mais visual, preservando backend, API, `IncidentService`, models, rotas, regras de negócio e chamadas HTTP.
- **Validação:** `npm run build` continua passando; repetição do checklist de fluxos críticos da Etapa 8.
- **Gate:** reverter alteração caso qualquer fluxo obrigatório deixe de funcionar.

### Etapa 10 — Documentação e finalização

- **Objetivo:** consolidar documentação e preparar entrega.
- **Dependências:** Etapa 9 concluída (ou Etapa 8, caso o redesign não fosse viável no tempo restante).
- **Atividades:** finalizar `README.md`; atualizar `PLAN.md`; atualizar `AI_LOG.md`; criar `FINAL_REPORT.md`; reexecutar `python manage.py test`, `python manage.py check` e `npm run build`; verificar instalação e execução do zero; verificar status do Git; commit e push finais.
- **Saída:** repositório pronto para avaliação.
- **Validação:** revisar o `README.md` e, se houver tempo antes do code freeze, executar reprodução completa a partir de ambiente limpo.
- **Gate:** code freeze só ocorre após todos os testes e verificações acima passarem.

## 10. Estratégia da regra crítica

A regra é implementada e testada em um único ponto do backend, evitando qualquer duplicação no frontend. A validação ocorre antes da persistência da mudança de status: se a transição for inválida (`Critical: Open → Resolved`), a operação é rejeitada, o incidente permanece no status anterior, nenhum histórico é criado e a API retorna um erro com mensagem compreensível, exibida pelo frontend. A cobertura de teste automatizado desta regra é tratada como pré-requisito (gate) para a implementação dos endpoints que dependem dela.

## 11. Estratégia de persistência e histórico

Os dados residem em SQLite, sem servidor adicional. Cada alteração válida de status gera um registro de histórico contendo status anterior, novo status, timestamp e vínculo com o incidente correspondente. A ausência de histórico duplicado (quando o novo status é igual ao atual) e a execução transacional da alteração de status são tratadas como parte da mesma regra de negócio, não como funcionalidades separadas. A persistência é validada tanto por teste automatizado quanto por verificação manual após reinicialização do backend.

## 12. Estratégia de frontend

O frontend é construído após a API estar estável e testada, evitando integração contra uma base instável. Toda comunicação HTTP é centralizada no `IncidentService`, e nenhuma regra de negócio é replicada na camada Angular — a interface apenas envia solicitações e exibe o retorno do backend, incluindo mensagens de erro. Essa centralização reduz risco de divergência entre a validação do backend e o comportamento exibido ao usuário.

## 13. Estratégia de redesign visual

O redesign visual foi tratado como parte de uma etapa condicionada à conclusão do core (Etapa 9), e não como desvio da prioridade original — é execução disciplinada da prioridade "funcionalidade antes de aparência" definida desde o início. A referência visual (Lovable) foi usada exclusivamente como exploração, a partir de screenshots das quatro telas existentes (Dashboard, Incidentes, Novo incidente, Detalhes), sem substituir a aplicação Angular. A aplicação do redesign (Codex) recebeu instrução explícita de preservar backend, API, `IncidentService`, models, rotas, regras de negócio e comportamento existente, alterando principalmente HTML e SCSS. Qualquer alteração de lógica durante essa etapa é tratada como desvio de escopo, não como parte do redesign.

## 14. Estratégia de testes

Os testes automatizados priorizam o backend, por concentrar a regra de negócio crítica e o maior risco de regressão silenciosa. A suíte cobre: criação de incidentes, validação de campos obrigatórios, status inicial `Open`, timestamps, listagem, filtros, detalhes, transições válidas de status, bloqueio da regra `Critical`, mensagens de erro, histórico, ausência de histórico duplicado, rollback em falha (transação), dashboard, atualização do dashboard após mudança de status e seed reproduzível. Ao final da etapa de backend, 26 testes automatizados estavam passando. No frontend, a validação é feita por `npm run build` combinado com verificação manual integrada, já que o volume de lógica de negócio no Angular é intencionalmente baixo.

Build, teste automatizado e teste manual são mecanismos complementares, não substitutos entre si: build não substitui teste funcional; teste automatizado não substitui integração real; teste manual não substitui teste automatizado.

## 15. Validação integrada

Com frontend e backend em execução simultânea, foram validados manualmente: carregamento do dashboard, listagem, filtro por status, filtro por severidade, filtros combinados, criação de incidente, detalhes, alteração válida de status, tentativa inválida `Critical: Open → Resolved`, mensagem de erro compreensível, histórico, atualização das métricas do dashboard e persistência após reinicialização do backend. Foram também utilizados `npm run build`, `python manage.py test` e `python manage.py check` como parte dessa verificação.

## 16. Critérios de aceite

| Área | Condição | Verificação | Evidência esperada |
|---|---|---|---|
| Criação | `title`, `description`, `severity` e `owner` obrigatórios; status inicia como `Open`; `created_at`/`updated_at` registrados | Teste automatizado + manual | Incidente persistido como `Open`, visível na listagem |
| Listagem | Título, severidade, responsável e status exibidos | Teste automatizado + manual | Lista renderizada com os campos corretos |
| Filtros | Filtro por `status` e por `severity`, isolados e combinados | Teste automatizado + manual | Resultado filtrado corresponde ao critério aplicado |
| Detalhes | Todos os campos do incidente exibidos | Manual | Tela de detalhes completa |
| Mudança de status | Transições válidas persistidas; `updated_at` atualizado | Teste automatizado + manual | Status alterado e refletido na interface |
| Regra Critical | Requisição de `Open → Resolved` para `Critical` é rejeitada; incidente permanece `Open`; nenhum histórico inválido é criado; frontend apresenta feedback compreensível | Teste automatizado + manual | Erro retornado pela API e exibido na interface |
| Histórico | Cada mudança válida gera registro com status anterior, novo status, timestamp e vínculo com o incidente | Teste automatizado + manual | Histórico visível na tela de detalhes |
| Dashboard | Contagens de `Open`, `Critical` não resolvidos e `Resolved` corretas | Teste automatizado + manual | Métricas corretas após alteração de status |
| Persistência | Dados mantidos após refresh e reinicialização do backend | Manual | Dados presentes após reinício do processo |
| Seed | Os três incidentes obrigatórios recriados corretamente | Teste automatizado | Registros conforme especificação do seed |
| Integração | Frontend e backend operando juntos sem divergência | Manual | Checklist de fluxos executado sem falhas |
| Testes | Suíte automatizada do backend passando | `python manage.py test` | 26 testes passando |
| Reprodução | Outra pessoa deve conseguir instalar e executar a partir do `README.md` | Validação final planejada | Instruções completas e, se houver tempo antes do code freeze, execução a partir de ambiente limpo |
| Documentação | `README.md`, `PLAN.md`, `AI_LOG.md`, `FINAL_REPORT.md` presentes e coerentes | Manual | Documentos completos no repositório |
| Frontend visual | Redesign aplicado sem quebrar fluxos obrigatórios | `npm run build` + manual | Build passando e checklist da Etapa 8 repetido com sucesso |

## 17. Matriz de rastreabilidade

| Requisito | Componente responsável | Validação | Critério de aceite |
|---|---|---|---|
| Criação de incidente | API + `IncidentService` + formulário Angular | Testes de API + manual | Incidente persistido como `Open` |
| Listagem e filtros | API (filtros) + listagem Angular | Testes de API + manual | Filtros retornam subconjunto correto |
| Detalhes | API (detalhe) + tela de detalhes Angular | Manual | Todos os campos exibidos |
| Regra Critical | Serviço de alteração de status no backend | Testes automatizados + manual | Transição inválida bloqueada |
| Histórico | Model `IncidentStatusHistory` + serviço + endpoint + tela de detalhes | Testes automatizados + manual | Alteração persistida e exibida |
| Dashboard | Endpoint `/api/dashboard/` + tela de dashboard Angular | Testes automatizados + manual | Métricas corretas |
| Persistência | SQLite + migrations | Manual (reinicialização) | Dados mantidos após restart |
| Seed | Management command `seed_incidents` | Testes automatizados | Três incidentes obrigatórios recriados |
| Reprodutibilidade | `README.md` | Manual | Instalação e execução por terceiros |

## 18. Gates de qualidade

- **Gate backend base:** migrations aplicadas; `python manage.py check` sem erros.
- **Gate regra crítica:** testes da regra de transição passando antes de implementar endpoints de status.
- **Gate API:** endpoints testados (automatizado) antes de iniciar o frontend.
- **Gate frontend:** `npm run build` sem erros antes da validação integrada.
- **Gate integração:** checklist de fluxos manuais passando antes do redesign.
- **Gate redesign:** build continua passando e fluxos obrigatórios preservados; qualquer regressão é revertida.
- **Gate final:** documentação atualizada, testes automatizados passando, `git status` limpo, commit e push realizados, hash do commit final registrado.

## 19. Gestão de riscos

| Risco | Impacto | Probabilidade | Mitigação | Evidência/controle |
|---|---|---|---|---|
| Complexidade de duas aplicações (frontend + backend) | Médio | Média | Manter ambos os lados simples, sem camadas desnecessárias | Estrutura enxuta do repositório |
| CORS mal configurado | Médio | Média | Validar comunicação básica Angular↔Django cedo (Etapa 6) | Requisição de teste bem-sucedida |
| Tempo de configuração inicial | Médio | Média | Sequenciar setup antes de features | Etapas 2 e 6 concluídas antes das telas de negócio |
| Divergência entre frontend e backend | Alto | Baixa | Regra de negócio centralizada no backend; frontend apenas exibe retorno | Ausência de lógica de negócio duplicada no Angular |
| Regra Critical duplicada indevidamente | Alto | Baixa | Revisão explícita garantindo que o frontend não reimplementa a regra | Inspeção do `IncidentService` e dos componentes |
| Regressão em funcionalidade já validada | Alto | Média | Reexecutar testes automatizados e checklist manual após mudanças relevantes, especialmente no redesign | Testes e checklist repetidos nas Etapas 8 e 9 |
| Falha de persistência após reinicialização | Alto | Baixa | Teste manual de reinicialização do backend | Dados presentes após restart |
| Documentação atrasada | Médio | Média | Atualizar `AI_LOG.md` e demais documentos progressivamente | Documentos atualizados ao longo das etapas, não apenas no final |
| Excesso de escopo (feature creep) | Médio | Média | Escopo obrigatório/desejável/fora de escopo definido antes da implementação | Seção 5 deste documento |
| Tempo gasto em design além do disponível | Médio | Média | Redesign só é iniciado após core validado (Etapa 8 concluída) | Gate da Etapa 9 |
| Limites de uso gratuito de IA (Codex) | Médio | Média | Agrupar tarefas relacionadas do frontend quando o limite gratuito começou a diminuir | Registrado como adaptação consciente na Seção 25 |
| Instrução de IA não seguida integralmente | Baixo | Média | Revisão manual de toda saída antes de aceitar | Revisão registrada no `AI_LOG.md` |
| Decisão arquitetural inadequada sugerida por IA | Médio | Baixa | Sugestão de Node.js avaliada e rejeitada com base em experiência prévia | Registrado na Seção 7 |
| Alteração visual quebrando lógica existente | Alto | Média | Instrução explícita ao Codex para preservar backend, API e regras de negócio; gate de build e checklist após o redesign | Gate da Etapa 9 |
| Falha de reprodução em outra máquina | Médio | Baixa | Documentação de instalação, seed e execução no `README.md` | Verificação de instalação do zero na Etapa 10 |

## 20. Estratégia de IA

Todo código, configuração técnica e lógica são produzidos por IA a partir de instruções em linguagem natural, seguindo o fluxo:

```
Objetivo → Contexto → Instrução → Execução → Validação → Correção → Nova validação → Decisão → Commit quando estável
```

Foi evitado solicitar a implementação da aplicação inteira em um único pedido. No backend, as tarefas foram divididas entre modelos, serializers, regra de negócio, endpoints, filtros e testes. No frontend, entre models/interfaces, serviços, componentes, integração com a API, validações e feedback.

Quando os limites de uso gratuito do Codex começaram a diminuir, tarefas relacionadas do frontend foram agrupadas em uma única solicitação mais detalhada. Essa mudança é tratada como gestão consciente de uma restrição de ferramenta, não como perda de controle de escopo — a divisão por camada e por responsabilidade foi mantida, apenas o agrupamento de tarefas correlatas foi ajustado.

Ferramentas efetivamente utilizadas: ChatGPT Free, Codex em acesso gratuito e Lovable em acesso gratuito. Nenhuma modalidade paga (ChatGPT Plus, ChatGPT Pro, API paga, créditos pagos, Codex com capacidade paga, Lovable pago ou conta corporativa premium) foi utilizada.

Nenhuma saída de IA foi aceita automaticamente como correta. Situações identificadas e tratadas criticamente incluíram: sugestão inicial de stack (Node.js) sem considerar a experiência prévia da equipe, sendo rejeitada; formatação não seguida perfeitamente em algumas instruções, sendo corrigida; e primeira versão do frontend funcional, porém visualmente simples, sendo posteriormente reavaliada na Etapa 9.

## 21. Controle de regressões

Estratégias aplicadas para conter regressão em funcionalidades já estabilizadas:

- regra crítica centralizada em um único ponto do backend, testada isoladamente;
- testes automatizados reexecutados após alterações relevantes;
- build do frontend reexecutado após alterações relevantes;
- repetição do checklist de integração manual após mudanças, especialmente após o redesign;
- escopo de cada tarefa de IA limitado, evitando refatorações não solicitadas;
- proibição explícita de alteração de lógica durante a etapa de redesign visual;
- commits intermediários realizados em estados estáveis, permitindo reverter caso uma mudança introduza regressão.

## 22. Controle de escopo

O controle de escopo (Seção 5.3) é tratado como decisão de engenharia, não apenas como uma lista de exclusões. Cada item fora de escopo (autenticação, permissões, multi-tenant, notificações, tempo real, gráficos, busca textual, paginação sem necessidade, deploy público, entre outros) reduz tempo de implementação e testes, reduz risco de introdução de bugs em áreas não avaliadas, mantém o foco nos requisitos obrigatórios do desafio e preserva a confiabilidade da entrega dentro do prazo de um dia. Ampliar escopo sem necessidade competiria diretamente com completude e confiabilidade dos requisitos obrigatórios.

## 23. Reprodutibilidade

A reprodutibilidade é tratada como requisito de primeira classe, não como item de documentação acessório. O `README.md` deve permitir que outra pessoa, sem contexto prévio, instale dependências do backend e do frontend, prepare o banco (`migrate`), disponibilize os dados iniciais (`seed_incidents`), inicie os dois servidores e execute os testes automatizados. Essa capacidade está prevista como uma validação final da Etapa 10 antes do code freeze. Caso não haja tempo para executar uma reprodução completa em um clone limpo, essa limitação deverá ser registrada explicitamente no relatório final.

## 24. Documentação e auditoria

| Documento | Função |
|---|---|
| `START.md` | Marco inicial do desafio |
| `PLAN.md` | Planejamento, decisões e estratégia de implementação |
| `AI_LOG.md` | Registro das interações relevantes com IA |
| `README.md` | Instalação, execução e reprodução |
| `FINAL_REPORT.md` | Retrospectiva e avaliação do resultado |
| Histórico Git | Commits intermediários em estados estáveis, permitindo rastrear a evolução da solução |

## 25. Evolução do plano durante a execução

O planejamento inicial não foi tratado como rígido. As seguintes adaptações ocorreram durante a execução, sem alterar o objetivo central da solução:

1. **Stack:** uma sugestão inicial de Node.js foi avaliada e rejeitada; o plano foi mantido em Angular + Django, com base na familiaridade prévia da equipe.
2. **Uso de IA:** algumas tarefas do frontend foram agrupadas em solicitações mais amplas quando o limite de uso gratuito do Codex começou a diminuir, como forma de gerir essa restrição sem perder a divisão por camada.
3. **Design:** inicialmente tratado como item desejável de baixa prioridade; após o core estar funcional, testado e validado (Etapa 8), foi promovido a uma etapa real de melhoria (Etapa 9).
4. **Ferramentas:** o Lovable foi incorporado posteriormente ao plano, especificamente como ferramenta de exploração e referência visual, sem substituir a codebase Angular existente.

Essas adaptações refletem reavaliação de tempo disponível e de risco a cada etapa concluída, não desvio da prioridade original definida na Seção 1.

## 26. Estratégia de finalização e code freeze

A finalização (Etapa 10) inclui: atualização de `README.md`, `PLAN.md`, `AI_LOG.md` e criação do `FINAL_REPORT.md`; reexecução de `python manage.py test`, `python manage.py check` e `npm run build`; verificação de instalação e execução a partir de um estado limpo; verificação do estado do Git; commit e push finais; e registro do hash do commit final. O code freeze só ocorre após todos os itens acima serem confirmados.

## 27. Prioridade geral

**Correção → Completude → Simplicidade → Confiabilidade → Extras.**

Toda decisão registrada neste plano — da escolha de stack ao momento de iniciar o redesign visual — é subordinada a essa ordem de prioridade. Funcionalidades adicionais e melhorias de aparência somente foram consideradas depois que os requisitos obrigatórios estavam implementados, testados e validados de ponta a ponta.