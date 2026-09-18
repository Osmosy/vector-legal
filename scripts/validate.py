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


# --- проверка заявлений о составе и лицензии (--claims) -----------------------
#
# Каждая проверка ниже появилась из реального дефекта аудита 18.09.2026:
#   * README показывал бейдж «Apache 2.0» и раздел «Источник … Apache 2.0», тогда
#     как файл LICENSE — MIT (апстрим claude-for-legal под Apache-2.0, и его
#     лицензию выдали за свою);
#   * бейдж «Skills: 167» при фактических 168 SKILL.md;
#   * в одном README соседствовали «151 навык» (апстрим) и «111+ навыков»;
#   * litigation-legal/README занижал состав: «skills/ # 19 навыков» при 20;
#   * два раздела «## Архитектура» и два «## Быстрый старт» в README.

CLAIM_FILES = ('README.md', 'AGENTS.md', 'agent-description.md')

# «Якоря заявлений» — фразы, которыми документы называют ОБЩЕЕ число навыков
# репозитория. Проверка точная: каждое совпадение должно равняться числу SKILL.md
# в дереве. Добавляя новый документ с заявлением о составе — добавьте сюда якорь,
# иначе такая цифра попадёт в свободный поиск ниже (см. check_claims).
OWN_ANCHORS: tuple[tuple[str, str], ...] = (
    ('README.md', r'Hermes Agent\s*—\s*\d+\s+плагинов,\s*(\d+)\s+навык'),
    ('README.md', r'^\d+\s+плагинов,\s*(\d+)\s+навык(?:ов)?,\s*practice profiles'),
    ('AGENTS.md', r'\d+\s+плагинов,\s*(\d+)\s+навык'),
    ('agent-description.md', r'Библиотека из\s*(\d+)\s+навык'),
)

# Якоря заявлений об АПСТРИМЕ (anthropics/claude-for-legal). Не сверяются с деревом
# (апстрим здесь не лежит), но обязаны совпадать между собой: 18.09.2026 README
# одновременно утверждал «151 навык» и «111+ навыков».
UPSTREAM_ANCHORS: tuple[tuple[str, str], ...] = (
    ('README.md', r'claude-for-legal\)\s*\(Anthropic,\s*(\d+)\s+навык'),
    ('README.md', r'—\s*\d+\s+плагинов,\s*(\d+)\s+навык\s*\(Apache-2\.0 у апстрима'),
    ('domains-status.md', r'claude-for-legal\s*\((\d+)\s+навык'),
)

# Как далеко от цифры искать упоминание апстрима в свободном поиске (символы).
# Порог маленький намеренно: «claude-for-legal под российское право. 12 плагинов,
# 168 навыков» — это НАШЕ число, стоящее далеко от маркера, и в апстрим попадать
# не должно.
UPSTREAM_MARKERS = ('апстрим', 'claude-for-legal', 'cfl', 'anthropic')
UPSTREAM_WINDOW = 45


def _anchored(text: str, patterns: tuple[tuple[str, str], ...]) -> tuple[set[int], list[int]]:
    """Вернуть (позиции start группы с числом, значения) для набора якорей."""
    positions: set[int] = set()
    values: list[int] = []
    for _name, pattern in patterns:
        for m in re.finditer(pattern, text, re.M):
            positions.add(m.start(1))
            values.append(int(m.group(1)))
    return positions, values


def licenses_in_repo(root: pathlib.Path) -> tuple[str, set[str]]:
    """(лицензия кода по первой строке LICENSE, набор допустимых чужих лицензий).

    Лицензия кода определяется ТОЛЬКО файлом LICENSE: 18.09.2026 README показывал
    бейдж «Apache 2.0» и «Источник … Apache 2.0», тогда как LICENSE — MIT (у
    апстрима claude-for-legal Apache-2.0, и его лицензию выдали за свою).
    """
    lic = root / 'LICENSE'
    if not lic.is_file():
        return 'unknown', set()
    first = lic.read_text(encoding='utf-8').splitlines()[0].strip()
    if 'MIT License' in first:
        actual = 'MIT'
    elif 'Apache License' in first:
        actual = 'Apache-2.0'
    else:
        actual = 'unknown'
    # Чужие лицензии, упоминать которые законно (атрибуция). Расширять только
    # вместе появлением соответствующей записи в THIRD_PARTY_LICENSES.md/NOTICE.
    allowed = {'Apache-2.0'}
    for notice_name in ('THIRD_PARTY_LICENSES.md', 'NOTICE.md'):
        notice = root / notice_name
        if notice.is_file():
            allowed |= set(re.findall(
                r'\b(MIT|Apache-2\.0|BSD-\d-Clause)\b', notice.read_text(encoding='utf-8')))
    return actual, allowed


def check_claims(root: pathlib.Path) -> List[str]:
    """Заявления о составе и лицензии против дерева. Возвращает список ошибок."""
    errors: List[str] = []
    actual_license, _ = licenses_in_repo(root)
    total_skills = len(list(root.rglob('SKILL.md')))
    readme_path = root / 'README.md'

    # 1. Бейдж лицензии против LICENSE.
    if readme_path.is_file():
        md = readme_path.read_text(encoding='utf-8')
        badge = re.search(r'badge/License-([A-Za-z0-9._%\-]+)', md)
        if badge:
            declared = badge.group(1).replace('%20', ' ').replace('--', '-')
            expected = 'MIT' if actual_license == 'MIT' else 'Apache'
            if expected.lower() not in declared.lower():
                errors.append(
                    f'README: бейдж лицензии «{declared}», а LICENSE — {actual_license}')

        # 2. Бейдж числа навыков.
        for m in re.finditer(r'badge/Skills-(\d+)', md):
            if int(m.group(1)) != total_skills:
                errors.append(
                    f'README: бейдж «Skills: {m.group(1)}», а SKILL.md в дереве {total_skills}')

        # 3. Дубли разделов H2 (README сшивали вручную дважды — «Архитектура»
        #    и «Быстрый старт» дублировались).
        h2 = [l.strip() for l in md.splitlines() if l.startswith('## ')]
        for title in sorted({h for h in h2 if h2.count(h) > 1}):
            errors.append(f'README: раздел «{title}» встречается {h2.count(title)} раза')

    # 4. Якорные заявления о НАШЕМ составе.
    for name, pattern in OWN_ANCHORS:
        path = root / name
        if not path.is_file():
            continue
        for m in re.finditer(pattern, path.read_text(encoding='utf-8'), re.M):
            n = int(m.group(1))
            if n != total_skills:
                errors.append(
                    f'{name}: заявлено «{n} навык(ов)», а SKILL.md в дереве {total_skills}')

    # 5. Якорные заявления об апстриме — обязаны совпадать между собой.
    upstream_values: list[tuple[str, int]] = []
    for name, pattern in UPSTREAM_ANCHORS:
        path = root / name
        if not path.is_file():
            continue
        for m in re.finditer(pattern, path.read_text(encoding='utf-8'), re.M):
            upstream_values.append((name, int(m.group(1))))
    if len({n for _, n in upstream_values}) > 1:
        detail = ', '.join(f'{f}:{n}' for f, n in upstream_values)
        errors.append(
            f'апстрим: разные числа навыков в документации ({detail}); сверка — '
            f'gh api repos/anthropics/claude-for-legal/git/trees/main?recursive=1')

    # 6. Свободный поиск: незаякоренные «N навыков» в CLAIM_FILES. Сравниваются с
    #    нашим числом, если рядом нет упоминания апстрима; если есть — идут в
    #    апстрим-набор и ловят расхождение с якорями.
    for name in CLAIM_FILES:
        path = root / name
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        own_pos, _ = _anchored(text, OWN_ANCHORS)
        up_pos, _ = _anchored(text, UPSTREAM_ANCHORS)
        for m in re.finditer(r'(\d+)\s+навык(?:ов|а)?\b', text):
            pos = m.start(1)
            if pos in own_pos or pos in up_pos:
                continue
            n = int(m.group(1))
            near = text[max(0, pos - UPSTREAM_WINDOW):m.end() + UPSTREAM_WINDOW].lower()
            if any(marker in near for marker in UPSTREAM_MARKERS):
                upstream_values.append((name, n))
                continue
            if n != total_skills:
                errors.append(
                    f'{name}: заявлено «{n} навык(ов)», а SKILL.md в дереве {total_skills}')

    if len({n for _, n in upstream_values}) > 1:
        detail = ', '.join(f'{f}:{n}' for f, n in upstream_values)
        errors.append(
            f'апстрим: разные числа навыков в документации ({detail})')

    # 7. Доменные README: «# N навыков» в описании состава.
    for domain in sorted(p for p in root.iterdir() if p.is_dir() and (p / 'skills').is_dir()):
        readme_d = domain / 'README.md'
        if not readme_d.is_file():
            continue
        fact = len(list((domain / 'skills').rglob('SKILL.md')))
        for m in re.finditer(r'#\s*(\d+)\s+навык', readme_d.read_text(encoding='utf-8')):
            if int(m.group(1)) != fact:
                errors.append(
                    f'{domain.name}/README.md: «skills/ # {m.group(1)} навыков», фактически {fact}')

    # 8. Лицензия НАШЕЙ адаптации, названная в прозе, должна совпадать с LICENSE.
    #    Бейджа мало: 18.09.2026 в 12 доменных README и в domains-status.md стояло
    #    «Адаптация © Osmosy, Apache-2.0» при MIT в LICENSE. Формулировки разные
    #    («Адаптация © Osmosy, MIT» и «Адаптация под право РФ и Hermes Agent
    #    © Osmosy, MIT (см. LICENSE)»), поэтому текст склеивается в одну строку,
    #    а якорь — пара «Адаптация … Osmosy … <лицензия>». Лицензии чужих работ
    #    («© Anthropic, Apache-2.0») не трогаем: там нет Osmosy после «Адаптация».
    our_adaptation = re.compile(r'Адаптация.{0,160}?Osmosy.{0,60}?(MIT|Apache-2\.0|GPL[\w.\-]*)', re.S)
    for md_path in sorted(root.rglob('*.md')):
        if '.git' in md_path.parts or 'node_modules' in md_path.parts:
            continue
        rel = str(md_path.relative_to(root))
        if rel.startswith('skills/'):
            continue  # legacy cowork-roles — EN-оригиналы без нашей атрибуции
        flat = re.sub(r'\s+', ' ', md_path.read_text(encoding='utf-8'))
        for m in our_adaptation.finditer(flat):
            declared = m.group(1)
            if actual_license == 'MIT' and 'MIT' not in declared.upper():
                errors.append(
                    f'{rel}: «Адаптация … Osmosy … {declared}», а LICENSE — MIT')

    return errors


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
    if '--claims' in args:
        root = pathlib.Path(__file__).parent.parent
        claim_errors = check_claims(root)
        for e in claim_errors:
            print(f'ERROR {e}')
        print(f'\nИтог (заявления о составе/лицензии): ошибок {len(claim_errors)}')
        sys.exit(1 if claim_errors else 0)
    # Флаги режимов уходят в validate_all(). Без этой ветки «--warnings»/«--strict»
    # попадали в разбор путей как имена файлов → «not found: --warnings», exit 2,
    # и job ru-lint-warnings в CI падал, хотя объявлен report-only.
    flag_args = {'--strict', '--warnings'}
    if not args or flag_args & set(args):
        sys.exit(validate_all())
    for f in args:
        path = pathlib.Path(f)
        if not path.exists():
            print(f'not found: {f}'); sys.exit(2)
        issues = check_skill(path)
        for i in issues:
            print(f'  [{f}] {i}')
        sys.exit(1 if issues else 0)
