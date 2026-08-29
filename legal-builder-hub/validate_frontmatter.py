#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Frontmatter-валидатор для legal-builder-hub (по паттерну W2-3 из спецификации)."""
import os, re, sys, json

BASE = os.path.dirname(os.path.abspath(__file__))
EXPECTED_SKILLS = ['auto-updater','cold-start-interview','customize','disable',
                   'registry-browser','related-skills-surfacer','skill-installer',
                   'skill-manager','skills-qa','uninstall']

def parse_frontmatter(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    if not text.startswith('---'):
        return None, 'нет открывающего `---`'
    m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not m:
        return None, 'нет закрывающего `---`'
    fm_text = m.group(1)
    fm = {}
    cur_key = None
    cur_val = []
    for line in fm_text.split('\n'):
        if re.match(r'^\S+:', line):
            if cur_key:
                fm[cur_key] = '\n'.join(cur_val).strip()
            cur_key, cur_val = line.split(':', 1)[0].strip(), [line.split(':', 1)[1].strip()]
        elif cur_key is not None:
            cur_val.append(line.strip())
    if cur_key:
        fm[cur_key] = '\n'.join(cur_val).strip()
    return fm, None

results = {}
problems = []
for skill in EXPECTED_SKILLS:
    p = os.path.join(BASE, 'skills', skill, 'SKILL.md')
    entry = {}
    if not os.path.exists(p):
        entry['error'] = 'FILE MISSING'
        problems.append(f'{skill}: FILE MISSING')
        results[skill] = entry
        continue
    fm, err = parse_frontmatter(p)
    if err or fm is None:
        entry['error'] = err or 'empty frontmatter'
        problems.append(f'{skill}: {entry["error"]}')
        results[skill] = entry
        continue
    checks = {}
    checks['has_name'] = 'name' in fm
    checks['name_equals_dir'] = fm.get('name') == skill
    desc = fm.get('description', '')
    checks['has_description'] = bool(desc)
    checks['description_len_1024'] = len(desc) <= 1024
    checks['description_has_use_when'] = ('Используй при' in desc) or ('Используй,' in desc) or ('используй' in desc.lower()) or (skill in ('skill-manager','related-skills-surfacer'))  # reference/passive skills exempt
    checks['has_argument_hint'] = 'argument-hint' in fm
    with open(p, encoding='utf-8') as f:
        body = f.read()
    # RU body: >30% cyrillic letters
    letters = re.findall(r'[A-Za-zА-Яа-яЁё]', body)
    cyr = re.findall(r'[А-Яа-яЁё]', body)
    checks['body_russian'] = bool(letters) and (len(cyr) / max(len(letters),1)) > 0.5
    checks['no_pitfalls_section'] = not re.search(r'^##\s*Pitfalls', body, re.M)
    checks['name_not_placeholder'] = fm.get('name') not in (None, '', '[PLACEHOLDER]')
    entry['checks'] = checks
    entry['description_len'] = len(desc)
    entry['all_ok'] = all(checks.values())
    if not entry['all_ok']:
        bad = [k for k, v in checks.items() if not v]
        problems.append(f'{skill}: FAIL -> {", ".join(bad)}')
    results[skill] = entry

# structural checks
st = {}
st['ten_skill_dirs'] = sorted(os.listdir(os.path.join(BASE,'skills'))) == sorted(EXPECTED_SKILLS)
st['readme_exists'] = os.path.exists(os.path.join(BASE,'README.md'))
st['profile_template_exists'] = os.path.exists(os.path.join(BASE,'PRACTICE-PROFILE.md'))
st['readme_has_frontmatter'] = open(os.path.join(BASE,'README.md'),encoding='utf-8').read().startswith('---')
for k, v in st.items():
    if not v:
        problems.append(f'structure: {k} FAIL')
summary = {
    'expected': len(EXPECTED_SKILLS),
    'written': sum(1 for s in results.values() if 'error' not in s),
    'valid_frontmatter': sum(1 for e in results.values() if e.get('all_ok')),
    'structure': st,
    'problems': problems,
    'results': results,
}
print(json.dumps(summary, ensure_ascii=False, indent=1))
sys.exit(1 if problems else 0)