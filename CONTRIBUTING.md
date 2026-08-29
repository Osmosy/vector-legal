# CONTRIBUTING — как контрибьютить в Vector Legal

## Что принимать

- **Адаптация существующих навыков** под отрасль или регион (с сохранением
  RU-права или добавлением новой юрисдикции по нашему паттерну)
- **Новые навыки** в доменах — по структуре существующих
- **MCP-коннекторы** к российским правовым источникам (см. CONNECTORS.md)
- **Исправления норм** — с указанием первоисточника (pravo.gov.ru,
  КонсультантПлюс) в description PR
- **Переводы** — RU-тело обязательно, EN-версии welcome как файлы
  `README.en.md`

## Чего не принимать

- Навыки, дублирующие существующие (сначала `rg "name:" <domain>/skills/`)
- Навыки с US-институтами без RF-замены (work product, deposition, non-compete
  для сотрудников — у нас своя система норм)
- Навыки с секциями «## Pitfalls» — знания о сбоях вплетаются в тело как
  корректная процедура (см. правило в `software-development:delegation-gate-checklist`)
- Навыки без provenance-тегов и дисклеймера для юриста

## Формат SKILL.md (обязателен)

```yaml
---
name: <skill-name>                        # = имени каталога, lowercase-hyphen
description: >
  Используй при <триггер-класс>. <Одно предложение — что делает>.
  RF-специфика: <нормы, если применимо>.
argument-hint: '<что передать>'
user-invocable: true|false                # false — reference skills
---

# /<skill-name>

## Matter context

Проверить `## Matter workspaces` в practice profile ... (для firm)

---

## Destination check

Канонический текст — practice profile → Shared guardrails → Destination check.

## Purpose
## Workflow
## Quality checks
```

Требования к телу:
- Русский язык, примеры из практики РФ
- Нормы с указанием статьи (ст. X ГК / ТК / АПК / 152-ФЗ / КоАП)
- Provenance-теги: `[kad.arbitr.ru]`, `[pravo.gov.ru]`, `[КонсультантПлюс]`,
  `[user provided]`, `[model knowledge — verify]`, `[settled — подтверждено
  YYYY-MM-DD]`
- `⚠️ Reviewer note` одним блоком над deliverable
- Decision tree «Что дальше?» после анализа
- Дисклеймер «черновик для проверки юристом» — для исходящих документов

## Процесс

1. Fork + branch от master (`feature/<domain>-<skill>`)
2. Проверить фронтматтер локально:
   ```python
   import yaml, re, pathlib
   s = pathlib.Path('SKILL.md').read_text()
   m = re.search(r'\n---\s*\n', s[3:])
   fm = yaml.safe_load(s[3:m.start()+3])
   assert fm['name'] == '<dirname>'
   assert len(str(fm['description'])) <= 1024
   ```
3. PR с описанием: что добавляет, какие домены затрагивает, источник норм.
4. Проверка мейнтейнером: frontmatter, RU-язык, нормы РФ, отсутствие
   дублирования. Дизайн-ревью: соответствует ли Legal Skill Design
   Framework (см. `legal-builder-hub/skills/skills-qa`).

## Структура репо

- `<domain>/skills/<skill-name>/SKILL.md` — навыки
- `<domain>/CLAUDE.md` — шаблон practice profile домена
- `<domain>/README.md` — обзор домена
- `references/` — общие шаблоны (company profile, dashboard)
- `managed-agent-cookbooks/` — cron-спеки агентов мониторинга
- `SPECIFICATION-cfl-transfer.md`, `domains-status.md` — план и статусы

## Лицензия

Apache-2.0. Каждому PR — DCO sign-off (`git commit -s`).