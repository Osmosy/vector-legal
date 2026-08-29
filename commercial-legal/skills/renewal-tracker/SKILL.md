---
name: renewal-tracker
description: >
  Показывать договоры с приближающимся cancel-by дедлайном и предупреждать до
  закрытия окна уведомления — на основе реестра продлений. Используй при
  «что продлевается?», «какие renewal скоро?», «пропустили ли окно отмены?»,
  «добавь в трекер продлений», или по расписанию (cronjob).
  Принимает handoff от saas-msa-review.
argument-hint: '[--days N | --missed]'
---

# /renewal-tracker — реестр продлений

Показывает, что продлевается и когда нужно отменить.

## Инструкции

1. **Читать `~/.hermes/legal/commercial-legal/renewal-register.yaml`.**

2. **Дефолтный режим:** что приближается в следующие 90 дней, группировка по
   срочности с half-open интервалами (каждый дедлайн ровно в одной полосе):
   🔴 0–13 дней, 🟠 14–44 дней, 🟡 45–89 дней.

3. **`--days N`:** сменить окно.

4. **`--missed`:** cancel-by дедлайны, которые прошли без зафиксированного
   уведомления об отмене.

5. **Если реестр пуст и ЭДО подключён:** предложить Mode 3 — сканировать ЭДО
   на активные договоры с датами продления и bulk-load.

6. **Выход включает рекомендованные действия:** кого пингануть (бизнес-владелец
   из записи), какие позиции без ценового лимита (использовать рычаг до
   закрытия окна).


---

## Shared guardrails (канон — practice profile)

**Reviewer note / decision tree / Destination check / Provenance /
No-silent-supplement / Currency trigger / Large input** — см.
practice profile (`~/.hermes/legal/<domain>/CLAUDE.md` → `## Shared
guardrails`, `## Outputs`). Блоки канонизируются там; если текст навыка
расходится с профилем — профиль контролирует.


## Примеры

```
renewal-tracker
renewal-tracker --days 180
renewal-tracker --missed
```

---

## Purpose

Никто не читает договор дважды. Дата продления извлекается один раз — при
ревизии — и потом живёт где-то. В идеале: кричит за 45 дней до cancel-by,
не через 45 после.

Этот навык поддерживает реестр и показывает, что приближается.

## Реестр

`~/.hermes/legal/commercial-legal/renewal-register.yaml`. Каждая запись:

```yaml
- counterparty: "Acme SaaS Inc."
  agreement: "Договор подписки на Acme Platform"
  signed_date: 2025-06-15
  initial_term_end: 2026-06-15
  current_term_end: 2026-06-15     # скроллится вперёд после каждого автопродления; cancel_by_* вычисляются из этой
  renewal_mechanism: "auto-renew annual"
  notice_period_days: 60
  notice_method: "email"           # email / портал / заказное письмо / по договору §X
  transit_buffer_days: 0           # 0 электронно; 5 заказное письмо РФ; 10 международное — или по договору §X
  cancel_by_calendar: 2026-04-16
  cancel_by_effective: 2026-04-16  # откат до последнего бизнес-дня, если нужно
  send_by_effective: 2026-04-16    # cancel_by_effective минус transit_buffer_days — дата, когда ОТПРАВИТЬ
  cancel_by_roll_note: ""
  cancel_by_provenance: "[model calculation — verify against the notice clause]"
  price_on_renewal: "then-current list (uncapped)"
  annual_value: 48000
  business_owner: "owner@company.com"
  edo_id: ""                       # если ЭДО подключён
  status: "active"                 # active | cancelled | renewed | lapsed
  notes: "Цена без cap — пересмотреть до продления. Альтернативные вендоры: X, Y."
```

**Транзитное время — алерт по `send_by_effective`, не по `cancel_by_effective`.**
60-дневное окно с заказным письмом — реально ~55 дней. Трекер, который алертит
по дате получения, — трекер, который пропустит дедлайн. Полосы срочности
Mode 2 — по `send_by_effective`; `cancel_by_effective`, метод и буфер —
в колонке деталей.

**Rolling renewals — реестр, который не скроллится вперёд, прав лишь один
раз.** Хранить `initial_term_end` для истории, но `cancel_by_*` вычислять из
`current_term_end`. Когда продление случилось (окно прошло, уведомления не
было) — предложить:

> Этот договор автопродлился [дата]. Обновить реестр: новый `current_term_end`
> [дата + период], новый `cancel_by_effective` [computed], новый
> `send_by_effective` [computed]. Подтверждаешь?

## Бизнес-дни для каждого cancel-by

**cancel-by дата — последний БИЗНЕС-день, на который уведомление действует, не
календарная дата.** Календарная дата на выходной — самый частый способ
пропустить renewal.

При вычислении (или загрузке) cancel-by:

1. **Календарная дата.** `cancel_by_calendar = initial_term_end −
notice_period_days`.
2. **Откат до бизнес-дня по праву договора.** РФ: нерабочие дни РФ
(производственный календарь, переносы по постановлениям Правительства).
Если выходной — откат НАЗАД до рабочего дня. Не вперёд: вперёд = уведомление
приходит после закрытия окна. Не можете определить календарь для
иностранного права — флаг: «Право договора — [X]; откат использует
производственный календарь РФ как placeholder. Проверить против [юрисдикция]».
3. **Проставить provenance.** `cancel_by_provenance: "[model calculation —
verify against the notice clause]"` до проверки юристом. Против: «[user
provided]», «[verified — подтверждено YYYY-MM-DD]».

## Пороги / матрица эскалаций

Реестр использует эскалационную матрицу из practice profile:
`annual_value > [порог]` → аппрувер [имя]. Использоваться при колонке
«Одобрение» в выходе.

## Интеграция

При подключённом ЭДО (Диадок/СБИС): если вендорский договор уже на ЭДО —
offer bulk-load. Если Telegram подключён — алерты идут туда (в канал из
House style → Renewal alerts).