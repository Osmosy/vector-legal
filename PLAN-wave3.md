# План доработки Vector Legal — Wave 3

> Дата: 29.08.2026 · Контекст: Ollama квота 77.6% сессии, до сброса ~3 ч.
> План — приоритированы, каждая задача имеет наблюдаемый критерий приёмки
> (по delegation-gate-checklist).

## Приоритет A — критично (выполнить today, 29.08 до сброса Ollama)

### A1. Переключить Hermes на прямой DeepSeek (bypass Ollama)

**Зачем:** сохранить остаток Ollama-квоты, получить доступ к DeepSeek V4
с более длинным контекстом.

```yaml
agent:
  model:
    default: deepseek-v4-chat      # или glm-5.3-flash:cloud
    provider: deepseek
    api_key_env: DEEPSEEK_API_KEY
    base_url: https://api.deepseek.com/v1
    context_length: 128000
```

**Acceptance:** `hermes config show` показывает `provider: deepseek`,
тестовый запрос уходит напрямую в DeepSeek (не через Ollama), exit 0.

**Время:** 5 мин.

### A2. Подключить ZCode GLM-5.3-Flash как second provider (300M ток до 31.08)

**Зачем:** GLM-5.3-Flash даёт 300M ток в день, а DeepSeek может жечь платно.
Для дотяжки 65 сокращений по Vector Legal — идеальный вариант: frontier-class
reasoning (GLM-5.3) на reasoning-heavy задачах, Flash на переформатирование.

1. Экспортировать `ZAI_API_KEY` из `~/.zcode/v2/config.json` в `~/.hermes/.env`
2. Добавить в `~/.hermes/config.yaml`:
   ```yaml
   providers:
     zai:
       kind: anthropic
       base_url: https://api.z.ai/api/anthropic
       api_key_env: ZAI_API_KEY
       model: glm-5.3-flash
   ```
3. Проверить: `hermes mcp` → zai provider enabled
4. Тестовый запрос через `delegate_task(model='zai/glm-5.3-flash', ...)`

**Acceptance:** запрос к `zai/api/anthropic/v1/messages` возвращает 200,
модель `glm-5.3-flash` доступна через delegate_task.

**Gate 4:** ZCode Coding Plan официально поддерживает Hermes Agent
(см. docs.z.ai/devpack/tool/others#step-2-general-purpose-agent-tool →
Hermes Agent listed).

---

## Приоритет B — дотяжка Vector Legal по RETRO-AUDIT-phase1 (65 нарушений)

> Делегировать на ZCode GLM-5.3-Flash / DeepSeek V4 (не через Ollama).
> Массовые прогоны — по 10-20 навыков за один delegate_task, чтобы
> соответствовать quota. Каждая задача — с 4-шлюзовым YAML-контрактом
> (см. skill delegation-gate-checklist).

### B1. Deep cold-start-interview в 4 доменах

- Domain: commercial, litigation, regulatory, ai-governance
- Status: ip-legal уже дотянут, остальные — ratio 0.15-0.19
- Что добавить: формулировки вопросов verbatim + RU-адаптация
  (интеграции Диадок/СБИС/КонсультантПлюс, юрисдикция АС/СОЮ/СИПН)
- Acceptance: каждый cold-start ≥30 явно сформулированных вопрос-фраз,
  фронтматтер валиден
- Модель: frontier (GLM-5.3 / DeepSeek V4)
- Объём: 4 домена × ~45K в среднем = ~180K ток вход + ~150K выход
- Время: ~1-2 часа

### B2. Destination check в 15 litigation-файлах + provenance в commercial

- 15 файлов litigation: добавить `## Destination check` блок (или ссылку
  на practice profile Shared guardrails)
- 9 файлов commercial: добавить по 1-2 provenance-тега в тело
- Модель: cheap (Flash / dsh-browser + GLM-5.3-Flash)
- Acceptance: каждый файл содержит `Destination check` + ≥1 provenance-тег

### B3. Reviewer note / decision tree в 15 файлах
- Дублировать блоки из practice profile в телах навыков, где CFL-оригинал
  имел их, а VL — нет
- Файлы: (список в RETRO-AUDIT-phase1.md §4.9)

### B4. ai-governance deep cold-start
- Дотянуть 30+ вопросов, Shadow-AI уже добавлен (bcbf8e9), добавить
  regulatory-footprint (Colorado/BIPA → РФ-контур 152-ФЗ/187-ФЗ)
- Модель: frontier
- Acceptance: ratio > 0.7 к CFL, содержит shadow-AI discovery,
  per-system roles, red-lines

### B5. corporate/ai-tool-handoff RU-нормы (borderline ratio 0.79)
- Добавить 152-ФЗ, ФЗ-187 КИИ, ГОСТ 59276
- Acceptance: ≥3 reference RF-нормы в теле

---

## Приоритет C — инфраструктура репо (доработка)

### C1. GitHub Actions усовершенствовать
- Разделить ru-lint на errors (fail) / warnings (not fail)
- Подключить pre-commit hooks для PII-скана

### C2. README.md «Домены (roadmap)» — удалить
- Раздел outdated (все 9 уже адаптированы), таблица «Домены» вверху —
  актуальна

### C3. agent-description.md переписать
- Текущий — 5 строк заглушка; переписать в формате Vector Agent-Ready
  (layer 4: AGENTS.md уже есть, нужен README для агента)

---

## Порядок выполнения

1. A1 переключение провайдера (5 мин)
2. A2 ZCode GLM-5.3-Flash как second provider (10 мин)
3. B1 → B2 → B4 → B3 → B5 — делегировать на GLM-5.3-Flash (не через Ollama)
4. Валидация (validate.py — должен быть 0 errors)
5. Финальный коммит + пуш по явной команде

**Ограничение:** не делать MCP-интеграции (отложено пользователем).