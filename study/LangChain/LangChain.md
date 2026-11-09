# LangChain — 모델과 도구로 업무 에이전트 만들기

Python 실습 · 기초부터 구조화 출력, 대화 상태, 권한 제어까지\
함께 읽기 · [LangGraph](../LangGraph/LangGraph.md) · [Deep Agents](../Deep_Agents/Deep_Agents.md)

## 1. 무엇을 제공하나

“KB-01 재고를 알려 줘”를 받은 LLM은 상품 번호를 해석하고 조회를 요청할 수 있다. 실제 재고는 업무 시스템에 있다. 앱이 조회 함수를 실행해 결과를 모델에 돌려줘야 답이 나온다. LangChain의 에이전트 API는 이 반복 실행과 모델·도구 연결을 제공한다.

| 구성 | 역할 |
| --- | --- |
| 모델 통합 | 공통 메시지·도구 인터페이스와 공급자 API를 연결한다. |
| 도구(tool) | 앱이 제공하는 실행 기능이다. 이름, 설명, 입력 스키마, 구현을 갖는다. |
| 에이전트(agent) | 모델이 다음 도구를 선택할 수 있게 호출과 결과 관찰을 반복한다. |
| 미들웨어(middleware) | 모델이나 도구 호출 경계에 검사, 제한, 관측 같은 공통 정책을 건다. |
| 런타임 | LangChain의 `create_agent`로 만든 에이전트는 LangGraph 위에서 실행된다. |

흐름은 **메시지 → 모델 → 도구 호출 요청 → 앱이 도구 실행 → 결과 메시지 → 모델**이다. 모델이 도구 호출 없이 응답하면 일반적인 도구 루프가 끝난다. 모든 요청에서 한 번의 분류만 필요하면 모델의 구조화 출력을 받고 Python에서 분기하는 것으로 충분할 수 있다. 사용자의 질문에 따라 조회할 데이터와 추가 조회 여부가 달라지면 에이전트 루프가 유용하다. [Agents 가이드](https://docs.langchain.com/oss/python/langchain/agents)

## 2. 기초 — 재고 조회 에이전트

아래 Python 블록을 표시된 파일명으로 저장한다. 모델 호출 예제에는 `OPENAI_API_KEY`와 도구 호출을 지원하는 모델이 필요하다. 예제의 모델 ID는 계정에서 사용 가능한 ID로 바꿀 수 있다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install langchain==1.4.9 langchain-openai==1.7.4
$env:STUDY_MODEL = 'gpt-4.1-mini'
.\.venv\Scripts\python.exe inventory_agent.py
```

```python
# inventory_agent.py
import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

INVENTORY = {"KB-01": 7, "MS-02": 0}


@tool
def get_stock(sku: str) -> str:
    """상품 코드로 현재 재고를 조회한다. 예: KB-01."""
    key = sku.strip().upper()
    if key not in INVENTORY:
        return f"{key}: 상품 코드 없음"
    return f"{key}: 재고 {INVENTORY[key]}개"


def make_agent(**options):
    return create_agent(
        model=ChatOpenAI(model=os.environ["STUDY_MODEL"]),
        tools=[get_stock],
        system_prompt="재고 답변 전에 도구로 조회하라. 없는 상품과 재고 0을 구분하라.",
        **options,
    )


if __name__ == "__main__":
    result = make_agent().invoke(
        {"messages": [{"role": "user", "content": "KB-01과 MS-02 재고를 알려줘."}]}
    )
    for message in result["messages"]:
        print(message.type, getattr(message, "tool_calls", []), message.content)
```

관찰할 값은 KB-01의 7개, MS-02의 0개다. ZZ-99도 넣어 상품 없음과 구분되는지 본다. `tool_calls`에는 도구 이름과 인자, 호출 ID가 들어간다. 도구 결과 메시지는 호출 ID로 원래 요청과 연결된다. 조회가 필수인 업무에서는 앱이 선조회하거나 실행 기록에서 실제 호출을 확인한다. [도구 가이드](https://docs.langchain.com/oss/python/langchain/tools)

## 3. 중급 — 구조화 출력과 대화 상태

아래 파일을 앞의 파일 옆에 둔다. 상품 목록을 화면이나 다른 API에 넘길 형태로 받고, 같은 대화에서 후속 질문을 한다.

```python
# inventory_typed.py
from typing import Literal

from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field

from inventory_agent import make_agent


class StockItem(BaseModel):
    sku: str
    status: Literal["available", "out_of_stock", "unknown"]
    quantity: int | None = Field(ge=0, description="상품을 모르면 null")


class StockReport(BaseModel):
    items: list[StockItem]


agent = make_agent(
    response_format=ToolStrategy(StockReport),
    checkpointer=InMemorySaver(),
)
config = {"configurable": {"thread_id": "inventory-demo"}}
for question in ["KB-01과 MS-02의 재고는?", "그중 품절인 상품만 보여 줘."]:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config=config,
    )
    print(result["structured_response"].model_dump())
```

- `ToolStrategy`는 도구 호출을 이용해 지정 형식의 출력을 받는다. `ProviderStrategy`는 모델 공급자의 네이티브 구조화 출력 기능을 사용한다. 공급자를 바꿀 때 업무 도구와 출력 형식을 함께 지원하는지 확인한다.
- 타입 검증과 업무 검증은 별개다. 이 스키마는 수량의 음수를 거부하지만, 상태가 품절인데 수량이 7인 사례는 별도 검사가 필요하다.
- 체크포인터는 스레드 상태를 저장한다. `InMemorySaver`의 데이터는 프로세스가 종료되면 사라진다. 스레드에 속한 메시지, 스레드 간 사용자 선호, 주문 DB의 확정 데이터는 수명과 조회 권한을 각각 설계한다.
- 대화가 길면 입력 토큰이 늘어난다. 요약으로 대화를 줄일 때 업무 결정과 원본 식별자를 별도 필드에 남겨 두면 누락을 조사하기 쉽다.

[구조화 출력](https://docs.langchain.com/oss/python/langchain/structured-output) · [단기 메모리](https://docs.langchain.com/oss/python/langchain/short-term-memory) · [장기 메모리](https://docs.langchain.com/oss/python/langchain/long-term-memory)

## 4. 심화 — 검색과 권한을 도구 경계에 두기

검색 증강 생성(RAG)은 문서 검색 결과를 모델 입력에 제공하는 방식이다. 항상 정책을 인용해야 하면 먼저 검색해 컨텍스트에 넣을 수 있다. 질문마다 정책, 상품, 주문 중 서로 다른 자료를 찾아야 하면 모델이 검색 도구를 선택하도록 구성할 수 있다. 아래 예제는 작은 인메모리 검색으로 권한 전달을 보여 준다.

```python
# policy_agent.py
import os
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.tools import ToolRuntime, tool
from langchain_openai import ChatOpenAI


@dataclass
class AccessContext:
    account_id: str


POLICIES = {
    "demo-account": {"return-v3": "미개봉 상품은 수령 후 14일 이내 반품 접수 가능."},
}


@tool
def lookup_policy(doc_id: str, runtime: ToolRuntime[AccessContext]) -> str:
    """로그인 계정의 정책을 조회한다. 반품 정책 문서 ID는 return-v3."""
    documents = POLICIES.get(runtime.context.account_id, {})
    if doc_id not in documents:
        return "조회 가능한 문서 없음"
    return f"[{doc_id}] {documents[doc_id]}"


agent = create_agent(
    model=ChatOpenAI(model=os.environ["STUDY_MODEL"]),
    tools=[lookup_policy],
    context_schema=AccessContext,
    middleware=[ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")],
    system_prompt="조회한 정책을 근거로 답하고 문서 ID를 인용하라.",
)
result = agent.invoke(
    {"messages": [{"role": "user", "content": "미개봉 반품 기한은?"}]},
    context=AccessContext(account_id="demo-account"),
)
print(result["messages"][-1].content)
```

실서비스에서는 서버가 인증된 계정으로 `AccessContext`를 만든다. 모델이 계정 ID를 지정할 수 있으면 권한 밖 조회를 요청할 수 있다. 조회 권한은 검색 결과를 모델에 넘기기 전에 검사한다. 검색 문서에 들어 있는 지시문도 외부 데이터로 취급한다. 모델 호출 제한은 반복 비용을 제어한다. 도구 타임아웃, 외부 변경 권한, 한도 초과 시 응답 처리 등에는 각각 별도 정책이 필요하다.

미들웨어로 공급자 라우팅, 도구 오류 정규화, 호출 로그를 공통화할 수 있다. 승인과 변경의 순서처럼 업무 절차 자체에 제약이 있을 때는 그래프 노드나 일반 함수로 그 순서를 명시한다. [커스텀 미들웨어](https://docs.langchain.com/oss/python/langchain/middleware/custom) · [내장 미들웨어](https://docs.langchain.com/oss/python/langchain/middleware/built-in)

## 5. 제작 관점의 장단점과 검증

| 장점 | 그에 따르는 작업 |
| --- | --- |
| 모델·도구·출력 형식을 조합해 프로토타입을 빨리 만든다. | 공급자마다 도구 선택 품질, 병렬 호출, 구조화 출력과 비용이 달라 재평가가 필요하다. |
| 공통 훅에 정책을 분리할 수 있다. | 훅이 여러 개일 때 적용 순서와 예외 경로가 복잡해진다. |
| 모델이 상황에 맞게 조회 순서를 고른다. | 호출 누락·반복·잘못된 인자를 추적하고 결정적인 규칙을 코드로 보장한다. |
| LangGraph 체크포인트를 사용할 수 있다. | 스레드 접근 제어, 보존 기간, 저장소 운영은 앱의 몫이다. |

먼저 `get_stock.invoke({"sku": "MS-02"})`로 모델 없이 도구를 확인한다. 모델 실험에서는 동일 질문을 반복해 호출 여부와 답의 근거를 기록한다. 다음으로 다른 계정, 미등록 상품, 호출 한도, 외부 시스템 지연을 재현한다. 운영 지표는 최종 답 정확도, 권한 위반 차단율, 요청당 도구·모델 호출 수, p95 지연과 비용을 함께 본다.

소스에서는 `create_agent`에서 모델 노드와 도구 노드를 만든 뒤 어떤 조건으로 엣지를 연결하는지 찾는다. 그 구조와 2절에서 출력한 메시지 순서를 대조하면 모델이 도구 결과를 받는 경계를 확인할 수 있다. [create_agent 구현](https://github.com/langchain-ai/langchain/blob/master/libs/langchain_v1/langchain/agents/factory.py) · [LangChain 소스 저장소](https://github.com/langchain-ai/langchain)
