<div align="center">

<img src="assets/vector-logo.png" alt="Vector Legal" width="200"/>

# Vector Legal

**Юридический AI-департамент для Hermes Agent — 12 плагинов, 167 навыков,
полный перенос Claude-for-Legal под российское право.**

[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue.svg)](https://github.com/NousResearch/hermes-agent)
[![Plugins: 12/12](https://img.shields.io/badge/Plugins-12%2F12-green.svg)](#домены)
[![Skills: 167](https://img.shields.io/badge/Skills-167-blue.svg)]()
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

</div>

---

Все 12 плагинов
[Claude-for-Legal](https://github.com/anthropics/claude-for-legal) (Anthropic,
151 навык) адаптированы под **российское право** — ГК РФ (включая ч. 4 — ИС),
152-ФЗ, ТК РФ, АПК/ГПК/КАС, КоАП, ФЗ-98 (КТ), ФЗ-115, ФЗ-135, ФЗ-149, ФЗ-324,
ФЗ-63, ФЗ-38, НК РФ — и Hermes Agent, с расширениями для российской практики:
протоколы разногласий вместо redline'ов, kad.arbitr/pravo.gov.ru/ЕГРЮЛ вместо
CourtListener/Westlaw/Federal Register, ЭДО и Telegram вместо Slack/DocuSign,
ЕГРЮЛ вместо SEC EDGAR, плюс 5 cron-агентов мониторинга и RF-новые
(vector-check DD, legal-research-ru, privacy-policy-ru, terms-of-service-ru,
patent-claim-chart).

**Архитектура, перенесённая из CFL:** каждый домен работает через **practice
profile** — файл практики, который пишет cold-start interview (агент
интервьюирует юриста, извлекает playbook из реальных подписанных договоров).
До настройки навыки работают в provisional mode с метками `[PROVISIONAL]`.
Provenance-теги обязательны: `[kad.arbitr.ru]` / `[pravo.gov.ru]` / `[ФИПС]` /
`[КонсультантПлюс]` / `[user provided]` / `[model knowledge — verify]`.
Cron-агенты мониторинга (cookbooks/) шипятся с 4-шлюзовым контрактом
(Google Cloud/DeepMind intelligent delegation).

**Все выходные данные — черновики для проверки юристом.** Не юридическая
консультация, не позиция Anthropic или Osmosy.

## Архитектура

**[Живая интерактивная диаграмма →](https://osmosy.github.io/vector-legal/vector-legal.architecture.html)**
12 плагинов, 167 навыков, practice profiles, MCP-коннекторы к РФ-базам,
consequential gates. Поиск узлов (`/`), трассировка маршрутов (`R`),
сравнение ролей (`L`), light/dark. Источник —
[docs/vector-legal.architecture.json](docs/vector-legal.architecture.json),
валидация Archify showcase 9/9.

## Домены (все 12 адаптированы)

| Плагин | Навыков | RF-ядро |
|-------|---------|--------|
| **commercial-legal** | 13+check | ГК (15/330/401/425/452), протоколы разногласий, 152-ФЗ в закупках, AI/ML 7-point playbook |
| **privacy-legal** | 9 | 152-ФЗ: поручения ст. 6, запросы субъектов 30 дней, оценка вреда ст. 18.1, ТИПЗ ФСТЭК №21, трансграничка ст. 12+№931, утечки 24/72ч, КоАП 13.11 |
| **corporate-legal** | 13 | ФЗ-14/208: крупные сделки, протоколы ст. 181.2 ГК, нотариат долей, ЕГРЮЛ-комплаенс |
| **employment-legal** | 20 | ТК РФ: закрытый перечень ст. 81 (ат-вилл не работает), сокращения, ГПХ-vs-трудовой (Пленум ВС №15), ЛНА |
| **litigation-legal** | 20 | АПК/ГПК/КАС: досудебный порядок ч. 5 ст. 4, kad.arbitr, сроки 1м/2м/3м, допрос ст. 88, обеспечение ст. 72, **patent-claim-chart** (ГК 1354–1358, СИПН) |
| **ai-governance-legal** | 10 | ЭПР ИИ ФЗ-123 [verify], ГОСТ Р 59276/ИСО 23894, Shadow-AI discovery, EU AI Act для экспорта |
| **regulatory-legal** | 9 | pravo.gov.ru монитор, гильотина ПП №1128, 44/223-ФЗ, ФАС, отраслевые (Минсельхоз/Россельхознадзор/Минпромторг) |
| **ip-legal** | 12 | Роспатент/ФИПС, ГК ч. 4 (1354-1407), СИПН, OSS (AGPL-triggers), патентный поверенный обязателен |
| **product-legal** | 9 | ФЗ-38 реклама + ЕРИР, ЗоЗПП, оферта ст. 437/428, Честный ЗНАК, 9-категорийный launch |
| **law-student** | 13 | LEARNING MODE NOT ANSWER MODE: Socratic, IRAC, case brief по КС/ВС РФ, bar-prep ФЗ-63 |
| **legal-clinic** | 14 | ФЗ-324, supervisor-gate (ничто клиенту без подписи), plain-language, 152-ФЗ-intake, семестровая отчётность |
| **legal-builder-hub** | 10 | app-store навыков: skills-qa 740 строк (13 параметров, 4-уровневый verdict no-override), SHA-pinning, injection-scan |

## Руководство пользователя

> Полная инструкция: [USER-GUIDE.md](USER-GUIDE.md). Установка, cold-start
> интервью, типовые запросы по каждому домену, 5 cron-агентов мониторинга,
> подключение правовых баз (MCP), работа в команде/firm, security,
> troubleshooting.

## Быстрый старт

```bash
git clone https://github.com/Osmosy/vector-legal.git
# В Hermes: укажи путь к домену и запусти cold-start interview:
#   «Пройти cold-start интервью commercial-legal»
```

Каждый домен: `<domain>/README.md` — описание и таблица навыков;
`<domain>/CLAUDE.md` — шаблон practice profile.

Статусы, план и принцип адаптации: [domains-status.md](domains-status.md).

## Агенты мониторинга

| Агент | Что отслеживает |
|-------|----------------|
| renewal-watcher | Даты продления контрактов |
| playbook-monitor | Изменения в playbook'ах и политиках |
| docket-watcher | Судебные дела (CourtListener) |
| reg-change-monitor | Изменения в нормативных реестрах |
| ip-renewal-watcher | Сроки патентов и товарных знаков |
| leave-tracker | Отпуска, больничные, compliance |
| dataroom-watcher | Состояние dataroom при сделках |
| launch-watcher | Compliance при запуске продуктов |

## MCP-коннекторы

| Коннектор | Система |
|-----------|---------|
| Ironclad | Управление контрактами |
| DocuSign | Электронная подпись |
| iManage | Документооборот |
| Everlaw | E-discovery |
| CourtListener | Судебные дела (PACER) |
| Slack | Коммуникации |
| Google Drive | Документы |
| Box | Хранилище |

## Архитектура

```
Юридическая задача → Vector Legal (оркестратор)
                       ├── КОММЕРЦИЯ: commercial-legal
                       ├── КОРПОРАТИВ: corporate-legal
                       ├── ТРУД: employment-legal
                       ├── СУДЫ: litigation-legal
                       ├── ПРИВАТНОСТЬ: privacy-legal
                       ├── РЕГУЛЯТОРЫ: regulatory-legal
                       ├── ИИ-ПРАВО: ai-governance-legal
                       ├── ИНТЕЛЛЕКТУАЛКА: ip-legal
                       ├── ПРОДУКТЫ: product-legal
                       └── ФОН: 8 агентов мониторинга
```

## Быстрый старт

```bash
git clone https://github.com/Osmosy/vector-legal.git

# Примеры
hermes "Проверь договор поставки мяса на риски"           # → commercial-legal
hermes "Отслеживай изменения в 152-ФЗ"                     # → regulatory-legal
hermes "Проверь compliance с EU AI Act"                    # → ai-governance-legal
hermes "Подготовь трудовой договор для обвальщика"         # → employment-legal
```

## Важное предупреждение

**Все выходные данные — черновики.** Агенты не заменяют юриста. Каждый документ требует проверки квалифицированным специалистом. Источники указываются явно.

## Связанные проекты Vector

| Проект | Роль |
|--------|------|
| [Vector Work](https://github.com/Osmosy/vector-work) | Базовые юр-задачи (NDA, договоры) |
| [Vector Meat](https://github.com/Osmosy/vector-meat) | Юрподдержка мясопереработки |
| [Vector Marketing](https://github.com/Osmosy/vector-marketing) | Юрподдержка агентства |

## Источник

Адаптировано из [Anthropic Claude-for-Legal](https://github.com/anthropics/claude-for-legal) — 60+ агентов, 111+ навыков. Apache 2.0.
