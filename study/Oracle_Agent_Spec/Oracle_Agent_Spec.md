# Oracle Open Agent Specification — 에이전트 정의를 런타임과 분리하기

Python 실습 · JSON/YAML 직렬화 · WayFlow · LangGraph 어댑터\
기준 버전 · PyAgentSpec 26.3.1, WayFlow Core 26.3.1\
함께 읽기 · [LangChain](../LangChain/LangChain.md) · [LangGraph](../LangGraph/LangGraph.md) · [Deep Agents](../Deep_Agents/Deep_Agents.md)

## 0. 무엇을 만들고 어떤 순서로 배우나

완성할 것은 상품 코드를 받아 실제 재고 도구를 실행하는 에이전트와, 같은 조회를 정해진 순서로 실행하는 플로다. Python 함수와 딕셔너리를 읽을 수 있으면 시작할 수 있다. 모델 API 키가 없다면 **2절 → 4절 → 8절** 순서로 진행한다. 이 경로만으로 선언을 만들고, 다른 두 런타임에서 동일한 업무 결과를 얻는 과정을 경험할 수 있다.

| 결과물 | 무엇을 확인하나 |
| --- | --- |
| `stock-agent.json` / `stock-agent.yaml` | 모델 설정과 도구 계약이 직렬화되는지 |
| WayFlow 또는 LangGraph 에이전트 | 선언과 앱의 Python 함수가 연결되는지 |
| `stock-flow.json` | 제어 경로와 데이터 경로가 어떻게 표현되는지 |
| 두 런타임의 조회 결과 | 같은 선언을 읽었을 때 정상·품절·미등록을 같은 의미로 처리하는지 |

직렬화는 실행 구성을 파일로 옮길 수 있는 데이터로 만드는 과정이다. 반대로 역직렬화는 파일을 읽어 구성 요소를 복원한다. 역직렬화와 런타임 변환은 별도 단계다. 변환에 성공한 뒤에야 실행 엔진이 도구나 모델을 호출한다.

## 1. 무엇을 해결하나

재고 상담 에이전트를 두 팀이 운영한다고 하자. 한 팀은 WayFlow를 쓰고 다른 팀은 LangGraph를 쓴다. 두 팀 모두 모델 설정, 재고 도구 이름과 입출력, 상담 지침을 공유하고 싶다. Oracle의 Open Agent Specification(Agent Spec)은 이런 구성을 선언하고 JSON이나 YAML로 교환할 수 있게 정의하는 공개 명세다. 명세의 `Agent`는 에이전트 선언이며, 실행 엔진은 어댑터가 그 선언을 번역한 뒤 동작한다.

| 구성 | 담당하는 일 |
| --- | --- |
| Agent Spec | 모델·도구·에이전트·워크플로를 표현하는 구성 형식과 의미를 정의한다. |
| PyAgentSpec | Python 객체로 구성을 만들고 JSON/YAML로 직렬화하거나 역직렬화한다. |
| 런타임 어댑터 | 구성 요소를 대상 프레임워크의 실행 객체로 변환한다. |
| WayFlow | Oracle의 참조 런타임이다. 에이전트나 플로를 로드해 실행한다. |
| 업무 코드 | 도구 구현, 인증, 권한, 데이터 저장, 외부 부작용을 처리한다. |

```text
Python 선언 → Agent Spec JSON/YAML → 런타임별 어댑터 → 실행 객체
                                     ↑                   │
                              업무 도구 레지스트리       └─ 모델·도구 실행
```

`Agent`에서는 모델이 다음 도구나 응답을 선택한다. `Flow`에서는 개발자가 실행 경로와 데이터 연결을 명시한다. 둘 다 동일한 명세 생태계에 속한다. MCP는 도구나 리소스를 제공하는 서버와 연결하는 프로토콜이고, A2A는 에이전트 간 요청·응답에 쓰는 프로토콜이다. Agent Spec은 이러한 연결을 포함해 에이전트와 플로의 구성을 기술한다. [언어 명세](https://oracle.github.io/agent-spec/26.3.1/agentspec/language_spec_26_3_1.html) · [기술 보고서](https://arxiv.org/abs/2510.04173)

### 정의와 실행의 경계를 예제로 읽기

재고 도구를 새 환경으로 옮긴다고 하자. `ServerTool`의 선언은 ‘어떤 이름의 도구가 어떤 SKU를 받아 무엇을 반환하는가’를 기술한다. 실제 재고 원장에 어떻게 접속하는지는 서비스가 제공하는 Python 함수의 일이다. 런타임 로더에 그 함수를 지정하면 둘이 연결된다. 같은 파일을 옮겨도 접속 권한이나 실제 재고 데이터까지 복제되는 것은 아니다.

| 옮길 요소 | 이 예제의 위치 |
| --- | --- |
| 모델 ID와 시스템 지침 | `stock-agent.json` |
| 도구 이름과 입력·출력 필드 | `stock-agent.json` |
| 실제 DB 연결과 권한 검사 | 실행 앱의 도구 구현 |
| 도구를 언제 실행할지 | 에이전트에서는 모델의 선택, 플로에서는 제어 연결 |
| 대화 이력과 실행 중 상태 | 대상 런타임 또는 앱의 저장소 |

[Oracle 공식 개요](https://oracle.github.io/agent-spec/26.3.1/) · [보안과 도구 레지스트리](https://oracle.github.io/agent-spec/26.3.1/security.html)

## 2. 기초 — 재고 에이전트를 JSON과 YAML로 내보내기

각 Python 블록을 표시된 파일명으로 같은 실습 폴더에 저장한다. 먼저 Python 3.11의 독립 가상환경을 만든다. 이 단계는 모델 API 키를 사용하지 않는다.

```powershell
py -3.11 -m venv .venv-wayflow
.\.venv-wayflow\Scripts\python.exe -m pip install pyagentspec==26.3.1 wayflowcore==26.3.1
$env:STUDY_MODEL = 'gpt-4.1-mini'
.\.venv-wayflow\Scripts\python.exe stock_spec.py
```

```python
# stock_spec.py
import os
from pathlib import Path

from pyagentspec.agent import Agent
from pyagentspec.llms import OpenAiConfig
from pyagentspec.property import StringProperty
from pyagentspec.serialization import AgentSpecDeserializer, AgentSpecSerializer
from pyagentspec.tools import ServerTool


def lookup_stock(sku: str) -> str:
    """상품 코드의 재고를 조회한다."""
    key = sku.strip().upper()
    counts = {"KB-01": 7, "MS-02": 0}
    if key not in counts:
        return f"{key}: 상품 없음"
    return f"{key}: 재고 {counts[key]}개"


stock_tool = ServerTool(
    name="lookup_stock",
    description="상품 코드 KB-01 또는 MS-02의 재고를 조회한다.",
    inputs=[StringProperty(title="sku")],
    outputs=[StringProperty(title="stock")],
)

agent = Agent(
    name="Inventory assistant",
    llm_config=OpenAiConfig(
        name="inventory-model",
        model_id=os.getenv("STUDY_MODEL", "gpt-4.1-mini"),
    ),
    system_prompt="재고를 답하기 전에 lookup_stock을 호출한다. 재고 0과 상품 없음을 구분한다.",
    tools=[stock_tool],
)

if __name__ == "__main__":
    serializer = AgentSpecSerializer()
    raw = serializer.to_json(agent)
    Path("stock-agent.json").write_text(raw, encoding="utf-8")
    Path("stock-agent.yaml").write_text(serializer.to_yaml(agent), encoding="utf-8")
    restored = AgentSpecDeserializer().from_json(raw)
    assert restored.tools[0].name == "lookup_stock"
    assert restored.tools[0].inputs[0].title == "sku"
```

내보낸 파일에서 `component_type`, `agentspec_version`, 모델 ID, 도구 이름, `sku`·`stock` 스키마를 찾는다. 생성된 표현에서 컴포넌트 ID와 참조가 같은 객체를 가리키는 방식도 살펴본다. 도구의 Python 구현은 런타임 레지스트리에 제공한다. JSON에서 같은 도구 이름을 썼더라도 다른 구현을 등록하면 결과가 바뀔 수 있으므로 운영에서는 도구 계약과 구현 버전도 관리한다. [PyAgentSpec 저장소 및 시작 예제](https://github.com/oracle/agent-spec)

## 3. 중급 — WayFlow에서 선언에 실제 도구 연결하기

실제 모델을 호출하려면 `OPENAI_API_KEY`를 환경 변수에 설정하고, `STUDY_MODEL`은 계정에서 도구 호출이 가능한 모델 ID로 설정한다. 모델을 바꿨다면 2절의 JSON을 다시 생성한다. 4절에는 키 없이 실행할 수 있는 플로가 있다.

```python
# run_wayflow.py
from pathlib import Path

from wayflowcore.agentspec import AgentSpecLoader
from wayflowcore.tools import ServerTool

from stock_spec import lookup_stock

implementation = ServerTool(
    name="lookup_stock",
    description="상품 코드의 재고를 조회한다.",
    parameters={"sku": {"type": "string"}},
    output={"title": "stock", "type": "string"},
    func=lookup_stock,
)


def load_agent():
    loader = AgentSpecLoader(tool_registry={"lookup_stock": implementation})
    return loader.load_json(Path("stock-agent.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    assistant = load_agent()
    conversation = assistant.start_conversation()
    conversation.append_user_message("KB-01과 MS-02의 재고를 확인해 줘.")
    conversation.execute()
    for message in conversation.get_messages():
        print(message.message_type, message.content)
```

같은 이름을 키로 하여 선언과 구현을 연결한다. 실행 결과에서 KB-01의 7개, MS-02의 0개와 도구 요청·응답을 확인한다. 미등록 SKU는 상품 없음으로 별도 처리한다. `Agent`의 프롬프트는 조회를 요청하도록 유도한다. 조회가 업무상 반드시 필요한 경우 4절처럼 도구 노드를 플로에 둔다. [WayFlow에서 실행하기](https://oracle.github.io/agent-spec/26.3.1/howtoguides/howto_execute_agentspec_with_wayflow.html)

### 선언을 읽을 때 오류가 나는 위치

- 모델 설정이나 도구 스키마가 명세에 맞지 않으면 먼저 생성·역직렬화 단계에서 확인한다.
- 선언은 유효해도 목표 어댑터가 해당 컴포넌트를 변환하지 못할 수 있다. 지원 매트릭스와 배포 버전을 확인한다.
- 변환할 때 도구가 누락되면 레지스트리 키를 선언의 이름과 대조한다. 동일 이름이어도 앱 함수가 받는 인자와 반환값이 계약과 일치해야 한다.
- 로드 성공 뒤에만 실제 모델 호출을 확인한다. 모델 접근 오류, 잘못된 모델 출력, 업무 도구 오류는 각각 별도로 처리한다.

## 4. 심화 — 고정 조회 절차를 Flow로 만들기

같은 도구를 모델 선택 없이 한 번 실행한다. 제어 엣지는 **시작 → 조회 → 종료** 순서를, 데이터 엣지는 **시작의 sku → 조회의 sku**, **조회의 stock → 종료의 stock** 연결을 나타낸다. 이 구분 덕분에 실행 순서와 전달되는 값을 따로 읽을 수 있다.

```python
# stock_flow.py
from pathlib import Path

from pyagentspec.flows.flow import Flow
from pyagentspec.flows.edges.controlflowedge import ControlFlowEdge
from pyagentspec.flows.edges.dataflowedge import DataFlowEdge
from pyagentspec.flows.nodes import EndNode, StartNode, ToolNode
from pyagentspec.serialization import AgentSpecSerializer

from stock_spec import stock_tool

start = StartNode(name="start", inputs=stock_tool.inputs)
lookup = ToolNode(name="lookup", tool=stock_tool)
end = EndNode(name="finish", outputs=stock_tool.outputs)

flow = Flow(
    name="Inventory lookup",
    start_node=start,
    nodes=[start, lookup, end],
    control_flow_connections=[
        ControlFlowEdge(name="start lookup", from_node=start, to_node=lookup),
        ControlFlowEdge(name="finish lookup", from_node=lookup, to_node=end),
    ],
    data_flow_connections=[
        DataFlowEdge(
            name="pass sku",
            source_node=start,
            source_output="sku",
            destination_node=lookup,
            destination_input="sku",
        ),
        DataFlowEdge(
            name="pass stock",
            source_node=lookup,
            source_output="stock",
            destination_node=end,
            destination_input="stock",
        ),
    ],
)

if __name__ == "__main__":
    Path("stock-flow.json").write_text(
        AgentSpecSerializer().to_json(flow), encoding="utf-8"
    )
```

```python
# run_stock_flow.py
from pathlib import Path

from wayflowcore.agentspec import AgentSpecLoader
from wayflowcore.executors.executionstatus import FinishedStatus

from run_wayflow import implementation

loader = AgentSpecLoader(tool_registry={"lookup_stock": implementation})
assistant = loader.load_json(Path("stock-flow.json").read_text(encoding="utf-8"))
for sku, expected in [("MS-02", "MS-02: 재고 0개"), ("ZZ-99", "ZZ-99: 상품 없음")]:
    conversation = assistant.start_conversation({"sku": sku})
    status = conversation.execute()
    assert isinstance(status, FinishedStatus)
    assert status.output_values["stock"] == expected
    print(expected)
```

위 순서대로 `stock_spec.py`, `stock_flow.py`, `run_stock_flow.py`를 실행한다. 4절에서는 `run_wayflow.py`에서 등록할 도구만 재사용한다. `Flow`에서 조건 분기가 필요하면 분기 노드 또는 `FlowBuilder.add_conditional`의 매핑과 기본 목적지를 선언한다. 주문 수정이나 취소라면 권한 검사, 승인, 실제 변경을 별도 단계로 분리하고 변경 작업의 멱등성 키를 업무 시스템에 전달한다. [조건 분기](https://oracle.github.io/agent-spec/26.3.1/howtoguides/howto_flow_with_conditional_branches.html) · [FlowBuilder](https://oracle.github.io/agent-spec/26.3.1/howtoguides/howto_flowbuilder.html)

## 5. 심화 — 같은 Agent Spec을 LangGraph에 로드하기

26.3.1 배포판에서 WayFlow Core와 PyAgentSpec의 LangGraph extra가 서로 겹치지 않는 `anyio` 범위를 요구한다. 런타임별 가상환경을 나누고 같은 JSON을 입력으로 사용한다.

```powershell
py -3.11 -m venv .venv-langgraph
.\.venv-langgraph\Scripts\python.exe -m pip install 'pyagentspec[langgraph]==26.3.1'
.\.venv-langgraph\Scripts\python.exe run_langgraph.py
```

```python
# run_langgraph.py
import asyncio
from pathlib import Path

from pyagentspec.adapters.langgraph import AgentSpecLoader

from stock_spec import lookup_stock


def load_agent():
    loader = AgentSpecLoader(tool_registry={"lookup_stock": lookup_stock})
    return loader.load_json(Path("stock-agent.json").read_text(encoding="utf-8"))


async def main():
    assistant = load_agent()
    result = await assistant.ainvoke(
        {"messages": [{"role": "user", "content": "MS-02 재고는?"}]}
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
```

WayFlow Core 26.3.1 배포본에서는 대화 객체의 `execute()`를 사용한다. LangGraph에서는 변환된 그래프에 메시지 상태를 넘긴다. 이식되는 것은 명세에 표현되고 어댑터가 지원하는 구성이다. 각 런타임의 대화·체크포인트 데이터, 호출 제한과 오류 처리, 프레임워크 전용 미들웨어는 별도로 비교한다. LangGraph 에이전트를 Agent Spec으로 내보내는 어댑터도 있지만 사용자 정의 Python 노드와 상태를 포함한 임의 그래프가 그대로 왕복 변환된다고 가정하면 안 된다. 대상 버전의 지원 항목을 확인하고 실제 구성으로 테스트한다. [LangGraph 어댑터](https://oracle.github.io/agent-spec/26.3.1/adapters/langgraph/index.html) · [어댑터 API](https://oracle.github.io/agent-spec/26.3.1/api/adapters.html)

## 6. 제작 관점의 장단점

| 장점 | 그에 따르는 작업 |
| --- | --- |
| 선언과 실행 코드를 분리해 구성 변경을 검토하고 배포할 수 있다. | 명세·어댑터·런타임·업무 도구의 버전 조합을 관리한다. |
| 도구 입출력과 플로의 연결을 명시할 수 있다. | 스키마 검증에 더해 실제 도구의 업무 의미와 권한을 검사한다. |
| 지원되는 구성으로 여러 런타임을 실험할 수 있다. | 고유 노드·모델·승인·스트리밍·예외 동작의 지원 여부를 확인한다. |
| 같은 구성으로 후보 런타임을 비교하기 쉽다. | 모델 호출 순서, 프롬프트 조립, 상태 복구, 지연과 비용을 별도로 측정한다. |

[LangChain](../LangChain/LangChain.md)으로는 도구를 등록해 바로 에이전트 루프를 구성할 수 있고, [LangGraph](../LangGraph/LangGraph.md)는 실행 상태와 엣지를 애플리케이션 코드에 직접 표현한다. [Deep Agents](../Deep_Agents/Deep_Agents.md)는 계획·작업 공간·위임을 묶은 하네스다. Agent Spec을 쓸 때는 구성 배포와 런타임 교체가 필요한지, 필요한 기능이 이식 가능한 범위 안에 있는지가 판단 기준이다. 한 런타임에서 커스텀 노드를 자주 수정하는 경우에는 어댑터 계층을 유지하는 비용도 계산한다.

## 7. 운영 점검과 소스 읽기

1. **검증을 두 층으로 나눈다.** 직렬화 왕복에서 도구와 데이터 연결이 유지되는지 확인한다. 실행 테스트에서는 값과 분기 외에도 도구 호출 횟수, 인자, 오류, 승인 거절 시 외부 변경 0회를 검증한다.
2. **신뢰 경계를 지정한다.** 제3자 명세를 배포하기 전에 허용 컴포넌트와 도구 목록, 접속 대상 URL, 템플릿과 플러그인을 검토한다. 로더의 허용·차단 옵션과 실행 환경의 네트워크 정책을 함께 적용한다. 원격 호출에는 사용자·테넌트 권한을 사용하고 비밀은 실행 환경에서 주입한다.
3. **업그레이드 전에 양쪽을 비교한다.** 동일 SKU, 미등록 SKU, 잘못된 입력, 도구 예외, 모델 호출 실패를 각 런타임에 넣어 본다. 최종 응답 문구 외에 구조화 결과와 실행 기록을 비교한다.
4. **실행 코드로 확인한다.** 소스의 어댑터 공통 로더에서 역직렬화와 컴포넌트 변환 경계를 찾고, LangGraph 어댑터의 서버 도구 변환과 WayFlow의 로더를 비교한다. 선언에 적힌 이름이 각 런타임의 함수 또는 도구로 연결되는 지점이 핵심이다.

[보안 가이드](https://oracle.github.io/agent-spec/26.3.1/security.html) · [버전별 변경점](https://oracle.github.io/agent-spec/26.3.1/changelog.html) · [Oracle 어댑터 예제 소스](https://github.com/oracle/agent-spec/tree/main/adapters_examples) · [WayFlow 실행 소스](https://github.com/oracle/wayflow)

## 8. 키 없이 이식성 확인하기 — 같은 Flow를 LangGraph에서 실행

4절에서 생성한 `stock-flow.json`을 그대로 사용한다. WayFlow 쪽에서는 `start_conversation({"sku": ...})`으로 값을 전달했다. 여기서는 LangGraph 어댑터가 만드는 플로 상태의 `inputs`에 값을 넣고 `outputs`에서 결과를 꺼낸다. 실행 인터페이스가 달라도 두 런타임이 동일한 업무 결과를 내는지 확인한다.

```python
# compare_flow_langgraph.py
from pathlib import Path

from pyagentspec.adapters.langgraph import AgentSpecLoader

from stock_spec import lookup_stock

source = Path("stock-flow.json").read_text(encoding="utf-8")
flow = AgentSpecLoader(tool_registry={"lookup_stock": lookup_stock}).load_json(source)
cases = {
    "KB-01": "KB-01: 재고 7개",
    "MS-02": "MS-02: 재고 0개",
    "ZZ-99": "ZZ-99: 상품 없음",
}
for sku, expected in cases.items():
    result = flow.invoke({"inputs": {"sku": sku}})
    assert result["outputs"]["stock"] == expected
    print(expected)
```

5절의 LangGraph 가상환경으로 실행한다. `{"sku": sku}`를 바깥에 직접 넘기면 이 플로의 시작 노드가 입력을 받지 못한다. 대화형 `Agent`의 `messages` 호출 형식과도 다르다. 설치된 어댑터의 시작 노드가 `inputs`를 읽고 마지막 노드가 `outputs`를 쓰는지 확인할 수 있다. [LangGraph 어댑터 예제](https://github.com/oracle/agent-spec/tree/main/adapters_examples/langgraph) · [어댑터 API](https://oracle.github.io/agent-spec/26.3.1/api/adapters.html)

## 9. 도구·모델·워크플로의 확장 선택지

| 요구 | 명세에서 살펴볼 구성 | 앱이나 런타임이 확인할 내용 |
| --- | --- | --- |
| 사내 Python 함수를 호출한다 | `ServerTool` | 등록된 구현의 인자와 실행 권한 |
| 호출을 외부 서비스에 맡긴다 | `RemoteTool` 또는 MCP 구성 | 대상 서버, 인증, 타임아웃, 응답 검증 |
| 호출을 클라이언트에서 수행한다 | `ClientTool` | 대상 런타임의 실행 요청·응답 처리 방식 |
| 지점별 재고를 동시에 조사한다 | `ParallelFlowNode` 또는 `ParallelMapNode` | 결과 결합 규칙, 동시성 한도, 실패 시 처리 |
| 모델 출력에서 SKU와 수량을 받는다 | 구조화 출력을 선언한 LLM 노드 | 모델·어댑터 지원과 업무 규칙 검증 |
| 취소 요청을 검토 뒤 실행한다 | 확인이 필요한 도구 또는 승인 분기 | 승인 주체, 검토한 인자, 재개 방식, 멱등성 |

두 개의 작업이 동시에 실행될 수 있는지는 데이터 의존성부터 따진다. 재고 조사와 주문 취소는 무조건 병렬화할 일이 아니다. 서로 독립적인 지점 조회를 병렬로 하고, 수량 합산과 권한 검사는 결과가 모인 뒤 한다. 도구 확인 요청을 명세에 표현하더라도 앱에서는 실제 사용자의 승인 권한과 승인 내용을 검증한다. [노드·도구 API](https://oracle.github.io/agent-spec/26.3.1/api/index.html) · [확인 처리의 버전별 변경점](https://oracle.github.io/agent-spec/26.3.1/changelog.html)

### 실습 — 구성에서 허용한 컴포넌트만 복원하기

아래 스크립트는 2절의 에이전트 JSON을 사용한다. 동일한 입력을 두 정책으로 읽어 본다. 첫 번째는 샘플에 필요한 세 컴포넌트를 허용한다. 두 번째는 서버 도구를 빼므로 복원을 거부해야 한다. 모델을 호출하지 않는다.

```python
# check_spec_policy.py
from pathlib import Path

from pyagentspec.serialization import AgentSpecDeserializer

raw = Path("stock-agent.json").read_text(encoding="utf-8")
allowed = AgentSpecDeserializer(
    allowed_components=["Agent", "OpenAiConfig", "ServerTool"],
)
restored = allowed.from_json(raw)
assert restored.tools[0].name == "lookup_stock"

restricted = AgentSpecDeserializer(
    allowed_components=["Agent", "OpenAiConfig"],
)
try:
    restricted.from_json(raw)
except ValueError as error:
    assert "ServerTool" in str(error)
    print("허용되지 않은 ServerTool 차단")
else:
    raise AssertionError("구성 정책이 ServerTool을 허용했습니다.")
```

클래스 허용 정책은 컴포넌트의 종류를 검사한다. 이름이 허용된 모델이나 서버 도구라도 대상 URL, 레지스트리 구현, 데이터 접근 권한은 앱에서 별도로 검토한다. 운영 로더에는 같은 종류의 정책을 전달하고, 비밀이 직렬화 파일이나 오류 로그에 포함되지 않도록 확인한다. [역직렬화 정책](https://oracle.github.io/agent-spec/26.3.1/security.html) · [직렬화 API](https://oracle.github.io/agent-spec/26.3.1/api/serialization.html)

## 10. 최종 실습 — 팀 사이에서 구성 파일을 전달하기

1. 2절 JSON과 YAML을 만든 뒤 도구의 이름, `sku`와 `stock` 필드를 비교한다. 새 환경에는 가상환경 설치 명령과 도구 계약, 예제 입력만 전달한다.
2. 다른 폴더에서 같은 이름의 조회 구현을 등록하고 양쪽에서 재고 0과 미등록 결과를 비교한다. 일부러 이름을 바꿔 로드 오류와 실행 오류가 어떻게 다른지 확인한다.
3. 둘 중 한 환경에만 지원되는 새 구성 요소를 도입한다고 가정한다. 배포 전에 변환 가능성을 확인하는 테스트를 넣고, 대체 경로가 필요할 때 어떤 의미를 보존해야 하는지 작성한다.
4. 구조화 응답이 있는 버전을 만들면 유효한 출력뿐 아니라 잘못된 SKU, 수량 0, 누락된 필드도 평가한다. 런타임 이식성 검사는 동일 선언의 변환 가능성과 업무 결과의 일치를 각각 측정한다.
5. 임의 JSON을 서비스에서 로드한다면 허용 컴포넌트와 등록 도구를 제한하고 파일·네트워크·토큰 접근을 실행 환경에서 제한한다. 실제 업무 쓰기 도구를 연결하기 전에 거절 시 변경 0회, 재시도 시 변경 1회를 검증한다.

[공식 실습 목록](https://oracle.github.io/agent-spec/26.3.1/howtoguides/index.html) · [평가 API](https://oracle.github.io/agent-spec/26.3.1/api/evaluation.html)
