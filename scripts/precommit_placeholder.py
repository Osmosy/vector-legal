#!/usr/bin/env python3
"""
Pre-commit hook: placeholder hygiene для vector-legal.

Проверяет, что в SKILL.md нет [PLACEHOLDER] (это ожидаемо только в
CLAUDE.md-шаблонах practice profile). Не блокирует коммит — advisory.

Возвращает 0 всегда (не блокирует); предупреждения печатает в stdout.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).parent.parent


def main() -> int:
    found = []
    for p in sorted(REPO.rglob('SKILL.md')):
        rel = str(p.relative_to(REPO))
        if '/skills/' not in rel or rel.startswith('skills/'):
            continue
        text = p.read_text(encoding='utf-8')
        if '[PLACEHOLDER]' in text:
            found.append(rel)
    if found:
        print(f'warning: [PLACEHOLDER] в {len(found)} SKILL.md (advisory, moves to CLAUDE.md):')
        for f in found[:20]:
            print(f'    {f}')
    else:
        print('OK: no [PLACEHOLDER] in SKILL.md')
    return 0


if __name__ == '__main__':
    sys.exit(main())
