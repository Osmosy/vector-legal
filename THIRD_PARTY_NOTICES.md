# Third-party notices

## anthropics/claude-for-legal (Apache License 2.0)

Репозиторий Vector Legal — русскоязычная адаптация открытого проекта
[anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal)
(Apache License 2.0, Copyright Anthropic PBC). Апстрим распространяется с
файлом `LICENSE` (Apache-2.0) и **без** файла `NOTICE`, поэтому обязанность
§4(d) Apache-2.0 (перенос NOTICE) не возникает; применяются §4(b) — сохранять
уведомления об авторстве — и §4(c) — фиксировать факт изменений.

**Что взято.** Структура доменов и 148 навыков, совпадающих по пути с
апстримом (`<domain>/skills/<name>/SKILL.md`). Точный перечень —
`docs/upstream-skills.txt`. На 19.11.2026: в апстриме 151 навык, в этом
репозитории 156 (без учёта `skills/cowork-roles/`), совпадение по пути — 148.

**Текст лицензии приложен.** Полный текст Apache License 2.0 —
`LICENSES/Apache-2.0.txt` (§4(a): получатель производной работы должен
получить копию лицензии).

**Что изменено (§4(c)).**

- тело навыков переписано на русском языке под право РФ (ГК, АПК, ГПК,
  152-ФЗ, 98-ФЗ, ТК и др.), ссылки на нормы США и западные базы заменены;
- введены обязательные provenance-теги (`AGENTS.md` §3) и правило
  проверки цитат против первоисточника;
- MCP-коннекторы и интеграции заменены на российские источники
  (`CONNECTORS.md`, `CONNECTORS-ru-mcp.md`);
- добавлены practice profiles, `scripts/validate.py`, `scripts/cron_sync_check.py`
  и тесты `tests/`, которых в апстриме нет;
- имена навыков и структура каталогов сохранены для совместимости.

**Собственные навыки репозитория** (в апстриме отсутствуют, написаны с нуля):
`commercial-legal/skills/vector-check`, `legal-research-ru`,
`litigation-legal/skills/patent-claim-chart`,
`product-legal/skills/privacy-policy-ru`,
`product-legal/skills/terms-of-service-ru`, `skills/api-tokens-in-chat`.

**Не перенесено из апстрима:** `external_plugins/cocounsel-legal/skills/deep-research`,
`legal-clinic/skills/form-generation`, `legal-clinic/skills/plain-language-letters`.

## Лицензионная позиция репозитория

Код и тексты этого репозитория распространяются по MIT (`LICENSE`,
Copyright (c) 2026 Osmosy). Apache-2.0 на репозиторий целиком не переносится:
адаптированные из апстрима файлы остаются под Apache-2.0, их перечень —
`docs/upstream-skills.txt`, текст лицензии — `LICENSES/Apache-2.0.txt`;
остальное — MIT. Подробнее — `AGENTS.md`, раздел «Лицензия».

**Как выглядит атрибуция фактически.** Уведомление об авторстве Anthropic
сейчас стоит в четырёх навыках (`*/skills/cold-start-interview/SKILL.md`,
строка «Против CFL-оригинала (anthropics/claude-for-legal, Apache-2.0)») и в
этом файле. В остальных перенесённых навыках построчной ссылки нет — она
даётся централизованно: этот файл + `docs/upstream-skills.txt` +
`LICENSES/Apache-2.0.txt`. Причина: файлы апстрима сами по себе не содержат
копирайт-строк (проверено на `commercial-legal/skills/review/SKILL.md` —
только frontmatter и тело), поэтому сохранять построчные уведомления не
требуется, а требование §4(c) «отметить изменения» закрыто разделом «Что
изменено» выше.

## Материалы, которые НЕ используются

Навыки z.ai (`autoclaw-skills`, раздел 17 Russia в
`docs.z.ai/guides/legal-mcp`) в репозиторий не копируются и не
пересказываются дословно: в архивах нет файла лицензии, на странице
документации лицензия не указана, уведомление об авторстве присутствует лишь
в одном файле из шести проверенных. Набор используется исключительно как
перечень тем — разбор в `docs/zai-gap-analysis.md`.
