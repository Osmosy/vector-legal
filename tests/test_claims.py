#!/usr/bin/env python3
"""Тесты проверки заявлений о составе/лицензии (scripts/validate.py --claims).

Запуск: python3 tests/test_claims.py

Каждый тест — либо чистый репозиторий (0 ошибок), либо конкретный дефект, который
проверка обязана поймать. Тесты не зависят от содержимого репозитория: работают
на синтетическом дереве, поэтому не ломаются при росте числа навыков.
"""
from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile
import textwrap

VALIDATE = pathlib.Path(__file__).resolve().parent.parent / 'scripts' / 'validate.py'


def make_repo(tmp: pathlib.Path, *, skills: int = 3, readme: str = '', agents: str = '',
              agent_description: str = '', license_text: str = 'MIT License\n\nCopyright (c) 2026 Osmosy\n',
              domain_readme: str | None = None, domains_status: str = '') -> pathlib.Path:
    """Синтетический репозиторий: skills файлы + документы с заявлениями.

    ВАЖНО: validate.py определяет корень репозитория как `__file__.parent.parent`,
    а не по cwd, — поэтому скрипт копируется внутрь фикстуры. Иначе проверка
    пойдёт по настоящему репозиторию и мутации в фикстуре ничего не изменят.
    """
    scripts = tmp / 'scripts'
    scripts.mkdir(parents=True, exist_ok=True)
    shutil.copy2(VALIDATE, scripts / 'validate.py')
    (tmp / 'LICENSE').write_text(license_text, encoding='utf-8')
    for i in range(skills):
        d = tmp / 'demo-legal' / 'skills' / f'skill-{i}'
        d.mkdir(parents=True, exist_ok=True)
        (d / 'SKILL.md').write_text(
            '---\nname: skill-%d\ndescription: demo\n---\n\nтело\n' % i, encoding='utf-8')
    # skills/ (legacy) — тоже считается в общее число, как в реальном репо
    legacy = tmp / 'skills' / 'demo' / 'legacy'
    legacy.mkdir(parents=True, exist_ok=True)
    (legacy / 'SKILL.md').write_text('---\nname: legacy\ndescription: demo\n---\n', encoding='utf-8')
    total = skills + 1

    if readme:
        (tmp / 'README.md').write_text(readme.format(total=total, skills=skills), encoding='utf-8')
    if agents:
        (tmp / 'AGENTS.md').write_text(agents.format(total=total), encoding='utf-8')
    if agent_description:
        (tmp / 'agent-description.md').write_text(
            agent_description.format(total=total), encoding='utf-8')
    if domains_status:
        (tmp / 'domains-status.md').write_text(domains_status, encoding='utf-8')
    if domain_readme is not None:
        (tmp / 'demo-legal' / 'README.md').write_text(
            domain_readme.format(skills=skills), encoding='utf-8')
    return tmp


def run_claims(repo: pathlib.Path) -> tuple[int, list[str]]:
    r = subprocess.run([sys.executable, str(repo / 'scripts' / 'validate.py'), '--claims'],
                       cwd=repo, capture_output=True, text=True)
    errors = [l[6:].strip() for l in r.stdout.splitlines() if l.startswith('ERROR')]
    return r.returncode, errors


def case(name, expect_fail: bool, expect_substring: str = '', **kwargs) -> bool:
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, **kwargs)
    except Exception as exc:  # noqa: BLE001
        print(f'FAIL  {name}: не собрать фикстуру: {exc}')
        shutil.rmtree(tmp, ignore_errors=True)
        return False
    try:
        code, errors = run_claims(tmp)
        failed = code == 1
        if failed != expect_fail:
            print(f'FAIL  {name}: exit={code}, ожидался {"1" if expect_fail else "0"}')
            for e in errors:
                print(f'        {e}')
            return False
        if expect_substring and not any(expect_substring in e for e in errors):
            print(f'FAIL  {name}: нет ошибки со «{expect_substring}»')
            for e in errors:
                print(f'        {e}')
            return False
        print(f'ok    {name}')
        return True
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


GOOD_README = textwrap.dedent('''\
    # Demo Legal

    [![Skills: {total}](https://img.shields.io/badge/Skills-{total}-blue.svg)]()
    [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

    Юридический AI-департамент для Hermes Agent — 12 плагинов, {total} навыков,
    полный перенос Claude-for-Legal под российское право.

    ## Быстрый старт

    ```
    hermes "проверь договор"
    ```

    ## Источник

    Адаптировано из [Claude-for-Legal](https://github.com/anthropics/claude-for-legal)
    (Anthropic, 151 навык) — у апстрима Apache-2.0, здесь MIT.

    ## License

    MIT.
    ''')


def main() -> int:
    results = []

    # --- положительные: корректное дерево проходит ---
    results.append(case(
        'корректный репозиторий — 0 ошибок', False,
        readme=GOOD_README,
        agents='# AGENTS\n\nПеренос из anthropics/claude-for-legal. 12 плагинов, {total} навыков.\n',
        agent_description='# Описание\n\nБиблиотека из {total} навыков (12 плагинов/доменов)\n',
        domain_readme='### Состав\n\n```\ndemo-legal/\n└── skills/                        # {skills} навыков\n```\n'))

    # --- дефекты, которые проверка обязана ловить ---
    results.append(case(
        'бейдж лицензии Apache при MIT в LICENSE', True, 'бейдж лицензии',
        readme=GOOD_README.replace('badge/License-MIT-green.svg', 'badge/License-Apache%202.0-yellow.svg')))

    results.append(case(
        'бейдж Skills с устаревшим числом', True, 'бейдж «Skills',
        readme=GOOD_README.replace('badge/Skills-{total}-blue', 'badge/Skills-99-blue')))

    results.append(case(
        'шапка README называет старое число', True, 'заявлено',
        readme=GOOD_README.replace('плагинов, {total} навыков', 'плагинов, 99 навыков')))

    results.append(case(
        'дубль раздела H2 в README', True, 'встречается 2 раза',
        readme=GOOD_README.replace('## License', '## Быстрый старт')))

    results.append(case(
        'числа апстрима не совпадают (README 151 vs domains-status 111)', True, 'апстрим',
        readme=GOOD_README,
        domains_status='# Статус\n\n> База: anthropics/claude-for-legal (111 навыков, 12 плагинов).\n'))

    results.append(case(
        'числа апстрима совпадают во всех документах — чисто', False,
        readme=GOOD_README,
        domains_status='# Статус\n\n> База: anthropics/claude-for-legal (151 навык, 12 плагинов).\n'))

    results.append(case(
        'доменный README занижает состав', True, 'фактически',
        readme=GOOD_README,
        domain_readme='```\n└── skills/                        # 99 навыков\n```\n'))

    # --- регрессии: логика, которую легко сломать ---
    results.append(case(
        'наше число рядом с упоминанием апстрима НЕ считается апстримным', False,
        readme=GOOD_README.replace(
            'полный перенос Claude-for-Legal под российское право.',
            'полный перенос claude-for-legal в наш стек: 12 плагинов, {total} навыков.')))

    results.append(case(
        'апстримное число (151) не сверяется с деревом', False,
        readme=GOOD_README,
        agents='# AGENTS\n\nСм. claude-for-legal (Anthropic, 151 навык). 12 плагинов, {total} навыков.\n'))

    results.append(case(
        'LICENSE = Apache-2.0 и бейдж Apache — корректно', False,
        readme=GOOD_README.replace('badge/License-MIT-green.svg', 'badge/License-Apache%202.0-yellow.svg')
                       .replace('здесь MIT', 'у нас Apache-2.0'),
        license_text='Apache License\nVersion 2.0, January 2004\n'))

    results.append(case(
        'частичное число («14 активных навыков») не сверяется с общим', False,
        readme=GOOD_README + '\nВ домене 14 активных навыков, остальные — provisional.\n'))

    results.append(case(
        'лицензия нашей адаптации в прозе не совпадает с LICENSE', True, 'а LICENSE — MIT',
        readme=GOOD_README.replace('здесь MIT', 'Адаптация © Osmosy, Apache-2.0'),
        domain_readme='## Источник\n\nАдаптация © Osmosy, Apache-2.0.\n'))

    results.append(case(
        'лицензия апстрима (Anthropic, Apache-2.0) — не наше заявление, чисто', False,
        readme=GOOD_README,
        domain_readme='## Источник\n\n[claude-for-legal](https://github.com/anthropics/claude-for-legal)\n'
                      '© Anthropic, Apache-2.0. Адаптация © Osmosy, MIT.\n'))

    results.append(case(
        'вторая формулировка («Адаптация под … © Osmosy, Apache-2.0») тоже ловится', True,
        'а LICENSE — MIT',
        readme=GOOD_README,
        domains_status='## Источник\n\nСкелет: claude-for-legal © Anthropic, Apache-2.0.\n'
                       'Адаптация под право РФ и Hermes Agent © Osmosy, Apache-2.0.\n'))

    # Режимы самого скрипта: флаги не должны трактоваться как имена файлов
    # (регресс 02.09.2026: job ru-lint-warnings падал «not found: --warnings»).
    for flag, expect in (('--warnings', 0), ('--strict', None)):
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            make_repo(tmp, readme=GOOD_README)
            r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), flag],
                               cwd=tmp, capture_output=True, text=True)
            bad = 'not found: --' in r.stdout or r.returncode == 2
            if flag == '--warnings' and r.returncode != 0:
                bad = True
            print(('FAIL  ' if bad else 'ok    ') + f'{flag} не трактуется как имя файла')
            results.append(not bad)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    ok = sum(results)
    print(f'\n{ok}/{len(results)} тестов прошло')
    return 0 if ok == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
