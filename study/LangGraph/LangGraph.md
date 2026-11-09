# LangGraph — 실행 순서와 상태를 설계하는 에이전트 런타임

Python 실습 · 상태 그래프, 도구 루프, 승인과 재개, 병렬 조사\
함께 읽기 · [LangChain](../LangChain/LangChain.md) · [Deep Agents](../Deep_Agents/Deep_Agents.md)

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
