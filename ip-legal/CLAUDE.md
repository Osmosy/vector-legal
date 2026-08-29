# IP Practice Profile (шаблон)
# Заполняется cold-start interview. До заполнения навыки работают в
# provisional mode и помечают выходы [PROVISIONAL].
# Путь конфигурации: ~/.hermes/legal/ip-legal/CLAUDE.md
# (этот файл в репо — шаблон CLAUDE.md; пользовательские данные
#  cold-start пишет в ~/.hermes/legal/, не сюда)

**Название компании:** [PLACEHOLDER]
**The thing that hurts:** [PLACEHOLDER — что по ИС болит: конкуренты копируют? вендоры сдают знаки? OSS-аудит?]
**Practice setting:** [PLACEHOLDER — In-house | Firm | Гос | Клиника]

---

## Who's using this

**Role:** [PLACEHOLDER — Юрист | Не-юрист с доступом к юристу | Не-юрист без доступа]
**Контакт юриста:** [PLACEHOLDER]
**Патентный поверенный:** [PLACEHOLDER — ФИО/фирма, договор ⚪/✓; для заявок и споров — обязательно]

---

## Доступные интеграции

| Интеграция | Статус | Фоллбэк |
|---|---|---|
| ФИПС открытые реестры | ⚪ нет MCP | web_search + `[verify]`, номер регистрации обязателен |
| WIPO Global Brand DB | ⚪ | web_search |
| kad.arbitr.ru / СИПН | ⚪ нет MCP | web_search + `[verify]` |
| Документохранилище | [PLACEHOLDER ✓/✗] | Локальные пути |
| Telegram (Hermes gateway) | [PLACEHOLDER ✓/✗] | Алерты инлайн |
| КонсультантПлюс / Гарант | ⚪ нет MCP | web_search + `[verify]` |

*Перепроверка: `cold-start-interview --check-integrations`*

---

## Портфель (обзор)

**Знаки:** [PLACEHOLDER — сколько, ключевые, классы МКТУ]
**Патенты/ПМ:** [PLACEHOLDER — что запатентовано, что в заявках]
**ПО и авторские права:** [PLACEHOLDER — что зарегистрировано в ФИПС (программы для ЭВМ), что нет]
**Реестр:** путь к портфелю — `~/.hermes/legal/ip-legal/portfolio.yaml` (или внешняя система)

---

## Enforcement posture (постур защиты)

**Общая настройка:** [PLACEHOLDER — агрессивная (претензии по каждому факту) / средняя (претензии по значимым нарушениям) / пассивная (только стоп-сценарии)]

**Маркеры для претензий:** [PLACEHOLDER — напр. «копия сайта, похожий знак в смежном классе, использование логотипа»

**Порог суммы для C&D:** [PLACEHOLDER — от какой оценки ущерба пишем претензию]

**СИПН-постур:** [PLACEHOLDER — готовы ли судиться: да по каким типам / нет, сначала АС общего перечня / никогда]

**Триаж входящих претензий:** [PLACEHOLDER — кто принимает решение, срок реакции (30 дней по ст. 1252 ГК через суд; фактический срок ответа на претензию — из профиля)]

---

## Escalation

| Кто одобряет | Порог | Эскалируется к | Канал |
|---|---|---|---|
| [PLACEHOLDER] | | | |

**Автоматические эскалации:** [PLACEHOLDER — напр. «любая претензия от известного правообладателя», «патентная угроза к продукту», «истечение срока действия знака»]

---

## OSS-политика

**Разрешённые лицензии (без одобрения):** [PLACEHOLDER — напр. MIT, BSD-2/3, Apache-2.0, ISC]
**Требуют одобрения:** [PLACEHOLDER — напр. LGPL, MPL, EPL]
**Запрещённые в SaaS-продуктах:** [PLACEHOLDER — напр. AGPL, GPL; SSPL, BUSL — коммерческая оценка]
**Хранилище NOTICES:** [PLACEHOLDER — файл/путь]
**Процесс добавления зависимости:** [PLACEHOLDER — кто одобряет OSS в production]

---

## House style

**Язык претензий:** [PLACEHOLDER — жёсткий/дипломатичный; типовая структура]
**Формат triage memo:** [PLACEHOLDER — длина, разделы]
**Куда сохраняются C&D/претензии:** [PLACEHOLDER]
**Renewal/дедлайны-алерты:** [PLACEHOLDER — Telegram/файл]
**Отчётность поверенному:** [PLACEHOLDER — что он получает, в каком виде]

---

## Outputs

**Header work product** (по роли):
- Юрист: `КОНФИДЕНЦИАЛЬНО — ВНУТРЕННИЙ ПРАВОВОЙ АНАЛИЗ`
- Не-юрист: `ЗАМЕТКИ ДЛЯ ИССЛЕДОВАНИЯ — НЕ ЯВЛЯЕТСЯ ЮРИДИЧЕСКОЙ КОНСУЛЬТАЦИЕЙ`

**Теги источников:**
- `[ФИПС]` — данные открытых реестров реально извлечены в этой сессии
- `[kad.arbitr.ru]` / `[СИПН]` — судебные данные из этого источника
- `[pravo.gov.ru]` / `[КонсультантПлюс]` — НПА
- `[user provided]` / `[model knowledge — verify]` / `[web search — verify]` / `[settled — подтверждено YYYY-MM-DD]`

**Reviewer note:** ⚠️ Reviewer note один блок над deliverable (формат —
commercial-legal профиль).

**Jurisdiction recognition:** дефолт — ГК РФ ч. 4; экспортные знаки —
Мадрид/PCT; иностранное право — `[РФ фреймворк — проверить против [юрисдикция]]`.

**Currency trigger:** судебную практику СИПН и изменения ГК проверять
web_search'ом перед опорой на модельные знания.

**Retrieved-content trust / No silent supplement / Large input:** —
как в commercial-legal профиле.

---

## Matter workspaces

*Только для firm-практик. In-house — выключено.*

**Enabled:** ✗
**Active matter:** none
**Cross-matter context:** off

Файлы дел: `~/.hermes/legal/ip-legal/matters/<slug>/`.

---

## Verification log

`~/.hermes/legal/ip-legal/verification-log.md`:
`[YYYY-MM-DD] [цитата/факт] проверено [кем] против [источник] — [вердикт]`

---

## Seed documents reviewed

| Документ | Тип (знак/патент/договор/OSS) | Дата | Что извлечено |
|---|---|---|---|

---

*Перезапуск интервью: `cold-start-interview --redo`*