export default {
  "folder": "OpenAI_Agents_SDK",
  "name": "OpenAI Agents SDK",
  "mark": "O.",
  "source": "OpenAI_Agents_SDK_2차_심층_학습_분석.md",
  "majorDepth": 2,
  "chapterCount": 57,
  "version": "원문 2026.10.31 · Python SDK v0.24.0",
  "lead": "Runner의 상태 전이와 도구·승인·저장·스트리밍 책임을 읽습니다.",
  "overview": "Agent 구성 객체와 Runner 실행을 나눈 뒤, 모델 응답을 NextStep으로 분류하는 흐름을 따라갑니다. Tool 실행 정책·Guardrail 적용 시점·RunState 재개와 애플리케이션의 운영 책임을 연결하는 과정입니다.",
  "groups": [
    {
      "title": "SDK와 실행 구조",
      "ids": [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7"
      ],
      "intro": "구성 객체와 실행 엔진의 수명을 나누고 Runner 진입부터 단일 모델 Turn까지 따라갑니다.",
      "focus": "새 실행과 재개, 자원 소유권과 정리를 확인하세요."
    },
    {
      "title": "상태 전이와 모델 입력",
      "ids": [
        "8",
        "9",
        "10"
      ],
      "intro": "RunAgain·Handoff·Final·Interruption 분기를 읽고 최종 Provider 입력의 조립 과정을 연결합니다.",
      "focus": "Python context와 모델 입력, Turn 상한과 Tool·시간·비용 상한을 구분하세요."
    },
    {
      "title": "Tool 계획과 실행",
      "ids": [
        "11",
        "12",
        "13",
        "14",
        "15",
        "16"
      ],
      "intro": "Tool 실행 위치와 스키마·Task 배치·결과 정책·실패 정규화를 나눕니다.",
      "focus": "Hosted Tool 경로, 병렬성의 단위, 모델 재호출 없이 종료하는 조건을 확인하세요."
    },
    {
      "title": "Guardrail과 승인",
      "ids": [
        "17",
        "18",
        "19",
        "20",
        "21"
      ],
      "intro": "Input·Output·Tool 검사의 적용 시점과 중단·승인·재개 상태를 연결합니다.",
      "focus": "병렬 Input Guardrail의 부작용 가능성과 서버가 소유하는 원본 RunState를 확인하세요."
    },
    {
      "title": "협업과 제어권",
      "ids": [
        "22",
        "23",
        "24",
        "25"
      ],
      "intro": "Handoff와 Agent as Tool의 제어권·History·중첩 승인 전파를 비교합니다.",
      "focus": "중첩 승인은 최상위 RunState와 최초 Starting Agent로 재개하는 조건을 보세요."
    },
    {
      "title": "Session·Memory·Cache",
      "ids": [
        "26",
        "27",
        "28",
        "29",
        "30"
      ],
      "intro": "저장 View·공개 결과·다음 모델 입력을 나누고 Session과 RunState, 압축과 캐시를 연결합니다.",
      "focus": "session_id와 인증, 직렬화와 외부 상태 복원, 캐시 키와 실제 Hit를 구분하세요."
    },
    {
      "title": "Streaming·Serving·확장",
      "ids": [
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39"
      ],
      "intro": "이벤트 소비와 실행 수명을 나누고 API·동시성·스케줄러·Adapter·MCP·Sandbox 경계를 읽습니다.",
      "focus": "마지막 토큰·break·cancel·정리와 외부 작업 완료는 각각 다릅니다."
    },
    {
      "title": "관측과 자체 설계",
      "ids": [
        "40",
        "41",
        "42",
        "43",
        "44"
      ],
      "intro": "Trace와 평가를 구분하고 인터페이스별 비용과 운영 통제를 비교합니다.",
      "focus": "Mock 기반 Loop 검사와 실제 Wire/API 검증은 다른 증거입니다."
    },
    {
      "title": "코드 추적 워크북",
      "ids": [
        "45",
        "46",
        "47",
        "48",
        "49",
        "50"
      ],
      "intro": "Final·Tool·Handoff·승인·연결 종료의 소스 경로를 입력→분기→상태→출력 순으로 기록합니다.",
      "focus": "실제 파일·함수에 근거한 설명과 실행하지 않은 후속 실험을 구분하세요."
    },
    {
      "title": "실패·발표·복습",
      "ids": [
        "51",
        "52",
        "53",
        "54"
      ],
      "intro": "실패 사례를 책임 계층에 연결하고 발표와 질문으로 핵심을 점검합니다.",
      "focus": "지원 기능보다 정책·상태·실패 경로를 실제로 제어할 수 있는지 확인하세요."
    },
    {
      "title": "출처·검증 한계",
      "ids": [
        "55",
        "56",
        "57"
      ],
      "intro": "공식 문서와 v0.24.0 고정 소스, 실제로 검증하지 않은 범위를 확인합니다.",
      "focus": "Python 조사 결과를 다른 언어·최신 버전과 동일시하지 마세요."
    }
  ],
  "splitAt": 7000,
  "pageBudget": 6000,
  "distinctions": [
    [
      "모델 입력 / 저장된 기록",
      "저장소에 있는 정보와 현재 요청에서 모델이 볼 수 있는 정보는 다릅니다."
    ],
    [
      "실행 취소 / 외부 효과 복구",
      "Task나 스트림을 끝내도 이미 발생한 파일·DB·API 변경까지 되돌아가지는 않습니다."
    ],
    [
      "공식 계약 / 공개 코드 / 설계 해석",
      "문서에 명시된 동작, 고정 소스에서 확인한 경로, 재구성한 의사코드와 미검증 항목을 구분합니다."
    ]
  ]
};
