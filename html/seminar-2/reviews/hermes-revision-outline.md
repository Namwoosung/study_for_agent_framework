# Hermes 발표자료 개정 목차

앞 5장 유지. Hermes는 화면 번호 6~21, 전체 발표자료는 47장. 청회색 디자인·키보드 build·Sources를 유지했다.

| 화면 번호 | ID | 범주 | 제목 |
|---|---|---|---|
| 6 | S04 | Hermes / 요청 처리 | Hermes는 범용 Agent Harness입니다 |
| 7 | S05 | Hermes / 요청 처리 | 사용자 요청 한 건의 실행 과정 |
| 8 | S07 | Hermes / 요청 처리 | 모델에 전달할 Context 구성하기 |
| 9 | S13 | Hermes / Tool 실행 | Tool·MCP·Plugin으로 기능 연결하기 |
| 10 | S13A | Hermes / Tool 실행 | Tool 요청이 실제 실행으로 이어지는 과정 |
| 11 | S13B | Hermes / Tool 실행 | 승인·오류·취소가 발생하면 어떻게 될까? |
| 12 | S10 | Hermes / 기억·재사용 | Session과 Memory는 무엇을 저장할까? |
| 13 | S11 | Hermes / 기억·재사용 | 과거 대화를 찾아 현재 작업에 사용하기 |
| 14 | S12 | Hermes / 기억·재사용 | Skill을 만들고 다시 사용하는 과정 |
| 15 | S08 | Hermes / 긴 작업·위임 | 반복되는 입력과 Prefix Cache |
| 16 | S09 | Hermes / 긴 작업·위임 | Context가 길어졌을 때 줄이고 보존하기 |
| 17 | S14 | Hermes / 긴 작업·위임 | 여러 Tool을 함께 실행하기 |
| 18 | S14A | Hermes / 긴 작업·위임 | 별도 Agent에게 작업 맡기기 |
| 19 | S14B | Hermes / 서비스 운영 | Gateway가 세션과 실행을 관리하는 방식 |
| 20 | S14C | Hermes / 서비스 운영 | Cron으로 예약 작업 실행하기 |
| 21 | S15 | Hermes / Demo | Hermes Demo |

## 반영 내용

- 요청 한 건의 전체 흐름을 먼저 제시하고, Tool 검증·실행 전 기록·정책·실행·결과 기록을 확대했다.
- 승인·오류·취소, Memory 쓰기와 snapshot, FTS 선택 주입, Skill 로딩/쓰기/Curator를 설명했다.
- Cache·압축 단계, 병렬 구간·결과 순서, Subagent의 별도 Loop·결과 통합을 분리했다.
- Gateway 세션 소유권·Busy 처리, Cron Claim·새 Session·외부 효과/전달의 구별을 추가했다.
- Demo는 요청·Tool·저장 확인 계획이다. 실제 서비스·Trace를 새로 구현하거나 연결한 것은 아니다.
- 일반 설계 제안과 Hermes 소스·공식 문서 설명을 Sources에서 구분했다.

## 근거

[기초 학습자료](../../../hermes/Hermes_Agent.md) · [심층 학습자료](../../../hermes/Hermes_Agent_2차_심층_학습_분석.md) · [추가 코멘트](../../../hermes/Hermes_Agent_발표_실무_시사점_코멘트.md) · [이전 미포함 검토](hermes-coverage-audit.md)

원 blueprint는 보존하고 개정 내용은 hermes_revision.py와 notes.json에 반영했다. 원문 S06 내용은 S05의 originalSpec에 함께 보관했다.
