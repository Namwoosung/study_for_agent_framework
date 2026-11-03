"""Attach the current slide's reading guide to both explanation surfaces."""
def add_explanations(slides, root):
    path = root / 'docs/slide-explanations.txt'
    guides = {}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        ident, reading, application = (field.strip() for field in line.split('|'))
        if ident in guides or not (reading and application):
            raise ValueError(f'Invalid explanation for {ident}')
        guides[ident] = {'reading': reading, 'application': application}
    ids = {slide['id'] for slide in slides}
    if ids != guides.keys():
        raise ValueError(f'Missing guides: {ids - guides.keys()}, obsolete guides: {guides.keys() - ids}')

    supplemental = {
        'S01': [('GUIDE', 'Anthropic · Building effective agents (설계 패턴)',
                 'https://www.anthropic.com/research/building-effective-agents')],
        'OAI05': [('GUARD', 'OpenAI Agents SDK · Guardrails', 'https://openai.github.io/openai-agents-python/guardrails/')],
        'CC11': [('HOOK-FAIL', 'Claude Code · Block the action when a hook fails',
                  'https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails')],
    }
    for slide in slides:
        ident = slide['id']
        slide['readingGuide'] = guides[ident]
        slide['note'] += '\n\n### 화면 읽기\n\n' + guides[ident]['reading']
        slide['note'] += '\n\n### 적용 예와 확인할 경계\n\n' + guides[ident]['application']
        slide['sources'].extend(supplemental.get(ident, []))
        if ident in {'S15', 'PA52'}:
            runtime = 'hermes' if ident == 'S15' else 'pydanticai'
            slide.setdefault('localEvidence', []).append({
                'path': f'demos/{runtime}/run.py', 'sections': '모델 연결과 실제 데모 시나리오 정의',
            })
