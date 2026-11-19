# Gap-анализ: навыки z.ai (`autoclaw-skills`) против Vector Legal

Источник разбора: <https://docs.z.ai/guides/legal-mcp>, раздел 17 Russia
(снято 19.11.2026; markdown-версия страницы доступна по
`docs.z.ai/guides/legal-mcp.md`). Проверка выполнена агентом из этого
репозитория 19.11.2026.

## 1. Что реально есть в разделе Russia

| Блок | Содержимое | Вывод |
|---|---|---|
| **MCP** | одна строка «None — Use this jurisdiction's Search URL for web searches» | своего РФ-MCP у z.ai нет; реальные MCP-серверы на странице указаны только у 5 разделов из 36 (Global — 4, US — 1, EU — 1, Japan — 1, Hong Kong — 1), у остальных «None» |
| **Search URL** | 7 адресов: pravo.gov.ru, publication.pravo.gov.ru, kremlin.ru/acts/bank, government.ru/docs, pravo-minjust.ru, ksrf.ru, vsrf.ru/documents | забраны в `legal-research-ru` и `CONNECTORS-ru-mcp.md` |
| **Skills** | 29 навыков в таблице раздела Russia; набор один и тот же для всех стран (всего на странице 37 уникальных архивов — включая страновые для US/EU/JP/HK) | РФ-специфики в навыках нет |
| **legal-dxe** | общий (не РФ) remote MCP для правки DOCX, 9 инструментов `dxe_*` | опциональный коннектор, описан в `CONNECTORS-ru-mcp.md` |

## 2. Лицензия архивов — проверена фактически

Скачаны и распакованы все шесть архивов (curl с браузерным User-Agent,
19.11.2026): `legal-core-rules-pack27` (4 028 б), `amendment-history-1.0.1`
(2 874), `contract-desensitize-1.0.0` (2 674), `legal-norm-validity-check-1.0.0`
(1 581), `research-start-1.0.0` (1 437), `legal-docx-revisor-1.0.4` (29 473).

Результат:

- файла `LICENSE` нет ни в одном архиве; на странице документации слово
  «license» не встречается ни разу;
- уведомление об авторстве есть ровно в одном файле из шести
  (`amendment-history/SKILL.md`: «Adapted from Anthropic's Claude for Legal
  under Apache License 2.0. See `THIRD_PARTY_NOTICES.md` at the workspace
  root»), причём упомянутый `THIRD_PARTY_NOTICES.md` в поставку не входит;
- в остальных 28 навыках атрибуции нет;
- `legal-core-rules` целиком на китайском (описание и тело) — то есть это не
  перевод апстрима, а собственная редакция z.ai без уведомления;
- содержательно архивы простые: только `SKILL.md`, у `legal-docx-revisor`
  дополнительно `scripts/dxe_client.py` (41 677 б) — клиент облачного DXE.

**Вывод: режим «только идеи».** Ни один текст z.ai в репозиторий не переносится,
ни целиком, ни фрагментами. Причина техническая: в поставке отсутствуют
обязательные уведомления, которые нужно сохранять при переработке
(§4(b) Apache-2.0), поэтому корректно атрибутировать даже потенциально
свободные файлы невозможно.

## 3. Законный источник тех же идей

Эталонный апстрим — [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal)
(Apache-2.0, файл `LICENSE` на месте, файла `NOTICE` нет → обязанность §4(d)
не возникает). Сверка путей 19.11.2026: в апстриме 151 навык, у нас 154
(без `skills/cowork-roles/`), **148 совпадают по пути**. Собственных навыков
шесть, из апстрима не перенесены три — перечень в `THIRD_PARTY_NOTICES.md`.

Отсюда правило: если для нужного навыка есть прототип в апстриме — берём
оттуда с атрибуцией Anthropic; если прототипа нет (российская специфика) —
пишем с нуля. z.ai остаётся перечнем тем.

## 4. Одиннадцать навыков, которые уже есть (не дублировать)

`amendment-history` (commercial-legal), `case-brief` (law-student),
`escalation-flagger`, `review`, `stakeholder-summary` (commercial-legal),
`feature-risk-assessment`, `is-this-a-problem` (product-legal),
`legal-risk-assessment` (cowork-roles/legal), `matter-briefing`
(litigation-legal), `research-start` (legal-clinic), `tabular-review`
(corporate-legal).

Уточнение по `amendment-history`: у z.ai это «amendment history and version
relationships of legal texts **or contracts**», тело — базовый договор и
допсоглашения, с оговоркой «do not decide legal priority between conflicting
documents». Это тот же смысл, что у нас. Отдельного навыка про историю
редакций нормы у z.ai нет — в плане это предположение снято.

## 5. Восемнадцать навыков, которых нет в репозитории

| Навык z.ai | Решение | Куда |
|---|---|---|
| `legal-norm-validity-check` | **Новый RU-навык.** Действует ли норма на дату: редакция, официальное опубликование, регистрация в Минюсте, позиции КС, гильотина, утрата силы | `regulatory-legal/skills/norm-validity-check` ✅ сделано |
| `contract-desensitize` | **Новый RU-навык.** Обезличивание документа перед отправкой во внешний ИИ/MCP, обратимая таблица замен, проверка косвенных идентификаторов и метаданных | `privacy-legal/skills/document-anonymize` ✅ сделано |
| `legal-core-rules` | Не отдельный навык. Наши правила источников и цитирования — `AGENTS.md` §3 + `legal-research-ru`. Китайский свод правил как текст не нужен | — |
| `contract-review` | Покрыто `commercial-legal/review` и специализированными review | — |
| `general-legal-risk-assessment` | Покрыто `legal-risk-assessment` | — |
| `legal-analysis-memo` | Отчёт `legal-research-ru` (Шаг 4) уже даёт структуру мемо | `legal-research-ru` |
| `legal-research-drafting` | Покрыто `legal-research-ru` + `brief-section-drafter` | — |
| `argument-chain-construction`, `argument-strength-evaluation`, `legal-interpretation-argument` | Один навык «позиция и контраргументы» — **написан** 19.11.2026 | `litigation-legal/skills/argument-builder` ✅ |
| `dispute-issue-identification`, `element-analysis`, `legal-element-extraction` | Один навык «предмет доказывания / элементы состава» — **написан** 19.11.2026 | `litigation-legal/skills/issue-elements` ✅ |
| `evidence-evaluation` | Оценка доказательств — **написан** 19.11.2026 (относимость, допустимость, достоверность, достаточность) | `litigation-legal/skills/evidence-review` ✅ |
| `legal-document-summarization`, `multi-document-summarization` | Не отдельные навыки: общая способность модели; при необходимости — режим в `matter-briefing` | — |
| `legal-docx` | Не нужен: создание .docx — runtime-задача (`python-docx`, `soffice`) | — |
| `legal-docx-revisor` | Только как коннектор `legal-dxe`, не как навык | `CONNECTORS-ru-mcp.md` |

Итог: пять навыков написаны (норма, обезличивание, позиция и контраргументы,
предмет доказывания, оценка доказательств), десять закрыты существующими или
признаны ненужными.

## 6. Правило на будущее

Любой следующий разбор z.ai-навыков начинается с этого файла. Тексты не
копировать; при совпадении темы идти в апстрим `claude-for-legal`; при
отсутствии прототипа писать своё с нуля по формату `CONTRIBUTING.md`.
