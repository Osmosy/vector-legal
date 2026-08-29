---
name: regulatory-legal
description: >
  Плагин «Регуляторика» для Vector Legal: мониторинг НПА и регуляторов
  (pravo.gov.ru, ЦБ, Минцифры, РКН, ФСТЭК, Роспотребнадзор, ФАС),
  diff новых требований против политик, surfacing пробелов, редлайн
  политик, трекинг комментариев на проекты НПА (regulation.gov.ru).
  Адаптация anthropics/claude-for-legal под право РФ (Регуляторная
  гильотина — ПП №1128, 44-ФЗ/223-ФЗ, отраслевые регуляторы) и Hermes.
  Используй при «что нового по нашему регулятору», «проверь изменения
  в НПА», «подготовь дайджест», «что требует новый приказ».
version: 1.0.0
author: Osmosy
license: Apache-2.0
metadata:
  hermes:
    tags: [legal, regulatory, russia, vector-legal, pravo-gov-ru]
    related_skills: [ai-governance-legal, commercial-legal]
---

# Regulatory Counsel — регуляторный мониторинг (Vector Legal)

Адаптация [claude-for-legal/regulatory-legal](https://github.com/anthropics/claude-for-legal)
(Anthropic, Apache-2.0) под право РФ и Hermes Agent.

## Что это

Мониторинг регуляторной среды компании: еженедельные (Monday-morning)
дайджесты по отраслевым регуляторам, diff новых НПА против внутренних
политик, трекер пробелов с дедлайнами, черновики комментариев на проекты
НПА. Замена paid-regulatory-feeds — pravo.gov.ru (бесплатный официальный
портал НПА) + regulation.gov.ru (обсуждения) + RSS регуляторов.

## ⚠️ Юридический дисклеймер (канонический)

**Всё, что производит плагин, — черновик для проверки юристом.** Не юридическая
консультация, не правовое заключение. Регуляторные цитаты require проверки
по первоисточнику (pravo.gov.ru) — теги источников указываются явно.

## Структура

```
regulatory-legal/
├── CLAUDE.md        # Шаблон practice profile (заполняет cold-start)
├── README.md                 # Этот файл
└── skills/
    ├── cold-start-interview/ # Интервью → practice profile (watchlist!)
    ├── customize/            # Точечная правка профиля
    ├── matter-workspace/     # Рабочие пространства дел (firm)
    ├── reg-feed-watcher/     # Пулл новых НПА/актов, классификация, дайджест
    ├── policy-diff/          # Diff нового НПА против внутренних политик
    ├── gaps/                 # Короткий трекер открытых gap'ов
    ├── gap-surfacer/         # Трекер gap'ов: статусы, напоминания, report
    ├── policy-redraft/       # Редлайн внутренней политики под новый НПА
    └── comments/             # Комментарии на проекты НПА + дедлайны
```

## Быстрый старт

```
cold-start-interview          # watchlist регуляторов + materiality
reg-feed-watcher              # проверить изменения с последней отметки
comments                      # открытые обсуждения + дедлайны
```

## Practice profile

Конфигурация живёт в `~/.hermes/legal/regulatory-legal/CLAUDE.md`
(шаблон — `CLAUDE.md` в корне плагина). Профиль содержит:
watchlist регуляторов, порог materiality (что «всегда важно»), путь к
библиотеке политик, feed-конфигурацию.

### Право Российской Федерации и коннекторы

| CFL (US) | Vector Legal (RU) |
|---|---|
| Federal Register API | **pravo.gov.ru** — официальный портал НПА (бесплатный; есть публикация проектов на regulation.gov.ru). RSS/API не гарантирован → web_search + тег `[pravo.gov.ru — verify]` |
| Regulations.gov docket (комментарии) | **regulation.gov.ru** — публичные обсуждения проектов; дедлайны обсуждений; также порталы субъектов |
| Paid regulatory feeds (Bloomberg Law и др.) | КонсультантПлюс/Гарант через web_search `[verify]`; официального MCP нет |
| Agency RSS (FTC, SEC, CFPB…) | Сайты регуляторов: ЦБ (cbr.ru), Минцифры, РКН (rkn.gov.ru), ФСТЭК, Роспотребнадзор, ФАС, Минфин, Минсельхоз; RSS нестабильны → web_search + прямые страницы «новостей» |
| OMB/OIRA review | Регуляторная гильотина — Постановление Правительства №1128 от 01.10.2020 (пересмотр обязательных требований, отмена неактуальных) `[verify]` |
| State AG enforcement |Надзор отраслевых органов + прокуратура; ФАС — контроль закупок и антимонопольных нарушений |
| Contract-based triggers (federal contracts) | **44-ФЗ / 223-ФЗ** — госзакупки: изменение закупочной документации, новые обязательные требования к участникам, изменения в КТРУ/ТРУ |
| Sector agencies | Отраслевой профиль пользователя: сельское хозяйство/производство — Минсельхоз (приказы), Россельхознадзор, Долгосрочно.рф (госпрограммы, субсидии) — указывается в watchlist на cold-start |

**Monday-morning digest:** навык рег-фида настроен на запуски по cron;
для сельского хозяйства/производства дефолтные фиды: Минсельхоз,
Россельхознадзор, Долгосрочно.рф, Минпромторг, ФАС (проверка закупок),
pravo.gov.ru (официальная публикация).

## Provisional mode

До заполнения профиля: watchlist по умолчанию (пустой), порог
materiality — «всегда важно» = акты, влияющие на обязательства компании.
Каждый выход помечается `[PROVISIONAL — запусти cold-start-interview]`.

## Отличия от CFL

1. pravo.gov.ru + regulation.gov.ru вместо Federal Register API (нет
   структурного API — web_search + `[verify]` вместо структурного полла)
2. Пути: `~/.hermes/legal/` вместо `~/.claude/plugins/config/`
3. RSS регуляторов США → страницы новостей российских ведомств (нестабильные
   — честная пометка `[verify]` на каждой находке)
4. CourtListener → kad.arbitr.ru (для судебных актов по спорам с ФАС/РКН)
5. Slack → Telegram через Hermes gateway

## Источник

[claude-for-legal](https://github.com/anthropics/claude-for-legal) © Anthropic,
Apache-2.0. Адаптация © Osmosy, Apache-2.0. Изменения: право РФ, пути Hermes,
русификация примеров. Не является юридической позицией ни Anthropic, ни Osmosy.