# Cozinha Lucrativa — App de Cursos (Renda Extra)

## Problem statement
Adicionar um novo curso de **Marmitas Fitness** ao app existente (enviado por zip `rendaextracoz1708-main`), seguindo o **exato padrão dos demais cursos**, **sem alterar** os cursos/arquivos existentes. Conteúdo (vídeos) vindo de 6 pastas públicas do Google Drive + apostila em PDF.

## Arquitetura
- **Frontend**: Next.js (porta 3000) — SPA React Router em `src/` + API interna em `app/api/[[...path]]/route.js` (conecta ao Mongo).
- **Backend**: FastAPI (porta 8001) — proxy de `/api/*` para o Next.js + rotas Python (IA, plantão, pagamentos Stripe/MercadoPago).
- **DB**: MongoDB (`cozinha_lucrativa`). Cursos são "seedados" de `frontend/lib/courses-seed.js` via `ensureSeeded()`.
- **Auth**: Emergent-managed Google Auth (login gera sessão; acesso ao player exige login/enrollment).
- Vídeos das aulas: Google Drive via `drivePreview(lesson.id)` → `drive.google.com/file/d/{id}/preview`.

## Feito nesta sessão (2026-08-17)
- Implantado o app correto (`rendaextracoz1708-main`) em `/app`, deps instaladas, serviços no supervisor.
- **NOVO curso `marmita-fitness`** adicionado em `courses-seed.js` (aditivo, nenhum curso existente alterado):
  - 6 módulos, 28 aulas em vídeo (IDs reais do Drive, todos retornam HTTP 200 = reproduzíveis):
    1. Boas-Vindas e Preparação (3) · 2. Bases e Preparações (6) · 3. Marmitas de Frango (8) · 4. Marmitas de Carne (7) · 5. Marmitas de Peixe (3) · 6. Sanduíche Natural (1)
  - Apostila PDF oficial: `frontend/public/apostilas/marmita-fitness-apostila.pdf` (campo `apostilas`).
  - Capa gerada: `frontend/public/images/cat-marmita.jpg`.
  - Metadados no mesmo padrão dos irmãos: preço R$27, categoria `start`, tags, investimento, potencial, etc.
- Verificado: `/api/courses` retorna o curso; página `/curso/marmita-fitness` renderiza (capa, preço, currículo, apostila); PDF servido (200).

## Modelo de preço (corrigido 2026-08-17)
- **Pagamento único R$57 = acesso a TODOS os cursos** (página `/planos`, MercadoPago/Stripe, PRICE=57).
- Removido o preço individual de R$27 das telas: `CourseDetail.jsx` (card "Acesso Completo R$57 → Liberar acesso completo") e `CourseCard.jsx` (badge "Incluído" no lugar do preço).

## Não verificado (barreira técnica)
- Reprodução do vídeo dentro do player e Dashboard logado dependem de login Google (OAuth), não automatizável. IDs de vídeo validados fora do player (todos 200).

## Backlog / próximos
- Configurar credenciais reais de pagamento (Stripe/MercadoPago) para cobrar de verdade.
- Configurar credenciais reais de pagamento (Stripe/MercadoPago) se for cobrar de verdade.
