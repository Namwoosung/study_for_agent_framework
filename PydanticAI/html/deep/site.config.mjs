export default {
  "folder": "PydanticAI",
  "name": "PydanticAI",
  "mark": "P.",
  "source": "PydanticAI_2차_심층_학습_분석.md",
  "majorDepth": 1,
  "chapterCount": 27,
  "version": "원문 2026.10.31 · Python Core v2.61.0",
  "lead": "Graph Node·ToolManager·Output·Deferred의 실행 계약을 따라갑니다.",
  "overview": "PydanticAI의 타입·검증을 내부 Agent Graph의 상태 전이와 연결합니다. Core와 별도 Harness를 구분하고, 유효 Output·도구 배리어·승인 재개·메시지 보존이 실제 실행에 미치는 영향을 살펴봅니다.",
  "groups": [
    {
      "title": "Core·Graph·Harness 경계",
      "ids": [
        "1",
        "2",
        "3"
      ],
      "intro": "기술의 정체성과 실행 책임을 나눈 뒤 고정 버전 소스 지도를 읽습니다.",
      "focus": "Core v2.61.0과 별도 Harness의 버전·기능 범위를 혼동하지 마세요."
    },
    {
      "title": "Node와 Run 수명",
      "ids": [
        "4",
        "5",
        "6"
      ],
      "intro": "UserPrompt→ModelRequest→CallTools의 전이와 State·Deps·Context를 연결합니다.",
      "focus": "텍스트·유효 Output·Deferred·오류·취소의 결과를 구분하세요."
    },
    {
      "title": "모델 입력과 Provider",
      "ids": [
        "7",
        "8"
      ],
      "intro": "메시지·Instructions·Schema가 Provider 요청으로 변환되는 과정을 읽습니다.",
      "focus": "Python deps는 모델 Context가 아니며 API 호환이 기능 호환을 보장하지 않습니다."
    },
    {
      "title": "Tool 정의·검증·동시성",
      "ids": [
        "9",
        "10",
        "11"
      ],
      "intro": "함수에서 스키마·ToolManager·검증·승인·실행으로 이어지는 경로와 병렬 배리어를 연결합니다.",
      "focus": "ModelRetry의 피드백과 즉시 함수 재실행, Batch 순차화와 시스템 격리를 구분하세요."
    },
    {
      "title": "Output와 Retry",
      "ids": [
        "12",
        "13"
      ],
      "intro": "Output 확정 정책이 실제 부작용에 미치는 영향을 비교하고 Retry 계층의 요청 증폭을 분석합니다.",
      "focus": "early·graceful·exhaustive의 조건과 Streaming으로 이미 확정된 출력의 차이를 확인하세요."
    },
    {
      "title": "Dependencies·Capabilities·승인",
      "ids": [
        "14",
        "15",
        "16"
      ],
      "intro": "Run별 자원과 실행 Hook, Deferred 요청을 후속 Run에서 해결하는 프로토콜을 연결합니다.",
      "focus": "승인 원본·History·메타데이터·Call ID와 결과 대응을 서버에서 보존해야 합니다."
    },
    {
      "title": "History·Context·외부 확장",
      "ids": [
        "17",
        "18",
        "19",
        "20"
      ],
      "intro": "보관 이력과 현재 입력을 나누고 압축·캐시·Skills·MCP·Child Loop를 연결합니다.",
      "focus": "권한·메모리 자동 상속을 가정하지 말고 ToolCall/Return 쌍 보존을 확인하세요."
    },
    {
      "title": "Serving·보안·장애",
      "ids": [
        "21",
        "22",
        "23"
      ],
      "intro": "Stream·Task·외부 작업·저장 완료를 나누고 실패 사례를 책임 계층에 연결합니다.",
      "focus": "취소는 Undo가 아니며 온도 0도 전체 실행의 재현성을 보장하지 않습니다."
    },
    {
      "title": "코드 추적 워크북",
      "ids": [
        "24"
      ],
      "intro": "진입·메시지·Tool·Output·병렬·승인·Hook 경로를 고정 소스와 연결합니다.",
      "focus": "실제 코드의 조건을 기록하고 재구성한 의사코드와 구분하세요."
    },
    {
      "title": "비교·발표·복습",
      "ids": [
        "25",
        "26"
      ],
      "intro": "기능 수보다 실행·검증·상태·권한의 설계를 비교하고 문답으로 설명해 봅니다.",
      "focus": "성능 순위로 읽지 말고 각 설계의 적용 조건과 비용을 연결하세요."
    },
    {
      "title": "출처·검증 한계",
      "ids": [
        "27"
      ],
      "intro": "고정 Core 소스와 공식 문서, 별도 Harness 기능과 미실행 범위를 확인합니다.",
      "focus": "학습 예시를 실제 모델·도구·복구·부하 실험 결과와 구분하세요."
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
