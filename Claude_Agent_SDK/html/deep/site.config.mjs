export default {
  "folder": "Claude_Agent_SDK",
  "name": "Claude Agent SDK",
  "mark": "C.",
  "source": "Claude_Agent_SDK_2차_심층_학습_분석.md",
  "majorDepth": 2,
  "chapterCount": 53,
  "version": "원문 2026.10.31 · Python v0.2.176 / CLI v2.1.316",
  "lead": "공개 SDK의 통신·제어 경로와 CLI 런타임의 책임을 구분합니다.",
  "overview": "Python SDK가 별도 Claude Code CLI Harness를 구동하고 제어하는 경로를 읽습니다. 공개 소스에서 확인하는 Transport·콜백·파싱과 공식 문서로 이해하는 CLI 실행 계약, 확인할 수 없는 내부 알고리즘의 경계를 유지합니다.",
  "groups": [
    {
      "title": "SDK와 CLI 실행 책임",
      "ids": [
        "1",
        "2",
        "3",
        "4"
      ],
      "intro": "공개 Python 코드의 통신과 문서화된 CLI 동작을 나눠 읽습니다.",
      "focus": "모델 API·SDK·CLI·외부 Tool의 실행 주체를 구분하세요."
    },
    {
      "title": "호출·프로세스·제어 프로토콜",
      "ids": [
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12"
      ],
      "intro": "query와 지속 Client의 연결·정리 책임, Query 중재와 메시지 파싱을 따라갑니다.",
      "focus": "요청 ID·Callback ID·Result와 원시 스트림 종료를 구분하세요."
    },
    {
      "title": "Tool·MCP·권한·Hook",
      "ids": [
        "13",
        "14",
        "15",
        "16",
        "17"
      ],
      "intro": "모델 요청과 실제 부작용 시점을 나누고 내장·외부 MCP·Python MCP 경로를 연결합니다.",
      "focus": "자동 승인·명시적 거부·Hook·콜백의 조건과 우회 가능한 경로를 확인하세요."
    },
    {
      "title": "Context·Session·이중 쓰기",
      "ids": [
        "18",
        "19",
        "20",
        "21"
      ],
      "intro": "현재 모델 입력·캐시·압축·대화 복원과 외부 SessionStore 미러를 나눕니다.",
      "focus": "로컬 기록 후 Mirror, 임시 Materialization과 파일 체크포인트의 지원 조합을 확인하세요."
    },
    {
      "title": "Skills·위임·중단·복구",
      "ids": [
        "22",
        "23",
        "24",
        "25"
      ],
      "intro": "재사용 절차와 독립 작업 Context, Interrupt·Cancel·Close·Resume를 연결합니다.",
      "focus": "각 동작이 무엇을 종료·보존하고 외부 효과에는 어디까지 영향을 주는지 확인하세요."
    },
    {
      "title": "워크북: 진입과 CLI 구성",
      "ids": [
        "26",
        "27",
        "28"
      ],
      "intro": "query→내부 Client→Transport에서 옵션 변환과 자원 정리를 추적합니다.",
      "focus": "실제 함수의 입력·실패·finally 정리와 실행 환경 전제를 기록하세요."
    },
    {
      "title": "워크북: 제어 요청과 콜백",
      "ids": [
        "29",
        "30",
        "31",
        "32"
      ],
      "intro": "initialize와 Request 상관관계, Permission·Hook 역호출을 추적합니다.",
      "focus": "Callback 등록·응답·오류·취소의 경계를 확인하세요."
    },
    {
      "title": "워크북: MCP·메시지·수명",
      "ids": [
        "33",
        "34",
        "35"
      ],
      "intro": "JSON-RPC 처리, typed message와 지속 Client의 async context 수명을 연결합니다.",
      "focus": "서버 요청과 모델 요청, 메시지 파싱과 성공 판정을 구분하세요."
    },
    {
      "title": "워크북: 저장·위임·취소",
      "ids": [
        "36",
        "37",
        "38",
        "39",
        "40"
      ],
      "intro": "Materialize·Mirror·Subagent 정의·원시 Stream·Custom Transport의 전제를 읽습니다.",
      "focus": "정의 직렬화와 실제 CLI 스케줄링, 옵션 전달과 자동 적용을 구분하세요."
    },
    {
      "title": "서비스 설계와 기술 비교",
      "ids": [
        "41",
        "42",
        "43",
        "44",
        "45",
        "46"
      ],
      "intro": "인증·세션 소유권·격리·비용·관측과 Runtime 재사용의 Trade-off를 비교합니다.",
      "focus": "기능 개수보다 Loop 소유권과 공개·변경 가능한 통제 경계를 보세요."
    },
    {
      "title": "장애·발표·복습",
      "ids": [
        "47",
        "48",
        "49",
        "50",
        "51"
      ],
      "intro": "24개 실패 사례와 운영 점검, 발표와 35문항으로 경계를 복습합니다.",
      "focus": "설계 분석과 실행·보안·성능 실측을 구분하세요."
    },
    {
      "title": "출처·검증 한계",
      "ids": [
        "52",
        "53"
      ],
      "intro": "공식 동작 계약과 v0.2.176 Python 고정 소스의 범위를 확인합니다.",
      "focus": "CLI 내부 Loop·압축·스케줄러 전체가 공개 Python 분석 범위는 아닙니다."
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
