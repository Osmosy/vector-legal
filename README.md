<div align="center">

<img src="assets/vector-logo.png" alt="Vector Legal" width="200"/>

# Vector Legal

**Юридический AI-департамент для Hermes Agent — 9 доменов российского права
на базе скелета Claude-for-Legal (Anthropic).**

[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue.svg)](https://github.com/NousResearch/hermes-agent)
[![Domains: 9](https://img.shields.io/badge/Domains-9-green.svg)](#домены)
[![Skills: 128](https://img.shields.io/badge/Skills-128-blue.svg)]()
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

</div>

---

Юридический AI-департамент: все 9 доменов
[Claude-for-Legal](https://github.com/anthropics/claude-for-legal) (Anthropic,
151 навык) адаптированы под **российское право** (ГК РФ, 152-ФЗ, ТК РФ, АПК,
КоАП, ФЗ-115, ФЗ-135, ФЗ-38) и Hermes Agent, с расширениями для российской
практики.

**Архитектура, перенесённая из CFL:** каждый домен работает через **practice
profile** — файл практики, который пишет cold-start interview (агент
интервьюирует юриста, извлекает playbook из реальных подписанных договоров).
До настройки навыки работают в provisional mode с метками `[PROVISIONAL]`.
Provenance-теги обязательны: `[kad.arbitr.ru]` / `[pravo.gov.ru]` /
`[КонсультантПлюс]` / `[user provided]` / `[model knowledge — verify]`.

**Все выходные данные — черновики для проверки юристом.** Не юридическая
консультация, не позиция Anthropic или Osmosy.

## Домены (все адаптированы)

| Домен | Навыков | RF-ядро |
|-------|---------|---------|
| **commercial-legal** | 13+check | ГК (15/330/401/425/452), протоколы разногласий, 152-ФЗ в закупках |
| **privacy-legal** | 9 | 152-ФЗ: поручения ст. 6, запросы субъектов 30 дней, оценка вреда ст. 18.1, ТИПЗ ФСТЭК №21, трансграничка ст. 12+№931, утечки 24/72ч, КоАП 13.11 |
| **corporate-legal** | 13 | ФЗ-14/208: крупные сделки, протоколы ст. 181.2 ГК, нотариат долей, ЕГРЮЛ-комплаенс |
| **employment-legal** | 20 | ТК РФ: закрытый перечень ст. 81 (ат-вилл не работает), сокращения, ГПХ-vs-трудовой (Пленум ВС №15), ЛНА |
| **litigation-legal** | 19 | АПК/ГПК: досудебный порядок ч. 5 ст. 4, kad.arbitr, сроки 1м/2м/3м, допрос ст. 88, обеспечение ст. 72 |
| **ai-governance-legal** | 10 | ЭПР ИИ ФЗ-123 [verify], ГОСТ Р 59276/ИСО 23894, EU AI Act для экспорта |
| **regulatory-legal** | 9 | pravo.gov.ru монитор, гильотина ПП №1128, 44/223-ФЗ, ФАС |
| **ip-legal** | 12 | Роспатент/ФИПС, ГК ч. 4, СИПН, OSS (AGPL-triggers) |
| **product-legal** | 9 | ФЗ-38 реклама + ЕРИР, ЗоЗПП, оферта ст. 437/428, Честный ЗНАК |

## Быстрый старт

```bash
git clone https://github.com/Osmosy/vector-legal.git
# В Hermes: укажи путь к домену и запусти cold-start interview:
#   «Пройти cold-start интервью commercial-legal»
```

Каждый домен: `<domain>/README.md` — описание и таблица навыков;
`<domain>/CLAUDE.md` — шаблон practice profile.

Статусы, план и принцип адаптации: [domains-status.md](domains-status.md).

## Домены (roadmap)

> Раздел ниже — исторический план; все 9 доменов уже адаптированы (таблица
> выше). Roadmap дальнейшего (углубление доменов, MCP-коннекторы РФ-систем):
> [domains-status.md](domains-status.md).

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
