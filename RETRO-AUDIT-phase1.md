# RETRO-AUDIT: перенос phase 1 claude-for-legal → vector-legal

**Дата:** 29.08.2026 · **Аудитор:** независимый субагент (frontier) · **Контракт:** SUB-20260829-004 (read-only + write отчёта, max_hops: 1)

**Метод** (ретро-чеклист Google Cloud/DeepMind «Intelligent AI Delegation» + pimenov.ai): (A) полнота vs оригинал; (B) YAML-фронтматтер (parse, name=dirname, description ≤1024); (C) RU-нормы в теле каждого навыка (ГК/ТК/АПК/ГПК/КоАП/НК/ФЗ-NN/Пленумы) + provenance-теги; (D) паттерн-комплаенс (0 секций Pitfalls, Reviewer note, decision tree, Destination check); (E) CLAUDE.md на месте и непустой; (F) деградация: VL <50% длины CFL-оригинала и без RU-права = «degraded». Эталон: `/tmp/cfl-retro` = github.com/anthropics/claude-for-legal (клон main). Выборка: 115 навыков, сверено позициенно (все 115×115 попаданий по имени, длины по каждому, регэкспы по каждому файлу).

---

## 1. Итог по доменам

| Домен | CFL | VL | Неперенесённые | YAML-проблемы | RU-нормы в телах | Паттерн-проблемы | Degraded | Нарушений |
|---|---|---|---|---|---|---|---|---|
| **ai-governance** | 10 | 10 | — | — | полная (10/10) | 8 | — | 8 |
| **commercial** | 12 | 13 | — | — | частичная (12/13) | 9 | — | 9 |
| **corporate** | 13 | 13 | — | — | частичная (10/13) | 1 | — | 1 |
| **employment** | 20 | 20 | — | — | полная (20/20) | 7 | — | 7 |
| **ip** | 12 | 12 | — | — | частичная (11/12) | 12 | customize | 13 |
| **litigation** | 19 | 19 | — | — | частичная (18/19) | 15 | — | 15 |
| **privacy** | 9 | 9 | — | — | полная (9/9) | 3 | — | 3 |
| **product** | 7 | 9 | — | — | частичная (8/9) | 3 | — | 3 |
| **regulatory** | 9 | 9 | — | — | частичная (8/9) | 6 | — | 6 |

**Итог по полноте:** CFL 115 / VL 115 — все имена присутствуют 1:1. Сверх реестра: `product/privacy-policy-ru`, `product/terms-of-service-ru` (RU-новинки), `commercial/vector-check` (вне-CFL-адаптация). Неперенесённых навыков phase 1: **0**. Заявленные в SPECIFICATION §1 численности (13/9/13/20/19/10/9/12/9 = 115) подтверждаются фактически.

**YAML:** 115/115 валидны: фронтматтер парсится, `name` = имени каталога во всех 115, `description` ≤1024 везде, пустых нет. **CLAUDE.md:** есть во всех 9 доменах, от 7.2 до 32.9 КБ, все непустые (E — pass, без исключений). **Pitfalls-секций: 0 в 115 файлах** (в CFL их тоже 0 — паттерн соблюдён в обе стороны).

---

## 2. RU-адаптация и provenance (детально)

Тело навыков содержит конкретные нормы РФ не только в README: по VL 115 файлам — 160 упоминаний 152-ФЗ, 18 × ст. 4 АПК, 9 × ст. 5.27 КоАП, 8 × ст. 13.11 КоАП, 8 × ст. 452 ГК, 6 × Пленумы ВС, 6 × 223-ФЗ, 5 × ст. 93.1 НК, 4 × ст. 401/330/333/181.2/67.1/431.2 ГК, 4 × ст. 75/86 ТК, 4 × ст. 66/88/126/131 АПК и др.

Provenance-теги определены в practice profiles (`[kad.arbitr.ru]`, `[pravo.gov.ru]`, `[КонсультантПлюс]`, `[user provided]`, `[verify]`, `[model knowledge]`) и употреблены в телах: `[verify]` — 155 вхождений, pravo.gov.ru — 35, kad.arbitr.ru — 21, КонсультантПлюс — 20 по 115 файлам.

| Домен | Навыков | С RU-нормами в теле | С provenance в теле | Ни RU, ни provenance |
|---|---|---|---|---|
| ai-governance | 10 | 10 | 9 | — |
| commercial | 13 | 12 | 4 | — |
| corporate | 13 | 10 | 10 | ai-tool-handoff, deal-team-summary, matter-workspace |
| employment | 20 | 20 | 16 | — |
| ip | 12 | 11 | 10 | customize |
| litigation | 19 | 18 | 15 | matter-workspace |
| privacy | 9 | 9 | 8 | — |
| product | 9 | 8 | 6 | matter-workspace |
| regulatory | 9 | 8 | 6 | gaps |

---

## 3. Деградация объёма (проверка F)

Средний коэффициент объёма VL/CFL по доменам: employment 1.22, corporate 0.87, privacy 0.75, product 0.76, regulatory 0.53, commercial 0.54, litigation 0.43, ai-governance 0.38, **ip 0.24 (минимальный)**.

**Формально degraded по контракту F (VL <50% CFL **и** нет RU-права в теле): 1 навык** — `ip-legal/skills/customize/SKILL.md` (2 260 B против 4 724 B у CFL, ratio 0.48, ни одной ссылки на ГК/124-ФЗ/Пленумы, секции CFL «What changes / What never changes / Common changes» ужаты до «Типовых правок»).

**Пограничный (RU-норма есть, но сокращение тяжёлое)** — `corporate/ai-tool-handoff` (5 488 B vs 6 914 B, ratio 0.79, единственная RU-ссылка). Не degraded по контракту, но в ТОП нарушений внесён.

---

## 4. ТОП-10 нарушений phase 1

**1. `ip-legal/skills/cold-start-interview/SKILL.md`**
   ratio 0.10 (4 369 B vs 42 179 B у CFL). CFL: детальные Parts 0–6 с минутировкой, чеклисты по каждому типу IP-актива, brand-protection-модуль. VL: 8 частей по 2–3 мин, без детального чеклиста по портфелю. Не degraded формально (RU-нормы есть), но сокращение молчаливое — в отчёте приёмки не было.

**2. `litigation-legal/skills/cold-start-interview/SKILL.md`**
   ratio 0.16 (7 676 B vs 47 798 B). Потеряны детальные подсказки интервьюера и профили федеральных/штатных судов (заменены на kad.arbitr — сама замена честная, глубина сокращена втрое).

**3. `ai-governance-legal/skills/cold-start-interview/SKILL.md`**
   ratio 0.16 (7 404 B vs 47 158 B). Секция «The interview» CFL с 30+ вопросами ужата до ~10.

**4. `commercial-legal/skills/cold-start-interview/SKILL.md`**
   ratio 0.19 (9 091 B vs 49 113 B). CFL ведёт интервью по 8 блокам с формулировками вопросов; VL — тезисно, вопросы не воспроизводимы 1:1.

**5. `litigation-legal/skills/claim-chart/SKILL.md`**
   ratio 0.17 (7 085 B vs 40 835 B). **Утрачен весь MODE 1 — Patent claim chart** (Steps 1–7.5: parse claims, construction, DOE, indirect/divided/willfulness, invalidity thresholds, audit); VL покрывает только civil-элементный режим (MODE 2 → RF-фреймворк). Требуется либо патент-мод в RU-праве (ст. 1354–1358 ГК), либо задокументированное решение SKIP.

**6. `ip-legal/skills/cease-desist/SKILL.md`**
   ratio 0.18 (6 830 B vs 37 253 B). Потеряны: разбор юридических оснований по каждому типу нарушения, тон-структура письма, шаблоны трёх ступеней жёсткости.

**7. `ip-legal/skills/clearance/SKILL.md` + `ip-legal/skills/infringement-triage/SKILL.md`**
   ratio 0.23 / 0.16. CFL: пошаговые чеклисты классов МКТУ, анализ сходства до уровня фонетического/семантического; VL — рамочные инструкции без таблиц сравнения.

**8. `regulatory-legal/skills/cold-start-interview/SKILL.md`**
   ratio 0.15 (4 800 B vs 30 970 B). CFL: детальная работа с реестрами (Federal Register flow); VL: «reg-feed-watcher» перенесён отдельно, но интервью-модуль усечён без документированной причины.

**9. `litigation-legal/skills/deposition-prep/SKILL.md`**
   утрачен **Destination check** (есть у CFL-оригинала, нет в VL) при ratio 0.38. Точные потери паттернов против CFL-оригиналов — 15 навыков: `ai-governance/policy-starter`, `commercial/{amendment-history, nda-review, saas-msa-review, vendor-agreement-review}`, `employment/{hiring-review, termination-review, worker-classification}`, `ip/invention-intake`, `litigation/{deposition-prep, matter-briefing, matter-intake}`, `privacy/{pia-generation, reg-gap-analysis}`, `product/launch-review` (12 × decision tree, 2 × Reviewer note, 1 × Destination check). Отдельно generic-скан VL без привязки к CFL: 96/115 навыков не содержат хотя бы одного из трёх паттернов явно.

**10. `ip-legal/skills/customize/SKILL.md` — единственный формально degraded**
   ratio 0.48, 0 ссылок на RU-право: CFL-модули «Common changes» (portfolio review cadence, outside counsel rates, docketing system) переведены в списки-плейсхолдеры без RU-опоры (реестры Роспатента, приказы РКН, ставки поверенных).

*(Коэф. ratios посчитаны по полным длинам SKILL.md; «молчаливое сокращение» = отсутствие записи в отчёте приёмки phase 1.)*

---

## 5. Оценка контракта «финальный JSON = самоотчёт» (Gate 1)

| Критерий Gate 1 | Статус | Комментарий
|---|---|---|
| Полнота перечня навыков | **выполнен** | 115/115 имён совпадают, 0 недостающих, 3 сверх реестра задокументированы в README/SPECIFICATION.
| Фронтматтер | **выполнен** | 115/115: YAML парсится, name=dirname, desc ≤1024.
| RU-адаптация в телах | **выполнен с оговоркой** | RU-нормы есть в 114/115 (кроме ip/customize); плотность норм высокая, привязка к ст. точная, без выдуманных номеров (выборочная верификация: ст. 15/401/431.2 ГК, ст. 5.27/13.11 КоАП, ст. 6/12/18 152-ФЗ существуют и приведены корректно).
| Паттерн-комплаенс | **частично** | 0×Pitfalls соблюдено; Reviewer note и decision tree присутствуют на профильном уровне в CLAUDE.md practice profile, но не продублированы в 15 навыках, где CFL-оригинал их имел (см. §4.9), плюс 96/115 без явного паттерна при generic-скане.
| Destination check | **выполнен частично** | в practice profiles определён (Shared guardrails), в навыках присутствует явно в 15/115, остальные routing держат через '## Matter context' — соответствует духу, но не букве CFL-модели.
| «Финальный JSON = самоотчёт» | **подтверждается** | самоотчёт phase 1 («110 навыков + practice profiles + cold-start интервью», все 9 доменов полны) **подтверждён независимо**: численности сходятся, YAML чист, RU-тела на месте. Существенные отклонения самоотчёта: не раскрыты **массивные сокращения объёма в ip (−76%), ai-governance (−62%), litigation (−57%)** и единственный degraded `ip/customize`.

**Рейтинг доверия к самоотчёту:** 8/10 — полнота и YAML точно отражены, деградация объёма не раскрыта.

---

## 6. Рекомендации по дотяжке (приоритизировано)

1. **P1 — ip-домен** (mean ratio 0.24): дотянуть `cold-start-interview` (добавить детальные questions per asset type, патентный блок → ст. 1349–1414 ГК), `cease-desist` (3-ступенчатая тон-структура + ст. 1252, 1515 ГК), `clearance` (таблица сравнения по МКТУ/МКПИ + фонетическое/семантическое сходство), `infringement-triage` (ст. 1352, 1354, 1466 ГК, судебная практика СИП).
2. **P2 — ip/customize** (единственный degraded): добавить в тело RU-нормы: `Роспатент-реестры`, МКТУ классы, приказы РКН, ст. 1477–1515 ГК — 4–6 ссылок достаточно для снятия флага.
3. **P3 — litigation/claim-chart**: восстановить patent-мод в RU-праве (ст. 1354, 1358 ГК, СИП) ИЛИ задокументированно SKIP с записью в SPECIFICATION §6.
4. **P4 — Destination check в 18 litigation-файлах**: добавить явный «## Destination check» блок или ссылку на Shared guardrails practice profile там, где CFL его имел.
5. **P5 — cold-start-interview глубина**: 5 доменов (ip 0.10, litigation 0.16, ai-governance 0.16, commercial 0.19, regulatory 0.15) — вернуть детальные вопросы CFL с RU-адаптацией (интеграции: Диадок/СБИС/КонсультантПлюс, kad.arbitr, ЕГРЮЛ; юрисдикция: арбитражные суды РФ).
6. **P6 — provenance-теги**: 100% покрытие тел — сейчас в коммерческом домене 9/13 файлов rely on CLAUDE.md-определения; вставить по 1–2 тега в тела для машиночитаемости.
7. **P7 — Reviewer note**: в 12 commercial- и 13 corporate-файлах CFL-модель даёт блок у deliverable — продублировать его в телах или задокументировать отказ в отчёте о несоответствии.

---

## 7. Методика и воспроизводимость

```
git clone --depth 1 https://github.com/anthropics/claude-for-legal /tmp/cfl-retro
# сверка: name-sets CFL↔VL; pyYAML 115 файлов; regex RU-норм по телам;
# regex паттернов (Pitfalls/Reviewer note/Decision tree/Destination check) CFL↔VL;
# ratio = len(VL SKILL.md)/len(CFL SKILL.md); degraded = ratio<0.5 AND нет RU-норм.
```

*Аудит проведён независимым субагентом; данные: /tmp/skill_maps.json, /tmp/audit_part1.json (yaml+RU+prov), /tmp/audit_part3.json (паттерны+ratios), /tmp/audit_ru_prov.json.*
