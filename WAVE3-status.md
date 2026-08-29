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

## Осталось: B1–B5 делегировать на DeepSeek direct + ZCode GLM-5.3

| Задача | Модель | Объём | Acceptance |
|---|---|---|---|
| B1 deep cold-start × 4 домена | GLM-5.3 (frontier) | 4 файла по 1-2KB | ≥30 вопросов, frontmatter OK |
| B2 Destination check + provenance | GLM-5.3-Flash | 15 lit + 9 comm | Каждый файл с блоком |
| B3 Reviewer note + decision tree | GLM-5.3-Flash | 15 файлов | Дублирование блоков |
| B4 ai-gov deep cold-start | GLM-5.3 | ratio > 0.7 | 30+ вопросов, shadow-AI есть |
| B5 corporate/ai-tool-handoff RU | GLM-5.3-Flash | ≥3 RF-нормы | 3 RF ссылки в теле |

Модель приоритета: **GLM-5.3-Flash** (cheap) на B2/B3/B5 (адаптация),
**GLM-5.3** (frontier) на B1/B4 (reasoning).

Все задачи делегируются через `delegate_task` с `model='zai/glm-5.3-flash|glm-5.3'` —
Coding Plan официально поддерживает Hermes Agent (см. docs.z.ai/devpack/tool/others).

## Известные ограничения

- ZCode Coding Plan ограничивает concurrent requests в зависимости от tier
- 152-ФЗ-нормы корректно вплетены только в домены RF (не в law-student /
  legal-builder-hub / legal-research-ru)
- Стадийные пороги (штрафы, ФАС, ЭПР) — везде [verify], сверять с pravo.gov.ru