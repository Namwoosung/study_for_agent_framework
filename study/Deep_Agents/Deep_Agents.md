# Deep Agents — 계획, 작업 공간, 위임을 갖춘 에이전트 만들기

Python 실습 · 보고서 작성 · 서브에이전트 · 게시 승인\
함께 읽기 · [LangChain](../LangChain/LangChain.md) · [LangGraph](../LangGraph/LangGraph.md)

## 1. 하네스란 무엇인가

재고 한 건을 조회하는 요청과 상품군 전체를 조사해 근거가 붙은 보고서를 만드는 요청은 실행 방식이 다르다. 후자에는 진행할 일 목록, 중간 결과를 보관할 공간, 일부 작업을 위임하는 방법이 도움이 된다. Deep Agents는 이러한 기능을 조합해 제공하는 에이전트 하네스다. Python에서는 `deepagents` 패키지의 `create_deep_agent`를 사용한다. SDK로 만든 앱은 개발자가 실행하며, LangChain이 별도로 제공하는 관리형 배포는 다른 실행 선택지다.

| 계층 | 제공하는 것 |
| --- | --- |
| LangGraph | 그래프 실행, 상태 및 체크포인트 |
| LangChain | 에이전트 루프, 모델·도구 통합, 미들웨어 |
| Deep Agents | 파일 작업 공간, 할 일 목록, 컨텍스트 관리와 서브에이전트 위임을 조합한 기본 구성 |

할 일 목록은 모델이 관리하는 진행 상태다. 규정상 반드시 실행해야 하는 순서라면 업무 코드나 그래프 엣지로 제약을 건다. 파일 도구는 중간 산출물을 보관하고 일부를 다시 읽게 해 준다. 요약은 긴 대화에서 토큰 부담을 낮추는 데 도움이 되지만, 인용이나 수치가 중요하면 원본과 검증 결과를 별도로 남긴다. [공식 개요](https://docs.langchain.com/oss/python/deepagents/overview) · [SDK 빠른 시작](https://docs.langchain.com/oss/python/deepagents/quickstart)

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

도구 로그에서 재고 조회, 파일 쓰기, 필요한 경우 할 일 목록 갱신을 확인한다. 보고서 완성 여부는 파일 내용과 근거 ID를 따로 검사한다. `StateBackend`가 기본값이며 에이전트 상태에 파일을 보관한다. `/inventory.md`는 이 예제에서 가상 경로다. 로컬 드라이브에 보고서를 쓰는 작업은 다른 백엔드나 별도 내보내기가 필요하다. [내장 도구](https://docs.langchain.com/oss/python/deepagents/tools) · [백엔드](https://docs.langchain.com/oss/python/deepagents/backends)

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
