// Conceptual traces of the examples. These panels never execute Python.
export const aids = {
  LangChain: {
    'chapter-2': {
      title: '메시지로 따라가는 도구 호출',
      intro: 'MS-02를 조회하는 한 가지 실행 예시입니다. 각 단계를 열어 누가 무엇을 만들고 다음 단계로 어떤 값이 넘어가는지 확인하세요.',
      steps: [
        ['사용자', '질문 전송', 'user: MS-02 재고는?', '사용자 메시지가 모델에 전달됩니다. 재고 수량은 아직 입력에 없습니다.'],
        ['모델', '도구 요청', 'ai.tool_calls → get_stock(sku="MS-02")\nid: lookup-1', '모델은 함수 이름과 인자를 제안합니다. Python 함수 실행은 앱이 맡습니다.'],
        ['앱', '조회 및 결과 연결', 'tool.tool_call_id: lookup-1\ncontent: MS-02: 재고 0개', '도구 결과는 호출 ID로 요청에 대응됩니다. 결과 메시지가 다시 모델 입력에 들어갑니다.'],
        ['모델', '최종 응답', 'ai.content: MS-02는 품절입니다.', '이 예시에서 모델은 추가 도구 요청 없이 응답하고 루프가 끝납니다.'],
      ],
      link: ['chapter-6', '모의 모델로 호출 ID 검증하기'],
    },
    'chapter-3': {
      title: '출력 검증은 어디에서 멈추나',
      intro: '같은 스키마라도 값의 관계와 실제 재고까지 별도로 검사해야 합니다. 세 응답을 비교하세요.',
      steps: [
        ['타입 검사', '필드 타입 오류', '{"sku":"KB-01","status":"available","quantity":"많음"}', '수량을 정수로 해석할 수 없어 스키마 검증에서 실패합니다.'],
        ['업무 규칙', '형식 통과, 값의 관계 위반', '{"sku":"KB-01","status":"out_of_stock","quantity":7}', '필드별 타입은 맞지만 상태와 수량이 충돌합니다. 이 단원의 추가 검증기가 거부합니다.'],
        ['원장 대조', '형식과 규칙 통과, 수량 불일치', '{"sku":"KB-01","status":"available","quantity":6}', '값의 관계는 맞지만 예제 원장의 재고는 7개입니다. 도구 결과와 대조해야 발견할 수 있습니다.'],
      ],
    },
  },
  LangGraph: {
    'chapter-3': {
      title: '마지막 메시지가 다음 노드를 정한다',
      intro: '같은 모델 노드에서도 마지막 메시지의 도구 요청 유무에 따라 실행 경로가 갈립니다.',
      steps: [
        ['도구 요청 있음', '도구 노드로 이동', 'START → model → tools → model', 'tools_condition이 도구 노드를 선택합니다. ToolNode가 호출을 실행하고 결과 메시지를 상태에 더합니다.'],
        ['도구 요청 없음', '실행 종료', 'model → END', '추가로 실행할 도구가 없으므로 그래프가 종료합니다. 첫 응답에서 이 경로로 가면 조회도 실행되지 않습니다.'],
      ],
      link: ['chapter-5', '여러 조회의 결과를 병합하는 방법'],
    },
    'chapter-9': {
      title: '예약 요청의 세 갈래',
      intro: '초기 재고가 7개인 예약 그래프를 비교합니다. 경로를 열어 승인 대기와 재고 변경이 언제 일어나는지 확인하세요.',
      stock: [4, 7, 7],
      steps: [
        ['3개 요청 · 승인', '한 번만 차감', 'check → review [대기] → reserve → END\n재고: 7 → 7 → 4', '승인 대기에는 재고가 그대로입니다. 승인 후에만 3개가 차감됩니다. 같은 요청 ID의 재시도는 4개를 유지합니다.'],
        ['3개 요청 · 거절', '변경 없이 종료', 'check → review [대기] → END\n재고: 7 → 7', '거절하면 reserve 노드에 진입하지 않습니다.'],
        ['8개 요청', '검사에서 종료', 'check → END\n재고: 7', '재고가 부족하므로 승인 요청을 만들지 않습니다.'],
      ],
    },
  },
  Deep_Agents: {
    'chapter-3': {
      title: '위임에서 오가는 것은 무엇인가',
      intro: '부모와 조사 에이전트의 역할을 비교합니다. 단계별로 전달되는 입력과 반환값을 확인하세요.',
      steps: [
        ['부모', '조사 범위 전달', '대상: MS-02\n반환 요청: SKU, 수량, 근거 ID', '부모가 위임 요청에 필요한 정보를 명시합니다.'],
        ['조사 에이전트', '근거 조회', 'fetch_inventory("MS-02")\n→ INV-203: MS-02 마우스 재고 0개.', '조사 에이전트는 자기 컨텍스트에서 도구를 사용하고 결과를 부모에게 돌려줍니다.'],
        ['부모', '근거를 포함한 초안 작성', '/inventory.md\nMS-02 | 0개 | INV-203', '부모는 조사 요약을 받아 파일을 작성합니다. 요약에 필요한 값이 빠지면 원본을 확인하거나 재조사합니다.'],
      ],
    },
    'chapter-8': {
      title: '새 스레드에서는 어떤 파일이 보이나',
      intro: '아래는 이 단원의 CompositeBackend 예제입니다. 동일 계정과 프로세스를 유지한 상태에서 스레드만 바꿉니다.',
      steps: [
        ['작업 초안', '기본 백엔드로 이동', '/inventory.md → StateBackend\n다른 스레드: 조회되지 않음', '초안은 원래 스레드의 상태에 남습니다.'],
        ['보고서 양식', '경로에 따라 스토어로 이동', '/memories/format.md → StoreBackend\n다른 스레드: 표로 작성', '두 스레드가 같은 계정 네임스페이스를 사용합니다. 예제의 InMemoryStore는 프로세스 종료 뒤에는 유지되지 않습니다.'],
      ],
      link: ['chapter-7', '기본 백엔드의 스레드 분리 실습'],
    },
  },
  Oracle_Agent_Spec: {
    'chapter-2': {
      title: '어떤 것이 JSON 파일에 들어가나',
      intro: '조회 도구 계약과 구현의 경계를 따라가 보세요.',
      flow: ['Python 선언', 'JSON/YAML', '런타임 어댑터', '실행 객체'],
      steps: [
        ['PyAgentSpec', '도구 계약 선언', 'ServerTool(name="lookup_stock")\n입력: sku · 출력: stock', '에이전트 이름, 모델 ID, 시스템 지침과 도구 계약을 구성합니다.'],
        ['JSON/YAML', '정의 전달', 'stock-agent.json / stock-agent.yaml', '파일을 다른 팀에 전달할 수 있습니다. 실제 Python 함수 본문이나 업무 시스템 접근 권한은 별도로 준비합니다.'],
        ['어댑터', '도구 구현 연결', 'tool_registry["lookup_stock"] → 실행 구현', '로더가 선언을 대상 런타임 객체로 변환하고 같은 이름의 도구 구현을 연결합니다.'],
      ],
    },
    'chapter-8': {
      title: '같은 Flow, 다른 호출 인터페이스',
      intro: '두 런타임에서 같은 stock-flow.json을 사용합니다. 입력을 넘기는 위치와 결과를 읽는 위치가 어떻게 다른지 비교하세요.',
      steps: [
        ['WayFlow', '대화 객체에서 실행', 'start_conversation({"sku": "MS-02"})\n→ execute()\n→ status.output_values["stock"]', '결과는 MS-02: 재고 0개입니다. 종료 상태의 출력에서 읽습니다.'],
        ['LangGraph', '컴파일된 그래프 호출', 'invoke({"inputs": {"sku": "MS-02"}})\n→ result["outputs"]["stock"]', '업무 결과는 같습니다. 입력과 출력이 그래프 상태의 별도 키에 들어갑니다.'],
      ],
      link: ['chapter-4', '공통 Flow 선언 살펴보기'],
    },
  },
};

export function renderAid(id, aid, escape) {
  const steps = aid.steps.map(([actor, label, payload, explanation], index) => {
    const stock = aid.stock?.[index];
    const meter = stock === undefined ? '' : `<div class="aid-meter">
      <span>실행 뒤 재고 <strong>${stock}개</strong> / 시작 7개</span>
      <meter aria-label="실행 뒤 재고" min="0" max="7" value="${stock}">${stock} / 7</meter>
    </div>`;
    return `
      <li>
        <details name="${id}-steps"${index === 0 ? ' open' : ''}>
          <summary><span class="aid-index" aria-hidden="true">${index + 1}</span><span><small>${escape(actor)}</small><strong>${escape(label)}</strong></span></summary>
          <div class="aid-detail">
            <pre tabindex="0" aria-label="${escape(label)}의 데이터"><code>${escape(payload)}</code></pre>
            <p>${escape(explanation)}</p>${meter ? `\n            ${meter}` : ''}
          </div>
        </details>
      </li>`;
  }).join('');
  const flow = aid.flow ? `<ol class="aid-flow" aria-label="변환 순서">${aid.flow.map((label, i) => (
    `<li>${i ? '<span aria-hidden="true">→</span>' : ''}${escape(label)}</li>`
  )).join('')}</ol>` : '';
  const link = aid.link ? `<p class="aid-link"><a href="#${aid.link[0]}">${escape(aid.link[1])}</a></p>` : '';
  return `<figure class="learning-aid" id="${id}">
    <figcaption><span>개념 실습 · 예시 데이터</span><strong>${escape(aid.title)}</strong></figcaption>
    <p>${escape(aid.intro)}</p>
    ${flow}<ol class="aid-steps">${steps}
    </ol>${link}
  </figure>\n`;
}
