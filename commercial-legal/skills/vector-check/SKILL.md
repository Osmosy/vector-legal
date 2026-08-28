---
name: vector-check
description: "Load when the user asks to проверь контрагента, комплексная проверка, due diligence, проверь поставщика, проверь перед сделкой, DD на компанию, background check, vendor DD, M&A target screening, оценка рисков партнёра, проверка бенефициаров, проверка по ИНН. Covers 12 domains (website, registries, financial, VDR/AI, cyber, ESG, sanctions, OSINT, content, media, legal, tech-ops) with depth adaptation (express/standard/full) and jurisdiction awareness (RF/EU/US/UK/China/cross-border). Produces structured report with red flags, risk matrix, and Go/No-Go recommendation."
version: 1.0.0
author: Vector Legal / Osmosy
license: Apache 2.0
metadata:
  hermes:
    tags: [due-diligence, compliance, kontragent, m-and-a, vendor-risk, osint, sanctions, 115-fz, egul, fssp, kad-arbitr, checko]
    related_skills: [ru-text, vector-push, vector-work, obsidian]
  vector_legal:
    domain: commercial-legal
    position: 1
    purpose: pre-transaction due diligence
    complements: cowork-legal-vendor-check (post-transaction agreement status)
---

# Vector Check — комплексная проверка контрагента (Due Diligence)

## Назначение

До-сделочная проверка компании или физлица перед сделкой, наймом, инвестицией, партнёрством, закупкой. Проверяет **цель** (юрлицо/ИП/физлицо), а не **существующие договоры** с ним — это разные задачи.

**Отличие от `cowork-legal-vendor-check`:** тот проверяет, всё ли подписано с уже существующим поставщиком (CLM/CRM/email). Vector Check — это разведка ДО подписания: кто этот контрагент, какие у него риски, стоит ли вообще входить в сделку.

**Когда загружать:**

- «проверь контрагента», «проверь поставщика», «проверь компанию X»
- «сделай due diligence», «DD на X», «проверь перед сделкой»
- «кто владелец X», «бенефициары X», «проверь по ИНН»
- «оцени риски партнёра», «стоит ли работать с X»
- «проверь перед инвестицией», «M&A screening», «vendor onboarding check»
- «background check на директора», «проверь физлицо»
- «комплексная проверка», «проверка благонадёжности»

**Когда НЕ загружать:**

- Проверить, всё ли подписано с существующим поставщиком → `cowork-legal-vendor-check`
- Разово посмотреть ИНН в ЕГРЮЛ → просто `web_extract egrul.nalog.ru`
- Проверить санкционный список одного физлица → `web_extract opensanctions.org`
- Финансовый анализ отчётности без DD-контекста → `financial-analyst`

## Workflow

### Шаг 0 — Scoping (всегда первый)

Перед сбором данных уточнить или вывести из контекста. Если непонятно — `clarify`. **Не угадывать:**

1. **Цель** — ИНН / ОГРН / название / домен / ФИО
2. **Тип сделки** — M&A / инвестиция / поставка / партнёрство / найм / разовая сделка
3. **Глубина** — Express (2-4 ч) / Standard (2-5 дн) / Full (2-6 нед)
4. **Юрисдикция** — Россия (по умолчанию для русскоязычного) / EU / US / UK / Китай / трансгранично
5. **Язык отчёта** — русский (по умолчанию) / английский
6. **Куда сохранить** — Obsidian / файл на диске / inline в чат

### Шаг 1 — Базовый скрининг (Express, всегда)

Запустить параллельно через `delegate_task` или последовательно:

| # | Что | Инструмент |
|---|-----|-----------|
| 1 | Базовая идентификация | EGRUL / Companies House / OpenCorporates / OpenSanctions |
| 2 | Санкции + PEP | OpenSanctions, OFAC SDN (если US-связи) |
| 3 | Бенефициары (>25%) | EGRUL + chain parsing + OpenSanctions на каждое ФИО |
| 4 | Суды РФ (если применимо) | kad.arbitr.ru по ИНН и ФИО директора/учредителей |
| 5 | Исполнительные производства | fssprus.ru по ИНН и ФИО |
| 6 | Банкротство | bankrot.fedresurs.ru по ИНН и ФИО |
| 7 | Финансы (если публичная или отчётность) | ГИР БО / Companies House accounts / 10-K |
| 8 | Реестр дисквалифицированных | service.nalog.ru/disqualified |
| 9 | Массовый адрес / номинальный директор | EGRUL + поиск по адресу / директору |
| 10 | Сайт (минимум) | web_extract — структура, тональность, контакты, реквизиты |

**Express = шаги 1-10** (экспресс-чеклист Приложения A из источника).

### Шаг 2 — Углубление (Standard / Full)

Подробные чеклисты по 12 доменам — в `references/01-website.md` … `12-tech-ops.md`. Каждый reference — инструкция агенту «как собрать данные по этому домену, какие источники, что извлекать, как форматировать в отчёт».

**Standard** = все 12 доменов в базовом объёме + юрисдикция (см. `references/jurisdiction-*.md`).
**Full** = все 12 доменов глубоко + VDR (если есть) + Q&A + интервью + мониторинг.

### Шаг 3 — Юрисдикционный глубокий анализ

После сбора общих данных подключить юрисдикционный reference:

- `references/jurisdiction-russia.md` — EGRUL deep dive, бенефициары, 115-ФЗ, ГИР БО, масс-адрес, реестр дисквалификации, ОКВЭД, лицензии
- `references/jurisdiction-eu.md` — CSRD/CSDDD/GDPR/DG Comp/Unternehmensregister
- `references/jurisdiction-us.md` — SEC EDGAR 10-K, PACER, OFAC 50% Rule, ITAR/EAR, state-level
- `references/jurisdiction-uk.md` — Companies House + PSC, OFSI, FCA, Modern Slavery Act
- `references/jurisdiction-china.md` — GSXT, SOE status, PIPL, Negative List
- `references/jurisdiction-crossborder.md` — OpenCorporates, OpenSanctions, BEPS, CbCR

### Шаг 4 — Синтез и отчёт

Структура отчёта — в `references/output-format.md`. Содержит: Executive Summary, Red Flag Summary, 10 секций, Risk Matrix, Recommendation (Go / No-Go / Conditional), Приложение с источниками.

**Язык:** русский по умолчанию для русскоязычного юзера, использовать `ru-text` skill для типографики (кавычки «», тире —, неразрывные пробелы). Имена компаний и продуктов — в оригинале.

**Severity:**

- **CRITICAL** — сделка невозможна (санкции, уголовное преследование, going concern, массовое мошенничество)
- **HIGH** — существенный риск (банкротство в течение 12 мес, отказ раскрыть бенефициаров, конфликт интересов, SecurityScorecard < 600)
- **MEDIUM** — требует внимания (смена CFO, утечка данных 24 мес, ESG-скандал, судебные иски <10% оборота)
- **LOW** — наблюдение (мелкие иски, незначительные изменения)

**Источники:** цитировать явно. Если данные нет — сказать «не доступно / требует ручной проверки», **не выдумывать**.

### Шаг 5 — Сохранение и доставка

- **Файл:** сохранить как `<Company-Name>-DD-Report-YYYY-MM-DD.md`
- **Путь по умолчанию:** `~/Документы/Vector/Check/<slug>/` (создать, если нет)
- **Obsidian:** если vault существует, сохранить в `Obsidian/Projects/Vector-Check/<slug>.md` + добавить frontmatter с тегами `#vector-check #dd #контрагент`
- **Уведомление:** если есть `vector-push` — отправить ntfy `vector-legal-deadlines` priority=high с кратким резюме (только для HIGH/CRITICAL)
- **Memory:** если уровень риска HIGH/CRITICAL, сохранить в `memory` краткое summary для будущих сессий

## Глубина: что входит на каждом уровне

| Домен | Express | Standard | Full |
|-------|---------|----------|------|
| 01 Сайт | Главная + контакты + реквизиты | Полный обход, тональность, вакансии | + Google dorks + Wayback полный |
| 02 Реестры | EGRUL/Companies House | + история изменений + бенефициары chain | + выписки из всех юрисдикций |
| 03 Финансы | — | Ключевые метрики 3+ года | QoE, нормализация EBITDA, working capital peg |
| 04 VDR/AI | — | Если есть доступ — базовый ИИ-анализ | Полный обход V7 Go / Kira / Hebbia |
| 05 Кибер | SecurityScorecard free | + Shodan + HIBP + SOC 2 | + пентест-отчёт + архитектура |
| 06 ESG | — | MSCI/Sustainalytics/CDP | + Scope 3 + CSDDD compliance |
| 07 Санкции | OpenSanctions | Все списки + PEP + OFAC 50% | + Kharon + export control |
| 08 OSINT | — | LinkedIn + Glassdoor | Maltego + полный footprint |
| 09 Контент | — | Earnings calls 2-4 квартала | Multi-quarter sentiment + конференции |
| 10 Медиа | Google News | Отраслевые издания | Полный media audit |
| 11 Юр | Реестр дисквалификации | + суды + ИС | Полный contract review |
| 12 Тех/опс | BuiltWith | + GitHub + G2 + uptime | + архитектура + supply chain |

## Адаптация под Hermes

### Используй `ru-text` skill

Все русскоязычные отчёты — через `ru-text` для корректной типографики. Кавычки « », тире —, неразрывный пробел перед валютой (100 ₽).

### Используй `vector-push` для эскалации

```bash
# CRITICAL — санкции, мошенничество
curl -H "Priority: max" -H "Tags: warning,rotating_light" \
     -H "Title: ВЫЯВЛЕН CRITICAL FLAG" \
     -d "Контрагент: ООО Ромашка (ИНН 7700000000). Прямое совпадение с OFAC SDN. Сделка заблокирована." \
     http://ntfy/vector-legal-deadlines

# HIGH — высокий риск, требует внимания
curl -H "Priority: high" -H "Tags: scales" \
     -H "Title: DD Report: ООО Ромашка — HIGH risk" \
     -d "Условие: банковская гарантия на полную сумму + раскрытие бенефициаров до подписания." \
     http://ntfy/vector-legal-deadlines
```

### Сохраняй в memory если HIGH/CRITICAL

```python
# После финализации отчёта
memory(
    action="add",
    target="memory",
    content=f"DD-CHECK {date}: ООО {name} (ИНН {inn}) — {verdict} ({severity}). {top_risk}. Не работать без {conditions}."
)
```

## Внешние навыки (загружай по необходимости)

- `ru-text` — типографика для русского
- `vector-push` — ntfy-уведомления
- `obsidian` — сохранение в vault
- `claude-design` — PDF-версия отчёта (если нужна красивая)
- `webwright` / `browser-os-emulation` — если web_extract не справляется с капчей (ЕГРЮЛ, kad.arbitr)

## Локализация: Россия-первая

В отличие от Mike AI-оригинала, этот скилл **приоритизирует российские источники**, потому что аудитория — русскоязычный юзер:

- EGRUL, ФНС, ФССП, ГИР БО, Fedresurs, kad.arbitr, Rusprofile, Контур.Фокус, СПАРК
- 115-ФЗ (бенефициары, AML/CFT)
- 152-ФЗ (персональные данные)
- checko.ru API (если есть ключ в `~/.hermes/.env: CHECKO_API_KEY`)
- ОКВЭД, ОГРН, ИНН как основные идентификаторы
- Российские медиа: Коммерсантъ, Ведомости, РБК, Интерфакс

Глобальные источники — для трансграничных целей.

## Типичные ошибки

1. **Пропуск санкционного скрининга** — даже для российских контрагентов, особенно если есть иностранные связи. OpenSanctions обязателен.
2. **Доверие к одному источнику** — перекрёстная проверка: EGRUL vs сайт vs пресс-релизы vs суды.
3. **Игнорирование бенефициаров** — собственник юрлица ≠ конечный бенефициар. Идти до физлица.
4. **Устаревшие данные** — дата выписки EGRUL не старше 7 дней для Standard, 30 дней для Full.
5. **Подмена анализа сбором** — отчёт должен содержать выводы и рекомендацию, а не стопку ссылок.
6. **Выдуманные данные** — если источник недоступен (капча, paywall), сказать явно. Не придумывать.
7. **Игнорирование контекста сделки** — поставщик расходников для разовой сделки на 50K ₽ ≠ стратегический партнёр с госконтрактами. Глубина должна соответствовать.
8. **Не сохранять отчёт** — каждый DD = файл. Без файла DD не существует.

## Чеклист верификации (для агента)

- [ ] Шаг 0 scoping завершён (цель, тип сделки, глубина, юрисдикция, язык, путь сохранения)
- [ ] Express-уровень собран (шаги 1-10) — для любой глубины
- [ ] Дополнительные домены добавлены согласно уровню глубины
- [ ] Юрисдикционный reference применён
- [ ] Отчёт соответствует `output-format.md`
- [ ] Severity расставлен (CRITICAL / HIGH / MEDIUM / LOW)
- [ ] Источники процитированы явно
- [ ] Рекомендация ясная: Go / No-Go / Conditional
- [ ] Отчёт сохранён в файл
- [ ] При HIGH/CRITICAL — ntfy + memory

## Источник

Переработано из `due-diligence` v2.0.0 by Mike AI (Apache 2.0) — 12 глав, 19 references, ~70 сервисов, методология Mike AI 2026 года. Локализовано под Hermes Agent и Vector Legal, приоритизированы российские источники, добавлена интеграция с ntfy / memory / ru-text.
