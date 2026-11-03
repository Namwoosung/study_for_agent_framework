"""Claude Code section for the second seminar."""
import json

ORDER = [
    'CLAUDE', 'CC01', 'CCA', 'CC02', 'CC03', 'CC04',
    'CCB', 'CC05', 'CC06', 'CC07', 'CC08',
    'CCC', 'CC09', 'CC10', 'CC11', 'CC12', 'CC13', 'CC14',
    'CCD', 'CC15', 'CC16', 'CC17', 'CC18', 'CC19', 'CC20',
    'CCE', 'CC21', 'CC22', 'CC23',
]
ALIASES = {'CC00': 'CLAUDE', 'S16': 'CC01', 'S17': 'CC03', 'S18': 'CC17', 'S19': 'CC22'}


def revise(slides, drawing):
    root = drawing['ROOT']
    text, box, arrow = (drawing[key] for key in ('text', 'box', 'arrow'))
    code, table = drawing['code_panel'], drawing['table']
    index = json.loads((root / 'research/claude-code-plan-sources.json').read_text(encoding='utf-8'))
    references = {r['id']: [(r['id'], link['title'], link['url']) for link in r['links']]
                  for r in index['references']}
    originals = {key: slides.pop(key) for key in ('S16', 'S17', 'S18', 'S19')}
    deep = index['localSources'][1]['path']
    comments = index['localSources'][2]['path']
    palette = ('context', 'runtime', 'tool', 'model')

    def flow(*nodes):
        width = 420 if len(nodes) == 3 else 350
        gap = (1652 - width * len(nodes)) / (len(nodes) - 1)
        result = ''
        for i, (name, desc) in enumerate(nodes):
            x = i * (width + gap)
            result += box(x, 180, width, 165, name, desc, palette[i])
            if i + 1 < len(nodes):
                result += arrow(f'M{x+width} 262 H{x+width+gap-14}', palette[i])
        return result

    def compare(headers, *rows):
        return table(headers, rows, widths=[370, 610, 672], y=85, row_h=115)

    def panel(caption, snippet, labels):
        result = code(0, 68, 920, 490, snippet, caption, 25)
        for i, (name, desc) in enumerate(labels):
            result += box(970, 95+i*150, 675, 118, name, desc, palette[i])
        return result

    def add(ident, title, sub, diagram, take, refs, section, detail, *concepts, kind='content-slide'):
        sources = [link for ref in refs.split() for link in references[ref]]
        evidence = [{'path': deep, 'sections': section}]
        if ident in ('CC15', 'CC23'):
            evidence.append({'path': comments, 'sections': '발표·실무 시사점'})
        old = next((originals[key] for key, value in ALIASES.items()
                    if key in originals and value == ident), None)
        slide = dict(id=ident, title=title, sub=sub, diagram=diagram, take=take,
                     steps=['전체 구성'], section='Claude Code', version='공식 문서 · 2026-11-03',
                     kind=kind, note=detail, explanation=detail, sources=sources, demo=None,
                     concepts=[dict(term=term, meaning=meaning) for term, meaning in concepts],
                     localEvidence=evidence)
        if old:
            slide['originalSpec'] = old['originalSpec']
            slide['sources'] += old['sources']
        slides[ident] = slide

    def divider(ident, title, sub, labels, refs, section, detail):
        diagram = text(0, 145, 'CLAUDE CODE', 27, 'context', 700)
        diagram += text(0, 253, title, 78, 'text', 700)
        diagram += text(0, 335, sub, 33, 'muted')
        for i, label in enumerate(labels):
            diagram += text(i*550, 475, f'{i+1:02}  {label}', 34, palette[i], 700)
        add(ident, title, sub, diagram, sub, refs, section, detail,
            (title, sub), kind='topic-divider')

    opener = text(0, 182, 'Claude Code', 86, 'text', 700)
    opener += text(0, 270, '코딩 작업을 위한 Agent Harness', 34, 'muted')
    opener += text(0, 394, 'Context · 실행 정책 · 위임', 30, 'context', 700)
    opener += box(1030, 40, 590, 112, 'CLI / Agent SDK', '사용자 또는 앱의 요청', 'context')
    opener += arrow('M1325 152 V218', 'context')
    opener += box(1030, 230, 590, 112, 'Claude Code Harness', '입력 구성 · 호출 · 결과 확인', 'runtime')
    opener += arrow('M1170 342 V408', 'model') + arrow('M1470 342 V408', 'tool')
    opener += box(1030, 420, 280, 112, 'Model', '다음 행동 판단', 'model')
    opener += box(1330, 420, 290, 112, 'Tools', '코드 읽기와 수정', 'tool')
    add('CLAUDE', 'Claude Code', '코딩 작업을 위한 Agent Harness', opener,
        'Context, 실행 정책, 위임을 살펴봅니다.', 'D01 S01 S04', 'Part I',
        'Claude Code는 프로젝트를 읽고 도구를 호출하며 결과를 확인하는 코딩 Harness입니다. 도식은 CLI와 SDK에서 접근하는 실행 구조를 설명합니다. 로컬 교재의 비교 기준은 CLI v2.1.314입니다. 현행 문서의 기능은 각 기능에 필요한 제품 버전과 설정을 따릅니다.',
        ('Harness','모델, 프로젝트 지침, 도구와 실행 정책을 연결하는 환경'), kind='topic-divider')
    add('CC01', '코딩 작업은 어떻게 진행될까?', '정보를 모으고, 도구를 쓰고, 결과를 확인합니다.',
        flow(('Gather','코드와 지침 읽기'), ('Act','Tool 실행 요청'), ('Verify','결과 확인과 다음 판단'))
        + arrow('M1442 345 V430 H210 V359', 'context')
        + text(826, 470, '추가 확인이 필요한 경우', 24, 'muted', 400, 'middle'),
        '결과가 더 필요하면 정보를 다시 모읍니다.', 'D01 S01', 'Part I · W01',
        'Hermes에서 본 모델·Tool·관찰의 반복을 그대로 연결해 설명합니다. Claude Code에서는 지침을 읽는 시점, Tool을 공개하는 방식, 권한 판정과 위임이 개입하는 지점을 살펴봅니다. 이 도식은 공식 문서의 동작을 요약한 개념도입니다.',
        ('Gather / Act / Verify','정보 수집, 실행, 검증이 반복되는 작업 흐름'))
    divider('CCA','Context와 기억','모델에 들어가는 입력과 다음 세션에 남는 기록',
            ('요청의 세 계층','지침 로딩','Auto Memory'), 'D02 D03 D04 D05','Part II–III',
            '먼저 요청의 논리 계층을 소개하고 프로젝트 지침과 기억 파일이 어느 시점에 들어오는지 살펴봅니다. 대화 재개와 저장소 파일의 현재 상태도 구분합니다.')
    add('CC02','모델 입력의 세 계층','고정 지침 위에 프로젝트 정보와 대화가 쌓입니다.',
        compare(('계층','입력 예시','들어오는 시점'),
                ('System','제품 지침과 Tool 정의','세션 및 실행 구성에 따라 준비'),
                ('Project','프로젝트 지침과 환경 정보','시작 또는 관련 경로 접근'),
                ('Conversation','질문, 응답, 도구 결과','턴이 진행되며 누적')),
        '세 계층은 요청을 이해하기 위한 구분입니다.', 'D02 D03','Part II · W02',
        '공식 캐싱 문서가 설명하는 System, Project, Conversation의 논리적 계층입니다. 도구 가용성이나 설정이 바뀌면 앞쪽 입력도 달라질 수 있습니다. 각 계층은 이해를 위한 묶음이며 실제 요청의 필드와 메시지 배열은 연결 방식에 따라 확인합니다.',
        ('Context','이번 모델 호출에 사용되는 지침, 대화와 도구 정보'))
    add('CC03','어떤 지침을 언제 읽을까?','파일 위치와 적용 조건이 로딩 시점을 결정합니다.',
        compare(('위치','읽는 시점','확인할 조건'),
                ('CLAUDE.md','사용자·프로젝트 지침은 시작 시','하위 폴더 지침은 관련 파일 접근 시'),
                ('.claude/rules/','전역 또는 일치하는 경로 작업 시','frontmatter의 paths 설정'),
                ('AGENTS.md','직접 로딩 또는 명시적 import','CLI 버전과 지침 파일 선택 설정')),
        '/memory에서 현재 적용 중인 지침을 확인할 수 있습니다.', 'D04','Part III · W04',
        '관리형, 사용자, 프로젝트 지침이 적용되는 위치를 먼저 구별합니다. 현행 문서에서 instructionFiles 기본값은 claude-md-or-agents-md입니다. 작업 디렉터리와 상위 경로에 CLAUDE.md 또는 CLAUDE.local.md가 없을 때 AGENTS.md를 읽습니다. claude-md-and-agents-md로 둘 다 읽을 수 있습니다. 내장 Plugin 비활성이나 이전 버전에서는 CLAUDE.md의 @AGENTS.md import를 사용할 수 있습니다. 직접 로딩은 InstructionsLoaded를 발생시키지 않으며 import는 해당 이벤트를 발생시킵니다.',
        ('경로 규칙','일치하는 파일을 다룰 때 적용하는 프로젝트 지침'))
    add('CC04','Auto Memory는 색인부터 읽습니다','자주 쓰는 내용은 MEMORY.md에, 상세 기록은 Topic 파일에 둡니다.',
        flow(('세션 시작','MEMORY.md 색인'), ('필요한 주제','Topic 파일 읽기'), ('학습 내용','Claude가 갱신')),
        '시작 시 색인의 앞 200줄 또는 25KB까지 읽습니다.', 'D04 D05','Part III · W05',
        'Auto Memory를 활성화한 환경에서 저장소별 기억은 worktree 사이에 공유됩니다. 시작 로딩은 200줄과 25KB 중 먼저 도달한 한도까지이며 상세 파일은 필요할 때 읽습니다. Hermes의 기억 파일과 비교할 수 있고, Hermes의 Session FTS는 이전 대화를 검색하는 별도 기능입니다. Claude Code의 resume 역시 대화 이력을 이어가는 별도 동작입니다.',
        ('Auto Memory','Claude가 작업에서 발견한 사실과 선호를 저장하는 파일 기반 기억'))
    divider('CCB','Tools와 Skills','도구 명세와 작업 절차를 필요한 때 불러옵니다.',
            ('Tool Search','Skill 호출','Plugin 배포'),'D06 D07 D09','Part IV',
            '모델에 도구 이름과 스키마가 공개되는 시점부터 살펴봅니다. 이어서 Skill 본문과 권한의 수명, 여러 구성 요소를 배포하는 Plugin을 설명합니다.')
    add('CC05','필요한 MCP Tool의 명세를 불러오기','ToolSearch로 작업에 맞는 명세를 요청합니다.',
        flow(('후보 정보','이름과 서버 지침'), ('ToolSearch','필요한 도구 찾기'), ('명세 로딩','선택한 도구의 스키마')),
        '호환 모델에서는 지연 로딩이 기본이며 auto는 임계값 모드입니다.', 'D06','Part IV · W06',
        '지연 로딩으로 시작 요청에 들어가는 전체 도구 명세의 양을 줄입니다. ENABLE_TOOL_SEARCH=auto는 10% 임계값 모드이고 auto:N은 비율을 지정합니다. 비호환 모델이나 일부 제공자 경로에서는 먼저 로딩할 수 있습니다. Gateway가 beta 헤더나 defer_loading을 처리하는지도 확인합니다.',
        ('ToolSearch','지연 공개된 Tool의 상세 스키마를 찾는 도구'))
    add('CC06','Skill 본문과 권한의 수명','본문이 대화에 남는 동안에도 사전 승인은 호출 턴에만 적용됩니다.',
        panel('Skill frontmatter 예시', '---\nname: review-changes\ndescription: Review changed files\nallowed-tools: Read, Grep\n---', [
            ('호출','사용자 명령 또는 모델 선택'), ('본문','호출 뒤 대화에 남을 수 있음'), ('사전 승인','지정 Tool에 호출 턴 동안 적용')]),
        '도구 범위를 제한할 때는 권한 규칙도 확인합니다.', 'D07 D10','Part IV · W07',
        'Skill의 이름과 설명으로 호출 여부를 판단하고 호출 시 본문을 읽습니다. 사용자나 모델의 호출 가능 여부는 frontmatter로 제어할 수 있습니다. allowed-tools는 해당 호출 턴에서 지정 도구의 사전 승인을 다룹니다. 사용 가능한 도구 자체를 제한하는 disallowed-tools나 관리형 권한과 적용 범위가 다릅니다.',
        ('allowed-tools','Skill이 호출된 턴에 적용되는 도구 사전 승인 설정'))
    add('CC07','Skill fork와 대화 fork의 입력','자식에게 무엇을 전달하는지 비교합니다.',
        compare(('경로','자식의 시작 입력','결과의 행선지'),
                ('Skill context: fork','Skill 본문이 작업 입력','호출자에게 결과 전달'),
                ('대화 fork','현재 대화에서 분기','분기한 대화에서 계속 작업'),
                ('Subagent의 skills','지정 Skill을 시작에 로드','역할 지침과 함께 자식에서 사용')),
        '어느 쪽에서 Skill을 지정하는지에 따라 로딩 방향이 달라집니다.', 'D07 D08','Part IV · W07',
        'Skill의 context: fork는 Skill 내용을 별도 Subagent에게 작업으로 넘깁니다. agent 필드로 사용할 역할을 지정할 수 있습니다. 반대로 Subagent 설정의 skills는 자식 시작 때 지정한 지침을 미리 넣습니다. 대화 fork는 기존 대화를 분기하는 별도 경로입니다.',
        ('context: fork','Skill 본문을 별도 실행 Context로 전달하는 설정'))
    add('CC08','Plugin으로 작업 환경을 배포하기','프로젝트마다 쓰던 확장 구성을 한 묶음으로 공유합니다.',
        panel('Plugin 디렉터리 예시', 'review-kit/\n  .claude-plugin/plugin.json\n  skills/review/SKILL.md\n  agents/reviewer.md\n  hooks/hooks.json\n  .mcp.json', [
            ('Manifest','이름과 구성 위치'), ('실행 구성','Skills · Agents · Hooks · MCP')]),
        'Hermes의 register(ctx)와 Claude Plugin은 확장 접점이 다릅니다.', 'D09 D10','Part IV · W08',
        'Claude Code Plugin은 문서, 설정, 외부 연결을 묶는 배포 단위입니다. Hermes의 register(ctx)는 Python 확장 등록 인터페이스입니다. Claude Code에서 코드로 권한 판정에 관여하는 Mods는 Plugin manifest와 별도이며 적용 가능한 환경과 정책을 권한 장에서 확인합니다.',
        ('Plugin','공유하고 설치할 수 있는 확장 구성 패키지'))
    divider('CCC','안전장치와 실행 기록','Tool을 실행하기 전의 판단과 실행 후에 남는 기록',
            ('권한과 Hook','Bash Sandbox','OTel과 Trace'),'D10 D11 D12 D13','Part V · Part VII',
            'Permission, Hook, Sandbox가 각각 제어하는 범위를 살펴봅니다. 이어서 대화 기록과 별도로 수집할 수 있는 지표, 이벤트와 Trace를 비교합니다.')
    add('CC09','권한 규칙은 Tool 호출에 적용됩니다','같은 Bash 호출도 규칙과 모드에 따라 결과가 달라집니다.',
        panel('settings.json 일부', '{\n  "permissions": {\n    "deny": ["Bash(rm *)"],\n    "ask": ["Bash(git push *)"],\n    "allow": ["Bash(git status *)"]\n  }\n}', [
            ('deny','일치하면 호출 차단'), ('ask','승인 필요'), ('allow','일치하는 호출 허용')]),
        '규칙은 deny, ask, allow 순으로 확인합니다.', 'D10 D11','Part V · W09',
        '예시는 규칙 우선순위를 설명하는 일부 설정입니다. 적용 규칙은 사용자·프로젝트·관리형 설정을 확인합니다. Plan은 탐색 중심의 모드이고 Auto의 자동 판단은 지원 환경과 별도 정책을 따릅니다. 일반 Hook allow는 명시적인 deny/ask를 우회하지 않습니다. Mod tool.check가 개입하는 조건은 로그인, 모드와 관리형 설정에 따라 공식 권한 문서를 대조합니다.',
        ('Permission rule','Tool 이름과 인자 패턴에 적용하는 실행 정책'))
    add('CC10','PreToolUse가 받는 입력과 돌려주는 결정','Tool 이름과 인자를 확인한 뒤 실행 전에 판단합니다.',
        panel('Command hook 응답 JSON 예시', '{\n  "hookSpecificOutput": {\n    "hookEventName": "PreToolUse",\n    "permissionDecision": "deny",\n    "permissionDecisionReason":\n      "Protected path"\n  }\n}', [
            ('matcher','이벤트가 적용될 Tool 선택'), ('tool_input','명령 또는 파일 인자 확인'), ('updatedInput','필요 시 실행 인자 수정')]),
        'PostToolUse는 실행 결과를 받고 Stop은 응답 종료에 개입합니다.', 'D11','Part V · W10',
        'Command hook은 stdin의 JSON에서 tool_name과 tool_input을 읽고 stdout으로 결정 JSON을 돌려줍니다. 예를 들어 handler에서 보호 경로와 일치하는지를 검사하고 이 JSON을 출력합니다. 입력을 수정하는 updatedInput과 실행 허용 여부인 permissionDecision은 서로 다른 필드입니다. 실행 뒤의 PostToolUse는 앞서 일어난 부작용을 되돌리는 단계가 아닙니다.',
        ('PreToolUse','Tool이 실행되기 전 호출되는 Hook 이벤트'))
    add('CC11','Hook이 실패하면 실행은 계속될까?','정책 거부와 handler 오류는 결과가 다릅니다.',
        compare(('상황','일반 PreToolUse 처리','확인할 예외'),
                ('명시 deny / exit 2','호출을 차단','구조화 결정과 종료 코드를 구분'),
                ('일반 오류','통상 기존 권한 흐름으로 진행','command/http onFailure: block'),
                ('timeout','통상 결정 없이 권한 흐름으로','SDK callback timeout은 차단'),
                ('onFailure: block','지원 조건에서 실패도 차단','네이티브 Windows 예외 확인')),
        '정책용 Hook은 오류와 timeout까지 별도로 시험합니다.', 'D11','Part V · W10',
        '실행 파일을 찾지 못하거나 명시적 거부 없이 종료 코드 1로 끝난 경우, 일반적으로 정책 결정이 없어 정상 권한 흐름으로 이어집니다. command/http Hook은 onFailure 설정으로 실패 차단을 요청할 수 있으며 플랫폼과 이벤트별 제약이 있습니다. SDK callback timeout의 동작은 별도입니다. Hermes의 실패 차단 Hook과 비교할 때 같은 실패 유형을 대응시킵니다.',
        ('onFailure','지원되는 Hook에서 실패 시 실행 처리 방식을 정하는 설정'))
    add('CC12','Bash Sandbox가 제한하는 범위','권한 판정 뒤 Shell 프로세스의 파일과 네트워크 접근을 제한합니다.',
        flow(('Permission','호출 허용 범위'), ('Sandbox 구성','파일·네트워크 정책'), ('격리된 Bash','정책이 적용된 상태로 실행')),
        '파일 Tool, MCP 서버, Hook은 각각의 실행 경계를 확인합니다.', 'D12 S02 S03','Part V',
        'Sandbox Runtime은 공개 부품입니다. 공개 API는 SandboxManager.initialize로 정책을 설정하고 wrapWithSandbox로 실행 명령을 감싸는 경로를 제공합니다. 이 API를 CLI 내부 호출의 증거로 쓰지 않습니다. 현행 Claude Code 문서는 네이티브 Windows에서 제품 Shell Sandbox가 적용되지 않는다고 설명합니다. 독립 Runtime의 플랫폼 지원과 제품 적용 범위는 별개입니다.',
        ('Sandbox','프로세스의 파일 및 네트워크 접근을 운영체제 수준에서 제한하는 경계'))
    add('CC13','지표, 이벤트, Trace는 무엇을 남길까?','기록 목적에 맞춰 수집과 내보내기를 설정합니다.',
        panel('Console metrics 설정 예시', 'export CLAUDE_CODE_ENABLE_TELEMETRY=1\nexport OTEL_METRICS_EXPORTER=console', [
            ('Metrics','세션 수, 토큰, 비용의 집계'), ('Events','Tool 결정과 실행 같은 사건'), ('Trace','한 요청에 속한 작업과 시간')]),
        '기본 비활성인 Trace는 별도의 활성화 설정을 확인합니다.', 'D13','Part VII · W14',
        '로컬 대화 기록과 OpenTelemetry 수집은 목적과 수명이 다릅니다. 환경 변수로 telemetry와 exporter를 선택합니다. 분산 Trace는 CLAUDE_CODE_ENABLE_TELEMETRY=1, CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1, OTEL_TRACES_EXPORTER 설정을 조합해 활성화합니다. 상세 beta 수집과 사용자 입력, Tool 내용의 수집 조건은 별도로 확인합니다. Hermes와 비교할 때는 Gateway 상태 지표와 대화 실행 Trace의 기록 단위를 구분합니다.',
        ('OpenTelemetry','지표, 로그와 Trace를 수집하고 내보내기 위한 표준'))
    add('CC14','승인 대기와 실행 시간을 나눠 보기','Tool span 안에서 사람이 기다린 시간과 실제 실행 시간을 읽습니다.',
        panel('공식 span 관계의 축약도', 'claude_code.interaction\n  +-- claude_code.llm_request\n  +-- claude_code.hook  (detailed beta)\n  +-- claude_code.tool\n        +-- blocked_on_user\n        +-- execution\n        +-- child agent spans', [
            ('모델 실패','llm_request 상태 확인'), ('승인과 실행','대기와 실행 구간 분리'), ('상관관계','trace_id와 span_id 연결')]),
        '입력과 출력 내용의 수집 범위는 별도 설정으로 결정합니다.', 'D13','Part VII · W14',
        '도식은 공식 span 계층을 축약한 예시입니다. blocked_on_user와 execution의 전체 이름에는 claude_code.tool 접두사가 붙습니다. Tool 실패, 권한 거부와 API 오류는 발생 위치가 다릅니다. Agent SDK와 비대화형 실행은 조건에 따라 상위 TRACEPARENT를 이어받습니다. 사용자 입력, 도구 세부 정보, 상세 beta payload는 각 수집 조건을 확인합니다.',
        ('Span','작업의 시작과 끝, 속성, 상위 작업과의 관계를 기록하는 단위'))
    divider('CCD','긴 작업과 위임','길어진 대화는 정리하고 독립된 작업은 나눕니다.',
            ('캐시와 압축','Subagent와 Teams','격리와 복구'),'D02 D03 D08 D14 D15','Part II · Part VI',
            'Prefix Cache와 압축이 입력에 주는 영향을 설명합니다. 이어서 위임할 때 전달하는 Context, 작업 공간 격리와 복원 가능한 상태를 비교합니다.')
    add('CC15','변경이 캐시에 미치는 범위','재사용할 수 있는 입력과 근거의 최신성을 따로 확인합니다.',
        compare(('변경 예시','캐시에서 볼 부분','업무에서 볼 부분'),
                ('모델·Tool 구성','앞쪽 요청 구성의 변경','도구 가용성과 모델 호환성'),
                ('파일·Skill 갱신','변경 내용이 입력된 위치','최신 파일을 다시 읽었는가'),
                ('대화 압축','Conversation 입력이 재구성','근거와 제약이 요약에 남았는가')),
        '캐시 적중은 같은 입력의 재사용을 보여 줍니다.', 'D02 D03','Part II · W03',
        'Hermes에서 본 Prefix Cache 원리와 연결합니다. 실제 무효화 범위는 변경된 입력 위치와 캐시 경계에 달려 있습니다. 예를 들어 SOP가 바뀌었어도 모델이 최신 파일을 다시 읽었는지는 별도로 확인해야 합니다. 캐시 효율과 업무 근거의 최신성을 같은 지표로 보지 않습니다.',
        ('Prefix Cache','동일한 앞쪽 입력의 처리를 재사용하는 캐시'))
    add('CC16','압축 뒤에는 무엇을 다시 읽을까?','대화 요약과 재주입되는 지침을 분리해 봅니다.',
        flow(('압축 전','긴 대화와 Tool 결과'), ('대화 요약','결정·남은 작업 정리'), ('재주입','루트 지침과 관련 내용')),
        '중요 파일과 경로 규칙은 다음 작업에서 다시 확인합니다.', 'D03 D04 D07','Part II · W03',
        '압축 뒤 루트 지침이 다시 들어오는 동작, 파일 접근으로 발동하는 경로 규칙, 사용한 Skill의 제한된 재주입을 구분합니다. 요약에는 진행 상황을 남기고 정확한 파일 내용이나 수치가 필요하면 원본을 다시 읽습니다. 이 흐름은 문서의 로딩 규약을 설명하기 위한 가상 예시입니다.',
        ('Compaction','대화 일부를 요약으로 바꿔 모델 입력의 공간을 확보하는 과정'))
    add('CC17','Subagent의 역할을 파일로 정의하기','역할 설명과 실행에 필요한 도구를 선택합니다.',
        panel('.claude/agents/reviewer.md 예시', '---\nname: reviewer\ndescription: Review changed files\ntools: Read, Grep, Glob\nmodel: inherit\n---\nCheck correctness and report findings.', [
            ('description','위임 대상을 고를 때 사용'), ('본문','자식의 역할 지침'), ('설정','도구·모델·권한·기억 범위')]),
        '부모는 작업을 전달하고 자식의 결과를 받습니다.', 'D08','Part VI · W11',
        'Hermes와 공통인 위임 원리를 짧게 연결합니다. Claude Code는 Markdown frontmatter로 도구와 모델, permissionMode, memory, skills 등을 구성합니다. 일반 전문 Subagent는 별도 Context에서 작업을 시작합니다. 자식이 받는 시작 지침과 대화 범위는 자식 종류와 fork 여부에 따라 확인합니다.',
        ('Subagent','별도 역할과 Context로 위임받은 작업을 수행하는 Agent'))
    add('CC18','새 Context, 대화 fork, background','입력의 범위와 결과를 기다리는 방식은 독립된 선택입니다.',
        compare(('선택','입력과 실행','호출자에게 돌아오는 방식'),
                ('전문 Subagent','역할 지침과 위임 작업','결과 보고'),
                ('대화 fork','기존 대화에서 분기','분기한 작업의 결과'),
                ('Background','실행을 맡기고 다른 작업 진행','완료 알림 또는 결과 회수')),
        '중첩 위임은 자식의 도구와 실행 환경 조건을 따릅니다.', 'D05 D08','Part VI · W11',
        '전문 역할을 별도로 시작하는 방법과 대화 분기를 구분합니다. Foreground와 background는 실행을 기다리는 방식의 차이입니다. 현행 제품 문서는 중첩 위임과 named-agent 메시징도 다룹니다. 권한과 가용성 조건을 확인하고 공개되지 않은 스케줄러 구현을 추정하지 않습니다.',
        ('Background','부모가 다른 작업을 계속하는 동안 진행되는 실행'))
    add('CC19','Teams는 작업 목록과 메시지로 협업합니다','Lead와 여러 독립 세션이 작업 상태를 공유합니다.',
        compare(('요소','팀에서 맡는 일','공유 범위'),
                ('Lead','작업을 만들고 진행을 조정','팀 구성과 작업 목록'),
                ('Teammate','별도 Context에서 할당 작업 수행','작업 상태와 팀 메시지'),
                ('Task list','할당, 의존성, 완료 상태 관리','팀 전체가 참조')),
        'Agent Teams는 실험 기능이며 기본 비활성입니다.', 'D08 D14','Part VI · W12',
        'Teams의 핵심은 공유 작업 목록과 독립 세션 간 조정입니다. Subagent에서도 설정에 따라 메시징과 중첩 위임을 쓸 수 있으므로 통신 가능 여부만으로 두 구성을 구별하지 않습니다. 독립 작업의 비용, 충돌 가능성과 작업 상태를 함께 비교합니다.',
        ('Agent Teams','여러 Claude Code 세션을 공유 작업과 메시지로 조정하는 기능'))
    add('CC20','대화와 파일을 각각 복구하기','격리하는 대상과 되돌릴 수 있는 대상을 확인합니다.',
        compare(('기능','주로 관리하는 상태','적용 범위'),
                ('resume / fork','대화 이력','이어서 진행하거나 대화를 분기'),
                ('Worktree','작업 디렉터리','다른 Git 작업 트리에서 편집'),
                ('Checkpoint / rewind','추적된 파일 변경과 대화','선택한 시점과 복원 대상을 지정')),
        'Shell과 외부 서비스의 부작용은 별도의 복구 절차가 필요합니다.', 'D05 D08 D15','Part VI · W12',
        'Worktree의 파일 격리와 Subagent의 Context 격리를 구분합니다. Checkpoint는 편집 도구가 추적하는 변경에 적용되며 모든 Bash 변경이나 외부 호출을 복원하는 범위로 확대할 수 없습니다. Background 실행의 변경도 main checkpoint와 함께 보장된다고 가정하지 않습니다. Hermes와는 checkpoint를 켜는 방식과 추적 범위를 비교합니다.',
        ('Rewind','지원되는 대화·파일 상태를 선택한 지점으로 되돌리는 기능'))
    divider('CCE','예약과 활용','작업의 실행 위치와 일상적인 사용 흐름을 정합니다.',
            ('예약의 수명','작업별 명령','Harness 선택'),'D16 D05 D10','Part VII',
            '반복 작업을 등록할 때 실행 위치와 세션 의존성을 먼저 살펴봅니다. 이어서 프로젝트를 읽고 실행하고 검토할 때 활용할 명령을 소개합니다.')
    add('CC21','예약 작업은 어디에 남을까?','등록 정보의 수명과 실제 실행에 필요한 호스트를 구분합니다.',
        compare(('경로','실행 위치','실행 조건'),
                ('Session / /loop','현재 Claude Code 세션','세션 실행 및 유효 기간'),
                ('Desktop','설정한 로컬 환경','앱과 호스트의 상태'),
                ('Cloud','설정한 클라우드 환경','환경·연결·예약 설정')),
        '예시  /loop 10m 열린 PR의 상태를 확인해 줘', 'D16','Part VII · W15',
        '현재 문서의 Session 예약은 만료 여부와 저장 조건에 따라 resume 시 복원될 수 있습니다. 복원 가능한 예약과 세션이 꺼져 있는 동안 실제로 실행되는 예약은 별개의 조건입니다. Hermes Cron과 비교할 때 스케줄 저장 위치, 실행 프로세스, 만료와 복원 조건을 확인합니다.',
        ('Session 예약','세션의 실행 상태와 예약 수명에 영향을 받는 작업'))
    add('CC22','탐색, 실행, 검토에 필요한 명령','코드 검토를 시작해 결과를 정리하는 순서로 살펴봅니다.',
        compare(('시점','명령','확인할 내용'),
                ('탐색','/context · /memory','입력 사용량과 적용 중인 지침'),
                ('실행','/permissions · /hooks','허용 규칙과 실행 전후 검사'),
                ('검토','/compact · /resume · /rewind','대화 정리, 이어가기, 복구')),
        '작업에 필요한 명령을 실행 구조와 연결해 기억합니다.', 'D03 D04 D05 D10 D11 D15','Part VII',
        '코드 검토를 시작할 때 지침과 Context를 살피고 실행 전 권한과 Hook을 확인합니다. 대화가 길어지면 압축하고 다시 이어갈 때 세션을 선택합니다. 복구가 필요하면 대화와 파일의 복원 범위를 고릅니다. 명령의 가용성은 사용하는 버전과 인터페이스에서 확인합니다.',
        ('Slash command','CLI에서 구성과 작업 상태를 확인하거나 바꾸는 명령'))
    add('CC23','두 Harness에서 어디까지 바꿀 수 있을까?','바꾸려는 동작에 따라 수정할 계층을 고릅니다.',
        compare(('변경 요구','Hermes','Claude Code'),
                ('업무 지침과 절차','프로젝트 지침·Skills','CLAUDE.md·Rules·Skills'),
                ('도구와 실행 정책','Plugin·Tool·Backend','MCP·Plugin·권한·Hook'),
                ('실행기 자체','공개 코어를 수정할 수 있음','공개 설정·확장 계약으로 통합')),
        '이제 PydanticAI에서 개발자가 구성하는 실행 경로를 살펴봅니다.', 'D01 D09 D10 S01 S04','Part I · Part X',
        '업무 규칙을 수정하는 일과 Harness 실행기를 수정하는 일을 구분합니다. Hermes는 공개 코어를 직접 읽고 수정할 수 있습니다. Claude Code에서는 문서화된 설정과 확장 접점으로 필요한 동작을 구성합니다. Python Agent SDK의 공개 subprocess transport는 앱과 CLI의 통합 경계를 보여 줍니다. 다음 구간에서 Python으로 Agent 구성과 업무 코드를 직접 정의하는 PydanticAI를 살펴봅니다.',
        ('Agent SDK','Claude Code의 Agent 기능을 앱에서 호출하기 위한 인터페이스'))
