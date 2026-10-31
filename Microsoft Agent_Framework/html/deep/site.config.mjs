export default {
  "folder": "Microsoft Agent_Framework",
  "name": "Microsoft Agent Framework",
  "mark": "M.",
  "source": "Microsoft_Agent_Framework_2차_심층_학습_분석.md",
  "majorDepth": 2,
  "chapterCount": 30,
  "pseudoDefault": true,
  "version": "원문 2026.10.31 · Python SDK python-1.24.0",
  "lead": "Agent Pipeline·Tool Loop·Harness Loop·Workflow의 제어권을 나눕니다.",
  "overview": "하나의 거대한 Loop 대신 외부 Agent Pipeline, ChatClient의 Function Invocation, 선택적 Harness 반복과 명시적 Workflow를 구분합니다. 상태 commit·승인 바인딩·복구와 외부 부작용의 경계를 고정 소스에 연결합니다.",
  "groups": [
    {
      "title": "계층과 호출 지도",
      "ids": [
        "1",
        "2",
        "3",
        "4"
      ],
      "intro": "SDK 배포와 Framework 제어 구조, Harness 합성을 나누고 요청 한 건의 경로를 읽습니다.",
      "focus": "어떤 계층이 실제 반복을 소유하는지 확인하세요."
    },
    {
      "title": "Agent·Context·Tool Loop",
      "ids": [
        "5",
        "6",
        "7"
      ],
      "intro": "RawAgent의 입력 준비와 Provider, ChatClient의 모델·도구 반복을 연결합니다.",
      "focus": "Provider 후처리의 실행 단위와 Tool Loop의 반복 단위를 구분하세요."
    },
    {
      "title": "Tool·정책·승인",
      "ids": [
        "8",
        "9",
        "10",
        "11",
        "12"
      ],
      "intro": "스키마·최종 인자·실행·결과와 Middleware 적용·실패·승인 상태를 연결합니다.",
      "focus": "정책 뒤 인자 변경, MiddlewareFailure·Termination, 특정 Session 요청에 바인딩된 승인을 보세요."
    },
    {
      "title": "상태와 모델 입력",
      "ids": [
        "13",
        "14"
      ],
      "intro": "Session·History·FileMemory·RAG·Checkpoint와 Context 변환을 나눕니다.",
      "focus": "Compaction·Prefix Cache·영구 기억은 목적과 수명이 다릅니다."
    },
    {
      "title": "Harness와 명시적 Workflow",
      "ids": [
        "15",
        "16",
        "17",
        "18"
      ],
      "intro": "전체 Agent 재실행과 Tool Loop를 나누고 Executor·Edge·Superstep commit을 읽습니다.",
      "focus": "내부 상태 commit과 외부 DB·API 효과의 원자성은 다른 경계입니다."
    },
    {
      "title": "복구와 협업 모델",
      "ids": [
        "19",
        "20",
        "21"
      ],
      "intro": "Checkpoint 리니지·Entry 저장과 Graph·실험적 Functional 표현을 연결합니다.",
      "focus": "순서 보장 범위와 재개 경계, 부모·자식 세션 및 승인 상태 전달을 구분하세요."
    },
    {
      "title": "외부 연결·보안·실패",
      "ids": [
        "22",
        "23",
        "24"
      ],
      "intro": "모델·MCP·Serving·Cron과 FIDES의 적용 범위를 나누고 실패 사례로 일관성을 점검합니다.",
      "focus": "Nested/Hosted Tool의 내부 실행과 실제 인프라 권한은 별도로 확인하세요."
    },
    {
      "title": "소스코드 추적 워크북",
      "ids": [
        "25"
      ],
      "intro": "진입·Context·Schema·Tool·정책·승인·반복·Graph·복구·FIDES 경로를 소스로 대조합니다.",
      "focus": "입력·분기·상태 변경·실패·출력과 검증하지 않은 질문을 구분하세요."
    },
    {
      "title": "설계 비교와 복습",
      "ids": [
        "26",
        "27",
        "28",
        "29"
      ],
      "intro": "교체 가능한 구성과 추적 복잡성의 비용을 비교하고 발표·문답으로 개념을 점검합니다.",
      "focus": "성능·보안 순위로 해석하지 말고 설계 선택의 조건을 연결하세요."
    },
    {
      "title": "출처·검증 한계",
      "ids": [
        "30"
      ],
      "intro": "Python 고정 버전과 공식 문서, 실험 기능·변경 포맷·미실행 범위를 확인합니다.",
      "focus": "Python·.NET·Go의 기능 동등성을 가정하지 마세요."
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
