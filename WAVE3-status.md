# Vector Legal — Wave 3 статус

> 29.08.2026 — план + выполнение статусов по приёму.

## A1 ✅ Переключить Hermes на прямой DeepSeek

- Model: `deepseek-chat` / `deepseek-v4-flash`
- base_url: `https://api.deepseek.com/v1` (минуя ollama-launch)
- api_key_env: DEEPSEEK_API_KEY (есть в ~/.hermes/.env)
- Context: 128 000 токенов
- Backup: ~/.hermes/config.yaml.bak.<timestamp>
- Test: `ping` → 200 OK, модель deepseek-v4-flash отвечает

## A2 ✅ Подключить ZCode GLM-5.3-Flash как second provider

- Provider блок в config.yaml: providers.zai (kind: anthropic)
- base_url: https://api.z.ai/api/anthropic
- api_key_env: ZAI_API_KEY (добавлен в ~/.hermes/.env из ZCode config)
- Модели: glm-5.3-flash, glm-5.3
- Тест: `ping` → GLM-5.3-Flash → `pong` 200 OK

## B1 ✅ Deep cold-start-interview × 4 домена (коммит 4d2808e)

| Домен | Строк | Вопросов | Acceptance |
|---|---|---|---|
| regulatory | 729 | 47 | ≥30 вопросов — ✅ |
| litigation | 981 | 67 | ≥30 вопросов — ✅ |
| ai-governance | 949 | 74 | ≥30 вопросов — ✅ |
| commercial | 1081 | 92 | ≥30 вопросов — ✅ |

RU-адаптация (Диадок/СБИС/КонсультантПлюс, юрисдикция АС/СОЮ/СИПН) — во всех 4.
Frontmatter валиден, ratio к CFL > 1.

## B2 ✅ Destination check + provenance (коммит 5143609)

- Destination check в litigation: 18 файлов (ожидалось 15) — ✅
- Provenance-теги в 9 commercial-файлах: amendment-history, customize,
  escalation-flagger, matter-workspace, renewal-tracker, review,
  review-proposals, stakeholder-summary, vector-check — ✅
- Проверено grep-паттерном scripts/validate.py

## B3 ✅ Reviewer note / decision tree (коммит 5143609)

- 17/20 litigation-файлов с Reviewer note + decision tree
- nda-review, vendor-agreement-review — оба блока добавлены
- pia-generation — decision tree добавлен
- Стиль согласован с образцами домена

## B4 ✅ ai-governance deep cold-start (коммит 4d2808e)

- Shadow-AI discovery — есть (cold-start, строка 371)
- 74 вопроса, per-system roles, red-lines
- Ratio > 0.7 к CFL — ✅

## B5 ✅ corporate/ai-tool-handoff RU-нормы (коммит 5143609)

- 152-ФЗ: ч. 3 ст. 6, ст. 9, ч. 5 ст. 18, ст. 18.1, ст. 22 — [pravo.gov.ru]
- ФЗ-187 КИИ: ст. 7 (категорирование), ст. 9/10, ст. 13 (ФСТЭК) — сверено
  с первоисточником (КонсультантПлюс)
- ГОСТ Р 59276-2020 «Системы ИИ. Способы обеспечения доверия» — название
  сверено с каталогом Росстандарта (действует)
- Acceptance «≥3 RF-нормы» — ✅ (9 упоминаний)

## C1 ✅ CI инфраструктура (коммит 5143609)

- validate.py: флаги `--strict` / `--warnings` (errors fail / warnings report-only)
- .github/workflows/validate.yml: job'ы разделены (frontmatter-errors,
  ru-lint-warnings, no-pii)
- .pre-commit-config.yaml: pii-scan, validate-skills, placeholder-hygiene

## C2 ✅ README roadmap удалён (коммит 5143609)

- Раздел «Домены (roadmap)» устарел (все домены адаптированы) — удалён

## C3 ✅ agent-description.md переписан (коммит 5143609)

- Формат Vector Agent-Ready (слой 4): что это, как устроено, как читать агенту

## Валидация

- `python3 scripts/validate.py` → PASS (warnings only), 0 errors
- PII-скан: чисто

## Известные ограничения

- ZCode Coding Plan ограничивает concurrent requests в зависимости от tier
- 152-ФЗ-нормы корректно вплетены только в домены RF (не в law-student /
  legal-builder-hub / legal-research-ru)
- Стадийные пороги (штрафы, ФАС, ЭПР) — везде [verify], сверять с pravo.gov.ru
