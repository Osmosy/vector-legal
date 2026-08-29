---
name: matter-workspace
description: >
  Управление рабочими пространствами дел Regulatory — создать, список,
  переключить, закрыть, отключиться (practice-level). Для мультиклиентских
  практик. Используй при создании дела, переключении, списках, архивации,
  или когда навык должен знать, в каком деле работает.
argument-hint: '<new | list | switch | close | none> [slug]'
---

# /matter-workspace — рабочие пространства дел (Regulatory)

Пространство дела держит контекст одного клиента/проекта отдельно от
остальных. Команда управляет пространствами.

## Подкоманды

- `new <slug>` — short intake (клиент, тип: мониторинг/diff/сертификация),
  записать `matters/<slug>/matter.md`, seed `history.md`, `notes.md`
- `list` — таблица дел со статусом и active-флагом
- `switch <slug>` — обновить `Active matter:` в practice-CLAUDE.md
- `close <slug>` — архивировать в `matters/_archived/`, залогировать дату
- `none` — practice-level

## Инструкции

1. Прочитать `~/.hermes/legal/regulatory-legal/CLAUDE.md` — секцию
   `## Matter workspaces`. `Enabled: ✗` → «Пространства выключены —
   in-house режим; для частной практики перезапусти
   `cold-start-interview --redo`». Не ошибка.
2. Диспетчить подкоманду (intake/list/switch/close/none).
3. Показать, что изменится, подтвердить до записи.

## Notes

- Чужие дела не читать без `Cross-matter context: on`.
- Общие для всех дел настройки (watchlist, materiality) живут в
  practice-level профиле, не в matter-папках. matter-специфика —
  только оверрайды: `## Matter-specific overrides` в matter.md (напр.,
  у клиента свои пороги материальности).
- Трекеры: gap-tracker.yaml и comment-tracker.yaml при включённых
  workspaces живут в `matters/<slug>/`; при выключенных — practice-level.
- Архивирование — не удаление; сроки хранения по регламенту организации
  (для адвокатов — ст. 29 ФЗ-63).

## matter.md шаблон (кратко)

```markdown
# Matter: [Клиент] — [кратко]
## Parties
## Matter type  (мониторинг / policy-diff / gap-трекинг / комментарий)
## Key facts
## Matter-specific overrides
## Notes on confidentiality
```

---

**Дефолт — выключено.** In-house не видит это; включается на cold-start
для частной практики.