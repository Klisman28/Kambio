---
description: Inicia la Fase 0 del proyecto Finances
---

Cuando el usuario escriba `/start-finances`, sigue este flujo:

1. Lee:
   - `.agents/agents.md`
   - `AGENTS.md`
   - `CLAUDE.md`
   - `docs/PRD.md`
   - `docs/ARCHITECTURE.md`
   - `docs/TASKS.md`

2. Usa `@pm` para:
   - refinar el alcance
   - definir Fase 0
   - actualizar `docs/PRD.md`, `docs/ARCHITECTURE.md` y `docs/TASKS.md`

3. Pausa y pide aprobación humana.

4. Tras aprobación:
   - usa `@backend` para crear scaffold FastAPI base
   - usa `@frontend` para integrar el tema comprado dentro de `frontend/`
   - usa `@qa` para revisar estructura, contratos y riesgos

5. Entrega siempre:
   - resumen
   - archivos creados/cambiados
   - riesgos
   - siguiente paso
