"""Run the seminar's deterministic examples with the pinned Core and Harness."""
from dataclasses import dataclass
from importlib.metadata import version
import json

from pydantic import BaseModel, Field
from pydantic_ai import Agent, DeferredToolRequests, DeferredToolResults, ModelRetry, RunContext
from pydantic_ai.conversation import ConversationTypeAdapter
from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart
from pydantic_ai.models.function import FunctionModel
from pydantic_ai_harness.memory import Memory

from pydantic_revision import CODE


def verify():
    assert version('pydantic-ai-slim') == '2.61.0'
    assert version('pydantic-ai-harness') == '0.61.0'
    scope = globals().copy()
    exec(CODE['minimal'][1], scope)
    exec(CODE['deps'][1], scope)
    requests = []

    def response(messages, info):
        requests.append(messages[-1].parts[0].part_kind)
        if len(requests) == 1:
            return ModelResponse(parts=[ToolCallPart('read_counts', {})])
        if len(requests) == 2:
            return ModelResponse(parts=[ToolCallPart('read_counts', {'lot_id': 'LOT-A'})])
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {
            'lot_id': 'LOT-A', 'snapshot': 'r3', 'yield_pct': 90 if len(requests) == 3 else 92,
        })])

    scope['model'] = FunctionModel(response)
    exec(CODE['agent'][1], scope)
    exec(CODE['plain'][1], {**scope, 'agent': Agent(scope['model'], deps_type=scope['Deps'])})
    exec(CODE['verify'][1], scope)
    exec(CODE['hook'][1], scope)
    deps = scope['Deps']({'LOT-A'}, 'r3', {'LOT-A': (92, 100)})
    result = scope['agent'].run_sync('LOT-A', deps=deps, capabilities=[scope['LotPolicy']()])
    assert result.output.yield_pct == 92 and len(requests) == 4
    conversation = ConversationTypeAdapter.validate_json(ConversationTypeAdapter.dump_json(result.conversation))
    assert conversation.messages == result.conversation.messages

    def mixed(messages, info):
        output = info.output_tools[0].name
        return ModelResponse(parts=[
            ToolCallPart('record', {'value': 'A'}),
            ToolCallPart(output, {'lot_id': 'LOT-A', 'snapshot': 'r3', 'yield_pct': 92}),
            ToolCallPart('record', {'value': 'B'}),
            ToolCallPart(output, {'lot_id': 'LOT-A', 'snapshot': 'r3', 'yield_pct': 91}),
        ])

    strategies = {}
    for strategy, expected in [('early', []), ('graceful', ['A', 'B']), ('exhaustive', ['A', 'B'])]:
        executed = []
        experiment = Agent(FunctionModel(mixed), output_type=scope['YieldReport'], end_strategy=strategy)

        @experiment.tool_plain
        def record(value: str) -> str:
            executed.append(value)
            return value

        outcome = experiment.run_sync('policy')
        assert sorted(executed) == expected and outcome.output.yield_pct == 92, (strategy, executed, outcome.output)
        strategies[strategy] = {'executed': executed, 'output': outcome.output.yield_pct}

    writes = []

    def approval_model(messages, info):
        if any(part.part_kind == 'tool-return' for part in messages[-1].parts):
            return ModelResponse(parts=[TextPart('done')])
        return ModelResponse(parts=[ToolCallPart('record_approval', {'version': 'r3'}, 'approval-1')])

    approval_agent = Agent(FunctionModel(approval_model), output_type=[str, DeferredToolRequests])

    @approval_agent.tool_plain(requires_approval=True)
    def record_approval(version: str) -> str:
        writes.append(version)
        return version

    pending = approval_agent.run_sync('record')
    assert isinstance(pending.output, DeferredToolRequests) and not writes
    approved = approval_agent.run_sync(conversation=pending.conversation,
        deferred_tool_results=DeferredToolResults(approvals={'approval-1': True}))
    assert approved.output == 'done' and writes == ['r3']
    assert type(Memory().store).__name__ == 'InMemoryStore'
    return {'core': '2.61.0', 'harness': '0.61.0', 'model': 'FunctionModel and TestModel',
            'requestParts': requests, 'yieldPercent': result.output.yield_pct,
            'conversationRoundTrip': True, 'endStrategies': strategies,
            'approvalResume': True, 'memoryDefault': 'InMemoryStore'}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
