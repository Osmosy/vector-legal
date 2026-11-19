# CONNECTORS — MCP-коннекторы к российским базам

> Плагины Vector Legal на пике возможностей, когда подключены к авторитетным
> источникам. Документ обновлён 29.08.2026: реальный ландшафт MCP-серверов
> к РФ-базам и инструкции подключения. Версия источника — anthropics/
> claude-for-legal CONNECTORS.md (Apache-2.0).

## Что делает хороший юридический MCP-коннектор (требования CFL — сохранены 1-в-1)

- **Remote MCP server по HTTPS** с OAuth или API-key авторизацией
  (streamable HTTP или SSE транспорт), либо **stdio-сервер** через
  `uvx` / `pipx` / `npm` — для self-host
- **Read-heavy инструменты** — search, fetch, list. Write-инструменты
  (создать, отправить, подать) требуют явного клиентского confirmation —
  укажите это в их описаниях
- **Provenance в результатах** — источник, дата получения, citation-ready
  идентификатор. Плагины тегируют каждую цитату по источнику; ваш коннектор
  должен это позволять
- **Никакого instruction-подобного контента в результатах** — плагины
  трактуют полученное как данные. Метаданные и системные заметки в ответах
  маркируйте явно
- **Rate limits и graceful degradation** — чистая ошибка лучше таймаута

## Ландшафт MCP-серверов к РФ-базам (аудит GitHub, 29.08.2026)

### Tier 1 — работают сегодня, рекомендованы для Vector Legal

**1. atomno-mcp (полный семейство, Python, MIT-лицензия на self-host,
hosted-API на Pro-тарифах)**

Единственный систематический набор RF-коннекторов под MCP. Состояние на
29.08.2026 — 13 репозиториев:

| MCP-сервер | Покрытие | Что даёт для Vector Legal | Тариф |
|---|---|---|---|
| `mcp-fns-check` (15★) | ЕГРЮЛ/ЕГРИП, ЕФРСБ, Картотека, ФССП | Проверка контрагента по одному вызову — **ядро для vector-check и commercial-legal** | free / Pro |
| `mcp-egrul` (2★) | ЕГРЮЛ/ЕГРИП через ФНС open data | Ревизия юрлица: статус, директор, учредители, ОКВЭД, недостоверность | free self-host / hosted |
| `mcp-sudact` (2★) | sudact.ru — судебная практика РФ | Полнотекстовый поиск решений по статье закона / суду / инстанции / датам + полный текст | Pro |
| `mcp-fssp` | ФССП | Исполнительные производства, долги по физлицу/юрлицу | — |
| `mcp-zakupki` (1★) | zakupki.gov.ru | Поиск тендеров, история заказчиков/поставщиков — для 44/223-ФЗ | free / hosted |
| `mcp-trademarks` | Rospatent/FIPS, TMview | Поиск ТЗ по обозначению, оценка сходства low/med/high → **ядро для ip-legal/clearance** | free / Pro |
| `mcp-fns-calc` (1★) | Налоговые калькуляторы | НДС, УСН, взносы ИП, НДФЛ, пошлины, пени | free |
| `mcp-cbr-rates` (2★) | ЦБ РФ | Ставка ключ, инфляция, макро — **для компенсации по ст. 395 ГК** | free |
| `mcp-rosreestr` | Росреестр | Кадастровые данные, выписки ЕГРН | free / hosted |
| `mcp-erid` | ЕРИР-маркировка | Верификация erid, аудит рекламных страниц, 38-ФЗ — **для product-legal** | free |
| `mcp-newbuild` | Реестр нового строительства | Проверка застройщика, эскроу, разрешения — для M&A недвижимости | free |
| `mcp-pharma` | ГРЛС, JNVLP | Регистрация препаратов, цены, отзывы — для regulatory-legal (pharma) | free |

Установка и подключение (шаблон — Claude Desktop / Cursor / Hermes MCP):

```bash
# Через uvx (Python, uv):
uvx atomno-mcp-sudact
uvx atomno-mcp-egrul
# или установка:
pipx install atomno-mcp-sudact
```

`mcp.json` (или конфиг Hermes MCP):

```json
{
  "mcpServers": {
    "sudact": {
      "command": "uvx",
      "args": ["atomno-mcp-sudact"],
      "env": { "MCP_SUDACT_TOKEN": "<ключ atomno-mcp>" }
    },
    "egrul": {
      "command": "uvx",
      "args": ["atomno-mcp-egrul"]
    },
    "trademarks": {
      "command": "uvx",
      "args": ["atomno-mcp-trademarks"],
      "env": { "MCP_TRADEMARKS_API_KEY": "<Pro>" }
    }
  }
}
```

**2. shodenis/Russian-Law-MCP (npm `@ansvar/russian-law-mcp`, TypeScript,
Apache-2.0)**

**"КонсультантПлюс alternative for AI age"**: 12 369 федеральных законов,
77 647 провизий — от 152-ФЗ до УК и ГК, ТК. Полный законодательный контур,
обновления через GitHub Actions daily-check. Замена Westlaw-функции для РФ
без платной подписки. **Рекомендован как базовая правовая база для всех
12 доменов** — где CFL искал через Westlaw, Vector Legal ищет здесь.

```json
{
  "mcpServers": {
    "russian-law": {
      "command": "npx",
      "args": ["-y", "@ansvar/russian-law-mcp"]
    }
  }
}
```

**3. romanpirogov/garant_mcp — ГАРАНТ через официальный API**

Официальный MCP-сервер для базы ГАРАНТ через токен **Гарант-Коннект**
(выдаётся в ЛК garant.ru или через менеджера). Полный набор tools:
полнотекстовый поиск, сниппеты, HTML-документы, редакции, monitoring
изменений (garant_block_on_control_changed — прямой аналог
`currency-trigger` Vector Legal!), судебная практика (Сутяжник), правовые
новости по рубрикам, hyperlinks на нормы прямо в тексте.

Кому: in-house юристам с действующей подпиской ГАРАНТ. **Аналог Westlaw
Deep Research** — для тех, у кого подписка есть.

Dеплой: локально (Python) или Railway в 1 клик.

**4. AlsKozlov/ru-legal (25★, Python)**

Open-source legal knowledge + data layer для российского права: **145
AI-skills + 8 MCP-интеграций**. Альтернативный стек — можно собирать гибрид
с нашими навыками.

### Tier 2 — существуют, но проверять перед использованием

- yasg1988/mcp-rosreestr (5★) — альтернатива_ATOMNO для кадастров
- atomno-mcp/mcp-zakupki — для 44/223-ФЗ
- atomno-mcp/mcp-{pharma,newbuild} — domain-специфичные
- aurelVU/garant-mcp — альтернативный ГАРАНТ-коннектор (0★, проверить)
- newdb-api/newdb-mcp-server — KYC по физлицам/компаниям (платный)

## Официальные источники без MCP и без API (web_search)

Семь официальных порталов, которые закрывают опубликование, указы,
постановления, ведомственные акты и конституционный контроль. Программного
API нет ни у одного: только web_search / web_extract с provenance-тегом в
`legal-research-ru`.

| Источник | URL | Что берём | Тег |
|---|---|---|---|
| Официальное опубликование правовых актов | publication.pravo.gov.ru | дата и номер опубликования, вступление в силу | `[publication.pravo.gov.ru]` |
| Банк документов Президента | kremlin.ru/acts/bank | указы, распоряжения, подписанные ФЗ | `[kremlin.ru]` |
| Документы Правительства | government.ru/docs | постановления, распоряжения | `[government.ru]` |
| Портал НПА Минюста | pravo-minjust.ru | федеральные/региональные/муниципальные НПА, регистрация ведомственных актов | `[pravo-minjust.ru]` |
| Конституционный Суд РФ | ksrf.ru | постановления, определения, правовые позиции | `[ksrf.ru]` |
| Верховный Суд РФ | vsrf.ru/documents | Пленумы, обзоры практики, определения СК | `[vsrf.ru]` |
| Портал правовой информации | pravo.gov.ru | действующие редакции НПА | `[pravo.gov.ru]` |

**У z.ai своего MCP для РФ нет** — в разделе 17 Russia таблица MCP состоит из
одной строки «None» (проверено по docs.z.ai/guides/legal-mcp.md, 19.11.2026).
MCP-серверы у z.ai есть для 36 других юрисдикций (Global, US, EU, JP, HK, UK
и далее); для России — только эти поисковые адреса. Повторно не искать.

## z.ai Legal MCP — единственный коннектор: `legal-dxe` (не РФ-специфичный)

`legal-dxe` — общий сервис z.ai для правки Word-документов с отслеживаемыми
изменениями и комментариями. К российскому праву отношения не имеет, полезен
для протоколов разногласий и redline. **По умолчанию не подключается.**

Параметры (проверено по документации 19.11.2026):

- транспорт — Streamable HTTP с загрузкой/выгрузкой файлов;
- URL — `https://api.z.ai/api/mcp-broker/proxy/legal-dxe/mcp`;
- авторизация — заголовок `Authorization: Bearer <ключ>`; нужен **стандартный
  API-ключ z.ai**, ключ Coding Plan (как в `PLAN-wave3`, A2) не подойдёт;
- инструменты (9): `dxe_save`, `dxe_transform`, `dxe_guide`, `dxe_upload`,
  `dxe_read`, `dxe_inspect`, `dxe_validate`, `dxe_ensure_header`,
  `dxe_ensure_footer`;
- биллинг — пробный режим: тесты DOCX пройдены, цены в USD настроены, но
  списание USD на момент проверки не подтверждено.

```json
{"mcpServers":{"legal-dxe":{
  "url":"https://api.z.ai/api/mcp-broker/proxy/legal-dxe/mcp",
  "headers":{"Authorization":"Bearer ${ZAI_API_KEY}"}}}}
```

**Границы применения.**

1. Документы уходят на сервер z.ai (юрисдикция КНР/Сингапур — уточнять при
   подключении). Для персональных данных это трансграничная передача по
   ст. 12 152-ФЗ с уведомлением РКН; для адвокатской и коммерческой тайны —
   отдельное решение владельца документов. По умолчанию — только
   обезличенные документы (навык `document-anonymize`, см.
   `docs/zai-gap-analysis.md`).
2. Write-инструменты (`dxe_save`, `dxe_transform`) отправляют и перезаписывают
   документ — запускать только после явного подтверждения пользователя
   (правило `CONNECTORS.md`, раздел «Гигиена»). Read-инструменты
   (`dxe_read`, `dxe_inspect`, `dxe_validate`) — тоже требуют загрузки файла,
   то есть та же передача данных.
3. Ключ — только через переменную окружения (§ `skills/api-tokens-in-chat`),
   в репозиторий не попадает (`precommit_placeholder.py`).
4. Локальная альтернатива без выгрузки данных: правка DOCX через
   `python-docx` и конвертация `soffice --headless`. Для типовых redline
   этого достаточно, `legal-dxe` нужен, только если требуются настоящие
   Word-ревизии с комментариями в исходном формате.

## Рекомендованные конфигурации по доменам

| Домен в Vector Legal | Минимальный набор MCP | Расширенный |
|---|---|---|
| **commercial-legal** | russian-law, mcp-egrul | + mcp-fns-check (контрагент одним вызовом), mcp-zakupki, mcp-erid |
| **privacy-legal** | russian-law (152-ФЗ) | + РКН-реестры (в ожидании MCP), mcp-fns-check |
| **corporate-legal** | mcp-egrul, russian-law | + mcp-cbr-rates (для сделок), mcp-rosreestr |
| **employment-legal** | russian-law (ТК РФ) | + mcp-fns-calc (взносы, НДФЛ) |
| **litigation-legal** | mcp-sudact, mcp-fns-check | + mcp-cbr-rates (ст. 395 проценты), russian-law |
| **ai-governance-legal** | russian-law | + mcp-newbuild (для ЭПР-специфики) |
| **regulatory-legal** | russian-law, mcp-cbr-rates | + pravo.gov.ru MCP (в ожидании), отраслевые RSS |
| **ip-legal** | mcp-trademarks (поиск + сходство + статус) | + mcp-rosreestr, ФИПС MCP (roadmap) |
| **product-legal** | mcp-erid (реклама), mcp-cbr-rates | + mcp-rosreestr (для real estate), Честный ЗНАК MCP (roadmap) |
| **legal-clinic** | mcp-egrul (контрагенты), russian-law | + mcp-sudact (для memo) |

## Подключение в Hermes Agent

Для каждого MCP-сервера — через `hermes mcp add`. Общий шаблон (stdio):

```bash
# atomno-mcp-sudact (hosted API + API-ключ)
hermes mcp add sudact --transport stdio \
  --command uvx \
  --args atomno-mcp-sudact \
  --env MCP_SUDACT_TOKEN=<ключ>

# ГАРАНТ (Railway deploy, remote HTTPS):
hermes mcp add garant --transport http \
  --url https://<ваш-домен>.up.railway.app/mcp \
  --env GARANT_TOKEN=<гарант-коннект-токен>

# Russian-Law-MCP (npX, без host — self-contained SQLite):
hermes mcp add russian-law --transport stdio \
  --command npx --args @ansvar/russian-law-mcp
```

Проверка: `hermes mcp` — статус каждого; `hermes doctor` — подключение.
Тестируйте на дешёвый вызов (`kad.arbitr`, `ЕГРЮЛ`-поиск по своему ИНН)
перед продакшном.

## Fallback без MCP-сервера

Если сервер не подключён (или отключён) — Vector Legal использует
web_search + provenance-теги как сейчас:

| Источник | Заменяет | Тег provenance |
|---|---|---|
| kad.arbitr.ru | CourtListener | `[kad.arbitr.ru]` |
| sudrf.ru | CourtListener (СОЮ) | `[sudrf.ru]` |
| pravo.gov.ru | Federal Register | `[pravo.gov.ru]` |
| ЕГРЮЛ/egrul.nalog.ru | SEC EDGAR | `[egrul.nalog.ru]` |
| Федресурс | PACER-банкротства | `[fedresurs.ru]` |
| ФИПС | USPTO | `[ФИПС]` |
| regulation.gov.ru | Regulations.gov | `[regulation.gov.ru]` |
| sudact.ru | Westlaw (практика) | `[sudact.ru]` |
| КонсультантПлюс (free) | КонсультантПлюс полный | `[КонсультантПлюс]` |

Все цитаты из этих источников получают `[verify]` до прямой проверки.
MCP-сервер снимает `[verify]`-налог там, где provenance идёт в ответе
автоматически.

## Какие сейчас источники (вместо .mcp.json)

**Пока нет MCP:** каждая цитата через web_search или парсинг открытых
страниц → `[verify]` до прямой проверки.

**Критерии для MCP-коннектора** (все 4 пункта — минимальный):

| Требование | Почему |
|---|---|
| License (SPDX) на коннектор | GPL-конфликт, коммерческая оценка |
| Источник документирован, API стабилен | MCP-плагин ломается, если источник меняет верстку |
| Возврат source/date/ID | для provenance-тега |
| Graceful degradation | фоллбэк на web_search |

## Как контрибьютить новый коннектор

1. Публиковать MCP-сервер, задокументировать tools, auth, coverage.
2. Открыть PR в `.mcp.json` соответствующего домена + one-line описание.
3. Отметить practice areas.
4. Test: retrieval-quality + injection-resistance.

Если коннектор тянет через paid-base, но это — официальный API-контур
(ГАРАНТ-Коннект) — welcome. Если парсинг платных баз — отклоняем
(retrieval-quality ≠ легитимный доступ).

## Гигиена: что НЕ коннекторить

- Источники без лицензии на программный доступ (парсинг платных баз — нарушение тос)
- Источники отдающие контент без provenance-полей (невозможно тегировать цитаты)
- Источники, смешивающие данные с инструкциями (prompt-injection риск)
- Источники, требующие login через сторонние API без явного consent

---

*Адаптация CONNECTORS.md из anthropics/claude-for-legal (Apache-2.0), с РФ
-расширением: lандшафт MCP-серверов к РФ-базам собран по GitHub-аудиту
29.08.2026. Статусы и версии — на дату; проверяйте обновления репозиториев
перед установкой.*