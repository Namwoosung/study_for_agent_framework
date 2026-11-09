# LangGraph — 실행 순서와 상태를 설계하는 에이전트 런타임

Python 실습 · 상태 그래프, 도구 루프, 승인과 재개, 병렬 조사\
함께 읽기 · [LangChain](../LangChain/LangChain.md) · [Deep Agents](../Deep_Agents/Deep_Agents.md)

## 0. 무엇부터 실습하나

이 교재에서는 **재고 조회**와 **승인 뒤 주문 취소**를 만든다. Python의 함수와 딕셔너리를 읽을 수 있으면 시작할 수 있다. 2절에서 설치한 뒤, 2·4·5·7절은 API 키 없이 실행한다. 3절의 실제 모델 호출만 모델 키가 필요하다. 앞 교재를 읽지 않았더라도 여기서부터 시작할 수 있다.

| 단계 | 실습으로 확인할 내용 |
| --- | --- |
| 기초 | 노드가 입력을 받아 일부 상태만 바꾸고 종료한다. |
| 중급 | 모델이 도구를 선택하면 그래프가 도구 실행으로 분기한다. |
| 심화 | 사람 승인 전후에 실행을 나누고, 여러 조회를 병렬로 합친다. |
| 운영 | 스레드 상태, 재시도, 스트리밍, 중복 실행 방지의 책임을 구분한다. |

일반 Python에서 `normalize(ticket)` 다음에 `classify(ticket)`를 호출하면 한 번의 순차 처리가 된다. 그래프로 바꾸면 두 함수와 순서를 명시하고, 조건 분기·상태 저장·중단이 필요한 지점을 같은 구조에서 다룰 수 있다. 데이터 정규화만 필요한 작은 함수라면 일반 Python으로도 충분하다.

## 1. 무엇을 제공하나

배송 취소 요청에서 주문 확인, 조건 검사, 사용자 승인, 취소 실행은 서로 다른 책임이다. 일부 단계에서만 LLM을 쓰고, 나머지 순서는 앱이 보장하고 싶다면 각 단계를 그래프의 노드로 만들 수 있다. LangGraph는 상태를 전달하며 그래프를 실행하고, 체크포인터를 연결하면 중간 상태를 저장할 수 있다.

| 구성 | 하는 일 |
| --- | --- |
| State | 노드가 함께 읽는 데이터의 스키마. 예를 들어 메시지 목록과 주문 ID를 담는다. |
| Node | 현재 상태를 읽고 갱신할 필드를 반환하는 함수나 실행 단위. |
| Edge | 다음 실행 노드로 이어지는 경로. 조건부 엣지는 상태에 따라 목적지를 고른다. |
| Reducer | 동일 상태 필드의 여러 업데이트를 합치는 규칙. 기본 갱신은 값을 교체한다. |
| Checkpointer | 스레드별 체크포인트를 저장하고 이전 상태를 불러온다. |
| Store | 여러 스레드에서 공유할 수 있는 별도의 데이터 저장 추상화. |

그래프의 순서는 개발자가 정의하고, 모델은 허용된 노드 안에서 필요한 결정을 맡는다. 고정 분기와 반복 모두 가능하다. `compile()`이 그래프를 실행 가능한 객체로 만들며 `invoke`·`stream` 등으로 실행한다. [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) · [상태 그래프 소스](https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/graph/state.py)

### 상태와 실행 경로를 따로 읽는다

아래는 2절 코드의 개념도다. `START`와 `END`는 시작과 종료를 나타내는 예약 지점이고 `normalize`와 `classify`만 앱 함수다.

```text
START → normalize → classify → END
           │            │
         sku 갱신      status 갱신
```

노드 입력은 전체 상태 또는 선언한 입력 범위이며, 일반적인 상태 갱신 결과는 바뀐 키만 담는다. 예를 들어 `quantity`는 첫 입력에서 들어오고 두 노드가 건드리지 않으므로 마지막에도 남는다. 두 노드가 순서대로 같은 키를 덮어쓰는 경우와 한 실행 단계에서 동시에 같은 키에 쓰는 경우를 구분해야 한다. 후자의 병합은 5절에서 리듀서로 정의한다. [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)

## 2. 기초 — 모델 없이 상태 갱신하기

Python 파일로 저장해 실행한다. 3절 모델 예제에서만 `OPENAI_API_KEY`가 필요하다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install langgraph==1.2.20 langchain-openai==1.7.4
$env:STUDY_MODEL = 'gpt-4.1-mini'
```

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class Ticket(TypedDict, total=False):
    sku: str
    quantity: int
    status: str


def normalize(state: Ticket) -> dict:
    return {"sku": state["sku"].strip().upper()}


def classify(state: Ticket) -> dict:
    return {"status": "available" if state["quantity"] > 0 else "out_of_stock"}


builder = StateGraph(Ticket)
builder.add_node("normalize", normalize)
builder.add_node("classify", classify)
builder.add_edge(START, "normalize")
builder.add_edge("normalize", "classify")
builder.add_edge("classify", END)
graph = builder.compile()

result = graph.invoke({"sku": " kb-01 ", "quantity": 0})
assert result == {"sku": "KB-01", "quantity": 0, "status": "out_of_stock"}
```

각 노드는 변경분을 반환한다. `classify`에서 `sku`를 반환하지 않아도 앞 단계의 값은 남는다. `TypedDict`는 정적 스키마를 표현하므로 실제 외부 입력 검증은 서버 경계에서 추가한다.

## 3. 중급 — 도구 선택을 모델에 맡기고 엣지를 제어하기

아래는 LangChain의 모델 어댑터와 도구 선언을 쓰되, LangGraph로 에이전트 루프를 직접 정의하는 독립 스크립트다.

```python
import os

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


@tool
def get_stock(sku: str) -> str:
    """상품 코드 KB-01 또는 MS-02의 재고를 조회한다."""
    return {"KB-01": "7개", "MS-02": "0개"}.get(sku.upper(), "상품 없음")


tools = [get_stock]
model = ChatOpenAI(model=os.environ["STUDY_MODEL"]).bind_tools(tools)


def call_model(state: MessagesState) -> dict:
    instructions = {"role": "system", "content": "재고 질문은 조회 후 답하라."}
    return {"messages": [model.invoke([instructions, *state["messages"]])]}


builder = StateGraph(MessagesState)
builder.add_node("model", call_model)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)
builder.add_edge("tools", "model")
graph = builder.compile()

result = graph.invoke(
    {"messages": [{"role": "user", "content": "MS-02 재고가 있나요?"}]},
    config={"recursion_limit": 12},
)
print(result["messages"][-1].content)
```

`tools_condition`은 마지막 모델 메시지에 도구 요청이 있으면 `tools`로, 없으면 종료로 보낸다. `ToolNode`가 도구를 실행해 호출 ID가 연결된 결과 메시지를 만든다. `MessagesState`의 메시지 리듀서는 새 메시지를 합치며 같은 ID의 갱신도 처리한다. `recursion_limit`는 그래프 실행 단계 제한이다. 결제 횟수나 모델 지출을 제한하려면 별도 정책이 필요하다. [공식 빠른 시작](https://docs.langchain.com/oss/python/langgraph/quickstart)

### 도구 경로를 상태 변화로 따라가기

예를 들어 첫 모델 응답이 `get_stock(sku="MS-02")`를 요청했다고 하자. `MessagesState`에는 사용자 메시지와 모델의 요청이 남는다. 조건 함수가 `tools`를 골라 실행하면 호출 ID가 붙은 도구 결과가 더해진다. 모델 노드는 이력을 다시 읽고 최종 답을 만든다. 답변에 새 호출 요청이 없으면 종료한다. 첫 모델이 도구 없이 답하면 도구 노드는 실행되지 않는다. 업무상 조회가 항상 필요하다면 시작 지점에 조회를 두는 식으로 제어한다.

| 증상 | 확인할 곳 |
| --- | --- |
| 처음부터 도구 실행이 없다 | 모델의 `tool_calls`, 바인딩된 도구 목록, 조건부 엣지 |
| 도구는 호출됐지만 결과가 이상하다 | 인자, 도구 반환값, 도구 메시지의 호출 ID |
| 같은 도구만 계속 실행된다 | 모델 지시문, 종료 조건, 호출 한도 |
| 분기 테스트가 재현되지 않는다 | 모델 대신 고정 응답을 주고 노드와 엣지를 먼저 확인 |

[그래프 실행과 에이전트 패턴](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

## 4. 심화 — 승인 후 재개와 중복 실행 방지

아래 예제에서 명시적 승인 값이 참일 때만 실행 노드로 간다. 외부 시스템 대신 인메모리 딕셔너리를 사용한다. 두 번째 실습으로 승인 값을 거절로 바꾸고 기록이 없는지 확인한다.

```python
from typing import Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class CancelState(TypedDict, total=False):
    request_id: str
    order_id: str
    outcome: str


ledger: dict[str, str] = {}


def review(state: CancelState) -> Command[Literal["execute", "__end__"]]:
    approved = interrupt({"action": "cancel_order", "order_id": state["order_id"]})
    if approved is True:
        return Command(goto="execute")
    return Command(update={"outcome": "rejected"}, goto=END)


def execute(state: CancelState) -> dict:
    request_id, order_id = state["request_id"], state["order_id"]
    existing = ledger.setdefault(request_id, order_id)
    if existing != order_id:
        raise ValueError("동일 요청 ID에 다른 주문이 연결되었습니다.")
    return {"outcome": f"cancelled:{existing}"}


builder = StateGraph(CancelState)
builder.add_node("review", review)
builder.add_node("execute", execute)
builder.add_edge(START, "review")
builder.add_edge("execute", END)
graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "cancel-001"}}
paused = graph.invoke({"request_id": "req-001", "order_id": "O-7"}, config)
assert paused["__interrupt__"][0].value["order_id"] == "O-7"
assert ledger == {}

done = graph.invoke(Command(resume=True), config)
assert done["outcome"] == "cancelled:O-7"
assert ledger == {"req-001": "O-7"}
```

재개할 때 같은 `thread_id`를 사용한다. 재개된 노드는 처음부터 다시 실행되므로 `interrupt()` 앞에서 외부 상태를 바꾸면 반복될 수 있다. 재개 전에 승인 주체와 스레드 소유권을 확인하고, 사용자가 검토한 주문 ID 및 요청 버전을 승인 기록에 연결한다. 인메모리 예제에서 프로세스가 종료되면 체크포인트와 취소 기록이 사라진다.

운영에서는 지속 가능한 체크포인터를 사용한다. 외부 API가 취소를 완료한 직후 체크포인트 저장 전에 프로세스가 죽으면 재개 시 취소 요청이 다시 전송될 수 있다. 외부 API의 멱등성 키, 또는 같은 트랜잭션에서 변경과 요청 ID를 기록하는 업무 저장소가 이 문제를 다룬다. 체크포인트는 그래프의 실행 상태를 저장하며 외부 시스템 전체를 원자적으로 커밋하지 않는다. [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) · [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

## 5. 심화 설계 — 병렬 수집, 재시도, 관측

- **Fan-out/fan-in.** 지역별 검색을 여러 노드에 맡기고 결과를 합쳐 검증한다. 개수가 입력에 따라 달라지는 작업은 `Send` 패턴을 참고한다. 여러 노드가 같은 키를 동시에 갱신하면 병합 규칙이 필요하다. 예를 들어 `Annotated[list[Finding], operator.add]`로 결과를 합치고, 렌더링 직전에 안정적인 ID로 정렬·중복 제거를 할 수 있다.
- **재시도.** 네트워크의 일시 오류와 사용자 입력 오류를 나눈다. 읽기 도구는 재시도를 허용하기 쉽다. 외부 쓰기는 멱등성 키와 상태 조회를 갖춘 뒤 재시도한다. 승인 대기와 모델 실행 실패도 다른 상태로 관측한다.
- **스트리밍.** 상태 변경과 모델 토큰 이벤트를 다른 UI 요소로 표시한다. 스트리밍 중간 출력은 최종 답과 구분하고, 재연결 후에는 저장 상태를 기준으로 진행 상황을 복구한다.
- **서브그래프.** 반복 사용되는 조사·검토 단계를 독립 그래프로 만든다. 부모와 자식 상태 키를 공유할지, 노드에서 입력·출력을 변환할지 먼저 결정한다.

[워크플로와 에이전트](https://docs.langchain.com/oss/python/langgraph/workflows-agents) · [스트리밍](https://docs.langchain.com/oss/python/langgraph/streaming) · [서브그래프](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)

아래 실코드는 주문에 포함된 상품 개수만큼 조회 작업을 나눈다. 각 작업은 `sku`만 받으며, 결과는 `findings`에 합쳐진다. 비어 있는 주문은 바로 종료한다.

```python
from operator import add
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class Batch(TypedDict, total=False):
    skus: list[str]
    findings: Annotated[list[tuple[str, int | None]], add]


class Lookup(TypedDict):
    sku: str


def dispatch(state: Batch):
    return [Send("lookup", {"sku": sku}) for sku in state["skus"]] or END


def lookup(state: Lookup) -> dict:
    sku = state["sku"]
    return {"findings": [(sku, {"KB-01": 7, "MS-02": 0}.get(sku))]}


builder = StateGraph(Batch)
builder.add_node("lookup", lookup)
builder.add_conditional_edges(START, dispatch, ["lookup", END])
builder.add_edge("lookup", END)
graph = builder.compile()

result = graph.invoke({"skus": ["MS-02", "KB-01"], "findings": []})
assert sorted(result["findings"]) == [("KB-01", 7), ("MS-02", 0)]
assert graph.invoke({"skus": [], "findings": []})["findings"] == []
```

이 예제는 결과를 모두 모은 뒤 호출자가 정렬한다. 그래프 안에서 요약까지 하려면 조회 다음에 종합 노드를 둔다. 실제 공급자 API를 병렬 호출할 때는 동시 호출 수, 타임아웃, 일부 조회 실패 시 결과 표시 방식을 정한다.

## 6. 제작 관점의 장단점

| 장점 | 그에 따르는 작업 |
| --- | --- |
| 분기·반복·승인 조건을 코드에서 읽을 수 있다. | 단일 조회 에이전트에도 그래프를 직접 만들면 코드가 늘어난다. |
| 체크포인트로 장시간 작업을 재개할 수 있다. | 실행 중인 스레드와 새 그래프 버전의 호환성, 저장소 보존 기간을 설계한다. |
| 모델 없이 노드·분기·상태를 검증할 수 있다. | 모델 호출 결과, 병렬 갱신, 중단 후 재개까지 통합 테스트해야 한다. |
| 업무 규칙과 모델 판단을 단계별로 분리한다. | 외부 서비스의 멱등성, 인증, 실행 제한은 애플리케이션이 설계한다. |

검증할 조합은 정상 종료, 거절, 재개 전 쓰기 0회, 동일 요청 키 재처리, 다른 주문에 요청 키 재사용, 모델 반복 한도 도달이다. 구현을 읽을 때는 `StateGraph.compile`로 시작해 상태와 엣지가 어떻게 실행 객체로 변환되는지 확인한 뒤, 승인 전후의 상태 스냅샷을 대조한다.

## 7. 실습 — 체크포인트를 읽고 실행 단계를 관찰하기

4절은 중단된 일을 재개했다. 이번에는 하나의 스레드에 새 입력을 두 번 보내고, 별도 스레드의 상태와 비교한다. 같은 ID로 다음 작업을 이어가는 것과 다른 ID로 시작하는 것의 차이를 확인할 수 있다. 아래 스크립트는 모델을 호출하지 않는다.

```python
# thread_inspection.py
from operator import add
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    events: Annotated[list[str], add]


def record(state: State) -> dict:
    return {"events": ["처리 완료"]}


builder = StateGraph(State)
builder.add_node("record", record)
builder.add_edge(START, "record")
builder.add_edge("record", END)
graph = builder.compile(checkpointer=InMemorySaver())

first = {"configurable": {"thread_id": "A"}}
second = {"configurable": {"thread_id": "B"}}
updates = list(graph.stream({"events": ["첫 요청"]}, first, stream_mode="updates"))
assert updates == [{"record": {"events": ["처리 완료"]}}]
graph.invoke({"events": ["후속 요청"]}, first)
graph.invoke({"events": ["다른 요청"]}, second)

assert graph.get_state(first).values["events"] == [
    "첫 요청", "처리 완료", "후속 요청", "처리 완료",
]
assert graph.get_state(second).values["events"] == ["다른 요청", "처리 완료"]
assert len(list(graph.get_state_history(first))) > 1
print(graph.get_state(first).values)
```

`updates` 모드는 이 예제에서 노드가 새로 반환한 변경분을 보여 준다. 마지막 전체 상태를 보려면 `get_state`를 읽는다. 이력에는 중간 체크포인트가 들어갈 수 있으므로 이력 길이를 사용자의 요청 수로 사용하지 않는다. 리듀서로 로그를 계속 누적하면 저장 용량과 모델 입력이 커질 수 있다. 서비스에서는 최근 작업 상태와 감사 로그의 보존 정책을 따로 둔다. [체크포인트와 이력](https://docs.langchain.com/oss/python/langgraph/persistence) · [스트리밍](https://docs.langchain.com/oss/python/langgraph/streaming)

## 8. 운영 설계 — 재시도, 영속 실행, 버전 변경

### 재실행 가능한 경계부터 만든다

| 작업 | 다시 실행될 때의 위험 | 구현 방향 |
| --- | --- | --- |
| 조회 입력 정규화 | 동일 입력에서 같은 결과 | 상태 계산 함수로 둔다. |
| 읽기 API 호출 | 지연이나 조회 시점 변경 | 일시 오류만 제한적으로 재시도한다. |
| 주문 취소 | 동일 요청으로 외부 변경 반복 | 업무 서비스에 멱등성 키를 전달한다. |
| 승인 대기 | 사용자가 확인한 인자와 실행 인자가 어긋남 | 요청 버전·승인 주체·대상 값을 함께 기록한다. |

체크포인트에서 재개할 때는 Python 함수의 임의 줄부터 이어지는 것으로 생각하면 안 된다. 재생 또는 재실행이 필요한 경계가 있으므로 순수 계산, 외부 호출, 승인 대기를 분리한다. 체크포인트가 durable 저장소에 남더라도 외부 업무 시스템의 트랜잭션을 대신하지 않는다. 시도 횟수와 재시도 가능한 오류는 업무 API 특성에 맞춰 정한다. [장애 허용과 재시도](https://docs.langchain.com/oss/python/langgraph/fault-tolerance) · [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

### 실행 중인 요청을 새 코드로 어떻게 이어갈지 정한다

승인 대기 중에 노드 이름이나 스키마를 바꾸면 기존 체크포인트와 새 코드의 호환성을 점검해야 한다. 배포 전에는 구버전에서 대기 상태를 만든 뒤 새 버전에서 복원하는 테스트를 준비한다. 구버전으로 마저 실행할지, 상태를 이관할지, 다시 승인을 받을지는 업무 규칙에 따라 결정한다. [그래프 변경 호환성](https://docs.langchain.com/oss/python/langgraph/backward-compatibility)

### 실습 — 일시 오류만 재시도하는 노드

오류를 무조건 다시 시도하면 잘못된 요청을 계속 보낼 수 있다. 이 예제는 첫 번째 호출에서 일시적인 연결 오류를 내고 두 번째 호출에서 성공하는 읽기 작업을 흉내 낸다. `max_attempts`는 첫 호출을 포함한 총 시도 한도다. 외부 서비스에 연결하는 코드는 없으며, 목록은 예제를 관찰하기 위한 테스트용이다.

```python
# retry_lookup.py
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy


class State(TypedDict, total=False):
    sku: str
    stock: int


attempts: list[str] = []


def fetch(state: State) -> dict:
    attempts.append(state["sku"])
    if len(attempts) == 1:
        raise ConnectionError("일시적인 조회 연결 오류")
    return {"stock": 7}


builder = StateGraph(State)
builder.add_node(
    "fetch",
    fetch,
    retry_policy=RetryPolicy(
        max_attempts=2,
        retry_on=ConnectionError,
        initial_interval=0.01,
        jitter=False,
    ),
)
builder.add_edge(START, "fetch")
builder.add_edge("fetch", END)
graph = builder.compile()
assert graph.invoke({"sku": "KB-01"})["stock"] == 7
assert attempts == ["KB-01", "KB-01"]
print("일시 오류 뒤 재조회 성공")
```

`ConnectionError`를 `ValueError`로 바꾸면 지정한 재시도 조건에 해당하지 않아 실패가 호출자에게 전달된다. 두 경우의 실행 로그를 비교한다. 변경 작업에 재시도를 추가하려면 이전 시도가 업무 시스템에 이미 반영됐는지부터 판단할 수 있어야 한다. [노드의 재시도 정책](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)

## 9. 최종 실습 — 승인형 재고 예약 설계

1. 그래프 입력을 `account_id`, `sku`, `quantity`, `request_id`로 설계한다. `account_id`는 인증 결과에서 넣는다.
2. 조회 결과가 충분할 때만 승인 노드로 가게 한다. 부족·미등록·권한 실패는 각각 사용자에게 구별해 전달한다.
3. 승인되면 예약 API를 호출하고 같은 `request_id`로 재실행해도 이중 차감되지 않는지 검증한다.
4. `stream`으로 상태 변경을 보여 주되, UI가 끊겨도 최종 결과는 저장 상태에서 조회하게 한다.
5. 한 사용자에게 다른 스레드의 재개 요청을 보내 보고, 그래프 호출 전에 접근이 차단되는지 확인한다.

구현을 설명할 때는 모델이 고르는 경로와 앱이 보장하는 경로를 각각 그려 본다. 어떤 상태를 리듀서로 합치고 어떤 상태를 단일 노드만 쓸 수 있게 제한했는지 코드에서 짚는다.

### 완성 예제 — 조건 검사, 승인, 멱등 예약

아래 실습에서 초기 재고는 7개다. 요청 수량이 재고보다 많으면 승인 요청을 만들지 않는다. 승인 중에 재고가 줄어들 수 있으므로 실제 예약 단계에서도 다시 확인한다. 이미 처리한 요청 ID라면 같은 상품과 수량인지 검사하고 재고를 두 번 줄이지 않는다.

```python
# reservation_graph.py
from typing import Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class Reservation(TypedDict, total=False):
    request_id: str
    sku: str
    quantity: int
    outcome: str


stock = {"KB-01": 7}
ledger: dict[str, tuple[str, int]] = {}


def check(state: Reservation) -> Command[Literal["review", "__end__"]]:
    sku, quantity = state["sku"], state["quantity"]
    if quantity <= 0 or sku not in stock:
        return Command(update={"outcome": "invalid"}, goto=END)
    previous = ledger.get(state["request_id"])
    if previous is not None:
        outcome = "reserved" if previous == (sku, quantity) else "conflict"
        return Command(update={"outcome": outcome}, goto=END)
    if stock[sku] < quantity:
        return Command(update={"outcome": "insufficient"}, goto=END)
    return Command(goto="review")


def review(state: Reservation) -> Command[Literal["reserve", "__end__"]]:
    approved = interrupt({
        "request_id": state["request_id"],
        "sku": state["sku"],
        "quantity": state["quantity"],
    })
    if approved is True:
        return Command(goto="reserve")
    return Command(update={"outcome": "rejected"}, goto=END)


def reserve(state: Reservation) -> dict:
    request, sku, quantity = state["request_id"], state["sku"], state["quantity"]
    previous = ledger.get(request)
    if previous is not None:
        return {"outcome": "reserved" if previous == (sku, quantity) else "conflict"}
    if stock[sku] < quantity:
        return {"outcome": "insufficient"}
    stock[sku] -= quantity
    ledger[request] = (sku, quantity)
    return {"outcome": "reserved"}


builder = StateGraph(Reservation)
builder.add_node("check", check)
builder.add_node("review", review)
builder.add_node("reserve", reserve)
builder.add_edge(START, "check")
builder.add_edge("reserve", END)
graph = builder.compile(checkpointer=InMemorySaver())

request = {"request_id": "R-1", "sku": "KB-01", "quantity": 3}
config = {"configurable": {"thread_id": "reserve-R-1"}}
paused = graph.invoke(request, config)
assert paused["__interrupt__"][0].value["quantity"] == 3
assert stock["KB-01"] == 7
assert graph.invoke(Command(resume=True), config)["outcome"] == "reserved"
assert stock["KB-01"] == 4

retry = {"configurable": {"thread_id": "retry-R-1"}}
assert graph.invoke(request, retry)["outcome"] == "reserved"
assert stock["KB-01"] == 4
print("승인 뒤 한 번만 재고가 차감됐습니다.")
```

이 예제의 딕셔너리 변경은 단일 프로세스의 순차 실습이다. 여러 작업자가 동시에 예약하는 앱이라면 조회 후 차감과 원장 기록을 업무 DB의 트랜잭션 또는 업무 API의 원자적 연산에 맡긴다. 앱 서버에서는 고객의 자연어를 구조화 입력으로 바꾸는 모델 호출을 앞단에 붙일 수 있다. 모델이 제안한 수량과 SKU는 위 그래프의 검증을 통과해야 한다. 승인 뒤 재고를 2개로 줄인 경우와 승인 값이 거짓인 경우도 만들어 재고가 차감되지 않는지 확인한다.
