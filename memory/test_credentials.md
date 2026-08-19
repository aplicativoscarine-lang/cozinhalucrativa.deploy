# Test Credentials — Cozinha Lucrativa

## Admin / Professora (painel de afiliados, plantão, códigos VIP)
- Acesso admin liberado por e-mail (login via Google OAuth gerenciado pela Emergent).
- Configurado em `ADMIN_EMAILS` / `TEACHER_EMAIL` (backend/.env e frontend/.env).
- **ADMIN_EMAILS:** `aplicativos.carine@gmail.com,casadalize2026@gmail.com`
- **TEACHER_EMAIL:** `casadalize2026@gmail.com`

## Testing note (backend admin sem OAuth)
Para testar rotas admin via API sem Google, seedar sessão no Mongo (db `cozinha_lucrativa`):
- users: { user_id: "admin-uid", email: "aplicativos.carine@gmail.com", name: "Admin" }
- user_sessions: { session_token: "<token>", user_id: "admin-uid", expires_at: ISO+7d }
- Chamar endpoints com header `Authorization: Bearer <token>`.

## Acesso aos cursos
- `BETA_MODE=true` → todos os cursos liberados sem pagamento (modo demo/lançamento).
- Só pagamento aprovado deve liberar 12 meses quando BETA_MODE=false.

## Regras de comissão de afiliados (A/B) — v1 fixas
- Venda direta A → A 50% · plataforma 50%.
- Venda B → B 30% · A indicador (parent) 30% · plataforma 40%.
- Comissão só é definitiva com pagamento aprovado (MP "approved" / Stripe "paid").

## Pagamentos (não configurados — credenciais reais só no Deploy)
- Mercado Pago (gateway principal): `MP_ACCESS_TOKEN`, `MP_WEBHOOK_SECRET` (vazios agora).
- Stripe: `STRIPE_SECRET_KEY` (placeholder sk_test_emergent).
