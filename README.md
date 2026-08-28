<div align="center">

<img src="assets/vector-logo.png" alt="Vector Legal" width="200"/>

# Vector Legal

**Юридический AI-департамент для Hermes Agent — российское право на базе
скелета Claude-for-Legal.**

[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue.svg)](https://github.com/NousResearch/hermes-agent)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

</div>

---

Юридический AI-департамент: домен-за-доменом адаптируется из
[Claude-for-Legal](https://github.com/anthropics/claude-for-legal) (Anthropic,
151 навык, 12 плагинов) под **российское право** (ГК РФ, 152-ФЗ, ТК, АПК,
КоАП) и Hermes Agent.

Статус всех доменов: [domains-status.md](domains-status.md).

## Готово: commercial-legal (пилот, 15 навыков)

`commercial-legal/` — полный домен: practice profile + cold-start interview +
12 workflow-навыков. Ревизия договоров против playbook компании, NDA-триаж
GREEN/YELLOW/RED, SaaS-подписки, реестр продлений, эскалации, протоколы
разногласий. Быстрый старт — [commercial-legal/README.md](commercial-legal/README.md).

Ключевая механика (перенесена из CFL): договор разбирается против **playbook
вашей команды**, извлечённого из ваших же подписанных договоров через
cold-start interview — не против абстрактного «рыночного стандарта». До
настройки навыки работают в provisional mode с метками `[PROVISIONAL]`.

**Все выходные данные — черновики для проверки юристом.** Не юридическая
консультация. Источники указываются явно, provenance-теги обязательны.

## Домены (roadmap)

Полная таблица статусов и план: [domains-status.md](domains-status.md).

| Домен | Статус | Замена США → РФ |
|-------|--------|-----------------|
| **commercial-legal** | ✅ готов (15 навыков) | договоры поставки/услуг, ГК, 152-ФЗ, протоколы разногласий |
| privacy-legal | next | 152-ФЗ вместо GDPR, оценка воздействия по модельным условиям РКН |
| corporate-legal | план | ФЗ об ООО/АО, entity compliance ФНС/ЦБ |
| employment-legal | план | ТК РФ, увольнения по ст. 81, ГПХ-vs-трудовой |
| litigation-legal | план | АПК/ГПК, kad.arbitr.ru вместо CourtListener |
| ai-governance-legal | план | ЭПР ИИ, ГОЗ-ограничения, EU AI Act для экспорта |
| regulatory-legal | план | pravo.gov.ru монитор, 44-ФЗ/223-ФЗ |
| ip-legal | план | Роспатент/ФИПС, ГК ч. 4 |
| product-legal | план | оферта, ФЗ-38 «О рекламе», ЗоЗПП |

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
