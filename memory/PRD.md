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
