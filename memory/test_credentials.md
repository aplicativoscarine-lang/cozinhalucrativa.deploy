# Test Credentials — Cozinha Lucrativa

## Admin / Professora (painel de afiliados, plantão, códigos VIP)
- O acesso admin é liberado por e-mail (login via Google OAuth gerenciado pela Emergent).
- Configurado em `ADMIN_EMAILS` / `TEACHER_EMAIL` (backend/.env e frontend/.env).
- **Valor atual (placeholder):** `admin@cozinhalucrativa.com`
- ⚠️ AÇÃO NECESSÁRIA: troque para o e-mail REAL do Google da professora nos dois `.env`
  e reinicie o backend, senão ninguém consegue acessar `/admin/afiliados`.

## Testing note (backend-only, sem OAuth)
Para testar rotas admin via API sem Google, seedar sessão no Mongo:
- users: { user_id: "admin-uid", email: "admin@cozinhalucrativa.com" }
- user_sessions: { session_token: "<token>", user_id: "admin-uid", expires_at: ISO+7d }
- Chamar com header `Authorization: Bearer <token>`.

## Acesso aos cursos
- `BETA_MODE=true` → todos os cursos liberados sem pagamento (modo demo/lançamento).
- Para exigir pagamento real, definir `BETA_MODE=false` e configurar credenciais de pagamento.

## Pagamentos (não configurados — precisam de credenciais reais)
- Mercado Pago (gateway principal): falta `MP_ACCESS_TOKEN` no backend/.env.
- Stripe: usa `STRIPE_SECRET_KEY` (atual: sk_test_emergent — placeholder inválido).
