#!/usr/bin/env python3
"""Сверка живых cron-задач с их спеками в репозитории.

Зачем. Источник истины — `cookbooks/<agent>/cron-spec.yaml`, но живые задачи
`hermes cron` живут вне Git (`~/.hermes/cron/jobs.json`) и обновляются вручную
через `cronjob_manage action=update`. Шаг «перенести правку в живую задачу»
терялся: после PR #11 (L1/L2) спеки изменились, а задачи остались на прежних
промптах — и в понедельник docket-watcher мог снова выдать «событий нет» при
недоступном kad.arbitr, ровно то, что закрывала задача L2.

Что делает. Читает `~/.hermes/cron/jobs.json`, сравнивает `prompt` каждой
задачи со `prompt` её спеки (нормализация пробелов; сравнивается текст, а не
YAML), сообщает diff и кодом возврата показывает, есть ли расхождения.

Запуск:  python3 scripts/cron_sync_check.py [--repo .]
Код 0 — всё сходится; 1 — есть расхождения (или задача/спека не найдены).

Вне CI: живой jobs.json — не часть репозитория, в CI задачи отсутствуют.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    print('нужен pyyaml (pip install pyyaml)', file=sys.stderr)
    raise SystemExit(2)

JOBS = pathlib.Path.home() / '.hermes' / 'cron' / 'jobs.json'


def spec_prompt(repo: pathlib.Path, agent: str) -> str | None:
    p = repo / 'cookbooks' / agent / 'cron-spec.yaml'
    if not p.is_file():
        return None
    data = yaml.safe_load(p.read_text(encoding='utf-8')) or {}
    return (data.get('prompt') or '').strip()


def jobs_by_name() -> dict[str, str]:
    if not JOBS.is_file():
        return {}
    data = json.loads(JOBS.read_text(encoding='utf-8'))
    items = data if isinstance(data, list) else data.get('jobs', [])
    return {j.get('name', ''): (j.get('prompt') or '').strip() for j in items}


def norm(text: str) -> list[str]:
    """Значимые строки: без пустых и коротких, с сжатыми пробелами."""
    out = []
    for line in text.splitlines():
        s = re.sub(r'\s+', ' ', line).strip()
        if len(s) > 25:
            out.append(s)
    return out


def line_diff(spec: str, live: str) -> tuple[list[str], list[str]]:
    ns, nl = norm(spec), norm(live)
    return ([l for l in ns if l not in nl], [l for l in nl if l not in ns])


def main() -> int:
    ap = argparse.ArgumentParser(description='Сверить живые cron-задачи со спеками репо')
    ap.add_argument('--repo', default='.', help='корень репозитория vector-legal')
    args = ap.parse_args()
    repo = pathlib.Path(args.repo).resolve()

    specs = sorted(p.parent.name for p in (repo / 'cookbooks').glob('*/cron-spec.yaml'))
    live = jobs_by_name()
    if not live:
        print('нет ~/.hermes/cron/jobs.json — живые задачи недоступны (в CI это норма)')
        return 0

    bad = 0
    for agent in specs:
        sp = spec_prompt(repo, agent)
        lv = live.get(agent)
        if sp is None:
            continue
        if lv is None:
            print(f'РАСХОЖДЕНИЕ {agent}: задача не найдена среди живых')
            bad += 1
            continue
        if sp == lv:
            print(f'ok          {agent}: живой промпт = спека')
            continue
        bad += 1
        only_spec, only_live = line_diff(sp, lv)
        print(f'РАСХОЖДЕНИЕ {agent}: только в спеке {len(only_spec)}, '
              f'только в живом {len(only_live)}')
        for l in only_spec[:4]:
            print(f'    спек:  {l[:110]}')
        for l in only_live[:4]:
            print(f'    живой: {l[:110]}')

    print()
    if bad:
        print(f'Итог: расхождений {bad} из {len(specs)}. '
              f'Обновить задачу: cronjob_manage action=update '
              f'с текстом prompt из спеки, затем повторить сверку.')
    else:
        print(f'Итог: живые промпты = спеки ({len(specs)}/{len(specs)})')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
