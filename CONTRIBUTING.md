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
2. Прогнать проверки локально (то же, что в CI):
   ```bash
   python3 scripts/validate.py            # фронтматтер и структура SKILL.md
   python3 scripts/validate.py --claims   # лицензия и числа против дерева
   python3 tests/test_claims.py           # тесты самих проверок
   ```
   Или одной командой: `pre-commit run --all-files`.
3. Если добавляете навык или меняете состав домена — обновите числа в
   документах. `--claims` сверяет их с деревом (бейдж `Skills-N`, шапки
   README/AGENTS/agent-description, `skills/ # N` в доменных README) и упадёт
   при расхождении: правьте цифры, а не проверку. Заявление о лицензии
   (`Адаптация © Osmosy, <лицензия>`) сверяется с файлом `LICENSE`.
4. PR с описанием: что добавляет, какие домены затрагивает, источник норм.
5. Проверка мейнтейнером: frontmatter, RU-язык, нормы РФ, отсутствие
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

Код и тексты этого репозитория — **MIT** (файл `LICENSE`, © 2026 Osmosy).
Адаптации из [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal)
сохраняют атрибуцию Anthropic: у апстрима лицензия Apache-2.0, на этот
репозиторий она не переносится. Указывайте лицензию так же, как в `LICENSE` —
иначе упадёт `python3 scripts/validate.py --claims`.

Каждому PR — DCO sign-off (`git commit -s`).