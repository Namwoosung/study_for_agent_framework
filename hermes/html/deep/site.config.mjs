export default {
  "folder": "hermes",
  "name": "Hermes Agent",
  "mark": "H.",
  "source": "Hermes_Agent_2차_심층_학습_분석.md",
  "majorDepth": 1,
  "chapterCount": 21,
  "version": "원문 2026.10.31 · Hermes v0.22.5",
  "lead": "완성형 Agent Runtime의 상태·도구·기억·운영 경계를 추적합니다.",
  "overview": "Hermes는 Agent Loop, Tool, State, Memory와 Gateway를 결합한 실행 환경입니다. 이번에는 모델이 선택한 행동을 런타임이 어떤 조건으로 기록·승인·반복·종료하는지 고정 버전 소스와 원문의 설명을 연결합니다.",
  "groups": [
    {
      "title": "실행 계층과 요청 경로",
      "ids": [
        "1",
        "2",
        "3",
        "4"
      ],
      "intro": "Gateway에서 AIAgent와 Turn Phase로 이어지는 경로를 따라갑니다. 모델 응답뿐 아니라 예산·중단·기록 실패가 실행에 미치는 영향을 읽습니다.",
      "focus": "사용자 요청·API 호출·Tool 호출 수를 나누고 persist-before-execute의 범위를 확인하세요."
    },
    {
      "title": "모델 입력·캐시·압축",
      "ids": [
        "5",
        "6",
        "7"
      ],
      "intro": "시스템 스냅샷과 대화·도구 스키마가 요청으로 조립되는 과정을 읽습니다. Prefix 계산 재사용과 메시지 압축은 서로 다른 문제를 풉니다.",
      "focus": "캐시가 유지되는 구간, 압축 후 잃는 정보와 Tool Call/Result 짝을 확인하세요."
    },
    {
      "title": "Memory·검색·Skills",
      "ids": [
        "8",
        "9",
        "10"
      ],
      "intro": "파일 기록과 현재 프롬프트 반영 시점을 나누고, FTS5 검색과 Skill의 점진적 로딩을 연결합니다.",
      "focus": "Memory Frozen Snapshot, 원본 DB와 검색 인덱스, Skill 생성과 신뢰성 검증을 구분하세요."
    },
    {
      "title": "도구·권한·동시성",
      "ids": [
        "11",
        "12",
        "13",
        "14"
      ],
      "intro": "Registry·Inline·MCP·Plugin의 실행 위치를 나눕니다. 승인과 병렬 구간, Child Loop의 상태·권한·비용을 함께 읽습니다.",
      "focus": "배리어·완료 순서·기록 순서와 Context·파일·Credential 격리를 따로 확인하세요."
    },
    {
      "title": "Gateway와 예약 실행",
      "ids": [
        "15",
        "16"
      ],
      "intro": "세션 정본의 쓰기 소유권과 요청·Run·Stream의 수명을 읽습니다. Cron은 예약 시각에 새 Agent Session을 시작합니다.",
      "focus": "스케줄 슬롯 Claim, 실행 성공, 결과 Delivery와 외부 효과 exactly-once를 구분하세요."
    },
    {
      "title": "실패와 설계 비교",
      "ids": [
        "17",
        "18"
      ],
      "intro": "실패 시나리오를 상태 불변식과 연결하고 다른 기술과 비교할 기준을 정리합니다.",
      "focus": "실제 확인한 구현, 일반 설계 제안과 실험으로 확인할 질문을 나눠 보세요."
    },
    {
      "title": "발표와 복습",
      "ids": [
        "19",
        "20"
      ],
      "intro": "발표 흐름과 심층 질문을 통해 각 실행 경계를 자신의 말로 설명해 봅니다.",
      "focus": "기능 이름보다 어떤 상태와 조건이 다음 행동을 결정하는지 설명해 보세요."
    },
    {
      "title": "출처·검증 한계",
      "ids": [
        "21"
      ],
      "intro": "공식 문서와 고정 소스를 나누고 조사하지 않은 실행·보안·성능 범위를 확인합니다.",
      "focus": "문서의 현재 동작과 v0.22.5에서 확인한 코드의 범위를 구분하세요."
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
