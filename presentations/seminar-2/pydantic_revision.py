"""PydanticAI slides, backed by the versioned source index."""
import json
from pathlib import Path

GROUPS = {
    1: ('Python 코드로 Agent 구성하기', '작은 LOT 조회 Agent에서 시작합니다.'),
    6: ('요청이 반복되고 끝나는 과정', '노드와 메시지를 따라 한 번의 Run을 읽습니다.'),
    13: ('모델 입력과 대화 상태', '공급자에게 보내는 값과 앱에 저장하는 값을 나눕니다.'),
    18: ('Tool 등록과 실제 실행', '함수 선언부터 인자 검증과 병렬 실행까지 추적합니다.'),
    25: ('출력 검증과 종료 정책', '결과 계약과 실행할 작업을 함께 판단합니다.'),
    31: ('Capability와 승인', '공통 정책을 조합하고 보류된 실행을 이어갑니다.'),
    38: ('선택 Harness 기능', '필요한 기억, 작업 환경, 복구 기능을 연결합니다.'),
    46: ('위임, 관측, 개발 범위', '자식 실행과 운영 경계를 같은 사례에 연결합니다.'),
}
ORDER = ['PYDANTIC']
for number in range(1, 53):
    if number in GROUPS:
        ORDER.append(f'PAD{list(GROUPS).index(number)+1:02}')
    if number not in (5, 8):
        ORDER.append(f'PA{number:02}')

LEGACY = [1, 2, 4, 7, 13, 18, 23, 25, 28, 30, 31, 16, 42, 39, 43, 46, 37, 38, 52]
ALIASES = {'PA00': 'PYDANTIC', **{f'S{i:02}': f'PA{n:02}' for i, n in enumerate(LEGACY, 20)}}

CODE = {
    'minimal': ('앱 코드 · 로컬 테스트 모델', '''from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

agent = Agent(TestModel())
result = agent.run_sync('LOT-A 조회 준비')
print(result.output)''', 'TestModel로 연결 확인', 'run_sync에서 결과 받기'),
    'agent': ('앱 코드 발췌 · LOT-A fixture', '''class YieldReport(BaseModel):
    lot_id: str
    snapshot: str
    yield_pct: float = Field(ge=0, le=100)

agent = Agent(model, deps_type=Deps,
              output_type=YieldReport)

@agent.tool
def read_counts(ctx: RunContext[Deps], lot_id: str):
    return ctx.deps.read_counts(lot_id)''', 'Tool 계약 · lot_id', '최종 계약 · YieldReport'),
    'deps': ('앱 코드 발췌 · 서버가 구성한 조회 범위', '''@dataclass
class Deps:
    allowed_lots: set[str]
    snapshot: str
    counts: dict[str, tuple[int, int]]

    def read_counts(self, lot_id: str):
        if lot_id not in self.allowed_lots:
            raise PermissionError(lot_id)
        good, total = self.counts[lot_id]
        return dict(good=good, total=total,
                    snapshot=self.snapshot)''', '앱에서 권한 검사', 'Tool 스키마에는 lot_id'),
    'plain': ('앱 코드 발췌 · RunContext 유무 비교', '''@agent.tool
def read_counts(ctx: RunContext[Deps], lot_id: str):
    return ctx.deps.read_counts(lot_id)

@agent.tool_plain
def yield_percent(good: int, total: int) -> float:
    return 100 * good / total''', 'tool · 실행 Context 사용', 'tool_plain · 인자만 사용'),
    'hook': ('앱 코드 발췌 · 검증된 LOT 인자 검사', '''from pydantic_ai.capabilities import AbstractCapability

class LotPolicy(AbstractCapability[Deps]):
    async def before_tool_execute(
        self, ctx, *, call, tool_def, args
    ):
        if call.tool_name == 'read_counts':
            if args['lot_id'] not in ctx.deps.allowed_lots:
                raise PermissionError(args['lot_id'])
        return args''', '검증된 인자 검사', '공통 정책으로 재사용'),
    'verify': ('앱 코드 발췌 · 수율 재계산', '''@agent.output_validator
def verify(ctx: RunContext[Deps], out: YieldReport):
    counts = ctx.deps.read_counts(out.lot_id)
    expected = 100 * counts['good'] / counts['total']
    if out.snapshot != counts['snapshot']:
        raise ModelRetry('snapshot을 확인하세요.')
    if abs(out.yield_pct - expected) > 0.01:
        raise ModelRetry('수율을 다시 계산하세요.')
    return out''', '합성 집계 · 92 / 100', '90% 보고서는 수정 요청'),
}

ROWS = """01|Pydantic과 PydanticAI가 맡는 일|데이터 계약과 Agent 실행을 분리해서 봅니다.|Pydantic~필드와 범위 검증;PydanticAI~모델·Tool·결과 연결;앱 코드~수율을 원본과 대조|yield_pct=120은 Field 범위에서 거절됩니다. 90은 타입과 범위를 통과해도 실제 92와 다를 수 있으므로 앱이 원본을 재계산합니다.|07 08
02|내 코드에서 모델까지|Core가 실행을 맡고 선택 기능은 Capability로 연결합니다.|앱~지침·Tool·결과 타입;Agent Graph~상태와 다음 노드;Model adapter~공급자 요청·응답|Graph는 ToolManager로 호스트 함수를 실행합니다. Provider는 추론을 맡습니다. Harness는 별도 패키지이며 이 Core 경로에 Memory나 Skills를 추가합니다.|01 03 04 19 35
03|가장 작은 Agent 실행|모델을 정하고 요청을 보내면 Core가 결과를 돌려줍니다.|@minimal|테스트 모델을 주입하면 네트워크 없이 호출 계약을 검증할 수 있습니다. 실제 모델 연결에서는 앱이 provider 설정과 모델 ID를 준비합니다.|01 02
04|Tool과 출력 타입 붙이기|같은 LOT 질문에 조회 함수와 보고서 타입을 추가합니다.|@agent|Core는 read_counts 인자와 최종 출력 계약을 요청에 반영합니다. 실제 집계 조회와 허용 범위, 결과 의미 검증은 앱 코드입니다.|01 06 07
05|선언이 실행에 필요한 객체로 바뀝니다|앱 코드 한 줄이 어느 경계에서 쓰이는지 따라갑니다.|Tool 함수~인자 스키마와 실행 핸들러;Output 타입~출력 스키마와 검증기;run 호출~메시지 이력과 Graph 상태|함수 서명에서 모델용 JSON Schema가 생성됩니다. 실제 함수는 호스트에 남고 실행마다 별도 Graph 상태를 사용합니다.|01 03 06 07
06|run에서 Graph가 열리기까지|호출 준비, 리소스 진입, 노드 순회를 나눠 봅니다.|AbstractAgent.run~실행과 결과 반환;Agent.iter~_prepare_run 및 리소스 진입;Graph 순회~노드 처리와 종료|_PreparedAgentRun.open이 실행 범위를 엽니다. run은 Graph를 소비하고 iter는 앱에 노드 진행을 노출합니다. 예외 시 리소스 정리 범위를 확인합니다.|01 02 03
07|세 노드가 나누어 맡는 실행|Core 내부 루프는 pydantic-graph로 구성됩니다.|UserPromptNode~입력과 이력 준비;ModelRequestNode~모델 호출;CallToolsNode~Tool·출력 처리|CallToolsNode는 다음 ModelRequestNode로 이어지거나 결과와 함께 종료합니다. 승인 응답으로 재개할 때는 기존 보류 호출을 먼저 처리할 수 있습니다. 사용자 정의 업무 Graph와 내부 노드는 다른 층입니다.|03
08|한 요청에서 모델이 세 번 응답한 경우|고정 응답으로 잘못된 인자부터 최종 보고서까지 추적합니다.|1차 응답~필수 lot_id 누락 · 재시도;2차 응답~LOT-A 조회 · Tool 반환;3차 응답~보고서 검증 · 종료|이 예시에서 모델 요청은 3회이고 업무 Tool 본체 실행은 1회입니다. 검증 스크립트에서는 수율 오류 응답도 추가해 4회 요청으로 수정까지 확인했습니다. 인자 오류 피드백과 실제 조회 결과는 서로 다른 메시지로 쌓입니다. 최종 보고서는 output Tool 처리입니다.|03 04 05 12
09|상태와 의존성을 구별하기|Graph 상태와 앱의 데이터 객체는 각각 다른 곳에 놓입니다.|GraphAgentState~이력·사용량·retry·step·run_id;GraphAgentDeps~모델과 실행 구성;RunContext.deps~조회 범위와 앱 데이터|build_run_context가 내부 상태의 일부와 앱 deps를 Tool·Hook에 전달합니다. deps 객체는 Python에 남으며 Tool이 반환한 값은 모델 입력이 될 수 있습니다.|03 10
10|응답에서 다음 노드를 고르는 조건|같은 응답에 함수 호출과 출력 후보가 함께 있을 수 있습니다.|Function Tool~실행 결과로 다음 모델 요청;Output / 텍스트~선언된 출력 계약에 따라 검사;Unknown / Deferred~피드백 또는 보류 결과|CallToolsNode._handle_tool_calls와 _process_response_output을 구별합니다. 유효한 출력과 실행할 Tool이 함께 있으면 EndStrategy가 처리에 관여합니다.|03 05 07
11|예산 소진과 취소|어느 작업이 이미 끝났는지 기록을 확인합니다.|한도~UsageLimits와 출력 retry 예산;오류~예외와 재시도 피드백 구분;취소~남은 task 정리와 완료 기록|consume_output_retry에서 출력 한도를 확인합니다. 동시에 실행한 작업의 취소로 이미 성공한 외부 쓰기가 되돌아가지는 않으므로 앱이 멱등성과 보상 절차를 설계합니다.|03 05 13
12|실행 API 다섯 가지|앱이 어느 단위에서 결과를 받아야 하는지에 따라 고릅니다.|run_sync~동기 호출의 최종 결과;run~비동기 최종 결과;run_stream~출력 스트림과 확정 시점;run_stream_events~모델·Tool 이벤트 소비;iter~Graph 노드 단위 관찰|run_stream은 최종 출력이 스트림에서 확정되는 시점에 주의합니다. 모든 실행 이벤트를 소비하고 싶다면 run_stream_events를 비교합니다. iter는 프레임워크 내부 노드 진행을 관찰할 때 사용합니다.|02 03 05
13|모델에 보내는 값과 Python에 남는 값|같은 Run에서 공급자 요청과 호스트 실행 상태를 분리합니다.|메시지~지침·사용자 입력·이력;요청 파라미터~Tool·Output schema·설정;Python 호스트~deps·함수 본체·권한 상태|_prepare_request_parameters에서 Tool·출력 계약이 요청용 데이터로 준비됩니다. 인증 객체를 deps에 넣는다고 공급자에 직렬화되는 것은 아니며 앱이 Tool 반환과 로그에 노출되는 값은 관리해야 합니다.|03 10 19
14|Instructions와 System Prompt의 수명|새 요청을 만들 때 지침과 이전 메시지를 따로 확인합니다.|Instructions~현재 실행에서 재평가;SystemPromptPart~메시지 이력에서 계승 가능;Model adapter~공급자 형식으로 변환|동적 system prompt는 _reevaluate_dynamic_prompts 경로에서 재평가될 수 있습니다. OpenAI Chat의 메시지와 Responses의 입력 항목은 서로 다른 요청 형식입니다. Anthropic 역시 별도 adapter의 system 블록 조립을 따릅니다.|03 12 19
15|deps로 조회 범위를 전달하기|인증과 스냅샷은 서버에서 결정하고 Tool은 그 범위 안에서 조회합니다.|@deps|서버가 허용한 LOT 목록과 읽기 snapshot을 RunContext에 넣습니다. 모델은 lot_id를 제안하며 Tool이 접근 권한을 확인합니다. 같은 schema를 보내도 tenant에 따라 실행 가능한 데이터는 달라집니다.|09 10 17
16|History와 Conversation의 차이|다음 Run에 넘기는 상태의 범위를 고릅니다.|message_history~이전 모델 메시지;Conversation~메시지·usage·ID·보류 호출;Agent 객체~공통 실행 설정|all_messages()는 메시지를 넘기는 경로입니다. result.conversation에는 누적 상태와 deferred_tool_requests도 포함됩니다. 새 요청에 어떤 상태를 전달할지 호출자가 정합니다.|02 11 12
17|대화를 저장하고 다시 열기|직렬화 기능 위에 앱의 저장소 정책을 얹습니다.|저장~ConversationTypeAdapter로 직렬화;불러오기~사용자·세션 권한 검사;갱신~버전 비교·충돌 처리·TTL|Conversation을 DB에 저장하는 위치와 TTL은 앱이 선택합니다. 동시에 두 Run이 진행되면 버전을 비교해 나중 저장이 먼저 저장한 메시지를 덮어쓰는 문제를 막습니다.|11 12
18|Python 함수에서 모델용 Tool 명세까지|함수의 입력 계약을 요청용 JSON Schema로 표현합니다.|함수 서명~이름·타입·docstring;function_schema~검증기와 JSON Schema;ToolDefinition~모델에 공개할 명세|FunctionToolset이 호출할 함수를 관리합니다. 이름, 설명과 schema가 모델에 전달되고 인자 검증에는 Pydantic validator가 쓰입니다. 함수 본체는 Python에서 실행됩니다.|06 09 17
19|tool과 tool_plain 선택하기|RunContext를 받는지 먼저 판단합니다.|@plain|tool은 RunContext가 필요한 조회·인가에 사용합니다. tool_plain은 앱 의존성이 필요 없는 순수 계산에 적합합니다. sync/async 선택은 함수가 I/O를 기다리는지에 따라 별도로 결정합니다.|01 06 17
20|Toolset이 공개 목록을 바꾸는 시점|모델 요청마다 보이는 도구와 실행할 수 있는 도구를 점검합니다.|get_tools~현재 Context에서 목록 구성;prepare / filter~노출 이름과 조건 결정;call_tool~선택된 함수를 호출|ToolManager.for_run_step이 실행 단계에 맞는 도구를 준비합니다. Combined, Filtered, Prefixed는 묶기·걸러내기·이름 구분에 쓰입니다. 데이터에 접근할 권한은 실행 경계에서도 검사합니다.|04 17 18
21|호출 검증과 함수 실행|인자가 잘못된 호출은 함수 본체에 도달하기 전에 처리합니다.|resolve~등록된 도구 확인;validate_tool_call~인자·검증 Hook;execute_tool_call~검증 결과로 실행|_resolve_tool과 _build_tool_context를 거쳐 _run_validate_hooks가 수행됩니다. 검증된 인자로 ValidatedToolCall을 만들고 실행 경로에 넘깁니다. 미등록 이름과 유효하지 않은 인자는 각 오류 경로로 처리됩니다.|04 05
22|타입 검사 이후의 업무 조건|LOT ID가 문자열이어도 조회 가능 여부는 별도 판단입니다.|입력 검증~lot_id 타입 확인;업무 인가~허용 LOT·snapshot 확인;결과 검증~단위·분모·근거 확인|합성 LOT-A의 동일 snapshot에서 good과 total을 읽습니다. 모델이 다른 LOT를 제안하면 조회를 차단하고 조회 권한 오류와 인자 수정 요청을 별도로 기록합니다.|04 06 10
23|병렬 Tool과 실행 장벽|같은 snapshot의 독립 조회는 묶고, 의존 작업은 분리합니다.|[A, B]~독립 조회를 함께 시작;[C]~sequential Tool 경계;[D, E]~다음 병렬 구간|_segment_by_barriers가 구간을 나누고 _call_tools가 task를 실행합니다. 동기 함수는 offload될 수 있습니다. 완료 이벤트 순서와 history 조립 인덱스는 구분합니다. B 입력에 A 결과가 필요하면 앱이나 후속 모델 요청이 의존성을 해결해야 합니다.|04 05 17
24|Local, MCP, Native Tool의 실행 위치|모델이 요청한 다음 실제 작업이 어디서 일어나는지 봅니다.|Function Tool~Python 호스트 함수;MCP Tool~클라이언트가 서버 호출;Native Tool~공급자 측 기능|MCP는 서버가 공개한 schema를 받아 원격 호출로 전달합니다. Native Tool의 실행과 결과 표현은 공급자 지원을 확인합니다. 앱은 MCP 인증과 접근 범위, 실제 모델 호환성을 관리합니다.|17 19 37 38
25|출력 모드 네 가지|요청에 계약을 실어 보내는 방식부터 달라집니다.|ToolOutput~출력 전용 Tool schema 공개;NativeOutput~공급자 구조화 출력 계약;PromptedOutput~지침으로 JSON 유도 후 파싱;TextOutput~문자열을 콜백으로 처리|ToolOutput은 처음부터 출력용 Tool을 제시합니다. NativeOutput의 지원 범위는 adapter에 달려 있습니다. PromptedOutput의 파싱·검증 실패는 retry 경로를 타며 TextOutput 콜백도 반환 형식을 앱이 결정합니다.|07 08 19
26|범용 Agent에서 최종 결과 타입 고르기|중간 Tool의 반환값과 앱이 받는 최종 결과를 따로 설계합니다.|자유 대화~str;업무별 결과~YieldReport 또는 다른 타입;복수 형태~출력 후보를 명시|Agent는 실행에 필요한 중간 Tool을 호출하면서 최종 출력 계약을 맞춥니다. 복수 출력은 앱이 각 타입을 처리할 수 있을 때 유용합니다. run별 override는 기존 validator와의 제약을 확인합니다.|01 02 07 08
27|수율과 근거를 원본에서 다시 검증하기|스키마를 통과한 90%도 원본이 92%라면 수정이 필요합니다.|@verify|output_validator에서 snapshot과 수치를 대조합니다. ModelRetry는 모델에게 수정 피드백을 줍니다. 권한 오류나 신뢰할 수 없는 원본은 앱이 실패로 다룹니다.|03 07 08
28|같은 응답, 서로 다른 종료 정책|방출 순서가 조회 A, 유효한 O1, 기록 B, 유효한 O2일 때를 비교합니다.|early~O1 채택 · A/B 생략;graceful~A → O1 검사 → B 처리;exhaustive~A/B 및 출력 후보 처리 · O1 채택|process_tool_calls가 각 Processor를 선택합니다. 고정 응답 시험에서 early는 A와 B를 실행하지 않았고 graceful과 exhaustive는 둘 다 실행했습니다. graceful은 방출 순서에 따라 함수 묶음을 처리하며 O1을 채택해도 뒤에 있는 B가 실행될 수 있습니다. 기록 B는 시험용 부작용이며 실제 발행은 별도 권한 경계로 둡니다.|03 05
29|최종 출력 후보가 있어도 재요청하는 경우|출력 실패, 함수 retry, 스트림 확정은 서로 다른 분기입니다.|invalid Output~다음 후보·수정 요청;function retry~정책에 따라 결과 억제;stream commit~확정 시점 예외|graceful은 실패한 출력 뒤의 함수 구간을 이어갈 수 있습니다. graceful/exhaustive의 retry-wins를 적용할 때 run_stream에서 이미 확정한 출력은 별도 경로로 처리합니다. Deferred의 보류 상태도 정상 완료와 구분합니다.|02 03 05
30|Retry 횟수는 어느 층에서 셀까?|Tool 수정 요청과 공급자 HTTP 재시도는 각각 다른 예산을 씁니다.|Core~Tool·출력 retry와 UsageLimits;전송~SDK·transport·모델 fallback;앱~업무 재시도·멱등 키|retries=2의 적용 범위는 Agent와 Tool·출력 설정을 확인합니다. HTTP 계층과 앱 재시도가 겹치면 실제 요청은 늘 수 있습니다. 이미 쓴 외부 효과의 재실행을 통제합니다.|01 04 13
31|Capability가 묶는 구성요소|반복되는 실행 정책을 여러 Agent에 연결합니다.|구성~Toolset·instructions·settings;Hook~모델·Tool·출력 경계;수명~Agent 구성과 run별 바인딩|Capability는 실행 경계와 구성 요소를 조합합니다. LOT 인가처럼 특정 Tool에만 필요한 정책은 해당 함수에서 검사하고 여러 도구가 공통으로 쓰는 정책은 재사용 가능한 단위로 둘 수 있습니다.|14 15
32|Capability의 앞·뒤·감싸기 순서|정렬한 두 Capability A와 B의 모델 요청 Hook을 비교합니다.|before~A → B;after~B → A;wrap~A 진입 → B 진입 → 호출 → 역순 복귀|CombinedCapability가 중첩 구조를 정규화하고 get_ordering과 for_run을 적용합니다. before_model_request와 after_model_request의 순서가 다르며 wrap_model_request는 handler chain을 구성합니다.|14 15
33|업무 정책을 Hook에 넣는 위치|검증, 마스킹, 지연 측정을 필요한 경계에 둡니다.|@hook|ToolManager._run_validate_hooks와 _run_execute_hooks는 서로 다른 단계입니다. DB 접근 권한은 데이터 경계에서 보장하고 Capability는 공통 정책과 관측을 조합하는 데 씁니다.|04 14 15
34|Guardrail이 판정하는 시점|입력과 Tool, 출력에 서로 다른 검사를 둡니다.|Input~첫 모델 요청 주변;Tool~검증된 인자와 실행 경계;Output~처리된 최종 출력|InputGuardrail의 병렬 모드는 모델 호출과 guard를 함께 시작할 수 있습니다. ToolGuardrail의 allow/block/retry/approve/replace는 실행 위치와 승인 상태를 확인합니다. OutputGuardrail은 partial output을 건너뜁니다.|26 27
35|승인 필요 여부를 결정하는 곳|승인이 필요한 호출은 검증된 인자와 함께 보류합니다.|정적 정책~requires_approval 설정;동적 정책~ApprovalRequired로 보류;보류 결과~DeferredToolRequests 전달|인자가 검증된 이후에 승인할 작업을 확정합니다. 조건부 정책과 승인 상태에 따라 실행을 보류하고 결과 타입에 보류 결과를 받을 구성을 둡니다.|04 09 16
36|승인 요청을 처리하는 세 경로|실행 환경에 맞는 승인 주체를 연결합니다.|Inline~HandleDeferredToolCalls로 처리;CLI~사람에게 응답을 받아 전달;앱 화면~보류 저장 후 후속 Run|서버는 승인 UI를 직접 선택합니다. 보류 결과를 반환하는 구성에서는 실행이 끝나고 앱에 요청이 전달됩니다. 사람의 응답이 없으면 앱의 대기·만료 정책을 적용합니다.|09 11 16
37|승인 결과로 다음 Run 시작하기|승인한 보고서 버전과 실행할 원본 호출을 연결합니다.|저장~call ID·인자·보고서 버전;확인~승인자·만료·변경 여부;재개~Conversation과 승인 결과 전달|DeferredToolResults를 기존 보류 호출에 연결합니다. override_args를 쓰는 경우 새 인자를 다시 확인합니다. 앱은 초안 수정, 중복 승인, 위조 및 접근 권한 변경을 재개 전에 검사합니다.|03 04 09 11
38|Core 위에 선택 Harness 붙이기|Core 2.61.0과 Harness 0.61.0은 별도 패키지입니다.|Core~Agent·Graph·Tool·Output;Harness~Memory·Skills·Guardrail;앱~필요한 기능과 운영 정책 선택|Core만으로 작은 Agent를 실행할 수 있습니다. Harness 기능을 조합하면 저장·작업 환경·위임에 필요한 구성 요소를 재사용합니다. Coder와 Researcher는 용도별 구성을 보여 줍니다.|14 35
39|Memory를 쓰고 찾는 Tool|모델의 기억 요청과 앱의 저장 범위를 분리합니다.|MemoryToolset~write·read·delete·search;MemoryStore~노트와 메타데이터;앱 정책~namespace·보존·권한|write_memory 등의 호출이 Store에 연결됩니다. namespace는 앱이 정하며 모델 인자가 아닙니다. 업무 데이터를 언제 기록할지와 사용자별 저장 범위는 앱 정책입니다.|21 22 23
40|기억이 모델 입력에 들어가는 시점|이번 Run에 사용할 제한된 기억을 가져옵니다.|for_run~실행별 scope 바인딩;before_model_request~snapshot 로딩;사용자 입력 곁~user-role 문맥에 주입|Memory는 기본 InMemoryStore를 사용하므로 수명은 프로세스입니다. 기본 snapshot 예산은 최대 2000토큰과 200줄이며 설정을 확인합니다. 앱은 영속 저장소와 기억의 공개 범위를 선택합니다.|21 23
41|과거 대화 검색과 노트 검색|같은 검색어라도 조회 대상과 반환 근거가 다릅니다.|대화 검색~Conversation source의 발췌;순위 계산~구간·토큰화·BM25;노트 검색~MemoryStore의 항목|ConversationSearchToolset은 대화 소스에서 범위를 정하고 결과를 발췌합니다. 모델이 낸 검색어와 내부 normalization, 앱이 제한한 세션 범위를 각각 관찰합니다.|22 39 40
42|압축 전후의 같은 대화|오래된 이력을 줄여도 현재 조회와 결과의 연결은 유지합니다.|압축 전~오래된 턴 + LOT 조회와 결과;압축 후~남길 턴 + 최근 ToolCall/Return;원본~앱 저장소에 보존할 범위|SlidingWindowCompaction은 임계조건을 확인하고 ctx.messages를 갱신합니다. 요약은 모델 비용과 손실 가능성이 있으며 Tool 결과 정리는 별도 전략입니다. LOT 식별자와 정확한 수치가 필요하면 원본을 다시 조회합니다.|28 29
43|Skill을 발견하고 선택해 로딩하기|목록을 보여 주고 필요한 절차를 활성화합니다.|발견~SKILL.md와 library 검사;선택~deferred Capability 카탈로그;로딩~load_capability와 참고파일|Skills.for_run과 loader가 카탈로그를 만듭니다. 본문을 사용하려면 적절한 Capability를 로딩합니다. 중복과 파싱 오류, 참고 파일 접근 및 자체 작성 절차는 앱의 검수 경계와 연결합니다.|24 25
44|파일·Shell·계획 기능 조합하기|업무에 필요한 작업 환경만 Agent에 연결합니다.|Workspace / FileSystem~파일 범위와 접근;Shell / Sandbox~명령 실행 환경과 제한;Planning~작업 계획을 구조화|개별 기능의 제공 범위와 실행 권한은 별도로 확인합니다. 업무 Agent는 읽기 전용 LOT 조회만으로 시작할 수 있습니다. 실제 Shell 환경을 붙일 때 작업 디렉터리와 권한, 격리 구현을 앱이 선택합니다.|14 35
45|대화 저장, Step 저장, Durable 실행|복구할 대상에 따라 기록 방식이 달라집니다.|Conversation~메시지와 보류 상태;StepPersistence~완료된 단계와 effect 기록;Durable 실행~외부 실행기의 재개 정책|직렬화된 대화와 실행 중 checkpoint의 복구 범위는 다릅니다. 외부 효과에 대한 정확히 한 번 실행을 보장하려면 저장 시점, replay 계약과 멱등성 정책을 따로 설계합니다.|11 34
46|위임과 Handoff에서 다음 작업을 정하는 곳|자식 결과의 행선지와 제어권을 비교합니다.|Agent-as-tool~부모에게 결과 반환;앱 Handoff~앱이 다음 Agent 선택;업무 Graph~명시적 전이 규칙|Agent-as-tool은 부모 모델의 Tool 실행 안에서 자식을 호출합니다. 앱 Handoff에서는 앱이 주체를 전환합니다. 사용자 Graph는 공정 검토 단계를 명시하며 Core 내부 모델·Tool 루프와 다른 역할입니다.|01 02 03 31
47|자식 Run이 받는 값|부모는 작업과 필요한 상태를 골라 자식에게 넘깁니다.|delegate_task~자식과 작업 선택;새 Run~독립 history·선택 deps;반환~결과를 부모 Tool 응답으로|SubAgentToolset._run_delegation의 실행 범위를 봅니다. 부모 history와 권한을 모두 공유한다고 가정하지 않습니다. deps 전달, 도구 상속, usage 공유와 깊이 제한은 각각 설정과 동작을 확인합니다.|30 31
48|Dynamic Workflow와 Advisor 선택하기|작업 그래프를 진행하는 경우와 조언을 받는 경우를 구분합니다.|Dynamic Workflow~단계와 의존성으로 작업 진행;Advisor~별도 관점에서 검토 의견;부모 Agent~결과 취합과 다음 판단|두 기능은 Harness의 별도 Capability입니다. 작업 단계를 구조화해야 할 때와 모델 판단을 보강할 의견이 필요할 때를 나눕니다. 자식의 입력과 결과를 누가 통합하는지 비교합니다.|31 32 33
49|Trace로 모델과 Tool 실행 이어 보기|Run에서 어떤 호출과 검증이 발생했는지 확인합니다.|Run span~요청 전체의 상관관계;Model / Tool span~호출 지연·사용량·오류;Output / 검증~처리와 오류 경계|Instrumentation의 wrap_run, wrap_model_request, wrap_tool_execute, wrap_output_process를 관측 경계에 연결합니다. OpenTelemetry exporter와 모델 입력·Tool 결과의 공개 범위는 앱이 설정합니다. 승인 감사 기록은 별도 계약입니다.|20 36
50|흐름 테스트와 답변 평가|고정 응답으로 실행을 재현하고 데이터셋으로 답변을 평가합니다.|TestModel~기본 연결 검사;FunctionModel~원하는 응답·오류 재현;Evals~사례별 수치·근거·품질 평가|테스트에서 잘못된 호출과 수정 응답을 주입해 실제 Tool 실행 횟수를 확인합니다. Evals에서는 원본 집계와 최종 수율 오차, 근거 연결 여부를 평가합니다.|02 03 12
51|어디까지 개발해야 Agent가 될까?|최소 실행에서 운영 서비스까지 책임이 늘어나는 지점을 봅니다.|최소 Agent~모델·조회 Tool·출력 타입;업무 Agent~인가·수치 검증·대화·승인;서비스~저장 충돌·복구·관측 운영|Agent와 Tool을 정의하면 반복 실행은 Core에 맡길 수 있습니다. 실제 업무에는 deps.py, validators.py, conversation_store.py, approval.py의 책임이 남습니다. Memory나 Skills가 필요하면 Harness 구성 파일에서 선택합니다.|01 11 14 35
52|코드와 내부 실행을 한 요청으로 따라가기|합성 LOT-A를 조회하고 수율 보고서를 검증합니다.|코드~Tool과 YieldReport 선언;실행~요청 → Node → Tool 반환;검증~수치 대조 → 출력과 Trace|고정 응답은 분기와 호출 횟수 재현에 쓰고 실모델 연결은 호환성과 결과 품질을 확인하는 별도 단계입니다. PydanticAI 데모 화면은 18001번이며 런타임은 10001번의 OpenAI 호환 모델 endpoint를 사용합니다. 고정 응답 시험에서 인자 오류와 수율 수정, 세 종료 정책, 대화 직렬화, 승인 재개를 재현했습니다.|02 03 05 19 36"""

FLOW = {5, 6, 7, 8, 17, 18, 21, 23, 37, 40, 43, 47, 52}


def revise(slides, drawing):
    root = drawing['ROOT']
    index = json.loads((root / 'research/pydanticai-plan-sources.json').read_text(encoding='utf-8'))
    sources = {int(s['id'][3:]): (f'PA-{s["id"]}', Path(s['path']).parent.name + '/' + Path(s['path']).name, s['url'])
               for s in index['sources']}
    study = [item['path'] for item in index['local_inputs'][:3]]
    original = {new: slides.pop(old) for old, new in ALIASES.items() if old != 'PA00'}
    text, box, arrow = (drawing[key] for key in ('text', 'box', 'arrow'))
    table, code = drawing['table'], drawing['code_panel']
    palette = ('context', 'runtime', 'tool')

    def add(ident, title, sub, diagram, take, detail, refs, concepts, section, kind='content-slide'):
        slide = dict(id=ident, title=title, sub=sub, diagram=diagram, take=take,
                     steps=['전체 구성'], section=section,
                     version='Core 2.61.0 · Harness 0.61.0' if section.endswith('Harness 기능') else 'Core 2.61.0',
                     kind=kind, note=detail, explanation=detail, sources=refs,
                     concepts=[dict(term=k, meaning=v) for k, v in concepts],
                     localEvidence=[{'path': study[1], 'sections': title}],
                     demo='pydanticai' if ident == 'PA52' else None)
        if ident in original:
            slide['originalSpec'] = original[ident]['originalSpec']
            slide['sources'] += original[ident]['sources']
        if ident in ('PA08', 'PA23', 'PA28', 'PA37'):
            slide['localEvidence'].append({'path': study[2], 'sections': '발표 실무 코멘트'})
        slides[ident] = slide

    opener = slides['PYDANTIC']
    opener['sub'] = 'Python 코드로 Agent를 구성하고 실행을 제어하기'
    opener['sources'] = [sources[i] for i in (1, 3, 35)]
    opener['localEvidence'] = [{'path': study[0], 'sections': 'PydanticAI의 개념과 구성'}]

    for row in ROWS.splitlines():
        num, title, sub, visual, detail, ref_ids = row.split('|')
        n = int(num)
        if n in (5, 8):
            continue
        refs = [sources[int(k)] for k in ref_ids.split()]
        if n in GROUPS:
            chapter, intro = GROUPS[n]
            section = f'PydanticAI / {chapter}'
            divider = f'PAD{list(GROUPS).index(n)+1:02}'
            diagram = text(0, 125, f'PYDANTIC AI   /   {divider[-2:]}', 26, 'context', 700)
            diagram += text(0, 250, chapter, 72, 'text', 700)
            diagram += text(0, 343, intro, 33, 'muted')
            diagram += drawing['rule'](0, 423, 1652, 423)
            add(divider, chapter, intro, diagram, intro, intro + ' ' + detail, refs,
                [(chapter, intro)], section, 'topic-divider')
        if visual.startswith('@'):
            caption, snippet, first, second = CODE[visual[1:]]
            diagram = code(0, 45, 1090, 525, snippet, caption, 23)
            diagram += box(1140, 130, 510, 115, first, '', 'context', 28)
            diagram += box(1140, 285, 510, 115, second, '', 'tool', 28)
            concepts = [(first, sub), (second, detail)]
            detail += '\n\n```python\n' + snippet + '\n```'
        else:
            concepts = [tuple(item.split('~')) for item in visual.split(';')]
            if n in FLOW:
                diagram = ''
                for i, (term, meaning) in enumerate(concepts):
                    x = i * 606
                    diagram += box(x, 172, 440, 175, term, meaning, palette[i], 28)
                    if i < 2:
                        diagram += arrow(f'M{x+440} 260 H{x+592}', palette[i])
            else:
                diagram = table(('구분', '실행에서 맡는 역할'), concepts,
                                widths=[495, 1157], y=65, row_h=100)
        if n == 52:
            detail += '\n\n실행 화면은 Graph, Deps, 대화 저장·복원, 출력 모드, 종료 정책, Core, Harness Memory, Subagents를 각각 다룹니다.'
        add(f'PA{num}', title, sub, diagram, sub, detail, refs, concepts, section)
