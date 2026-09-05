# PLAN.md

## Entendimento

O objetivo é construir a primeira versão do **Incident Hub**, uma aplicação web para uma pequena equipe de operações registrar, acompanhar e resolver incidentes operacionais.

A aplicação deverá permitir criar incidentes, listar e filtrar registros, visualizar detalhes, alterar status, manter histórico persistente das mudanças de status e apresentar um dashboard com informações resumidas.

Cada incidente deverá possuir identificador, título, descrição, severidade, responsável, status, data/hora de criação e data/hora da última atualização.

As severidades possíveis serão:

* Low
* Medium
* High
* Critical

Os status possíveis serão:

* Open
* In Progress
* Resolved

Todo novo incidente deverá iniciar automaticamente com status `Open`.

Existe uma regra de negócio crítica: incidentes com severidade `Critical` não poderão passar diretamente de `Open` para `Resolved`. Esses incidentes deverão obrigatoriamente passar primeiro por `In Progress`.

A aplicação deverá persistir os dados para que continuem disponíveis após atualização da página ou reinicialização da aplicação.

A prioridade será entregar uma solução funcional, simples, testada, reproduzível e claramente documentada, evitando funcionalidades não solicitadas.

---

## Escopo

### Obrigatório

* Criar incidentes.
* Validar os campos obrigatórios:

  * título;
  * descrição;
  * severidade;
  * responsável.
* Definir automaticamente novos incidentes como `Open`.
* Registrar automaticamente data/hora de criação.
* Registrar data/hora da última atualização.
* Listar incidentes.
* Exibir na listagem:

  * título;
  * severidade;
  * responsável;
  * status.
* Filtrar incidentes por status.
* Filtrar incidentes por severidade.
* Visualizar os detalhes completos de um incidente.
* Alterar o status de um incidente.
* Impedir a transição direta `Open → Resolved` para incidentes `Critical`.
* Apresentar feedback compreensível para transições inválidas.
* Registrar histórico persistente das alterações de status.
* Mostrar no histórico:

  * status anterior;
  * novo status;
  * data/hora da alteração.
* Implementar dashboard contendo:

  * quantidade de incidentes atualmente abertos;
  * quantidade de incidentes `Critical` ainda não resolvidos;
  * quantidade de incidentes resolvidos.
* Persistir os dados.
* Disponibilizar os três incidentes iniciais definidos no desafio.
* Tratar entradas inválidas relevantes.
* Possuir interface minimamente utilizável.
* Criar testes automatizados para as regras de negócio críticas.
* Possibilitar execução local.
* Documentar instalação, execução, dados iniciais e testes.
* Garantir que a solução possa ser reproduzida a partir do repositório.

### Desejável

Somente após todos os requisitos obrigatórios estarem implementados, funcionando, testados e documentados:

* melhorar organização visual;
* melhorar mensagens de feedback;
* melhorar experiência dos filtros;
* adicionar pequenos indicadores visuais para severidade e status;
* adicionar estados de carregamento ou vazio quando fizer sentido.

### Fora de escopo

Não será implementado nesta primeira versão:

* autenticação;
* cadastro de usuários;
* recuperação de senha;
* níveis de permissão;
* organizações;
* múltiplos tenants;
* notificações;
* comentários;
* anexos;
* integrações externas;
* deploy público obrigatório;
* recursos em tempo real;
* funcionalidades não solicitadas.

---

## Decisões técnicas

### Stack

A aplicação será desenvolvida utilizando:

* **Angular** no frontend;
* **Django** no backend;
* **Django REST Framework** para exposição da API;
* **SQLite** para persistência local.

A principal razão para essa escolha é a familiaridade prévia com Angular e Django, o que reduz risco técnico e tempo de adaptação durante um desafio com duração limitada.

A intenção não é construir uma arquitetura sofisticada, mas utilizar uma stack conhecida para implementar rapidamente uma solução confiável e testável.

### Frontend

O Angular será responsável por:

* dashboard;
* listagem de incidentes;
* filtros;
* formulário de criação;
* visualização dos detalhes;
* alteração de status;
* histórico;
* feedback das operações.

A interface será simples e funcional, priorizando clareza e comportamento correto em vez de sofisticação visual.

### Backend

O Django será responsável por:

* persistência;
* exposição da API;
* validação dos dados;
* regras de negócio;
* alteração de status;
* criação do histórico;
* cálculo ou fornecimento dos dados necessários ao dashboard.

A regra de negócio de transição de status será implementada no backend para não depender exclusivamente da interface.

### Persistência

Será utilizado **SQLite**.

Motivos:

* já possui integração simples com Django;
* não exige servidor externo;
* facilita execução local;
* reduz configuração;
* atende ao tamanho e objetivo do desafio;
* facilita reprodução pelo avaliador.

### Estrutura geral

A solução será dividida em:

* frontend Angular;
* backend Django REST;
* banco SQLite;
* testes de regras críticas no backend;
* testes adicionais quando forem relevantes ao tempo disponível.

A arquitetura será mantida simples, evitando camadas e serviços que não tragam benefício claro ao desafio.

### Estratégia de testes

Os testes automatizados terão prioridade nas regras de negócio do backend.

Serão considerados críticos inicialmente:

1. novo incidente inicia com `Open`;
2. campos obrigatórios são validados;
3. incidente `Critical` não pode realizar `Open → Resolved`;
4. incidente `Critical` pode realizar `Open → In Progress → Resolved`;
5. alterações válidas de status criam registros de histórico;
6. a última atualização é alterada corretamente;
7. dados utilizados pelo dashboard refletem o estado atual;
8. filtros funcionam corretamente.

Os principais fluxos também serão validados manualmente pelo frontend.

---

## Decomposição

### Etapa 1 — Preparação inicial

* Criar `START.md`.
* Criar primeira versão do `PLAN.md`.
* Garantir o checkpoint obrigatório antes das 08:45.
* Definir a estrutura inicial do repositório.

### Etapa 2 — Backend base

* Criar projeto Django.
* Criar app principal.
* Configurar Django REST Framework.
* Criar modelos:

  * Incident;
  * StatusHistory.
* Criar migrations.
* Configurar SQLite.
* Criar dados iniciais.

### Etapa 3 — API e regras de negócio

* Criar endpoints para:

  * listar incidentes;
  * criar incidente;
  * visualizar detalhes;
  * alterar status;
  * consultar histórico;
  * fornecer dados do dashboard.
* Implementar filtros.
* Implementar validações.
* Implementar regra `Critical`.
* Garantir atualização dos timestamps.
* Persistir histórico.

### Etapa 4 — Testes do backend

* Testar criação.
* Testar validações.
* Testar regra `Critical`.
* Testar transições válidas.
* Testar histórico.
* Testar filtros.
* Testar dashboard.

### Etapa 5 — Frontend base

* Criar projeto Angular.
* Configurar acesso à API.
* Criar estrutura de serviços.
* Criar componentes/telas necessárias.

### Etapa 6 — Interface funcional

* Dashboard.
* Lista de incidentes.
* Filtros por status e severidade.
* Criação de incidente.
* Detalhes do incidente.
* Alteração de status.
* Histórico.
* Feedback de erros e validações.

### Etapa 7 — Validação integrada

* Testar frontend + backend.
* Criar incidente.
* Filtrar.
* Abrir detalhes.
* Alterar status.
* Testar tentativa inválida para `Critical`.
* Confirmar histórico.
* Confirmar dashboard.
* Reiniciar backend e confirmar persistência.

### Etapa 8 — Documentação e finalização

* Finalizar `README.md`.
* Atualizar `PLAN.md`.
* Atualizar `AI_LOG.md`.
* Criar `FINAL_REPORT.md`.
* Executar todos os testes.
* Verificar instalação e execução.
* Verificar Git.
* Commitar e enviar tudo antes do code freeze.
* Registrar hash do commit final.

---

## Critérios de aceite

### Criação

Concluído quando:

* título, descrição, severidade e responsável forem obrigatórios;
* novo incidente iniciar automaticamente com `Open`;
* criação e última atualização forem registradas;
* o incidente for persistido;
* o novo incidente aparecer na listagem.

### Listagem

Concluído quando:

* os incidentes forem exibidos;
* título, severidade, responsável e status forem visíveis;
* filtro por status funcionar;
* filtro por severidade funcionar.

### Detalhes

Concluído quando forem exibidos:

* título;
* descrição;
* severidade;
* responsável;
* status;
* criação;
* última atualização.

### Alteração de status

Concluído quando:

* mudanças válidas forem persistidas;
* `Critical Open → Resolved` for bloqueado;
* a aplicação apresentar mensagem compreensível;
* `Critical Open → In Progress → Resolved` funcionar;
* a última atualização for alterada.

### Histórico

Concluído quando:

* cada mudança válida gerar registro;
* o registro possuir status anterior;
* novo status;
* data/hora;
* vínculo com o incidente;
* persistência após reinicialização.

### Dashboard

Concluído quando mostrar corretamente:

* incidentes atualmente abertos;
* incidentes `Critical` ainda não resolvidos;
* incidentes resolvidos.

### Persistência

Concluído quando os dados permanecerem após:

* atualizar a página;
* reiniciar o frontend;
* reiniciar o backend.

### Dados iniciais

Deverá ser possível disponibilizar de maneira simples:

1. `Payment API instability` — Critical — Ana — Open;
2. `Reconciliation delay` — High — Bruno — In Progress;
3. `Incorrect customer notification` — Medium — Carla — Resolved.

### Reprodução

Outra pessoa deverá conseguir utilizar apenas o `README.md` para:

* instalar dependências do backend;
* instalar dependências do frontend;
* preparar o banco;
* disponibilizar dados iniciais;
* iniciar Django;
* iniciar Angular;
* executar os testes.

---

## Riscos

### 1. Complexidade de duas aplicações

Angular + Django implica frontend e backend separados.

**Mitigação:** manter ambos extremamente simples, sem funcionalidades ou camadas desnecessárias.

### 2. Configuração consumir tempo

Integração frontend/backend, CORS e configuração inicial podem gerar retrabalho.

**Mitigação:** realizar a integração básica cedo e validar comunicação entre Angular e Django antes de expandir a aplicação.

### 3. Escopo visual

Existe risco de gastar tempo excessivo estilizando Angular.

**Mitigação:** construir inicialmente apenas uma interface clara e utilizável. Melhorias visuais ficam para depois dos requisitos obrigatórios.

### 4. Regra de negócio implementada apenas no frontend

**Mitigação:** regra `Critical` deverá existir no backend e possuir teste automatizado.

### 5. Regressões

**Mitigação:** executar testes do backend após alterações relevantes e repetir fluxos críticos pela interface.

### 6. Persistência

**Mitigação:** testar reinicialização do backend e confirmar permanência dos dados no SQLite.

### 7. Documentação atrasada

**Mitigação:** atualizar `AI_LOG.md` e documentos progressivamente, sem deixar tudo para o final.

### 8. Limites de IA

**Mitigação:** manter documentação e contexto importante no repositório e ter ferramentas gratuitas alternativas disponíveis.

---

## Estratégia de IA

Todo código, configuração técnica e lógica será produzido por IA a partir de instruções em linguagem natural.

A IA será utilizada de forma incremental e controlada.

O fluxo esperado será:

1. definir objetivo;
2. fornecer contexto;
3. solicitar alteração pequena;
4. revisar o resultado;
5. executar;
6. testar;
7. fornecer erros à IA quando necessário;
8. solicitar correção;
9. testar novamente;
10. verificar regressões;
11. registrar interações relevantes;
12. commit quando a etapa estiver estável.

Será evitado pedir que a IA implemente toda a aplicação de uma vez.

No backend, as tarefas serão divididas entre modelos, serializers, regras de negócio, endpoints, filtros e testes.

No frontend, as tarefas serão divididas entre modelos/interfaces, serviços, componentes, integração com API, validações e feedback visual.

Caso a IA sugira padrões diferentes ou complexidade que não sejam necessários para o problema, a solução será questionada e simplificada.

Erros encontrados serão investigados com a IA antes de alterações adicionais.

As principais interações serão documentadas no `AI_LOG.md`.

---

## Prioridade geral

A ordem de prioridade será:

**Correção → Completude → Simplicidade → Confiabilidade → Funcionalidades adicionais**

A escolha por Angular + Django é deliberada: apesar de envolver frontend e backend separados, é a stack com a qual tenho maior familiaridade, reduzindo risco de adaptação durante o tempo limitado do desafio.
