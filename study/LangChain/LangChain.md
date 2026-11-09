# LangChain — 모델과 도구로 업무 에이전트 만들기

Python 실습 · 기초부터 구조화 출력, 대화 상태, 권한 제어까지\
함께 읽기 · [LangGraph](../LangGraph/LangGraph.md) · [Deep Agents](../Deep_Agents/Deep_Agents.md)

## 0. 시작하기 전에

이 교재에서는 사용자 요청을 받아 상품 코드로 재고를 조회하고, 검증 가능한 결과를 돌려주는 상담 에이전트를 만든다. 먼저 한 번의 모델 호출과 도구 실행의 차이를 이해한 다음, 실행 기록을 읽고 구조화 출력과 권한을 붙인다. 마지막에는 실제 모델 없이 반복 가능한 테스트를 만든다.

| 순서 | 할 수 있게 되는 것 |
| --- | --- |
| 0–1절 | 메시지, 모델, 도구, 에이전트를 구분한다. |
| 2절 | 상담 에이전트를 실행하고 중간 도구 호출을 읽는다. |
| 3–4절 | 후속 질문, 구조화 출력, 권한이 있는 문서 조회를 구현한다. |
| 5–8절 | 운영 책임을 나누고 실패와 테스트를 설계한다. |

Python 함수, 딕셔너리, 타입 힌트가 기본 전제다. `def get_stock(sku: str) -> str`에서 `sku: str`은 문자열 인자를, `-> str`은 반환 타입을 나타낸다. `@tool` 데코레이터는 이 정보를 도구 정의에 사용한다. 실습 폴더를 만든 뒤 2절 명령을 실행하고, 각 코드를 표시된 이름의 파일에 저장한다. API 키가 없어도 6절의 모의 모델 실습을 실행할 수 있다.

### 모델에 전달되는 것

모델에 보내는 메시지는 역할과 내용을 가진다. 시스템 지침은 응답 원칙을, 사용자 메시지는 요청을 나타낸다. 모델의 응답에는 자연어 본문 외에 구조화된 도구 호출 요청이 들어갈 수 있다. 도구 정의에는 이름, 설명, 인자 스키마가 들어가며 Python 함수 본문은 앱에서 실행된다. 모델이 만든 SKU와 사용자가 실제로 접근할 수 있는 SKU는 앱이 따로 확인한다.

한 번만 모델을 호출하는 Python 코드는 다음과 같다. 2절의 설치를 먼저 하고 `OPENAI_API_KEY`와 `STUDY_MODEL`을 설정한다. 입력과 응답을 먼저 확인한 뒤, 2절에서 도구가 포함될 때 어떤 메시지가 추가되는지 비교한다.

```python
# model_only.py
import os

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model=os.environ["STUDY_MODEL"])
reply = model.invoke([
    {"role": "system", "content": "상품 코드를 보고 문자열 형식만 설명하라."},
    {"role": "user", "content": "KB-01은 어떤 형식인가요?"},
])
print(reply.type, reply.content)
```

실제 재고는 이 입력에 없다. 어떤 숫자가 답에 나타나도 앱이 업무 DB를 읽었다는 증거가 되지 않는다. 2절에서는 도구 요청과 실행 결과가 메시지에 추가되면서 그 근거를 추적할 수 있다. [모델과 메시지](https://docs.langchain.com/oss/python/langchain/models)

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

### 실행 기록을 읽는 순서

1. 사용자 메시지에 상품 코드 두 개가 들어갔는지 확인한다.
2. `ai` 메시지의 `tool_calls`에서 함수 이름과 `args`를 읽는다. 한 모델 응답에 도구 요청이 여러 건 올 수 있다.
3. `tool` 메시지에서 실제 반환값을 찾는다. KB-01은 7개, MS-02는 0개다. 알 수 없는 상품의 응답도 따로 확인한다.
4. 마지막 모델 응답이 도구의 값과 일치하는지 비교한다. 도구가 실행됐는데 최종 답이 틀릴 수도 있다.

모델 호출이 실패하면 먼저 키 설정과 모델 접근 권한을 확인한다. 호출은 성공했지만 조회가 없으면 모델의 도구 지원과 지시문, 등록된 도구 목록을 검사한다. 조회는 됐지만 함수가 잘못된 상품을 읽었다면 모델 인자와 도구 입력 정규화를 나눠 점검한다.

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

### 실습 — 출력 형태와 업무 규칙을 함께 검사하기

3절의 기본 스키마에는 상태와 수량이 일치해야 한다는 규칙이 없다. 아래 코드에서 품절은 0, 정상은 양수, 미등록은 null로 연결한다. 이 예제는 모델을 호출하지 않는다. 구조화 출력을 실행할 때 이 클래스를 `ToolStrategy`에 넘기면 동일한 스키마를 재사용할 수 있다. 실제 재고와의 일치는 도구 응답이나 DB와 따로 대조한다.

```python
# verify_stock_schema.py
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, model_validator


class StockItem(BaseModel):
    sku: str
    status: Literal["available", "out_of_stock", "unknown"]
    quantity: int | None = Field(ge=0)

    @model_validator(mode="after")
    def status_matches_quantity(self):
        expected = (
            "unknown" if self.quantity is None
            else "out_of_stock" if self.quantity == 0
            else "available"
        )
        if self.status != expected:
            raise ValueError("재고 상태와 수량이 일치해야 합니다.")
        return self


assert StockItem(sku="MS-02", status="out_of_stock", quantity=0).quantity == 0
assert StockItem(sku="ZZ-99", status="unknown", quantity=None).quantity is None

try:
    StockItem(sku="KB-01", status="out_of_stock", quantity=7)
except ValidationError as error:
    assert "재고 상태와 수량" in str(error)
    print("형식은 맞지만 업무 규칙이 틀린 결과를 차단했습니다.")
else:
    raise AssertionError("잘못된 재고 상태가 통과했습니다.")
```

`quantity`에서 null이 허용된다는 것은 값이 없는 상품을 표현할 수 있다는 뜻이다. 필드 자체를 생략해도 된다는 뜻은 아니다. 에이전트가 유효한 형식을 반환하지 못했을 때는 오류를 별도 결과로 처리하고, 제한 없이 모델에 수정 요청을 반복하지 않는다. [구조화 출력과 오류 처리](https://docs.langchain.com/oss/python/langchain/structured-output)

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

## 6. 모델 요금 없이 에이전트 루프 테스트하기

테스트에서 모델이 도구 호출을 제안하는 메시지와 마지막 답을 직접 공급하면, 네트워크나 모델 변동성 없이 **도구가 실제로 실행되고 올바른 호출 ID로 결과가 연결되는지** 확인할 수 있다. 이 실습은 2절 파일 옆에 저장하고 `inventory_agent.py`의 도구를 재사용한다.

```python
# test_inventory_loop.py
from langchain.agents import create_agent
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, ToolMessage

from inventory_agent import get_stock


class ScriptedModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


model = ScriptedModel(messages=iter([
    AIMessage(content="", tool_calls=[
        {"name": "get_stock", "args": {"sku": "MS-02"}, "id": "lookup-1"},
    ]),
    AIMessage(content="MS-02는 품절입니다."),
]))
agent = create_agent(model=model, tools=[get_stock])
result = agent.invoke({"messages": [{"role": "user", "content": "MS-02 재고는?"}]})
observations = [m for m in result["messages"] if isinstance(m, ToolMessage)]
assert len(observations) == 1
assert observations[0].tool_call_id == "lookup-1"
assert observations[0].content == "MS-02: 재고 0개"
assert result["messages"][-1].content == "MS-02는 품절입니다."
print("도구 실행과 호출 ID 연결을 확인했습니다.")
```

이 테스트는 모델의 답을 미리 정했다. 실제 모델이 잘못된 도구를 고르거나 인자를 누락하는 비율은 별도 평가에서 측정한다. 실제 평가 질문은 한 상품, 여러 상품, 불명확한 SKU, 접근 금지 상품, 결과가 바뀐 상품을 각각 포함한다. [LangChain 테스트](https://docs.langchain.com/oss/python/langchain/test)

## 7. 상담 에이전트를 서비스로 옮기는 순서

### 업무 데이터와 대화 데이터를 분리한다

| 데이터 | 저장 위치 예시 | 갱신 주체 |
| --- | --- | --- |
| 현재 재고와 상품 상태 | 업무 DB 또는 사내 API | 재고 시스템 |
| 직전 질문과 조회 결과 | 스레드 체크포인트 | 에이전트 런타임 |
| 여러 대화에서 쓸 알림 선호 | 계정별 저장소 | 앱의 명시적 업데이트 |
| 평가 입력, 성공률, 지연 | 운영 관측·평가 데이터셋 | 테스트와 운영 도구 |

대화 메시지에 어제 조회한 재고가 있어도 오늘 재고는 다시 읽어야 한다. 후속 질문의 ‘그 상품’은 대화에서 해석하되 수량은 최신 업무 시스템에서 조회한다. 체크포인트에는 인증 토큰을 담지 않고, 스레드 ID만 알아도 다른 사람의 대화를 읽는 일이 없도록 서버에서 소유권을 확인한다.

### 도구를 작게 나누고 실패를 구분한다

`get_stock`과 `reserve_stock`은 분리한다. 읽기 호출은 재시도가 가능하더라도 예약 호출은 중복으로 재고를 차감할 수 있다. 예약은 서버에서 권한과 수량을 확인하고, 사용자의 승인 대상과 멱등성 키를 업무 서비스에 전달한다. 도구가 상품 없음과 재고 0을 구분하듯, 운영에서는 네트워크 시간 초과, 인가 거절, 입력 검증 실패도 별도로 기록한다.

### 앱의 반환 계약을 정한다

성공 시에는 상품별 상태와 수량을 반환한다. 권한 실패나 조회 지연 시에는 그 실패를 명시하고, 모델이 만들어 낸 수량을 정상 결과로 저장하지 않는다. 여러 상품 중 일부만 실패할 수 있다면 상품별 오류를 별도 필드로 표시한다. `invoke`는 최종 상태가 필요한 동기 실행에 맞고, 비동기 서버에서는 `ainvoke`를 사용할 수 있다. 모델 토큰과 실행 진행 상태를 UI에서 구별해 보고 싶을 때 스트리밍을 적용한다. [스트리밍](https://docs.langchain.com/oss/python/langchain/streaming)

### 검색을 실제 문서 서비스에 연결할 때

4절에서는 문서 ID로 정확히 한 건을 찾아오는 작은 도구를 만들었다. 실제 질문에서 ID를 모른다면 인덱스를 준비하고 질의로 관련 자료를 찾는다. 일반적인 흐름은 **문서 수집 → 문단 분할과 메타데이터 부여 → 인덱싱 → 사용자 권한 범위에서 검색 → 발췌와 출처를 모델에 전달**이다.

- 문단마다 문서 ID, 버전, 제목을 보존한다. 인용 ID를 클릭했을 때 사용자가 같은 문서와 버전을 찾을 수 있어야 한다.
- 키워드 검색은 상품 코드나 정확한 문구에 유리하다. 임베딩 검색은 표현이 다른 유사 질의를 찾는 데 활용할 수 있다. 임베딩은 텍스트를 벡터로 표현하며, 그 벡터의 가까움이 해당 계정에서 읽을 권한을 의미하지 않는다.
- 검색에 실패했다면 답변을 생성하기 전에 ‘근거를 찾지 못함’을 표현할 수 있게 한다. 근거가 부족한 사례와 검색은 됐지만 답에 반영하지 않은 사례를 분리해 평가한다.
- 프롬프트, 검색, 모델 호출이 항상 같은 순서라면 고정 파이프라인이 간결하다. 외부 기능을 선택해야 할 때는 검색 도구를 에이전트에 제공한다. LangChain의 Runnable 조합을 읽을 때도 고정 연결과 `create_agent`의 동적 루프를 구분한다.

[공식 실습 목록의 RAG Agent](https://docs.langchain.com/oss/python/learn) · [도구](https://docs.langchain.com/oss/python/langchain/tools)

### 도구 연동과 배포를 구분한다

Python 함수 도구는 애플리케이션에서 직접 실행한다. MCP 서버를 연결하면 서버가 노출하는 도구를 클라이언트가 사용할 수 있다. 기존 서비스를 MCP로 노출하면 여러 클라이언트가 같은 도구 계약을 활용할 수 있지만, 서비스 인증·인가·타임아웃은 여전히 설계해야 한다. SDK·런타임·호스팅 서비스는 별도 의존성으로 기록한다. 로컬 테스트를 먼저 통과시키고, 호스팅을 선택할 때는 승인 대기 상태의 보존 방식, 동시 실행 정책, 로그에 포함되는 데이터를 검토한다. [MCP 연동](https://docs.langchain.com/oss/python/langchain/mcp)

## 8. 확장 실습과 확인 문제

1. 상품 없음, 재고 0, 정상 재고를 모두 테스트한다. 기대값이 다를 경우 함수 정규화, 도구 요청 인자, 최종 모델 응답 중 어느 층이 원인인지 구분한다.
2. `StockItem`에 상태·수량 관계를 검사하는 검증을 추가한다. 모델이 `out_of_stock`과 수량 7을 함께 반환했을 때 앱이 결과를 받아들이지 않도록 만든다.
3. 두 계정에 같은 문서 ID를 등록하되 서로 다른 내용을 넣는다. 서버가 만든 인증 컨텍스트로 결과가 분리되는지 확인한다.
4. 정책 검색을 고정 선검색과 모델 선택 도구 두 가지로 구현해 본다. 같은 질문 10개에 대해 검색 횟수, 근거 문서 ID 누락률, 응답 시간을 비교한다. [공식 실습 목록의 RAG Agent](https://docs.langchain.com/oss/python/learn)

스스로 설명할 수 있어야 하는 질문은 세 가지다. ‘도구 함수는 누가 실행하는가’, ‘잘 구성된 출력이 왜 올바른 업무 결과를 보장하지 않는가’, ‘어떤 상태를 스레드와 업무 DB에 각각 저장하는가’. 답을 2–4절 코드의 구체적인 함수와 필드에 연결해 확인한다.
