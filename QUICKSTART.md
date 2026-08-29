# QUICSTART — Быстрый старт Vector Legal (Hermes Agent)

**60 секунд до первого навыка.**

## Установка в Hermes Agent

1. Клонировать репо (или скопировать нужные домены):

```bash
git clone https://github.com/Osmosy/vector-legal.git ~/projects/vector-legal
```

2. Подключить домен(ы) к агенту — Hermes читает SKILL.md из пути репо:

```bash
# Указать в config.yaml toolsets/skills пути, либо для текущей сессии:
# «Работай из ~/projects/vector-legal» — скиллы подгрузятся по запросу
```

3. **Запустить setup.** 2 минуты (quick) или 10–15 (full):

```
«Пройти cold-start интервью commercial-legal»
```

4. **Подключить правовой источник.** Citations без него помечаются
   «unverified». Сейчас РФ-источники работают через web_search
   (kad.arbitr.ru, pravo.gov.ru, КонсультантПлюс-free) с обязательными
   provenance-тегами. MCP-коннекторы к российским базам — в roadmap
   (см. CONNECTORS.md).

## User scope, не project scope

Устанавливать user-scope (все проекты), не project-scope: project scope
блокирует навыку чтение файлов вне папки проекта — договоров из Загрузок,
писем из Documents. Это counterintuitive, но user scope безопаснее
(настройки прав всё равно резают доступ к чужим файлам per-assignment).

## Какой домен ставить первым

| Если ты… | Начни с |
|---|---|
| in-house коммерческий / закупки | `commercial-legal` |
| privacy / комплаенс ПДн | `privacy-legal` |
| in-house корпоратив / M&A | `corporate-legal` |
| HR-юрист | `employment-legal` |
| судебная работа | `litigation-legal` |
| внедряешь ИИ в продукте/процессах | `ai-governance-legal` |
| следишь за НПА и регулятором | `regulatory-legal` |
| ИС / товарные знаки / OSS | `ip-legal` |
| запуск продуктов / реклама | `product-legal` |
| НКО / юрклиника | `legal-clinic` |
| студент / junior | `law-student` |
| работаешь сразу с несколькими | `legal-builder-hub: cold-start-interview` (рекомендует starter pack) |

## Что делает cold-start interview

Агент интервьюирует юриста и пишет **practice profile** — playbook,
извлечённый из ваших реальных подписанных договоров (не «рыночный
стандарт»). Все навыки домена читают профиль до какого-либо действия.
Without setup — **provisional mode** с метками `[PROVISIONAL]`.

## Требования

- Node 18+ (для Hermes), git
- Для РФ-источников: web_search backend с доступом из РФ (см. config `web.search_backend`); DeepSeek/Ollama-провайдер — работает без VPN

## Источник

Адаптация QUICKSTART.md из anthropics/claude-for-legal (Apache-2.0):
установка через Hermes вместо `/plugin marketplace`, РФ-специфика.