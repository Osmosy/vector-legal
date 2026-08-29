---
name: matter-workspace
description: >
  Управление рабочими пространствами дел AI Governance — создать, список,
  переключить, закрыть, отключиться (practice-level). Для мультиклиентских
  практик. Используй при создании дела, переключении активного, списке
  дел, архивации, или когда навык должен знать, в каком деле работает.
argument-hint: '<new | list | switch | close | none> [slug]'
---

# /matter-workspace — рабочие пространства дел (AI Governance)

Практики работают по нескольким клиентам и делам. Пространство дела держит
контекст одного клиента/проекта отдельно от остальных. Команда управляет
пространствами.

## Подкоманды

- `matter-workspace new <slug>` — создать, короткий intake, записать `matter.md`
- `matter-workspace list` — список дел со статусом и active-флагом
- `matter-workspace switch <slug>` — установить активное дело
- `matter-workspace close <slug>` — архивировать (в
  `~/.hermes/legal/ai-governance-legal/matters/_archived/`, не удалять)
- `matter-workspace none` — отвязаться, работать practice-level

## Инструкции

1. Прочитать `~/.hermes/legal/ai-governance-legal/CLAUDE.md` — проверить
   `## Matter workspaces`. Если `Enabled: ✗` — сказать: «Пространства дел
   выключены — ты in-house, плагин работает от practice-level контекста.
   Если работаешь по нескольким клиентам — перезапусти
   `cold-start-interview --redo` и выбери частную практику.» Не ошибка —
   ожидаемое состояние.
2. Диспетчить первый токен:
   - `new` — intake: клиент, тип (импact assessment / расследование /
     политика), ключевые факты, конфиденциальность → `matters/<slug>/matter.md`,
     seed `history.md` и `notes.md`
   - `list` — таблица `matters/*/matter.md`, отметить active
   - `switch` — обновить `Active matter:` в practice-CLAUDE.md
   - `close` — в `_archived/<slug>/`, залогировать дату в `history.md`
   - `none` — `Active matter: none — только practice-level`
3. Показать, что изменится, подтвердить до записи.

## Notes

- Навык никогда не читает чужие дела без `Cross-matter context: on`.
- Заучивания, которые переносятся между делами, — в practice-level
  CLAUDE.md, не в папку дела.
- Архивирование — не удаление. Сроки хранения — по регламенту организации
  (для адвокатских образований — ст. 29 ФЗ-63).
- Slugs — lowercase с дефисами; реюз slug между archived и active —
  archived остаётся в `_archived/<slug>/`.

## matter.md шаблон (кратко)

```markdown
# Matter: [Клиент] — [кратко]
## Parties
## Matter type  (AIA / расследование / политика / вендор-ревью)
## Key facts
## Matter-specific overrides  (отклонения от practice profile — только здесь)
## Notes on confidentiality
```

---

**Дефолт — выключено.** In-house пользователи никогда не видят это;
пространства включаются на cold-start для частной практики.