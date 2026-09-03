# DataNewton API — проверка контрагентов (справочник)

Источник: официальная OpenAPI-схема 3.1 (93 пути, v1). Схема-полная: `datanewton-api-openapi-schema.json` (рядом).
Сайт: https://datanewton.ru · Доки: https://datanewton.ru/docs/api · ООО «Датаномика», ИНН 9728006808.

## Подключение

```bash
source ~/.config/datanewton.env   # DATANEWTON_API_KEY, DATANEWTON_API_BASE

# ВАЖНО: key передаётся в QUERY-параметре, НЕ в Bearer-заголовке!
curl -s "https://api.datanewton.ru/v1/counterparty-basic?key=$DATANEWTON_API_KEY&inn=7707083893"
```

- **Формат:** GET (почти все), `key=...` в query; POST — для fssp, batch-методов, ogrnsByAddress/Domain
- **Идентификация:** `inn=` (10/12 цифр) **или** `ogrn=` (13/15 цифр)
- **Ответ всегда содержит:** `available_count` / `demo_available_count` — остаток лимита
- **MCP** (`https://datanewton.ru/mcp`) — отдельный платный тариф (роль API_MCP_FULL), REST-ключ не действует (403)

## Лимиты

- Демо-доступ при регистрации: **200 единиц** (у нас на ключе было 999 на 2026-09-03)
- 200 запросов/мин, пакетные методы — 100/мин, max 10 TCP-соединений с IP
- Превышение → HTTP 429

## Методы по группам проверки

### Базовая карточка (выраженная проверка — начать с этого)
| Метод | Что даёт |
|---|---|
| `GET counterparty-basic` | Реквизиты, статус, адрес (недостоверность), директора, владельцы, ОКВЭД, уставный капитал, численность, налоговый режим, Росстат-коды, MSP-блок, negative_lists |
| `GET counterparty` | Расширенная карточка (параметр `filters`) |
| `GET scoring` | Скоринг (score/status/percent) |
| `GET risks` | Флаги рисков по категориям (негативные публикации и др., color=NEGATIVE) |
| `GET registration-docs` | Регистрационные документы |

### Финансы
| Метод | Что даёт |
|---|---|
| `GET finance` | Бухотчётность |
| `GET taxInfo` | Налоговая информация |
| `GET paidTaxes` | Уплаченные налоги |
| `GET blockedBankAccounts` | Заблокированные счета (115-ФЗ) |
| `POST taxpayerStatuses` | Статусы налогоплательщика (batch) |

### Суды и долги
| Метод | Что даёт |
|---|---|
| `GET arbitration-cases` | Арбитраж: role/dispute/status/даты, need_document |
| `POST fssp` | ФССП: body `{"inn":...,"limit":N}` (limit=0 — только статистика) |
| `GET bankruptcy` | Банкротство |
| `POST courtCases` | Суды общей юрисдикции (СОЮ) |
| `GET complaints` | Жалобы (role/status/даты) |

### Связи и структура
| Метод | Что даёт |
|---|---|
| `GET links` (v1) / `GET /v2/links` | Граф аффилированности (v2: level, include_addresses, edge_types). У Сбера: 5000 узлов/6342 ребра |
| `GET nkoReestr` | Реестр НКО |
| `GET sroMembership` | Членство в СРО |
| `GET corporateActions` | Корпоративные действия (реорганизация и т.п.) |
| `GET intellectual_property` | Лицензии, товарные знаки, ПО |

### Госконтракты и закупки
| Метод | Что даёт |
|---|---|
| `GET governmentContracts` | Обязательный `types=`: FZ44/FZ223/PP615/ALL; statuses: E/IN/EC/ET; role: CUSTOMER/SUPPLIER/ALL |
| `GET governmentContractsStat` | Статистика (ogrn + types) |
| `GET lease-contracts` | Договоры лизинга |

### Надзор и прочее
| Метод | Что даёт |
|---|---|
| `GET inspections` / `inspectionsStat` | Проверки надзорных органов |
| `GET complaints` | Жалобы |
| `GET grants` | Гранты |
| `GET okpdList` | Продукция по ОКПД |
| `GET vacancies` (POST batch) | Вакансии |
| `POST ogrnsByAddress` / `ogrnsByDomain` | ОГРН по адресу / по домену сайта |
| `POST websites/search` | Поиск по сайтам компаний |

### Пакетные методы (массивы ОГРН, 100/мин)
`batchCards`, `batchCardsByFilters`, `batchChanges` (мониторинг изменений!), `batchContracts`, `batchCourtCases`, `batchProducts`, `batchVacancies`, `batchCases*` (арбитраж), `leases`, `suggestions`, `filtersPreview`

### Сегменты (выгрузки, как в вебе)
`GET/POST segment`, `segment/{id}/counterparties`, `segment/{id}/export[/batch]`

## Проверенный пример (ПАО СберБанк, ИНН 7707083893, 2026-09-03)

- `counterparty-basic`: статус «Действует», адрес без недостоверности, negative_lists=false
- `scoring`: demo-скоринг (HIGH/100 — в демо не реальный)
- `risks`: негативные публикации (флаги color=NEGATIVE с деталями)
- `links` v1: 5000 узлов / 6342 ребра
- `arbitration-cases`: 1.3 МБ дел
- `fssp` (POST): исполнительные производства
- `governmentContracts` (types=ALL): 79 275 контрактов

## Интеграция в vector-check

1. **Express-проверка** (2 ед. лимита): `counterparty-basic` + `scoring` → Go/No-Go pre-check
2. **Standard** (+4 ед.): `risks`, `fssp`, `arbitration-cases`, `bankruptcy`
3. **Full** (+3 ед.): `links` (v2 с level), `finance`, `governmentContracts` (types=ALL, role=SUPPLIER для поставщика)
4. **Мониторинг после сделки:** `batchChanges` по списку ОГРН → смена директора/владельцев, банкротство

Лимит демо-ключа (~999 ед.) ≈ 150–300 полных проверок. Платный тариф — через поддержку (info@datanewton.ru).