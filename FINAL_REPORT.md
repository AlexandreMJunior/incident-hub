# FINAL_REPORT.md

# Incident Hub — Relatório Final

## 1. O que foi entregue?

Foi entregue uma aplicação web funcional para registro e acompanhamento de incidentes operacionais, composta por frontend Angular e backend Django REST Framework.

As principais funcionalidades concluídas foram:

- criação de incidentes;
- listagem de incidentes;
- filtro por status;
- filtro por severidade;
- visualização dos detalhes de um incidente;
- alteração de status;
- histórico persistente das alterações de status;
- dashboard com:
  - quantidade de incidentes Open;
  - quantidade de incidentes Critical ainda não resolvidos;
  - quantidade de incidentes Resolved;
- persistência utilizando SQLite;
- comando reproduzível para criação/reset dos dados iniciais;
- tratamento de entradas inválidas;
- feedback para operações inválidas;
- regra de negócio para incidentes Critical;
- testes automatizados do backend;
- validação integrada de frontend e backend;
- documentação para instalação, execução, testes e reprodução da solução;
- redesign visual do frontend após conclusão e validação dos requisitos funcionais;
- sidebar de navegação;
- header operacional;
- cards de métricas;
- badges visuais de severidade e status;
- melhoria visual da tabela de incidentes;
- reformulação do formulário de criação;
- reorganização visual da tela de detalhes;
- histórico apresentado de forma visualmente mais organizada;
- identidade visual consistente entre as páginas.

A regra crítica:

`Critical: Open → Resolved`

foi implementada no backend e bloqueada corretamente.

O fluxo válido permanece:

`Open → In Progress → Resolved`

Também foram entregues:

- `START.md`;
- `PLAN.md`;
- `AI_LOG.md`;
- `README.md`;
- `FINAL_REPORT.md`;
- código do backend;
- código do frontend;
- testes automatizados.

---

## 2. O que não foi entregue?

Não foram implementadas funcionalidades que não faziam parte dos requisitos obrigatórios ou que aumentariam desnecessariamente o escopo da aplicação.

Entre os itens não implementados estão:

- autenticação;
- níveis de permissão;
- cadastro de usuários;
- organizações;
- múltiplos tenants;
- notificações;
- anexos;
- comentários;
- atualizações em tempo real;
- deploy público;
- paginação;
- busca textual;
- gráficos;
- dark mode;
- recursos analíticos adicionais.

Inicialmente, a interface produzida pela IA era funcional, porém visualmente muito simples.

Depois que os requisitos obrigatórios estavam implementados, testados e integrados, decidi utilizar parte do tempo restante para melhorar a apresentação visual da aplicação.

O redesign foi realizado sem alterar regras de negócio, contratos da API ou fluxos existentes.

---

## 3. O que você deliberadamente decidiu não fazer?

Decidi não adicionar funcionalidades extras enquanto existissem requisitos obrigatórios a serem implementados, testados ou documentados.

Também decidi não investir tempo em:

- animações complexas;
- bibliotecas visuais pesadas;
- autenticação;
- infraestrutura de deploy;
- arquitetura mais complexa;
- abstrações que não fossem necessárias;
- gráficos;
- dark mode;
- funcionalidades adicionais não solicitadas.

Inicialmente, também não priorizei o design visual, pois a primeira meta era garantir que todos os fluxos obrigatórios funcionassem corretamente.

Depois que backend, frontend, integração e testes principais estavam concluídos, reavaliei essa decisão.

Como ainda havia tempo disponível e a interface original estava visualmente abaixo do que eu considerava adequado, decidi realizar uma etapa específica de redesign.

Essa mudança de prioridade só ocorreu depois que os requisitos funcionais estavam estáveis.

A prioridade durante todo o desenvolvimento permaneceu:

**correção → completude → simplicidade → confiabilidade → funcionalidades adicionais**

Uma decisão importante foi utilizar SQLite em vez de PostgreSQL ou outro banco com servidor separado.

A intenção foi reduzir dependências externas e tornar a execução pelo avaliador mais simples e reproduzível.

---

## 4. Quais foram as três principais decisões técnicas?

### 1. Angular + Django REST Framework

A primeira decisão importante foi utilizar Angular no frontend e Django REST Framework no backend.

Essa escolha ocorreu principalmente pela minha familiaridade com essas tecnologias.

Em um desafio com tempo limitado, considerei mais seguro trabalhar com uma stack conhecida do que aprender ou adaptar uma stack diferente durante o desenvolvimento.

### 2. SQLite para persistência

Escolhi SQLite para evitar a necessidade de instalar, configurar e executar um servidor de banco adicional.

Para o tamanho e objetivo desta primeira versão, SQLite oferece persistência suficiente e simplifica significativamente a reprodução da aplicação.

### 3. Centralização da alteração de status no backend

A regra de alteração de status foi centralizada em:

`change_incident_status(incident, new_status)`

A intenção foi evitar que a regra crítica:

`Critical: Open → Resolved`

fosse duplicada entre frontend, serializer e view.

Isso também tornou a regra mais simples de testar e reduziu o risco de comportamentos inconsistentes.

---

## 5. Qual foi o maior erro produzido pela IA durante o desenvolvimento?

O principal problema que identifiquei no uso da IA não foi apenas um erro de código, mas um erro de tomada de decisão no início do processo.

Ao discutir a stack inicial, a IA sugeriu Node.js como base da solução sem primeiro perguntar qual era minha experiência ou preferência tecnológica.

Essa recomendação não era adequada ao meu contexto, pois não tenho familiaridade prática com Node.js para esse tipo de aplicação e já possuo experiência considerável com Angular e Django.

Considero esse comportamento uma falha relevante porque a IA deveria primeiro coletar contexto suficiente antes de recomendar uma decisão arquitetural.

Em engenharia de software, uma tecnologia não deve ser escolhida apenas porque parece tecnicamente simples. Familiaridade da equipe, risco, tempo disponível e experiência prévia são fatores importantes.

A recomendação inicial da IA desconsiderou esse aspecto até que eu explicitamente informasse minha preferência.

Outro problema relevante foi a qualidade visual produzida inicialmente no frontend.

A primeira versão gerada pela IA estava funcional, mas possuía aparência muito próxima de HTML básico: pouca hierarquia visual, navegação simples, tabelas pouco trabalhadas, formulários sem acabamento e baixo uso de elementos visuais para comunicar severidade e status.

Esse resultado foi uma das principais insatisfações que tive com a IA durante o desafio.

Inicialmente, aceitei essa limitação porque funcionalidade tinha prioridade.

Depois que os principais requisitos estavam implementados e validados, decidi voltar ao frontend e corrigir essa deficiência visual.

Para isso, utilizei o Lovable como ferramenta de exploração e referência visual e, posteriormente, utilizei o Codex para reproduzir o redesign dentro da aplicação Angular existente, mantendo a lógica e os contratos já implementados.

---

## 6. Como você identificou esse erro?

Identifiquei o problema da escolha tecnológica imediatamente ao analisar a sugestão de Node.js.

Minha própria experiência permitiu perceber que seguir essa recomendação aumentaria o risco do projeto.

Eu teria que desenvolver utilizando uma tecnologia com a qual não estava confortável, mesmo possuindo uma stack que já conhecia e que atendia completamente aos requisitos.

Interrompi essa direção e informei à IA que preferia Angular + Django.

Após fornecer esse contexto, o planejamento foi refeito considerando minha experiência real.

No caso da interface visual, o problema foi identificado durante a execução do frontend no navegador.

A aplicação estava funcional, mas a apresentação visual estava abaixo do que eu consideraria uma interface bem acabada.

A comparação entre a aplicação funcional e uma proposta visual mais estruturada deixou evidente que o problema não era funcional, mas de apresentação, hierarquia e experiência de uso.

Essa análise motivou uma etapa posterior exclusivamente dedicada ao redesign.

---

## 7. Como você corrigiu e validou a correção?

Para a decisão da stack, a correção foi feita alterando o planejamento antes de iniciar a implementação principal.

Foi adotado:

- Angular;
- Django;
- Django REST Framework;
- SQLite.

A decisão foi validada ao longo do desafio pela velocidade com que consegui compreender, revisar e validar a estrutura produzida.

A aplicação foi concluída dentro da stack escolhida e os principais fluxos funcionaram corretamente.

Para o problema visual, a correção aconteceu em duas etapas.

Primeiro, utilizei o Lovable para produzir uma referência visual das quatro páginas existentes:

- Dashboard;
- Incidentes;
- Novo incidente;
- Detalhes do incidente.

A ferramenta foi orientada a preservar os mesmos fluxos e requisitos, trabalhando apenas em layout, hierarquia, cores, componentes e apresentação.

Depois, utilizei essa referência para fornecer ao Codex uma especificação visual detalhada, página por página.

O Codex foi instruído explicitamente a não alterar:

- backend;
- endpoints;
- contratos da API;
- services;
- models;
- rotas;
- regras de negócio;
- comportamento funcional.

As alterações ficaram concentradas principalmente em HTML e SCSS.

Para questões de implementação e validação, utilizei diferentes mecanismos:

- `python manage.py check`;
- testes automatizados do Django;
- `npm run build`;
- execução do backend;
- execução do frontend;
- validação manual dos fluxos no navegador.

Após o redesign, o frontend foi novamente compilado e os principais fluxos foram revisados para garantir que a melhoria visual não tivesse introduzido regressões.

A suíte final do backend permaneceu passando após as alterações.

---

## 8. Houve alguma regressão?

Não identifiquei uma regressão funcional persistente durante a validação final.

Uma preocupação adicional surgiu durante o redesign do frontend, porque uma alteração visual extensa poderia quebrar elementos que já estavam funcionando.

Por isso, o redesign foi explicitamente limitado à camada visual.

O Codex recebeu instruções para preservar:

- serviços;
- modelos;
- rotas;
- chamadas HTTP;
- contratos da API;
- regras de negócio.

Após as alterações visuais, o frontend foi compilado novamente e os principais fluxos foram revisados.

A estratégia foi preservar o comportamento funcional existente enquanto a camada visual era modificada.

Também foi adicionada cobertura para verificar a atualização do dashboard após alterações de status.

---

## 9. Em qual parte houve mais retrabalho?

O maior retrabalho ocorreu na interação com a IA, principalmente em dois aspectos.

### Formatação de código e texto

Em alguns momentos, a IA não seguiu completamente instruções específicas de formatação.

Isso ocorreu mesmo quando o formato esperado havia sido explicitamente informado.

Esse comportamento exigiu repetição de instruções e revisão adicional.

Minha expectativa é que, quando uma restrição de formatação é fornecida de forma clara, a IA a trate como requisito e não apenas como preferência.

### Frontend e apresentação visual

O frontend foi uma das áreas que exigiu uma segunda rodada significativa de trabalho.

A primeira versão produzida pela IA era funcional, porém visualmente pobre.

Os principais problemas percebidos foram:

- baixa hierarquia visual;
- navegação muito básica;
- excesso de aparência padrão de browser;
- pouco destaque para métricas;
- severidade e status apresentados apenas como texto;
- formulários pouco trabalhados;
- tela de detalhes pouco organizada.

Em vez de aceitar definitivamente essa limitação, decidi realizar uma segunda etapa dedicada à aparência.

Usei o Lovable para explorar uma direção visual mais adequada e depois utilizei o Codex para reproduzir essa direção na aplicação Angular já funcional.

Esse processo gerou retrabalho, mas considero que melhorou significativamente a percepção de qualidade da entrega.

---

## 10. Cite uma situação em que você rejeitou ou alterou uma abordagem sugerida pela IA.

A situação mais clara foi a escolha inicial da stack.

A IA inicialmente sugeriu uma abordagem utilizando Node.js.

Eu rejeitei essa sugestão porque:

- não tenho experiência suficiente com Node.js para esse contexto;
- já tenho familiaridade com Angular e Django;
- havia tempo limitado;
- adotar uma tecnologia menos conhecida aumentaria o risco;
- não existia requisito que justificasse a mudança.

Solicitei que o planejamento fosse refeito utilizando Angular + Django.

Essa decisão foi mantida até o final do projeto.

Esse episódio também reforçou uma limitação que percebi no uso de IA: ela pode propor uma decisão tecnicamente válida, mas inadequada ao contexto humano se não fizer perguntas antes de assumir preferências ou experiência.

Para mim, nesse tipo de decisão, a IA deveria perguntar antes de presumir.

Outra alteração importante de abordagem aconteceu no frontend.

Inicialmente, aceitei uma interface visual simples porque a prioridade era funcionalidade.

Depois que os requisitos funcionais estavam concluídos, decidi reabrir essa decisão e investir no redesign da aplicação, utilizando ferramentas de IA específicas para exploração visual e implementação.

---

## 11. Qual parte da aplicação você considera menos confiável?

A parte que considero menos confiável é a cobertura automatizada do frontend.

O backend possui uma suíte automatizada cobrindo as principais regras de negócio, API, filtros, dashboard, histórico e dados iniciais.

No frontend, a validação foi baseada principalmente em:

- `npm run build`;
- execução integrada com o backend;
- testes manuais dos principais fluxos pelo navegador.

O frontend passou por uma etapa posterior de redesign, e apesar de os fluxos terem sido preservados e novamente validados, ainda considero que testes automatizados dos componentes e fluxos Angular aumentariam significativamente a confiança na solução.

Portanto, minha principal preocupação não é mais a qualidade visual, mas a diferença entre o nível de cobertura automatizada do backend e do frontend.

---

## 12. Se tivesse mais duas horas, quais seriam suas três prioridades?

### 1. Aumentar os testes automatizados do frontend

Criaria testes para:

- filtros;
- formulário de criação;
- tratamento de erros;
- alteração de status;
- histórico;
- dashboard;
- navegação.

### 2. Refinar e validar o redesign em diferentes tamanhos de tela

O redesign visual já foi realizado, mas eu utilizaria tempo adicional para:

- validar mais resoluções;
- revisar comportamento mobile;
- ajustar detalhes de espaçamento;
- revisar estados de erro;
- revisar estados vazios;
- melhorar acessibilidade;
- verificar consistência visual entre todos os componentes.

### 3. Testar a reprodução em um ambiente completamente limpo

Faria um clone novo do repositório e executaria todo o processo descrito no README:

- criação do ambiente virtual;
- instalação de dependências;
- migrations;
- seed;
- backend;
- npm install;
- frontend;
- testes;
- build.

---

## 13. Como você avalia sua estratégia inicial?

A estratégia inicial, após a correção da escolha da stack, funcionou bem.

Manteria:

- Angular + Django;
- SQLite;
- separação entre frontend e backend;
- desenvolvimento incremental;
- regra de negócio centralizada;
- testes frequentes;
- validação antes de avançar;
- escopo limitado aos requisitos obrigatórios.

Mudaria principalmente a forma de interação com IA.

Eu forneceria ainda mais cedo instruções explícitas como:

- não escolher framework sem perguntar;
- não assumir preferências tecnológicas;
- respeitar estritamente formatação solicitada;
- não criar abstrações ou funcionalidades não pedidas;
- apresentar alternativas antes de tomar decisões arquiteturais.

Uma mudança importante durante o desafio foi justamente reservar uma etapa de acabamento visual depois que os requisitos obrigatórios estavam estáveis.

Essa decisão funcionou bem.

Eu manteria essa estratégia: primeiro garantir comportamento correto e confiável; depois, se houver tempo disponível, melhorar a apresentação sem modificar a base funcional já validada.

---

## 14. Aproximadamente quantas interações relevantes com IA foram necessárias?

Foram necessárias aproximadamente entre 20 e 30 interações relevantes com IA ao longo do desenvolvimento.


Nem todas as mensagens ou pequenas correções foram consideradas interações relevantes para este relatório.

As principais interações envolveram:

- planejamento;
- escolha da stack;
- configuração do ambiente;
- configuração Django;
- modelagem;
- regra de negócio;
- API;
- seed;
- testes;
- estrutura Angular;
- integração HTTP;
- dashboard;
- telas restantes;
- investigação de problemas;
- documentação;
- revisão;
- avaliação crítica da primeira interface;
- criação de referência visual com Lovable;
- especificação detalhada do redesign;
- aplicação do redesign pelo Codex;
- validação pós-redesign.

O número de interações também foi influenciado pelos limites disponíveis nas modalidades gratuitas das ferramentas.

Em determinado momento, para economizar utilização do Codex gratuito, optei por agrupar três funcionalidades relacionadas do frontend em uma única solicitação bem delimitada.

---

## 15. Quais ferramentas de IA foram utilizadas?

Foram utilizadas exclusivamente ferramentas em modalidades gratuitas disponíveis ao público.

### ChatGPT Free

Utilizado principalmente para:

- compreender os requisitos;
- planejamento;
- decomposição das tarefas;
- revisão de decisões;
- investigação de erros;
- orientação da estratégia;
- documentação;
- acompanhamento do progresso;
- preparação de prompts;
- avaliação crítica do resultado visual.

### Codex — acesso gratuito

Utilizado principalmente para:

- criação e alteração de arquivos;
- configuração técnica;
- implementação do backend;
- implementação dos testes;
- implementação do frontend;
- execução de verificações e builds;
- aplicação do redesign visual no Angular existente.

O uso do Codex foi realizado exclusivamente com acesso gratuito.

### Lovable — acesso gratuito

Utilizado em uma etapa posterior do desenvolvimento como ferramenta de exploração e referência visual.

A aplicação já estava funcional nesse momento.

O Lovable foi utilizado para produzir uma proposta visual para as quatro páginas existentes:

- Dashboard;
- Incidentes;
- Novo incidente;
- Detalhes do incidente.

A proposta foi utilizada como referência de:

- layout;
- hierarquia;
- sidebar;
- header;
- cards;
- badges;
- formulários;
- tabelas;
- apresentação do histórico.

O código produzido pelo Lovable não substituiu a aplicação Angular existente.

O resultado foi utilizado como referência visual para orientar posteriormente o Codex na alteração do frontend já implementado.

Nenhum plano pago ou crédito adicional foi utilizado para aumentar a capacidade disponível durante o desafio.

Não utilizei:

- ChatGPT Plus durante o desafio;
- créditos pagos de API;
- Codex com capacidade proveniente de assinatura paga;
- contas corporativas com limites superiores aos gratuitos;
- outras modalidades premium de IA.

Não foi necessário trocar definitivamente de ferramenta, mas os limites das modalidades gratuitas influenciaram a estratégia de uso.

---

# Retrospectiva sobre o uso de IA

A IA foi extremamente útil para acelerar a implementação, especialmente em tarefas mecânicas de código, criação de testes, configuração e ajustes visuais.

Ao mesmo tempo, o desafio deixou claras algumas limitações importantes.

## 1. A IA não deve presumir decisões de arquitetura sem contexto

A sugestão inicial de Node.js foi tecnicamente válida, mas inadequada para mim.

Minha expectativa é que uma IA utilizada como ferramenta de engenharia pergunte primeiro:

- qual stack o desenvolvedor domina;
- quais restrições existem;
- qual experiência a equipe possui;
- quais tecnologias já estão disponíveis.

Somente depois deveria propor uma decisão.

## 2. Instruções explícitas nem sempre são obedecidas perfeitamente

Em alguns momentos houve desobediência a instruções de formatação de código ou texto.

Isso aumenta retrabalho e exige supervisão constante.

Uma das principais conclusões do desafio foi que instruções claras ajudam bastante, mas não eliminam a necessidade de revisão humana.

## 3. Qualidade funcional e qualidade visual não evoluem necessariamente juntas

A IA conseguiu produzir rapidamente uma interface funcional, mas a primeira versão visual ficou muito abaixo do resultado funcional.

O design inicial foi uma das minhas principais insatisfações.

A primeira reação foi não priorizar essa questão, pois ainda existiam requisitos funcionais mais importantes.

Depois que a aplicação estava funcionando, integrada e testada, decidi mudar essa estratégia.

Usei uma ferramenta de IA voltada à exploração visual para criar uma referência de interface mais madura e depois utilizei outra IA para transportar essa direção visual para o Angular existente.

Essa etapa foi interessante porque separou dois tipos de trabalho:

1. exploração visual;
2. implementação visual dentro de uma codebase existente.

O resultado reforçou que uma IA que funciona bem para implementação não necessariamente produz automaticamente um bom design.

Também mostrou que resultados melhores podem surgir quando ferramentas diferentes são usadas para funções específicas, mantendo o desenvolvedor responsável por coordenar e validar o processo.

## 4. O desenvolvedor precisa saber quando reabrir uma decisão

Inicialmente, considerei suficiente entregar uma interface simples porque aparência tinha prioridade menor.

Depois de concluir os requisitos obrigatórios, percebi que ainda havia espaço para melhorar a qualidade da entrega sem comprometer funcionalidade ou prazo.

Decidi então reabrir a questão visual.

Essa mudança não aconteceu porque a IA sugeriu espontaneamente, mas porque eu avaliei criticamente o resultado e decidi que ele ainda poderia melhorar.

Considero isso uma parte importante do processo: uma decisão tomada corretamente em um momento pode precisar ser revista quando o contexto muda.

## Conclusão

A experiência confirmou que IA é muito eficiente como ferramenta de implementação, mas não elimina a necessidade de decisões humanas.

Durante o projeto, meu papel foi principalmente:

- entender;
- questionar;
- restringir;
- revisar;
- testar;
- rejeitar abordagens inadequadas;
- corrigir direção;
- reavaliar decisões;
- coordenar ferramentas diferentes;
- validar o resultado.

A IA acelerou a produção do software, mas a responsabilidade pelas decisões e pelo resultado permaneceu comigo.