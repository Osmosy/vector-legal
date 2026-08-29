---
name: matter-workspace
description: >
  Управление рабочими пространствами дел IP — создать, список,
  переключить, закрыть, отключиться (practice-level). Для
  мультиклиентских практик. Используй при создании дела, переключении,
  списках, архивации или когда навык должен знать, в каком деле работает.
argument-hint: '<new | list | switch | close | none> [slug]'
---

# /matter-workspace — рабочие пространства дел (IP)

Пространство дела держит контекст одного клиента/проекта отдельно.
Команда управляет пространствами.

## Подкоманды

- `new <slug>` — intake (клиент, тип: clearance / спор / вендор /
  OSS-аудит / заявка) → `matters/<slug>/matter.md`, seed history/notes
- `list` — таблица дел с active-флагом
- `switch <slug>` — обновить `Active matter:` в practice-CLAUDE.md
- `close <slug>` — архив в `matters/_archived/` (не удалять), лог даты
- `none` — practice-level

## Инструкции

1. Прочитать `~/.hermes/legal/ip-legal/CLAUDE.md` — `## Matter workspaces`.
   `Enabled: ✗` → «Выключено — in-house режим; для частной практики
   перезапусти `cold-start-interview --redo`». Не ошибка.
2. Диспетчить подкоманду.
3. Показать изменения, подтвердить до записи.

## Notes

- Чужие дела без `Cross-matter context: on` не читать.
- Общие настройки (постур, OSS-политика) — practice-level; оверрайды —
  в `## Matter-specific overrides` matter.md.
- Портфель общий для practice-level; per-client портфели — если firm
  и ведём реестры клиентов (отдельно от practice-портфеля).
- Конфликт интересов: новое дело по бренду, смежному с действующим
  клиентом — surfacing конфликта при `new` (перекрёстная проверка
  сторон по matter.md закрытых дел — только при Cross-matter: on).
- Архивирование — не удаление; сроки хранения — регламент организации
  (для адвокатов — ст. 29 ФЗ-63).

## matter.md шаблон (кратко)

```markdown
# Matter: [Клиент] — [кратко]
## Parties
## Matter type  (clearance / спор / вендор / OSS / заявка)
## Key facts
## Matter-specific overrides
## Notes on confidentiality
```

---

**Дефолт — выключено.** In-house не видит; включается на cold-start
для частной практики.