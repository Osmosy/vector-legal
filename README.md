<div align="center">

<img src="assets/vector-logo.png" alt="Vector Legal" width="200"/>

# Vector Legal

**Юридический AI-департамент — 9 доменов права, 111+ навыков, 8 агентов мониторинга**

[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue.svg)](https://github.com/NousResearch/hermes-agent)
[![Domains: 9](https://img.shields.io/badge/Domains-9-green.svg)](#домены-права)
[![Skills: 111+](https://img.shields.io/badge/Skills-111%2B-orange.svg)](https://github.com/anthropics/claude-for-legal)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

</div>

---

Юридический AI-департамент на базе Claude-for-Legal (Anthropic). 9 доменов права, 111+ навыков, MCP-коннекторы к реальным системам (Ironclad, DocuSign, iManage, Everlaw, CourtListener).

## Домены права

| Домен | Навыков | Что делает |
|-------|---------|-----------|
| **commercial-legal** | 12 | Коммерческие договоры, закупки, due diligence, deal debrief |
| **corporate-legal** | 13 | M&A, корпоративные сделки, board resolutions, dataroom |
| **employment-legal** | 20 | Трудовые договоры, споры, политики, leave tracking |
| **litigation-legal** | 19 | Иски, претензии, e-discovery, CourtListener, docket watch |
| **privacy-legal** | 9 | GDPR, обработка данных, утечки, DPIA |
| **regulatory-legal** | 9 | Compliance, расследования, reg-change monitoring |
| **ai-governance-legal** | 10 | EU AI Act, оценка рисков ИИ-систем |
| **ip-legal** | 12 | Патенты, товарные знаки, лицензирование, renewal watch |
| **product-legal** | 7 | Terms of Service, EULA, privacy policy, launch review |

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
