---
name: matter-workspace
description: >
  Управление рабочими пространствами дел для мультиклиентских практик:
  создать, перечислить, переключить, закрыть или отвязать активное дело.
  Для firm/мультиклиент; in-house по дефолту выключено. Используй при
  «заведи рабочее пространство», «смени активное дело», «список дел»,
  «архивируй дело».
argument-hint: '<new | list | switch | close | none> [slug]'
---

# /matter-workspace

Практики работают по нескольким клиентам и делам. Рабочее пространство
дела держит контекст одного клиента/дела отдельно от других. Это команда
управления пространствами.

## Subcommands

- `new <slug>` — создать пространство, короткое mini-intake, записать
  `matter.md`
- `list` — список дел со статусом и флагом активного
- `switch <slug>` — назначить активное дело
- `close <slug>` — архивировать (в `~/.hermes/legal/litigation-legal/matters/_archived/`,
  никогда не удалять); полный close с исходом — через `matter-close`
- `none` — отвязаться от активного дела, work на practice-level

Note: `/matter-briefing [slug]` — отдельная команда-брифинг по конкретному
делу. Управление пространствами — здесь.

## Instructions

1. Прочитать `~/.hermes/legal/litigation-legal/CLAUDE.md` — секция
   `## Matter workspaces`. Если `Enabled: ✗` → сообщить: «Пространства
   выключены — вы настроены как инхаус-практика с одним клиентом, плагин
   работает с practice-level контекстом. Если работаете по нескольким
   клиентам — перезапустите `cold-start-interview --redo` и выберите
   частную практику.» Не ошибка — ожидаемое состояние для инхауса.
2. Dispatch по первому токену аргументов:
   - `new` → mini-intake (клиент, дело, подведомственность, сторона,
     конфликт-чек!) → записать `matters/<slug>/matter.md`, seed `history.md`
     и `notes.md`
   - `list` → перечислить `matters/*/matter.md`, таблица, флаг активного
   - `switch` → обновить `Active matter:` в practice-level CLAUDE.md
   - `close` → переместить в `matters/_archived/<slug>/`, дата закрытия
     в history.md
   - `none` → `Active matter: none — practice-level context only`
3. Показать пользователю, что меняется, и подтвердить перед записью.

## Заметки

- Скилл никогда не читает между делами, пока `Cross-matter context: on`
  в practice-level CLAUDE.md
- Архивирование ≠ удаление — закрытые дела остаются читаемыми для
  retention/конфликтов
- Slug — lowercase с дефисами; повтор между архивом и активными — архивный
  сохраняется как `_archived/<slug>/`
- **Клиентская изоляция абсолютна** — для мультиклиентской практики:
  конфликт-чек перед `new`, cross-matter read — только осознанно
  через `Cross-matter context: on`
- Путь по канону CFL: `~/.hermes/legal/litigation-legal/matters/<slug>/`

## Что дальше?

После создания пространства — предложить `/matter-intake` для полного
intake (риск-триаж, материальность, _log.yaml-строка).
