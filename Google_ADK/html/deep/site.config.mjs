export default {
  "folder": "Google_ADK",
  "name": "Google ADK",
  "mark": "G.",
  "source": "Google_ADK_2차_심층_학습_분석.md",
  "majorDepth": 2,
  "chapterCount": 41,
  "version": "원문 2026.10.31 · Python ADK v2.13.0",
  "lead": "Runner·Flow·Event와 Workflow Scheduler의 상태 경계를 읽습니다.",
  "overview": "ADK의 객체 개념에서 실제 호출자·상태 소유자·실패 단위로 학습을 확장합니다. LlmAgent의 모델·도구 흐름과 명시적 Workflow 실행을 나누고 Event·SessionService·Node 상태와 재개의 범위를 살펴봅니다.",
  "groups": [
    {
      "title": "실행 계층과 요청 진입",
      "ids": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "intro": "Runner·LlmAgent·Flow·Workflow·Services의 책임과 버전 경계를 나누고 Invocation을 추적합니다.",
      "focus": "사용자 입력 한 건과 Invocation·Event·Session, 신규 요청과 Resume를 구분하세요."
    },
    {
      "title": "Loop와 모델 입력",
      "ids": [
        "6",
        "7",
        "8",
        "9",
        "10"
      ],
      "intro": "BaseLlmFlow의 반복과 한 Step의 전처리·모델 호출·후처리를 연결합니다.",
      "focus": "종료·Abort·Partial과 Processor 순서, 실제 Provider 입력을 확인하세요."
    },
    {
      "title": "Tool 준비·병렬·실패",
      "ids": [
        "11",
        "12",
        "13",
        "14"
      ],
      "intro": "선언 생성·Lookup 준비·Callback·Python 실행과 병렬 Task 처리를 나눕니다.",
      "focus": "_prepare_single은 Tool 본체·before Callback을 실행하지 않습니다. 부분 성공 보존의 조건도 확인하세요."
    },
    {
      "title": "Event와 상태 저장",
      "ids": [
        "15",
        "16",
        "17",
        "18"
      ],
      "intro": "final Event의 범위와 Partial·temp: 저장 경계를 읽습니다.",
      "focus": "참여 Agent의 종료와 전체 Workflow 완료, 저장 인터페이스와 일관성 보장을 구분하세요."
    },
    {
      "title": "Cache·압축·검색",
      "ids": [
        "19",
        "20",
        "21"
      ],
      "intro": "Prefix 계산 재사용과 History 요약, 검색 저장소의 역할을 나눕니다.",
      "focus": "최적화 사이 간섭과 정보 손실, 근거의 재조회 가능성을 확인하세요."
    },
    {
      "title": "협업·Graph·복구",
      "ids": [
        "22",
        "23",
        "24",
        "25",
        "26",
        "27"
      ],
      "intro": "기존 패턴·AgentTool·Transfer와 새 Graph 실행의 Trigger·Scheduler·Checkpoint를 연결합니다.",
      "focus": "deprecated의 잔여 제약, Resume·Replay·Retry와 미완료 복원 범위를 확인하세요."
    },
    {
      "title": "확장·운영·실패",
      "ids": [
        "28",
        "29",
        "30",
        "31",
        "32"
      ],
      "intro": "Callback·Plugin·MCP·Skills·Serving의 경계를 나누고 실패 사례를 관측 지표와 연결합니다.",
      "focus": "Cron Trigger와 실행 지속성, Trace와 평가를 같은 기능으로 보지 마세요."
    },
    {
      "title": "코드 추적 워크북",
      "ids": [
        "33"
      ],
      "intro": "Runner 분기·Tool 준비·동시성·저장·Graph와 정책 경로를 소스에서 대조합니다.",
      "focus": "입력·분기·상태·출력과 미구현 TODO·실험 질문을 구분해서 기록하세요."
    },
    {
      "title": "설계 비교와 복습",
      "ids": [
        "34",
        "35",
        "36",
        "37",
        "38"
      ],
      "intro": "실행·상태·권한·실패 단위를 비교하고 발표와 질문으로 이해를 점검합니다.",
      "focus": "기능 감사나 성능 순위가 아닌 설계 차이로 읽으세요."
    },
    {
      "title": "출처·검증 한계",
      "ids": [
        "39",
        "40",
        "41"
      ],
      "intro": "v2.13.0 고정 소스·공식 문서와 미실행 범위, 후속 질문을 확인합니다.",
      "focus": "태그에서 확인한 코드와 최신 문서, 실제 테스트 결과를 구분하세요."
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
