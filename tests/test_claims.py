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
import zipfile

VALIDATE = pathlib.Path(__file__).resolve().parent.parent / 'scripts' / 'validate.py'


def make_repo(tmp: pathlib.Path, *, skills: int = 3, readme: str = '', agents: str = '',
              agent_description: str = '', license_text: str = 'MIT License\n\nCopyright (c) 2026 Osmosy\n',
              domain_readme: str | None = None, domains_status: str = '',
              list_skills: bool = True, skill_body: str = 'тело\n',
              extra_files: dict[str, str | bytes] | None = None,
              claim_docs: dict[str, str] | None = None) -> pathlib.Path:
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
            '---\nname: skill-%d\ndescription: demo\nargument-hint: "[демо]"\n---\n\n' % i + skill_body,
            encoding='utf-8')
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
    if claim_docs:
        for rel, content in claim_docs.items():
            p = tmp / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding='utf-8')
    if domain_readme is not None:
        text = domain_readme.format(skills=skills)
        if list_skills:  # доменный README обязан называть каждый навык
            text += '\n' + ''.join(f'- skill-{i}\n' for i in range(skills))
        (tmp / 'demo-legal' / 'README.md').write_text(text, encoding='utf-8')
    for rel, content in (extra_files or {}).items():
        path = tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding='utf-8')
    return tmp


def pptx_bytes(*slides: list[str]) -> bytes:
    """Минимальный .pptx для проверки: только ppt/slides/slideN.xml с <a:t>."""
    import io
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        for i, runs in enumerate(slides, 1):
            body = ''.join(f'<a:t>{r}</a:t>' for r in runs)
            z.writestr(f'ppt/slides/slide{i}.xml', f'<p:sld>{body}</p:sld>')
    return buf.getvalue()


COOKBOOK = {'cookbooks/reg-monitor/cron-spec.yaml': 'schedule: "0 9 * * 1"\n',
            'cookbooks/docket-watcher/cron-spec.yaml': 'schedule: "0 8 * * *"\n'}
AGENTS_SECTION = ('\n## Агенты мониторинга\n\n| Агент | Что |\n|---|---|\n'
                  '| reg-monitor | НПА |\n| docket-watcher | суды |\n')


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

    # --- согласованность, аудит 24.09.2026 ---
    results.append(case(
        'навык домена не упомянут в его README', True, 'не упомянут',
        readme=GOOD_README, domain_readme='# Demo\n\nskill-0 и skill-1.\n', list_skills=False))

    results.append(case(
        'битая относительная ссылка в markdown', True, 'несуществующий',
        readme=GOOD_README + '\nСм. [коннекторы](../../CONNECTORS.md).\n'))

    results.append(case(
        'ссылка на существующий файл и на URL — чисто', False,
        readme=GOOD_README + '\nСм. [лицензию](LICENSE) и [апстрим](https://example.org/x.md).\n'))

    results.append(case(
        'SKILL.md ссылается на отсутствующий references/*.md', True, 'рядом с навыком',
        readme=GOOD_README, skill_body='Чеклист — в `references/output-format.md`.\n'))

    results.append(case(
        'агент мониторинга в README без cron-спеки', True, 'нет cookbooks/ghost-watcher',
        readme=GOOD_README + AGENTS_SECTION + '| ghost-watcher | призрак |\n', extra_files=COOKBOOK))

    results.append(case(
        'cron-спека не описана в README', True, 'нет строки для cookbooks/docket-watcher',
        readme=GOOD_README + AGENTS_SECTION.replace('| docket-watcher | суды |\n', ''),
        extra_files=COOKBOOK))

    results.append(case(
        'неверное число агентов мониторинга в тексте', True, 'cron-спек в cookbooks/ 2',
        readme=GOOD_README + AGENTS_SECTION + '\nФон: 8 агентов мониторинга.\n', extra_files=COOKBOOK))

    results.append(case(
        'агенты мониторинга совпадают с cookbooks — чисто', False,
        readme=GOOD_README + AGENTS_SECTION + '\nФон: 2 cron-агента.\n', extra_files=COOKBOOK))

    results.append(case(
        'пример USER-GUIDE ведёт в навык чужого домена', True, 'ведёт в «cease-desist»',
        readme=GOOD_README,
        extra_files={'USER-GUIDE.md': '**Demo-legal:**\n- «претензия по ИС» → `cease-desist`\n'}))

    results.append(case(
        'пример USER-GUIDE ведёт в навык своего домена — чисто', False,
        readme=GOOD_README,
        extra_files={'USER-GUIDE.md': '**Demo-legal:**\n- «сделай X» → `skill-1`\n'}))

    results.append(case(
        'презентация: устаревшее число навыков', True, 'слайд 1',
        readme=GOOD_README,
        extra_files={'deck.pptx': pptx_bytes(['12', 'плагинов', '99', 'навыков'])}))

    results.append(case(
        'презентация: лицензия адаптации Apache при MIT', True, 'лицензия адаптации не MIT',
        readme=GOOD_README,
        extra_files={'deck.pptx': pptx_bytes(['Адаптация (Osmosy, Apache-2.0) — русское право'])}))

    results.append(case(
        'презентация: число апстрима и верная лицензия — чисто', False,
        readme=GOOD_README,
        extra_files={'deck.pptx': pptx_bytes(
            ['Основа: anthropics/claude-for-legal (Anthropic, Apache-2.0) — 151 навык',
             'Адаптация (Osmosy, MIT)', '{total}', 'навыков'.replace('{total}', '4')])}))

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

    # name во фронтматтере = имени каталога (докстринг validate.py обещал это с
    # самого начала, но проверки не было до 24.09.2026).
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README)
        skill = tmp / 'demo-legal' / 'skills' / 'skill-0' / 'SKILL.md'
        skill.write_text(skill.read_text(encoding='utf-8').replace('name: skill-0', 'name: other'),
                         encoding='utf-8')
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py')],
                           cwd=tmp, capture_output=True, text=True)
        bad = r.returncode != 1 or '!= каталог' not in r.stdout
        print(('FAIL  ' if bad else 'ok    ') + 'name во фронтматтере ≠ каталогу — ошибка')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Разбор advisories 27.09.2026: три класса ложного шума. Проверки должны
    # молчать на корректном дереве и ловить настоящий дефект.

    def _warn_repo(skill_body: str, skill_fm: str = '') -> tuple[str, int]:
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            make_repo(tmp, readme=GOOD_README, skill_body=skill_body)
            if skill_fm:
                p = tmp / 'demo-legal' / 'skills' / 'skill-0' / 'SKILL.md'
                p.write_text(p.read_text(encoding='utf-8').replace('description: demo', skill_fm),
                             encoding='utf-8')
            r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), '--warnings'],
                               cwd=tmp, capture_output=True, text=True)
            return r.stdout, r.returncode
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # 1. Тег [settled — подтверждено ДАТА] (формат из AGENTS.md) признаётся тегом.
    out, _ = _warn_repo('Срок — 10 рабочих дней (ст. 20 152-ФЗ) '
                        '`[settled — подтверждено 2026-09-27, КонсультантПлюс]`\n')
    bad = 'no provenance-tag' in out
    print(('FAIL  ' if bad else 'ok    ') + '[settled — подтверждено ДАТА] = валидный тег')
    results.append(not bad)

    # 2. Ссылка-ориентир на статью без числа тега не требует.
    out, _ = _warn_repo('Проверить по ст. 15 ГК и ст. 393 ГК: основания и последствия.\n')
    bad = 'no provenance-tag' in out
    print(('FAIL  ' if bad else 'ok    ') + 'ссылка на статью без факта — тег не требуется')
    results.append(not bad)

    # 3. Норма с конкретным числом без тега — предупреждение остаётся.
    out, _ = _warn_repo('Срок ответа — 10 рабочих дней (ст. 20 152-ФЗ), продление до 5.\n')
    bad = 'no provenance-tag' not in out
    print(('FAIL  ' if bad else 'ok    ') + 'норма с числом без тега — предупреждение')
    results.append(not bad)

    # 4. Упоминание маркера [PLACEHOLDER] в инструкции — не дефект.
    out, _ = _warn_repo('Если профиль содержит [PLACEHOLDER] — остановиться и сказать об этом.\n')
    bad = '[PLACEHOLDER] в SKILL.md' in out
    print(('FAIL  ' if bad else 'ok    ') + 'упоминание [PLACEHOLDER] в инструкции — не дефект')
    results.append(not bad)

    # 5. Незаполненный маркер в выдаваемом тексте — дефект.
    out, _ = _warn_repo('Резолюция: [PLACEHOLDER — заполнить содержание обсуждения]\n')
    bad = '[PLACEHOLDER] в SKILL.md' not in out
    print(('FAIL  ' if bad else 'ok    ') + 'незаполненный [PLACEHOLDER] — предупреждение')
    results.append(not bad)

    # 5b. Пример речи пользователя в «ёлочках» — не утверждение репозитория.
    out, _ = _warn_repo('Пользователь говорит «порог 6 млн», «по ст. 14.3 КоАП столько-то» —\n'
                        'сверить перед записью.\n')
    bad = 'no provenance-tag' in out
    print(('FAIL  ' if bad else 'ok    ') + 'пример речи в «ёлочках» — тег не требуется')
    results.append(not bad)

    # 6. argument-hint нужен вызываемым навыкам, но не reference-навыкам.
    out, _ = _warn_repo('тело про ревизию договора\n', skill_fm='description: demo\nuser-invocable: false')
    bad = 'missing argument-hint' in out
    print(('FAIL  ' if bad else 'ok    ') + 'user-invocable: false — argument-hint не требуется')
    results.append(not bad)

    # 6b. Тот же навык, но argument-hint убран — предупреждение возвращается.
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README, skill_body='тело про ревизию договора\n')
        p = tmp / 'demo-legal' / 'skills' / 'skill-0' / 'SKILL.md'
        p.write_text(p.read_text(encoding='utf-8').replace('argument-hint: "[демо]"\n', ''),
                     encoding='utf-8')
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), '--warnings'],
                           cwd=tmp, capture_output=True, text=True)
        bad = 'missing argument-hint' not in r.stdout
        print(('FAIL  ' if bad else 'ok    ') + 'hint убран у вызываемого навыка — предупреждение')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 6b. CLAUDE.md (шаблон практики) участвует в проверке лицензии адаптации:
    #     англоязычная строка «adaptation of … Apache-2.0» при MIT — ошибка.
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README, claim_docs={
            'corporate-legal/CLAUDE.md':
                '*Перезапуск: `cold-start-interview --redo`. Шаблон по умолчанию\n'
                '(adaptation of commercial-legal/CLAUDE.md, Apache-2.0).*\n'})
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), '--claims'],
                           cwd=tmp, capture_output=True, text=True)
        bad = 'LICENSE — MIT' not in r.stdout
        print(('FAIL  ' if bad else 'ok    ') + 'CLAUDE.md: adaptation … Apache-2.0 при MIT — ошибка')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 6c. Атрибуция апстрима (Anthropic, Apache-2.0) — законна, ошибкой не считается.
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README, claim_docs={
            'AGENTS.md': 'Скелет: claude-for-legal © Anthropic, Apache-2.0 (апстрим).\n'})
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), '--claims'],
                           cwd=tmp, capture_output=True, text=True)
        bad = 'LICENSE — MIT' in r.stdout
        print(('FAIL  ' if bad else 'ok    ') + 'атрибуция «© Anthropic, Apache-2.0» — не ошибка')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 6d. Заявление о числе навыков в CLAUDE.md сверяется с деревом.
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README, claim_docs={
            'corporate-legal/CLAUDE.md': 'В домене 999 навыков.\n'})
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), '--claims'],
                           cwd=tmp, capture_output=True, text=True)
        bad = '999 навык' not in r.stdout
        print(('FAIL  ' if bad else 'ok    ') + 'CLAUDE.md: «999 навыков» против дерева — ошибка')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 6e. Верное число в CLAUDE.md ошибкой не считается.
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README, claim_docs={
            'corporate-legal/CLAUDE.md': 'В домене {total} навыков.\n'.format(total=4)})
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), '--claims'],
                           cwd=tmp, capture_output=True, text=True)
        bad = 'навык' in r.stdout and 'LICENSE' in r.stdout
        print(('FAIL  ' if bad else 'ok    ') + 'CLAUDE.md: верное число навыков — чисто')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 6f. Отчёт, цитирующий дефект в «ёлочках», ошибкой не считается.
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README, claim_docs={
            'docs/report.md': 'Исправлено: «Адаптация … Apache-2.0» → MIT (слайды 1, 12).\n'})
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), '--claims'],
                           cwd=tmp, capture_output=True, text=True)
        bad = 'LICENSE — MIT' in r.stdout
        print(('FAIL  ' if bad else 'ok    ') + 'цитата дефекта в «ёлочках» — не ошибка')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 6g. Provenance в справочниках skills/*/references/*.md: норма с фактом
    #     без тега — ОШИБКА (задача A2 плана 27.09.2026: 15 справочников
    #     vector-check были написаны без единого тега, валидатор их не видел;
    #     после разбора advisories в справочниках стало 0, поэтому проверка
    #     переведена в ошибки — иначе новые справочники снова пойдут без
    #     источников). Тело навыка берём русское: иначе валидатор падает
    #     раньше по правилу «<5 кириллических знаков».
    RU_BODY = 'Проверка реестров и судебных дел для контрагента.\n'
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README, skill_body=RU_BODY, extra_files={
            'demo-legal/skills/skill-0/references/99-test.md':
                '# Тест\n\n| Норма | Что |\n|---|---|\n| ст. 30 ФЗ-14 | сделка оспорима (ст. 174 ГК) |\n'})
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py')],
                           cwd=tmp, capture_output=True, text=True)
        bad = 'no provenance-tag' not in r.stdout or r.returncode != 1
        print(('FAIL  ' if bad else 'ok    ') + 'справочник: норма с фактом без тега — ошибка')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 6h. Тот же справочник с тегом — чисто.
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README, skill_body=RU_BODY, extra_files={
            'demo-legal/skills/skill-0/references/99-test.md':
                '# Тест\n\n| Норма | Что |\n|---|---|\n| ст. 30 ФЗ-14 | сделка оспорима (ст. 174 ГК) '
                '`[settled — подтверждено 2026-09-27, КонсультантПлюс]` |\n'})
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), '--warnings'],
                           cwd=tmp, capture_output=True, text=True)
        bad = 'no provenance-tag' in r.stdout
        print(('FAIL  ' if bad else 'ok    ') + 'справочник: норма с фактом и тегом — чисто')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 6i. Справочник с числом навыков не ломает проверку состава (references
    #     не участвуют в подсчёте) и не даёт ложного «N навыков».
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        make_repo(tmp, readme=GOOD_README, skill_body=RU_BODY, extra_files={
            'demo-legal/skills/skill-0/references/99-test.md':
                '# Тест\n\nВ домене 999 навыков.\n'})
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'validate.py'), '--claims'],
                           cwd=tmp, capture_output=True, text=True)
        bad = '999 навык' in r.stdout
        print(('FAIL  ' if bad else 'ok    ') + 'справочник: произвольное число не считается заявлением')
        results.append(not bad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    ok = sum(results)
    print(f'\n{ok}/{len(results)} тестов прошло')
    return 0 if ok == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
