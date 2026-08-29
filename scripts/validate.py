#!/usr/bin/env python3
"""
vector-legal validators: frontmatter + RU-lint + structural checks
Запуск: python3 scripts/validate.py        # all skills
        python3 scripts/validate.py <domain>/skills/<name>/SKILL.md   # one skill

Проверки:
1. Frontmatter: YAML parse, `---` opening/closing, name == dirname,
   description присутствует и ≤ 1024 символов, начинается с «Используй»
   или «Use» (trigger-first по Hermes-конвенции), argument-hint
2. Body: русское тело (кириллица ≥50% среди букв), есть # заголовок
3. Anti-pattern: нет «## Pitfalls»/«## Common Pitfalls» секций
4. Consequential-gates: навыки с 'send|file|takedown|sign|претензия' в
   description содержат указание «отправку/подписание делает человек»
5. Provenance-теги: описание упоминаетkad.arbitr/pravo.gov.ru/ФИПС/или
   соответствующий раздел есть в теле
"""
import sys
import re
import pathlib
import yaml
from typing import List, Tuple

REPO = pathlib.Path(__file__).parent.parent

KIRILL_RE = re.compile(r'[а-яё]', re.I)
PITFALL_RE = re.compile(r'^##\s.*[Pp]itfall', re.M)
PROVENANCE_TAGS_RE = re.compile(
    r'\[(?:kad\.arbitr\.ru|pravo\.gov\.ru|ФИПС|КонсультантПлюс|user\s+provided|'
    r'model\s+knowledge\s*[—-]\s*verify|web\s+search\s*[—-]\s*verify|'
    r'settled\s*[—-]*\s*подтверждено|egrul\.nalog\.ru|sudrf\.ru|fedresurs\.ru|'
    r'sudact\.ru|regulation\.gov\.ru|СИПН|vsrf\.ru)\]'
)
REVIEWER_NOTE_RE = re.compile(r'⚠️\s*Reviewer\s+note', re.I)
DECISION_TREE_RE = re.compile(r'Что\s+дальше\?|Decision\s+tree', re.I)

# Ключевые слова, при которых требуется явное «человек решает» в теле
CONSEQUENTIAL_KEYWORDS = [
    'takedown', 'подать', 'подписать', 'отправить', 'файл', 'filing',
    'cease', 'претенз', 'договор подпис', 'исковое заявление',
]


def validate_frontmatter(s: str) -> List['str']:
    """Возвращает список ошибок фронтматтера. [] — ок."""
    issues = []
    if not s.startswith('---'):
        issues.append('no leading `---`')
        return issues
    m = re.search(r'\n---\s*\n', s[3:])
    if not m:
        issues.append('no closing `---`')
        return issues
    try:
        fm = yaml.safe_load(s[3:m.start()+3])
    except yaml.YAMLError as e:
        issues.append(f'yaml parse error: {e}')
        return issues
    if not isinstance(fm, dict):
        issues.append('frontmatter is not a mapping')
        return issues

    name = fm.get('name')
    if not name:
        issues.append('no `name`')
    desc = fm.get('description')
    if not desc:
        issues.append('no `description`')
    elif len(str(desc)) > 1024:
        issues.append(f'description is {len(str(desc))} chars (max 1024)')
    # argument-hint: advisory
    if 'argument-hint' not in fm:
        issues.append('advisory: missing argument-hint')
    return issues


def check_skill(path: pathlib.Path) -> List['str']:
    """Все проверки одного SKILL.md."""
    issues = []
    s = path.read_text(encoding='utf-8')
    fm_issues = validate_frontmatter(s)
    issues.extend([f'frontmatter: {i}' for i in fm_issues])

    # Body после закрытия frontmatter
    m = re.search(r'\n---\s*\n', s[3:])
    body = s[m.end():] if m else s

    # Anti-pattern: Pitfalls в любом виде
    if re.search(r'^##\s+.?[Pp]itfall', body, re.M):
        issues.append('anti-pattern: `## Pitfalls` section (норм — вплетать в тело)')

    # RU-язык body: хотя бы 5% кириллицы от общего числа букв символов
    cyrillic = sum(1 for c in body if KIRILL_RE.match(c))
    if cyrillic < 5:
        issues.append('body has <5 cyrillic chars, expected Russian')
    # Too English-dominant body (более 2/3 латиницы и менее 5% кириллицы)
    if cyrillic < 100 and len(body) > 2000:
        issues.append(f'body very low on Russian (only {cyrillic} cyrillic chars in {len(body)}-byte body)')

    # Provenance в теле (если упоминает суды/закон/базу — ожидается тег)
    if mentions_sources(body) and not PROVENANCE_TAGS_RE.search(body):
        issues.append('advisory: no provenance-tag found while referencing norms/sources')

    # Consequential-gate: если навык описывает takedown/c&e/подача —
    # должно быть указание, что делает человек
    if re.search(r'(?i)(takedown|cease[- ]and[- ]desist|подать в (арбитраж|суд)|отправить претензию|подписать договор)',
                 body or ''):  # body only, not frontmatter
        if 'человек' not in body.lower() and 'решение — юрист' not in body.lower() \
           and 'клиент' not in body.lower() and 'гate' not in body.lower() \
           and 'gate' not in body.lower():
            issues.append('advisory: consequential-skill, verify practice-profile controls')

    # Placeholder count: [PLACEHOLDER] — это ожидаемо в шаблоне, но не в теле
    # навыков (только в CLAUDE.md). Если найдены в SKILL.md — предупредить
    if '[PLACEHOLDER]' in body:
        issues.append('WARNING: [PLACEHOLDER] в SKILL.md — advisory only')
    return issues


def mentions_sources(body: str) -> bool:
    """Тело упоминает нормативные акты / судебную практику."""
    return bool(re.search(r'\b(ст\.|ГК|ТК|АПК|ГПК|КАС|КоАП|НК|ФЗ|Пленум|152-ФЗ|44-ФЗ)\b', body))


def validate_all() -> int:
    """Прогнать все SKILL.md; return exit code.

    Флаги (совместимо с GitHub Actions):
      --strict   warnings тоже считаются ошибками (exit 1 при любых findings)
      --warnings вывести только advisories/warnings, errors молча (для
                 отдельного report-only job'а в CI)
    """
    root = pathlib.Path(__file__).parent.parent
    strict = '--strict' in sys.argv
    warnings_only = '--warnings' in sys.argv
    all_errors = []
    all_warnings = []
    total = 0
    counts = {}
    for p in sorted(root.rglob('SKILL.md')):
        rel = str(p.relative_to(root))
        if '/skills/' not in rel:
            continue
        # RU-strict только для 12 адаптированных доменов; legacy skills/ — skip
        if rel.startswith('skills/'):
            continue  # legacy cowork-roles — EN-оригиналы
        total += 1
        issues = check_skill(p)
        errs = [i for i in issues if 'advisory' not in i.lower() and 'WARNING' not in i and 'missing argument-hint' not in i]
        warns = [i for i in issues if i.startswith('WARNING') or i.startswith('advisory:')]
        if errs:
            all_errors.append((rel, errs))
        for w in warns:
            all_warnings.append((rel, w))
        parts = pathlib.Path(rel).parts
        dom = parts[0] if parts[0] != 'skills' else 'root'
        counts[dom] = counts.get(dom, 0) + 1

    print(f'=== Vector Legal validation ===')
    print(f'  SKILL.md total: {total}')
    for d, n in sorted(counts.items(), key=lambda x: -x[1] if x[0] != 'root' else 0):
        print(f'    {d}: {n}')
    print(f'  Errors: {len(all_errors)} | Advisories: {len(all_warnings)}')

    if warnings_only:
        # Report-only job: печатаем только warnings, ошибки уже видит error-job
        if all_warnings:
            print('Advisories (report-only, not blocking):')
            for rel, w in all_warnings:
                print(f'    [advisory] [{rel}] {w}')
        else:
            print('Warnings: none')
        return 0

    if all_errors:
        print('ERRORS by file:')
        for rel, errs in all_errors:
            for i in errs:
                print(f'    [ERR] [{rel}] {i}')
        return 1
    if all_warnings and strict:
        print('Warnings (STRICT mode → treated as errors):')
        for rel, w in all_warnings:
            print(f'    [warning] [{rel}] {w}')
        return 1
    if all_warnings:
        print('Advisories (not blocking):')
        for rel, w in all_warnings[:30]:
            print(f'    [advisory] [{rel}] {w}')
        print('PASS (warnings only)')
        return 0
    print('OK: 0 errors, 0 warnings')
    return 0


if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        for f in args:
            path = pathlib.Path(f)
            if not path.exists():
                print(f'not found: {f}'); sys.exit(2)
            issues = check_skill(path)
            for i in issues:
                print(f'  [{f}] {i}')
            sys.exit(1 if issues else 0)
    else:
        sys.exit(validate_all())
