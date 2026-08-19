# Cozinha Lucrativa — App de Cursos (Renda Extra)

## Problem statement (sessão atual — 2026-08-19)
Trazer o app do GitHub (`aplicativoscarine-lang/cozinhadeploy`) para o ambiente Emergent,
subir/rodar (deploy no preview) e **finalizar de onde o outro agente parou**: a conversão
do sistema de afiliados para o modelo de **2 gerações (A/B)** com indicador (parent).

## Arquitetura
- **Frontend**: Next.js 15 (porta 3000, dir `/app/frontend`) — SPA React Router em `src/`
  + API interna em `app/api/[[...path]]/route.js` (conecta ao Mongo).
- **Backend**: FastAPI (porta 8001, dir `/app/backend`) — proxy de `/api/*` para o Next.js
  + rotas Python (IA, plantão, afiliados, pagamentos Stripe/MercadoPago, códigos de acesso).
- **DB**: MongoDB (`cozinha_lucrativa`). Cursos seedados de `lib/courses-seed.js`.
- **Auth**: Emergent-managed Google Auth (cookie `session_token` → user_sessions → users).
- Admin liberado por `ADMIN_EMAILS`/`TEACHER_EMAIL`.

## Feito nesta sessão (2026-08-19)
- **Deploy no ambiente**: zip do repo extraído para `/app/frontend` (Next.js) e `/app/backend` (FastAPI).
  - `.env` criados (MONGO_URL, DB_NAME=cozinha_lucrativa, REACT_APP_BACKEND_URL, EMERGENT_LLM_KEY,
    STRIPE_SECRET_KEY, APP_URL, CORS_ORIGINS, BETA_MODE=true).
  - Deps instaladas (yarn + pip); serviços rodando no supervisor.
  - **Fix crítico**: `allowedDevOrigins` em `next.config.js` não cobria o host atual do preview
    (`*.cluster-12.preview.emergentcf.cloud`), o que bloqueava os chunks `/_next/*` e deixava a
    página em branco. Adicionados os hosts explícitos + wildcards. App renderiza (home, /planos,
    /curso/:slug, admin) OK.
- **Afiliados 2 gerações (A/B) — concluído** (`backend/affiliate_routes.py` + `src/screens/AffiliatesAdmin.jsx`):
  - Modelos `AffiliateCreate`/`AffiliateUpdate`: campos `generation` (A/B), `parent_code`, `commission_rate` (alias de `commission_pct`).
  - `create_affiliate`: valida geração; B exige indicador A existente (não pode ser ele mesmo; indicador tem que ser geração A).
  - `update_affiliate`: patch do outro agente aplicado (troca de geração limpa/define `parent_affiliate_id`).
  - `list_affiliates`: retorna `generation`, `parent_affiliate_id`, `commission_rate`.
  - UI admin: seletor de Geração (A/B) + seletor de Indicador (afiliados A), coluna "Geração" com badges e hierarquia "↳ por CÓDIGO".
  - Verificado via API (create A, create B, validações 400, patch de comissão/geração) e visualmente no `/admin/afiliados`.

## Modelo de comissão A/B
- Cada afiliado tem seu próprio `commission_pct`. Geração A = indicador direto; B = indicado por um A.
- A/B é **organizacional/hierárquico** (quem indicou quem). Pagamento é manual pela professora.
- (Em aberto) Override automático: A ganhar % sobre vendas dos seus B — NÃO implementado (aguarda decisão).

## Não verificado / barreira técnica
- Login Google real (OAuth) e reprodução de vídeo no player não automatizáveis.

## Backlog / próximos
- Definir o e-mail admin REAL da professora em `ADMIN_EMAILS`/`TEACHER_EMAIL` (hoje placeholder).
- Configurar credenciais reais de pagamento: `MP_ACCESS_TOKEN` (Mercado Pago) e/ou Stripe real.
- (Opcional) Override de comissão de geração A sobre vendas dos B.
- Publicar em produção pelo botão Deploy.

## Sessão 2026-08-19 (parte 2) — Regras A/B definitivas + padronização Marmitas
### Comissões A/B (fixas v1) — `backend/commissions.py`
- Venda direta A → A 50% · plataforma 50%. Venda B → B 30% · A indicador 30% · plataforma 40%.
- Override do A é automático (independe de o A vender), via `parent_affiliate_id`.
- Comissão só definitiva com pagamento aprovado (MP "approved" / Stripe "paid"); pendente/recusado/estornado = void (excluído da agregação).
- Registro de venda gravado no pedido (mp_orders/payment_transactions): gross/net, seller/indicador code+geração, comissões, plataforma, commission_status.
- Painel admin: colunas Afiliado | Código | Geração | Indicador | Cliques | Vendas | Receita | Comissão (removido o % editável; regra é fixa). "Indicado por A01" para B.
- Verificado por testing_agent: 12/12 backend (cenários 1-4 + validações). ADMIN_EMAILS = aplicativos.carine@gmail.com, casadalize2026@gmail.com; TEACHER_EMAIL = casadalize2026@gmail.com.

### Padronização Marmitas Fitness
- Adicionado ao catálogo da landing (`src/screens/Landing.jsx` array COURSES) logo após "Lanches Kids", mesmo componente OpportunityCard. price="≈ R$ 25 / unidade", volume="50 marmitas por semana", investment="R$ 150–400". Contadores 10→11 (landing + /planos).
- Página interna `/curso/marmita-fitness` já usa o padrão dos demais (CourseDetail renderiza modules/lessons). Removido "6 módulos e 28 aulas" da descrição (contradizia o meta "7 módulos" = 6 + Apostila Oficial, padrão de todos os cursos).
- Lint + build OK. next dev restaurado (rm -rf .next após build).

### Pagamento real (preparado, NÃO ativar automaticamente)
- MP_ACCESS_TOKEN / MP_WEBHOOK_SECRET permanecem vazios (credenciais reais só via Deploy pelo usuário). Não usar chaves de teste em produção. BETA_MODE=true mantido para testes; não mudar para false automaticamente.
- APP_URL/REACT_APP_BACKEND_URL sincronizados com o preview atual (resume-deploy-8).

### Backlog (follow-ups do review)
- DELETE de afiliado A com filhos B: adicionar guarda (409) ou reparent para não perder o override.
- Campos legados commission_rate/commission_pct ainda graváveis (ignorados no cálculo) — remover/marcar read-only.
- Confirmar se Marmitas precisa de módulo "Página de Vendas" como outros cursos.
