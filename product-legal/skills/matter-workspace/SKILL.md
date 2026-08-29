---
name: matter-workspace
description: >
  Управление matter workspaces — new, list, switch, close, none (detach).
  Используй при работе по нескольким клиентам или делам в частной практике,
  когда нужно создать/переключить/закрыть активное дело, чтобы контекст
  одного клиента не утёк в другой.
argument-hint: '<new | list | switch | close | none> [slug]'
---

# /matter-workspace

Практики работают по нескольким клиентам и делам. Matter workspace держит
контекст одного клиента или дела отдельно от всех остальных. Навык управляет
этими пространствами.

## Subcommands

- `matter-workspace new <slug>` — создать workspace дела, короткий intake,
  записать `matter.md`
- `matter-workspace list` — перечислить дела со статусом и активным флагом
- `matter-workspace switch <slug>` — назначить активное дело
- `matter-workspace close <slug>` — архивировать дело (перенести в
  `~/.hermes/legal/product-legal/matters/_archived/`, никогда не удалять)
- `matter-workspace none` — отвязаться от активного дела, работать на
  practice-level

## Инструкции

1. Прочитать `~/.hermes/legal/product-legal/CLAUDE.md` — убедиться, что
   секция `## Matter workspaces` заполнена. Если `Enabled: ✗`, сказать:
   «Matter workspaces выключены — вы настроены как in-house с одним клиентом,
   плагин работает на practice-level автоматически. Если вы всё же работаете
   по нескольким клиентам — перезапусти `cold-start-interview --redo` и выбери
   настройку частной практики. Иначе `/matter-workspace` не нужен.» Не
   ошибка: выключенное состояние — ожидаемое для in-house.
2. Применить структуру хранения и логику subcommands ниже.
3. Диспатч по первому токену `$ARGUMENTS`:
   - `new` → intake-интервью, записать
     `~/.hermes/legal/product-legal/matters/<slug>/matter.md`, засидить
     `history.md` и `notes.md`.
   - `list` → перечислить
     `~/.hermes/legal/product-legal/matters/*/matter.md`, вывести таблицу,
     отметить активное дело.
   - `switch` → обновить строку `Active matter:` в practice profile.
   - `close` → mv каталога в `_archived/`, сбросить `Active matter:` в `none`.
   - `none` → сбросить `Active matter:` в `none`.

## Структура хранения

```
~/.hermes/legal/product-legal/matters/
├── <slug>/
│   ├── matter.md       # intake: клиент, продукт, режим, контакты, особые условия
│   ├── history.md      # append-only лог сессий
│   └── notes.md        # рабочие заметки
└── _archived/
```

## Intake (subcommand new)

Коротко, 5–7 вопросов:

1. Клиент (название) и контакт юриста
2. Тип продукта/услуги (товар/сервис/телематики/фин)
3. Рынки: РФ / экспорт — какие юрисдикции
4. Регуляторы, с которыми уже работали
5. Существующие документы: оферта, политика ПДн, история launch review
6. Активные споры/предписания, затрагивающие продукт
7. Специфическая чувствительность (КТ-режим, дети как аудитория, мед-данные)

## Правила изоляции

- Каждый скилл проверяет `## Matter workspaces` до входа.
- **Чужие файлы не читать без `Cross-matter context: on`** — ни для «быстрой
  справки», ни для «по-моему, там было похоже». Пересечения дел — только через
  явное включение флага.
- Выходы направляются в `matters/<slug>/`, если активное дело выбрано; иначе
  на practice-level — и помечаются, что не привязаны к делу.
- При `close` — всё переносится в `_archived/` целиком. Архивированные дела
  не удаляются: история калибровки и прецедентов — raw-материал для будущих
  ревизий.

## Когда matter-workspaces не нужны

In-house с одним клиентом: `Enabled: ✗`, practice-level автоматом. Не
создавать пустые каталоги, не спрашивать о matter'ах на каждом шаге — если
настройка выключена, это ожидаемо. При in-house запускать `/matter-workspace`
нет причины; это не ошибка, а нормальная жизнь плагина.