"""Connect implementation walkthroughs to concrete application decisions."""


def refine_purpose(slides, env):
    table = env['table']
    updates = {
        'S44': (
            '한 요청을 끝까지 검증하기',
            '모델 응답, 도구 실행, 업무 결과를 서로 연결해서 확인합니다.',
            [('입력', '요청 직전 messages·tools 확인', '지시·조회 범위·이력 전달'),
             ('실행', 'Tool Call ID와 실제 실행 연결', '검증 실패·승인 전에는 실행 0회'),
             ('결과', '원본 snapshot과 수치 비교', 'A17의 42 / 1000 = 4.2%'),
             ('복구', '실패 후 같은 업무 키로 재시도', '저장 성공 여부와 중복 발행 확인')],
            '테스트의 기대값은 답변 문장뿐 아니라 실행 횟수와 저장 상태에도 둡니다.'),
        'S45': (
            '내 Agent를 만들 때 결정할 것',
            'Hermes의 제공 기능과 PydanticAI의 조합 지점을 개발 선택으로 연결합니다.',
            [('어떤 작업을 맡길까?', '조회·분석·발행의 경계', '모델 판단 / 고정 업무 규칙'),
             ('어떤 기능을 줄까?', 'Tool과 실제 데이터 접근 범위', '읽기 / 쓰기 / 사용자 승인'),
             ('무엇을 다음 실행에 남길까?', '대화·기억·실행 상태·보고서', '저장 수명 / 복원 / 버전'),
             ('어떻게 맞았다고 확인할까?', '실행 기록과 원본 근거', '재시도 / 중복 방지 / 평가')],
            '3차에서는 같은 업무를 구현하고, 실행 경로와 검증 결과로 설계를 비교합니다.'),
    }
    for ident, (title, sub, rows, take) in updates.items():
        slide = slides[ident]
        detail = '\n\n'.join(f'{a} — {b}. {c}.' for a, b, c in rows)
        slide.update(title=title, sub=sub, take=take,
                     diagram=table(('개발 질문', '확인할 대상', '선택 기준'), rows,
                                   widths=[490, 610, 552], y=50, row_h=126),
                     steps=['전체 보기', *[row[0] for row in rows]],
                     concepts=[dict(term=a, meaning=b+' · '+c) for a,b,c in rows],
                     explanation=detail, note=detail)
    for slide in slides.values():
        section = slide['section']
        if slide['id'] in updates:
            slide['learningRole'] = '개발 판단'
        elif section.startswith('Hermes'):
            slide['learningRole'] = 'Harness 내부'
        elif section.startswith('PydanticAI'):
            slide['learningRole'] = 'SDK 내부'
        elif slide['id'].startswith(('CC', 'CAS', 'ADK', 'MAF', 'OAI')) or slide['id'] == 'SDKMAP':
            slide['learningRole'] = '실행 방식 비교'
        else:
            slide['learningRole'] = '발표 흐름'
