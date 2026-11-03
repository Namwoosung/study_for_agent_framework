export default {
  "folder": "Claude_Code",
  "name": "Claude Code",
  "mark": "C.",
  "source": "Claude_Code_2차_심층_학습_분석.md",
  "majorDepth": 2,
  "chapterCount": 54,
  "version": "원문 2026.10.31 · Claude Code v2.1.314 · 참조 SDK v0.2.174",
  "lead": "Harness의 Context·도구·권한·협업을 관찰 가능한 경계로 분석합니다.",
  "overview": "모델의 제안과 Harness·Host의 실행 통제를 나누고 공식 인터페이스에서 관찰 가능한 동작을 추적합니다. 공개 Python SDK가 보여 주는 통신 경로를 Claude Code 코어 전체의 공개 구현과 동일시하지 않습니다.",
  "groups": [
    {
      "title": "Model·Harness·Host",
      "ids": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "intro": "제어권을 가진 계층과 사용자에게 보이는 상태를 나눕니다.",
      "focus": "Agent Loop 도식과 의사코드는 공개 코어 구현을 복제한 것이 아닙니다."
    },
    {
      "title": "모델 입력·Cache·압축",
      "ids": [
        "6",
        "7",
        "8",
        "9",
        "10"
      ],
      "intro": "System·Project·Conversation 층과 재전송·재계산·요약을 나눕니다.",
      "focus": "Provider·모델·설정별 Cache Break 예외와 압축 후 재주입 조건을 보세요."
    },
    {
      "title": "Instructions·Memory·Session",
      "ids": [
        "11",
        "12",
        "13",
        "14",
        "15"
      ],
      "intro": "지침 파일의 존재·선택·로딩 시점과 실제 정책 강제를 구분합니다.",
      "focus": "AGENTS fallback과 병합, Auto Memory의 선택 지식과 대화 이력을 나눠 읽으세요."
    },
    {
      "title": "Skills·MCP·Plugin·Tool",
      "ids": [
        "16",
        "17",
        "18",
        "19",
        "20",
        "21"
      ],
      "intro": "절차 선택과 외부 기능 실행·배포, Tool 전후 Hook 효력을 연결합니다.",
      "focus": "모든 파일 입력이 Read Tool을 거치는 것은 아니라는 조건을 확인하세요."
    },
    {
      "title": "권한·Sandbox·실패",
      "ids": [
        "22",
        "23",
        "24",
        "25",
        "26"
      ],
      "intro": "규칙·모드·Hook·Mod·Backend 권한의 강제 범위를 비교합니다.",
      "focus": "도구 거부 규칙과 범용 OS ACL, Shell 격리와 외부 MCP 권한은 다릅니다."
    },
    {
      "title": "동시성·Subagent·Teams",
      "ids": [
        "27",
        "28",
        "29",
        "30",
        "31",
        "32"
      ],
      "intro": "Tool·Background·Child Context·협업 메시지와 완료 장벽을 구분합니다.",
      "focus": "Context 격리·Worktree·Credential·외부 DB 자원은 각기 다른 경계입니다."
    },
    {
      "title": "Serving·예약·관측",
      "ids": [
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "40.1"
      ],
      "intro": "CLI·SDK 진입과 API·큐·세션·취소·스케줄링·Gateway 경계를 읽습니다.",
      "focus": "Scheduler는 실행 Trigger이며 복구·권한·정확성을 대신 보장하지 않습니다."
    },
    {
      "title": "소스·인터페이스 워크북",
      "ids": [
        "W01",
        "W02",
        "W03",
        "W04",
        "W05",
        "W06",
        "W07",
        "W08",
        "W09",
        "W10",
        "W11",
        "W12",
        "W13",
        "W14",
        "W15"
      ],
      "intro": "요청·Context·Cache·지침·기억·Skill·MCP·정책·협업·SDK·예약의 계약을 소스와 공식 인터페이스에 연결합니다.",
      "focus": "관찰 가능한 사실, 비공개 내부 구현의 추정, 실행할 후속 실험을 구분해 기록하세요."
    },
    {
      "title": "부작용 복구와 설계 비교",
      "ids": [
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48"
      ],
      "intro": "실패 분석 표와 취소·정책 변경·Exactly-once 문제를 연결하고 자체 Harness의 설계 선택을 비교합니다.",
      "focus": "분석 시나리오는 실제 장애 실측이 아니며 중립 설계 인터페이스는 제품 API가 아닙니다."
    },
    {
      "title": "발표와 학습 점검",
      "ids": [
        "49",
        "50",
        "51"
      ],
      "intro": "발표 구성과 40문항으로 핵심 실행 경계를 설명해 봅니다.",
      "focus": "기능 이름을 넘어 로딩·승인·저장·종료 시점의 조건을 설명하세요."
    },
    {
      "title": "출처·공개·검증 범위",
      "ids": [
        "52",
        "53",
        "54"
      ],
      "intro": "제품 릴리스와 독립적으로 고정한 Python SDK 소스, 공개 범위의 한계를 확인합니다.",
      "focus": "서로 다른 버전 번호의 일치나 호환성을 가정하지 마세요."
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
