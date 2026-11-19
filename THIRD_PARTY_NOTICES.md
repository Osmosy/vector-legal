# Third-party notices

## anthropics/claude-for-legal (Apache License 2.0)

Репозиторий Vector Legal — русскоязычная адаптация открытого проекта
[anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal)
(Apache License 2.0, Copyright Anthropic PBC). Апстрим распространяется с
файлом `LICENSE` (Apache-2.0) и **без** файла `NOTICE`, поэтому обязанность
§4(d) Apache-2.0 (перенос NOTICE) не возникает. Применяются §4(a) — передать
получателю копию лицензии, §4(b) — поместить в каждый изменённый файл
уведомление о том, что файл изменён, и §4(c) — сохранить уведомления об
авторстве из исходной формы.

**Что взято.** Структура доменов и 148 навыков, совпадающих по пути с
апстримом (`<domain>/skills/<name>/SKILL.md`). Точный перечень —
`docs/upstream-skills.txt`. На 19.11.2026: в апстриме 151 навык, в этом
репозитории 156 (без учёта `skills/cowork-roles/`), совпадение по пути — 148.

**Текст лицензии приложен.** Полный текст Apache License 2.0 —
`LICENSES/Apache-2.0.txt` (§4(a): получатель производной работы должен
получить копию лицензии).

**Что изменено (§4(b)).**

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

**Как выглядит атрибуция.** В каждом из 148 перенесённых навыков (перечень —
`docs/upstream-skills.txt`) последней строкой стоит уведомление:
«Адаптировано из anthropics/claude-for-legal (Apache-2.0, Anthropic);
изменения — Osmosy». Это закрывает §4(b) построчно, а не только общим файлом.
Дополнительно: копия лицензии — `LICENSES/Apache-2.0.txt` (§4(a)), описание
изменений — раздел выше (§4(c) требует сохранять уведомления, а не создавать
их; собственных копирайт-строк в файлах апстрима нет — проверено на
`commercial-legal/skills/review/SKILL.md`).

## Материалы, которые НЕ используются

Навыки z.ai (`autoclaw-skills`, раздел 17 Russia в
`docs.z.ai/guides/legal-mcp`) в репозиторий не копируются и не
пересказываются дословно: в архивах нет файла лицензии, на странице
документации лицензия не указана, уведомление об авторстве присутствует лишь
в одном файле из шести проверенных. Набор используется исключительно как
перечень тем — разбор в `docs/zai-gap-analysis.md`.
