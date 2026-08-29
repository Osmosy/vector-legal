# Спецификация: полный перенос claude-for-legal → vector-legal

> Статус: draft v1.0 от 29.08.2026. Основа: аудит CFL @ master (151 SKILL.md,
> 12 плагинов + cookbooks + scripts) против текущего vector-legal (128 SKILL.md,
> 9 доменов + legacy skills/).
> Соответствие: delegation-gate-checklist (4 шлюза, 12 пунктов) — каждый
> следующий spawn прогоняет их письменно в YAML-контракте.

## 1. Что уже перенесено (phase 1, готово)

9 из 12 плагинов доменного уровня: commercial (13+check), privacy (9),
corporate (13), employment (20), litigation (19), ai-governance (10),
regulatory (9), ip (12), product (9). = 110 навыков + practice profiles +
cold-start интервью. RU-адаптация: ГК/ТК/АПК/КоаП/152-ФЗ, протоколы
разногласий, kad.arbitr/pravo.gov.ru вместо CourtListener/Federal Register.

Пробелы phase 1 (случайные сокращения против CFL-оригиналов):
- commercial: 13 vs 13 у CFL?? — нет: CFL 12, VL 13 (+vector-check) ✔
- legal-builder-hub: нет в VL (10 навыков инфраструктуры плагинов)

## 2. Чего НЕ перенесено из CFL (gap = 37 навыков + 5 групп ассетов)

### 2.1 law-student (13 навыков) — приоритет ВЫСОКИЙ
Обучение юристов: Socratic drilling, case brief, IRAC grading, flashcards,
bar-prep, exam forecast. Принцип плагина: «learning mode, not answer mode» —
навык структурирует мышление, никогда не пишет за студента.
RF-адаптация минимальна (учебные методики юрисдикция-нейтральны): IRAC,
case brief — по российским судебным актам; bar-prep → экзамен на статус
адвоката / магистратура. Кому: магистранты, стажёры, junior-юристы.

### 2.2 legal-clinic (16 навыков) — приоритет ВЫСОКИЙ
Юридические клиники (доступ к правосудию): intake, memo, client letter,
deadlines, semester-handoff, supervisor-review-queue. RF-адаптация:
бесплатная юрпомощь по ФЗ-324 «О бесплатной юридической помощи»,
юрклиники при вузах. Кому: НКО, юрклиники, прок-бонус.

### 2.3 legal-builder-hub (10 навыков) — приоритет СРЕДНИЙ
Инфраструктура плагинов: registry-browser, skill-installer, skills-qa,
auto-updater, related-skills-surfacer, disable/uninstall. Это «app store».
RF-адаптация: скан prompt-injection при установке чужих скиллов; источники —
GitHub-реестры; QA-фреймворк Legal Skill Design Framework. Специфично
полезно: в Hermes нет собственного «маркета навыков».

### 2.4 external_plugins/cocounsel-legal (deep-research) — SKIP
Обёртка над платным Westlaw Deep Research — в РФ недоступен и не нужен.
Вместо него: RF-эквивалент «legal-research-ru» (см. §3.3).

### 2.5 Repo-уровень (не навыки:

a) **managed-agent-cookbooks** (5 агентов, HIGH) — прямо мапятся в
Hermes cronjob: reg-monitor, renewal-watcher, diligence-grid, launch-radar,
docket-watcher. У каждого: agent.yaml (системпромпт + скиллы), leaf-workers
(только один с Write), steering-examples. В Hermes → cronjob c enabled_toolsets
+ delegation-gate YAML-контракт.

b) **references/** — company-profile-template.md (общий для всех плагинов),
dashboard-template.md (стандарт дашбордов с guardrail'ами) — перенести
дословно с RU-локализацией.

c) **scripts/** — validate.py, lint-tool-scope.py, orchestrate.py,
deploy-managed-agent.sh, test-cookbooks.sh. Перенести validate/lint
(адаптировать под Hermes-path), orchestrate — по выбору.

d) **Governance-файлы**: QUICKSTART.md (установка в Hermes вместо
marketplace), CONNECTORS.md (как публиковать RF-коннекторы: kad.arbitr,
ЕГРЮЛ, КонсультантПлюс-API), CONTRIBUTING.md, CODE_OF_CONDUCT.md, CLA.md —
простые копии с RU-адаптацией.

## 3. Новые навыки сверх CFL (RU-специфика)

3.1 **legal-research-ru** (замена cocounsel): правовой поиск по открытому
контурy — kad.arbitr (судебная практика), pravo.gov.ru (НПА), ЕГРЮЛ,
КонсультантПлюс-free источники. Процедура provenance-тегов обязательна.

3.2 **Проверки санкционного соответствия** (уже есть в vector-check) —
расширить на corporate-legal.

3.3 **Госпошлины-калькулятор** (литигация): ст. 333.21/333.22 НК — расчёт
по цене иска.

## 4. Спецификация execution

### 4.1 Work breakdown (Wave 2)

| # | Задача | Объём | Модель | Критерий приёмки (наблюдаемый) |
|---|---|---|---|---|
| W2-1 | law-student 13 навыков | ~1.6k строк | cheap* | 13 SKILL.md + README + CLAUDE.md; frontmatter 13/13 valid; нет Pitfalls-секций; RU-тело; Socratic-принцип сохранён |
| W2-2 | legal-clinic 16 навыков | ~2.2k | cheap* | 16 SKILL.md + README + CLAUDE.md; frontmatter 16/16; ФЗ-324-контекст; supervisor-review-gate сохранён |
| W2-3 | legal-builder-hub 10 навыков | ~1.8k | cheap | 10 SKILL.md + README + CLAUDE.md; scan-инжекция при установке; QA-фреймворк |
| W2-4 | cookbooks → cronjob-спеки (5 агентов) | ~600 | frontier | 5 папок cron-спеков с YAML-контрактами; leaf-workers с Write-только-у-одного; steering-events RU |
| W2-5 | references + QUICKSTART + CONNECTORS + governance | ~1k | cheap | 6 файлов RU; company-profile-template.md общий; dashboard-template с guardrails |
| W2-6 | legal-research-ru (новый, замена cocounsel) | ~400 | frontier | SKILL.md + README; работает в open-контур (kad.arbitr + pravo.gov.ru); provenance-теги |

*cheap = адаптация шаблона, не requiring юр-верификацию (контент методик
юрисдикция-нейтрален). frontier для W2-4/W2-6: требуется
процессуальная точность и работа с источниками.

### 4.2 4-gate контракты (по delegation-gate-checklist)

**W2-1 law-student** (пример):
```yaml
task_id: "SUB-20260829-001"
role: "адаптер плагина law-student"
intent: "перенос учебного плагина CFL на RU и Hermes для магистрантов/юниоров"
inputs:
  data_slice: "CFL law-student (13 SKILL.md + README + CLAUDE.md); эталон commercial-legal"
permissions:
  mode: "least_privilege"
  allow: ["read:/tmp/cfl-audit", "write:vector-legal/law-student/**"]
  deny: ["send:external", "git:commit", "git:push", "read:full_dataset"]
  expires_at: "2026-08-29T23:59:59+03:00"
model_routing:
  selected_endpoint: "cheap"
  reason: "адаптация шаблона с заменой институциональной специфики; юр-верификация не требуется (методика юрисдикция-нейтральна)"
  via: "hermes_delegate_task"
verification:
  acceptance: "13 SKILL.md в skills/*/ + README.md + CLAUDE.md; каждый: frontmatter (---, name=dirname, description ≤1024 с 'Используй при', argument-hint), тело на русском, 0 секций Pitfalls, Socratic-принцип виден; контроль скриптом frontmatter-check"
  method: "schema_check (frontmatter-валидатор) + spot-read 3 файла"
escalation:
  on_ambiguous: "challenge_delegator"
  human_when: "спорная институциональная замена (напр. bar exam модель)"
constraints:
  max_hops: 1
  no_full_context_forward: true
```

W2-2, W2-3 — аналогично c другими списками и объёмами.
W2-4 cookbooks — frontier, т.к. процессуальная точность + cron-специфика.
W2-6 legal-research-ru — frontier (норм-верификация, kad.arbitr — сложный).

### 4.3 Verification method

- **schema_check:** python-валидатор frontmatter (уже есть) на каждый 
  SKILL.md + структурный чек (README, CLAUDE.md на месте, skills/<name>/ 
  соответствует CFL-набору)
- **spot-read:** 3 случайных файла на рус., отсутствие Pitfalls,
  Socratic/cold-start-принцип
- **cross-check:** число навыков = CFL-набору (± documented deviations)

### 4.4 Порядок и параллелизм

Волна 2a (параллельно, 3 субагента): W2-1, W2-2, W2-3.
Волна 2b (после приёмки 2a): W2-5 (небольшая, дешёвая), W2-4 + W2-6 (frontier).

## 5. Definition of Done (для всего переноса)

- Каждый плагин CFL присутствует в VL (12/12), включая 4 новых
- Repo-уровень: README, QUICKSTART, CONNECTORS, CONTRIBUTING, CLA,
  COC, references/, scripts/ (адаптированные), managed-agent-cookbooks →
  cron-спеки
- Все SKILL.md валидны; 0 Pitfalls-секций; RU-адаптация по домену
- Каждому домену — practice profile + cold-start interview
- Не нарушены паттерны commercial-legal (эталон)
- Пуш по явной просьбе

## 6. Внеплановое (задокументировано, не переносим)

- Westlaw/CoCounsel Deep Research — недоступен в РФ, замена legal-research-ru
- AP2/UCP-протоколы — раздел 6 бумаги; для Hermes сейчас нерелевантно
  (нет крипто-эскроу), вернуться при развитии протоколов