# Deep Agents — 계획, 작업 공간, 위임을 갖춘 에이전트 만들기

Python 실습 · 보고서 작성 · 서브에이전트 · 게시 승인\
함께 읽기 · [LangChain](../LangChain/LangChain.md) · [LangGraph](../LangGraph/LangGraph.md)

## 0. 만들 결과와 준비물

이 교재의 최종 목표는 **재고 보고서를 조사하고 초안을 저장한 뒤, 사람이 승인한 경우에만 게시 기록을 남기는 에이전트**를 설계하는 것이다. Python 함수와 딕셔너리를 읽을 수 있으면 시작할 수 있다. 2절의 버전으로 설치하고, 각 코드를 표시된 파일명으로 같은 폴더에 저장한다. 실제 모델 예제는 키가 필요하며 7절은 키 없이 실행할 수 있다.

| 학습 단계 | 관찰할 결과 |
| --- | --- |
| 보고서 초안 | 도구가 반환한 재고 근거를 작업 파일에 기록한다. |
| 조사 위임 | 부모와 전문 조사 에이전트가 각자 맡은 일을 한다. |
| 게시 승인 | 승인 전에는 외부 변경이 없고, 승인 뒤에만 기록이 생긴다. |
| 작업 공간 검증 | 같은 스레드에서 작업 파일을 읽고 다른 스레드에서는 분리된다. |

이 교재에서 **모델**은 다음 행동을 제안하고, **도구**는 조회·파일 기록·게시 같은 행동을 실행한다. **하네스**는 모델이 도구를 사용할 수 있게 반복을 운영하며 계획, 작업 공간, 위임, 승인과 같은 기능을 함께 구성한다. 모델에게 ‘보고서를 작성했다’는 답을 받는 것과 파일에 검증 가능한 보고서를 남기는 것은 다른 완료 조건이다.

## 1. 하네스란 무엇인가

재고 한 건을 조회하는 요청과 상품군 전체를 조사해 근거가 붙은 보고서를 만드는 요청은 실행 방식이 다르다. 후자에는 진행할 일 목록, 중간 결과를 보관할 공간, 일부 작업을 위임하는 방법이 도움이 된다. Deep Agents는 이러한 기능을 조합해 제공하는 에이전트 하네스다. Python에서는 `deepagents` 패키지의 `create_deep_agent`를 사용한다. SDK로 만든 앱은 개발자가 실행하며, LangChain이 별도로 제공하는 관리형 배포는 다른 실행 선택지다.

| 계층 | 제공하는 것 |
| --- | --- |
| LangGraph | 그래프 실행, 상태 및 체크포인트 |
| LangChain | 에이전트 루프, 모델·도구 통합, 미들웨어 |
| Deep Agents | 파일 작업 공간, 컨텍스트 관리와 서브에이전트 위임을 조합한 기본 구성. 할 일 도구 등은 미들웨어로 추가할 수 있다. |

할 일 목록은 모델이 관리하는 진행 상태다. 규정상 반드시 실행해야 하는 순서라면 업무 코드나 그래프 엣지로 제약을 건다. 파일 도구는 중간 산출물을 보관하고 일부를 다시 읽게 해 준다. 요약은 긴 대화에서 토큰 부담을 낮추는 데 도움이 되지만, 인용이나 수치가 중요하면 원본과 검증 결과를 별도로 남긴다. [공식 개요](https://docs.langchain.com/oss/python/deepagents/overview) · [SDK 빠른 시작](https://docs.langchain.com/oss/python/deepagents/quickstart)

### 보고서 한 건이 만들어지는 흐름

아래는 개념 흐름이다. 어느 도구를 몇 번 쓰는지는 요청과 모델에 따라 달라진다.

```text
요청과 완료 조건
    ↓
모델이 할 일과 다음 도구를 선택
    ↓
재고 도구가 원본 수치와 근거 ID 반환
    ↓
파일 도구로 초안을 작성하고 필요할 때 다시 읽음
    ↓
완료 보고 또는 누락된 근거 확인
```

모델의 컨텍스트는 이번 호출에서 모델이 읽는 정보다. 보고서와 모든 원자료를 매번 붙이면 이전 대화가 길어질수록 반복 입력이 늘어난다. 파일에 원문을 남겨 필요한 부분을 다시 읽거나, 서브에이전트가 조사하고 근거 요약만 반환하면 메인 에이전트의 입력 구성을 달리할 수 있다. 저장한 파일은 도구가 읽기 전까지 모델이 그 내용을 자동으로 알고 있다고 가정하지 않는다. [컨텍스트 설계](https://docs.langchain.com/oss/python/deepagents/context-engineering)

## 2. 기초 — 보고서 초안을 작업 공간에 남기기

모델 예제는 `OPENAI_API_KEY`가 필요하다. 아래 Python 블록을 `research_agent.py`로 저장한다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install deepagents==0.7.34 langchain-openai==1.7.4
$env:STUDY_MODEL = 'gpt-4.1-mini'
.\.venv\Scripts\python.exe research_agent.py
```

```python
# research_agent.py
import os

from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

CATALOG = {
    "KB-01": "INV-202: KB-01 키보드 재고 7개.",
    "MS-02": "INV-203: MS-02 마우스 재고 0개.",
}


@tool
def fetch_inventory(sku: str) -> str:
    """상품 코드 KB-01 또는 MS-02의 재고와 근거 ID를 조회한다."""
    return CATALOG.get(sku.strip().upper(), "근거 없음")


def study_model():
    return ChatOpenAI(model=os.environ["STUDY_MODEL"])


if __name__ == "__main__":
    agent = create_deep_agent(
        model=study_model(),
        tools=[fetch_inventory],
        middleware=[TodoListMiddleware()],
        system_prompt=(
            "할 일을 기록하고 두 상품을 조사하라. "
            "근거 ID와 재고를 /inventory.md에 작성하고 결과를 요약하라."
        ),
    )
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "KB-01, MS-02 재고 보고서를 만들어 줘."}]},
        config={"recursion_limit": 30},
    )
    for message in result["messages"]:
        for call in getattr(message, "tool_calls", []):
            print(call["name"], call["args"])
    print(result["messages"][-1].content)
```

이 예제는 `TodoListMiddleware`를 명시적으로 추가한다. 도구 로그에서 재고 조회, 파일 쓰기, 필요한 경우 할 일 목록 갱신을 확인한다. 보고서 완성 여부는 파일 내용과 근거 ID를 따로 검사한다. `StateBackend`가 기본값이며 에이전트 상태에 파일을 보관한다. `/inventory.md`는 이 예제에서 가상 경로다. 로컬 드라이브에 보고서를 쓰는 작업은 다른 백엔드나 별도 내보내기가 필요하다. [내장 도구](https://docs.langchain.com/oss/python/deepagents/tools) · [백엔드](https://docs.langchain.com/oss/python/deepagents/backends)

### 예제의 완료 조건을 관찰하기

보고서가 완성됐다고 판단하려면 (1) 두 SKU가 조회됐는지, (2) 결과의 근거 ID가 각각 INV-202와 INV-203인지, (3) 파일 쓰기 요청이 성공했는지 확인한다. 마지막 응답만 읽으면 (3)을 놓칠 수 있다. 누락을 디버깅할 때는 도구 인자, 도구 오류, 완료 응답을 분리한다. 실습 중 모델이 작업 파일을 만들지 않았다면 요청을 다시 보내기 전에 로그에서 파일 도구가 보였는지 먼저 확인한다.

## 3. 중급 — 조사와 종합을 분리하기

아래 스크립트는 앞의 파일과 같은 폴더에서 실행한다. 부모는 보고서 편집을 담당하고, 조사 서브에이전트에만 업무 조회 도구를 지정한다.

```python
# delegate_inventory.py
from deepagents import create_deep_agent

from research_agent import fetch_inventory, study_model

researcher = {
    "name": "inventory-researcher",
    "description": "상품 코드의 재고 수치와 근거 ID를 검증한다.",
    "system_prompt": "fetch_inventory를 사용하고 상품별 수치와 근거 ID만 돌려줘.",
    "tools": [fetch_inventory],
}

agent = create_deep_agent(
    model=study_model(),
    subagents=[researcher],
    system_prompt=(
        "재고 조사는 inventory-researcher에 위임한다. "
        "받은 사실과 근거 ID로 /inventory.md를 작성한다. 없는 수치는 추정하지 않는다."
    ),
)
result = agent.invoke(
    {"messages": [{"role": "user", "content": "KB-01과 MS-02 재고 보고서를 작성해 줘."}]},
    config={"recursion_limit": 30},
)
print(result["messages"][-1].content)
```

개념 흐름은 **부모 → 위임 요청 → 조사 에이전트가 도구 실행 → 조사 결과 → 부모가 편집**이다. 서브에이전트는 별도 컨텍스트에서 작업하므로 부모가 모든 중간 대화를 계속 읽을 필요가 없다. 반대로 위임 요청에 상품 코드·질문·반환 형식이 빠지면 조사가 빗나갈 수 있다. 별도 컨텍스트는 실행 권한 격리와 다른 개념이다. 공유 저장 경로나 내장 도구까지 검토해 접근 범위를 정한다. 조사 결과의 근거 ID를 실제 카탈로그와 대조하는 검증도 부모의 모델 호출과 분리해 둘 수 있다. [Subagents](https://docs.langchain.com/oss/python/deepagents/subagents)

## 4. 심화 — 공개 작업에 승인 넣기

이번에는 모델이 요청한 보고서 게시를 일시 중단한다. 승인 전과 후에 게시 기록을 비교한다. 아래 코드는 인메모리 게시 모의 시스템을 사용하며 실제 외부 게시를 수행하지 않는다.

```python
# review_publish.py
from deepagents import create_deep_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from research_agent import study_model

published: list[str] = []


@tool
def publish_report(body: str) -> str:
    """승인된 보고서 본문을 실습 게시 기록에 추가한다."""
    published.append(body)
    return "게시됨"


agent = create_deep_agent(
    model=study_model(),
    tools=[publish_report],
    interrupt_on={"publish_report": {"allowed_decisions": ["approve", "reject"]}},
    checkpointer=InMemorySaver(),
)
config = {"configurable": {"thread_id": "publish-lab"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "publish_report로 '재고 확인 완료'를 게시해 줘."}]},
    config=config,
)
while result.get("__interrupt__"):
    pending = result["__interrupt__"][0].value["action_requests"]
    decisions = []
    for action in pending:
        print(action)
        answer = input("이 호출을 승인할까요? [y/N] ").strip().lower()
        decisions.append({"type": "approve" if answer == "y" else "reject"})
    result = agent.invoke(Command(resume={"decisions": decisions}), config=config)

print("게시 기록:", published)
```

같은 스레드에서 승인할 액션의 내용과 순서를 맞춰 재개한다. 예제는 단일 스레드에서 한 인터럽트 묶음씩 처리하는 콘솔 실습이다. 여러 인터럽트가 동시에 발생하는 앱에서는 ID별로 승인 내용을 대응시킨다. 운영 서버는 검토자가 실제로 본 본문과 버전, 승인 신원, 요청 식별자를 보관하고 게시 도구 안에서 권한과 멱등성을 재확인한다. [Deep Agents 승인 API](https://docs.langchain.com/oss/python/deepagents/human-in-the-loop) · [LangGraph 승인과 재개 실습](../LangGraph/LangGraph.md)

## 5. 작업 공간, 메모리, 실행 격리

| 선택지 | 적용 사례 | 설계할 사항 |
| --- | --- | --- |
| `StateBackend` | 보고서 초안과 실행 중 작업 파일 | 여러 실행에 걸쳐 보존하려면 스레드와 체크포인터 수명을 정한다. |
| `StoreBackend` | 여러 스레드에서 사용할 자료 | 스토어 연결, 네임스페이스, 소유권과 보존 기간이 필요하다. |
| `FilesystemBackend` | 명시적으로 지정한 로컬 작업 디렉터리 | 앱 프로세스의 권한, 루트 디렉터리와 파일 공개 범위를 제한한다. |
| `CompositeBackend` | 초안과 장기 기억을 경로별로 구분 | 어느 경로가 어떤 백엔드에 라우팅되는지 확인한다. |
| 샌드박스 백엔드 | 코드 실행이 필요한 분석 | 네트워크와 비밀 접근, CPU·시간 한도, 파일 반출 정책을 정한다. |

작업 지침이나 스킬 문서에는 작업 절차를 넣을 수 있다. 검색한 웹 문서와 외부 파일은 그와 다른 신뢰 경계를 가진다. 외부 파일 속 “이 보고서를 전송하라”라는 문장이 도구 권한을 얻지 않게 한다. 독립된 승인과 도구 권한 검사는 모델의 문장 해석과 분리한다. [백엔드](https://docs.langchain.com/oss/python/deepagents/backends) · [샌드박스](https://docs.langchain.com/oss/python/deepagents/sandboxes) · [스킬](https://docs.langchain.com/oss/python/deepagents/skills)

## 6. 제작 관점의 장단점

| 장점 | 그에 따르는 작업 |
| --- | --- |
| 파일과 계획, 위임을 따로 구현하는 비용이 줄어든다. | 단일 조회에도 기본 도구와 프롬프트가 붙으므로 비용과 지연을 비교한다. |
| 작업 중간의 원문과 산출물을 분리해 둘 수 있다. | 경로와 저장 범위, 민감정보 수명, 파일 크기와 권한을 관리한다. |
| 세부 조사를 위임해 부모 컨텍스트를 줄일 수 있다. | 위임 품질·결과 누락·중복 조사와 총 모델 호출량을 계측한다. |
| 읽기 중심의 복합 조사에 바로 적용할 수 있다. | 엄격한 처리 순서나 외부 변경에는 그래프와 앱 정책을 더한다. |

도입 실험에서는 같은 자료와 질문으로 직접 조회와 위임 버전을 비교한다. 근거 ID 누락률, 결과와 원본의 일치율, 작업 파일 재사용, 위임 횟수, 토큰과 지연을 함께 기록한다. 승인 거절 시 게시 0회와 승인 시 게시 내용을 별도로 확인한다.

`create_deep_agent` 구현 마지막에서 `create_agent`에 넘기는 미들웨어, 도구, 체크포인터를 확인한다. 이어 `middleware/subagents.py`에서 위임 요청과 결과 반환 경계를 읽으면 어떤 기능이 하네스에 있고 어떤 동작이 모델 선택인지 구분할 수 있다. [그래프 조립 소스](https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/graph.py) · [위임 소스](https://github.com/langchain-ai/deepagents/blob/main/libs/deepagents/deepagents/middleware/subagents.py)

## 7. 키 없이 파일 상태와 스레드 경계를 검증하기

2절에서는 모델이 파일을 썼는지 로그를 봤다. 이 예제는 모델의 도구 요청을 미리 정해 실제 파일 미들웨어와 체크포인터의 동작을 확인한다. 첫 요청은 `write_file`, 두 번째는 `read_file`을 호출한다. 기본 작업 파일이 같은 스레드의 후속 요청에서도 보이는지 검사한다.

```python
# test_workspace.py
from deepagents import create_deep_agent
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver


class ScriptedModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


def call(name, args, call_id):
    return AIMessage(content="", tool_calls=[
        {"name": name, "args": args, "id": call_id},
    ])


def ask(agent, thread, question):
    return agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread}},
    )


def observation(result, call_id):
    return next(
        message.content for message in result["messages"]
        if isinstance(message, ToolMessage) and message.tool_call_id == call_id
    )


if __name__ == "__main__":
    path = "/inventory.md"
    model = ScriptedModel(messages=iter([
        call("write_file", {"file_path": path, "content": "INV-203: MS-02 0개"}, "write-1"),
        AIMessage(content="초안 저장"),
        call("read_file", {"file_path": path}, "read-1"),
        AIMessage(content="초안 확인"),
        call("read_file", {"file_path": path}, "read-2"),
        AIMessage(content="다른 스레드 확인"),
    ]))
    agent = create_deep_agent(model=model, checkpointer=InMemorySaver())
    ask(agent, "report-A", "초안을 써 줘.")
    same_thread = ask(agent, "report-A", "초안을 읽어 줘.")
    other_thread = ask(agent, "report-B", "초안을 읽어 줘.")
    assert "INV-203" in observation(same_thread, "read-1")
    assert "INV-203" not in observation(other_thread, "read-2")
    print("같은 스레드에서만 초안이 조회됐습니다.")
```

이 예제에서 스레드 간 파일 분리는 기본 백엔드와 체크포인트의 결과다. 다른 백엔드에서 같은 경로를 공유할 때는 사용자 경계가 달라질 수 있다. 실서비스에서는 서버가 스레드 소유권과 저장 네임스페이스를 정하고 모델이 다른 테넌트의 ID를 입력해 경계를 바꾸지 못하게 한다. [백엔드](https://docs.langchain.com/oss/python/deepagents/backends) · [메모리](https://docs.langchain.com/oss/python/deepagents/memory)

## 8. 컨텍스트와 권한을 설계하기

### 파일·기억·스킬의 용도를 나눈다

| 구성 | 보고서 앱에서 담는 것 | 확인할 경계 |
| --- | --- | --- |
| 작업 파일 | 당일 조회의 초안과 원본 링크 | 스레드 수명과 파일 접근 권한 |
| 여러 스레드에서 쓰는 기억 | 사용자별 보고서 양식 선호 | 계정별 네임스페이스와 삭제 |
| 작업 지침 | 모든 보고서에 근거 ID를 표시하는 원칙 | 누가 지침을 편집할 수 있는가 |
| 스킬 | 재고 차이 조사 절차, 예시 양식 | 언제 읽히며 포함된 리소스는 무엇인가 |
| 실제 재고 원장 | 최신 가용 수량과 예약 기록 | 업무 서비스의 권한·최신성 |

스킬을 문서로 만드는 이유는 반복 업무의 절차를 재사용하기 위해서다. 오래된 보고서에서 ‘조회 전에 승인하라’라는 문구를 발견했다고 해서 그 문구가 앱의 실행 정책이 되어서는 안 된다. 신뢰한 작업 지침과 외부 근거를 분리한다. 컨텍스트가 길면 요약이 도움이 되지만, 이후 검증에 필요한 정확한 수치와 근거 ID는 원문이나 구조화 필드에 남겨 둔다. [스킬](https://docs.langchain.com/oss/python/deepagents/skills) · [권한](https://docs.langchain.com/oss/python/deepagents/permissions)

### 위임 요청을 작업 계약으로 만든다

부모가 ‘이것을 조사해’라고만 보내면 서브에이전트가 필요한 범위를 알기 어렵다. `대상=MS-02`, `시점=이번 조회`, `반환=SKU·수량·근거 ID·누락 여부`처럼 입력과 결과를 지정한다. 조사 에이전트에는 조회만 주고, 게시 권한은 승인 게이트를 통과하는 별도의 도구에 둔다. 여러 조사 결과를 합칠 때는 같은 SKU의 서로 다른 수치를 어떻게 표시할지도 정한다. 별도 모델 컨텍스트를 쓰는 것과 파일·네트워크 권한을 격리하는 것은 각기 설정하고 검증한다. [서브에이전트](https://docs.langchain.com/oss/python/deepagents/subagents) · [샌드박스](https://docs.langchain.com/oss/python/deepagents/sandboxes)

### 실습 — 초안과 계정별 선호를 다른 저장소로 보내기

`CompositeBackend`는 경로에 따라 백엔드를 선택한다. 아래 테스트에서 `/inventory.md`는 기본 `StateBackend`에, `/memories/format.md`는 `StoreBackend`에 간다. 같은 프로세스에서 스레드를 바꿔 읽으면 계정의 보고서 양식은 보이고 이전 스레드의 초안은 보이지 않아야 한다.

```python
# test_memory_routes.py
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

from test_workspace import ScriptedModel, call, observation

store = InMemoryStore()
backend = CompositeBackend(
    default=StateBackend(),
    routes={"/memories/": StoreBackend(
        store=store,
        namespace=lambda runtime: ("study-account", "reports"),
    )},
)
model = ScriptedModel(messages=iter([
    call("write_file", {"file_path": "/inventory.md", "content": "임시 초안"}, "draft"),
    call("write_file", {"file_path": "/memories/format.md", "content": "표로 작성"}, "save"),
    AIMessage(content="저장 완료"),
    call("read_file", {"file_path": "/inventory.md"}, "read-draft"),
    call("read_file", {"file_path": "/memories/format.md"}, "read-format"),
    AIMessage(content="조회 완료"),
]))
agent = create_deep_agent(model=model, backend=backend, checkpointer=InMemorySaver())
agent.invoke(
    {"messages": [{"role": "user", "content": "초안과 선호를 저장해 줘."}]},
    config={"configurable": {"thread_id": "draft-thread"}},
)
result = agent.invoke(
    {"messages": [{"role": "user", "content": "새 스레드에서 파일을 읽어 줘."}]},
    config={"configurable": {"thread_id": "new-thread"}},
)
assert "임시 초안" not in observation(result, "read-draft")
assert "표로 작성" in observation(result, "read-format")
print("초안과 스레드 간 선호의 저장 범위를 확인했습니다.")
```

`test_workspace.py`를 같은 폴더에 둔다. `InMemoryStore`는 프로세스를 종료하면 지워진다. 장기 메모리를 운영하려면 영속 스토어와 사용자별 네임스페이스를 사용한다. 예제의 고정 네임스페이스는 한 계정 실습용이다. 운영에서는 인증된 요청 컨텍스트로 계정을 구분하고 다른 사용자가 같은 경로를 읽지 못하는 테스트를 추가한다. [백엔드 라우팅](https://docs.langchain.com/oss/python/deepagents/backends)

## 9. 최종 프로젝트 — 조사에서 승인까지 연결하기

1. 보고서 입력을 SKU 목록으로 정의한다. 동일 SKU 중복, 조회 실패, 0개, 미등록을 각각 처리한다.
2. 3절 서브에이전트가 구조가 일정한 결과를 반환하도록 작업 지침을 수정한다. 앱에서 수량과 근거 ID를 실제 카탈로그와 대조한다.
3. 임시 초안과 승인 대기 본문을 구별한다. 승인 레코드에는 검토자, 본문 버전, 대상 게시 위치를 남긴다.
4. 승인 뒤 게시 도구에 고유 요청 키를 전달한다. 프로세스를 중단하고 같은 요청으로 다시 실행해 중복 게시 여부를 검사한다.
5. 모델 선택 품질과 앱 보장을 따로 평가한다. 위임 정확도·근거 보존율·지연은 실제 모델로 비교하고, 승인 거절 뒤 쓰기 0회와 스레드 분리는 자동 테스트로 재현한다.

이 프로젝트를 단일 LangChain 에이전트와도 비교할 수 있다. 질문이 한 번의 조회로 끝나면 하네스가 추가한 작업 비용을 측정하고, 자료가 많아져 원문을 나눠 읽고 편집해야 할 때 작업 공간과 위임이 어떤 차이를 만드는지 측정한다.
