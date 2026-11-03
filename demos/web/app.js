const $ = (id) => document.getElementById(id);
const labels = {
    context: '요청 본문', response: '모델 응답', loop: '루프', node: 'Graph',
    tool: 'Tool', deps: 'Deps', state: '상태', hook: 'Hook', search: '검색',
    approval: '승인', skill: 'Skill', delegation: '위임', memory: '기억',
    case: '실험', result: '결과', error: '오류',
};
let config, scenario, active, received = 0, pending;
const stage = (label, category, match = '.') => [label, category, new RegExp(match)];
const wire = stage('모델로 보낸 요청', 'context');
const result = stage('최종 응답', 'result');
const calls = stage('모델이 요청한 도구', 'tool', 'Tool Call');
const returned = stage('도구 실행 결과', 'tool', '완료|반환');
const flows = {
    loop: [stage('Hermes 함수 경계', 'loop'), wire, calls, returned, result],
    context: [wire, stage('모델 응답', 'response', '^모델 HTTP'), returned, result],
    search: [calls, stage('세션 DB 검색', 'search'), stage('검색 Tool 반환', 'tool', '실행 완료'), wire, result],
    tools: [stage('모델에 공개한 스키마', 'tool', '전달된 Tool 명세'), calls, stage('실행 전 Hook', 'hook'), returned, wire],
    approval: [calls, stage('발행 정책', 'hook'), stage('사람의 결정', 'approval', '대기|결정'), returned, result],
    guard: [calls, stage('업무 도구 검사', 'hook'), stage('터미널 명령 검사', 'approval'), returned, result],
    skill: [calls, stage('Skill 관리 함수', 'skill'), returned, result],
    delegate: [calls, stage('위임 함수와 자식 실행', 'delegation'), wire, result],
    graph: [stage('Agent Graph 노드', 'node'), wire, calls, returned, result],
    deps: [wire, stage('도구에서 읽은 RunContext', 'deps'), returned, result],
    conversation: [stage('이전 대화 로드', 'state', '로드'), wire, result, stage('새 이력 저장', 'state', '직렬화')],
    outputs: [stage('출력 방식별 비교', 'case'), wire, stage('모델 응답', 'response', '^모델 HTTP'), result],
    end: [stage('공통 첫 모델 응답', 'case', '재사용$|함께 들어오지'), stage('종료 정책별 결과', 'case', '정책별 실제 실행 비교'), stage('기록 도구 실행', 'tool', 'record_review'), result],
    core: [stage('앱과 Core의 역할', 'case'), stage('Core Graph', 'node'), stage('업무 코드와 검증', 'tool', '업무 Tool|수치 검증'), result],
    harness: [stage('Memory 연결', 'case'), stage('Memory 호출', 'memory'), wire, result],
    delegation: [calls, stage('Subagents 실행', 'delegation'), wire, result],
};

const views = {
    loop: ['sequence', 'Hermes가 도구 결과를 받은 뒤 어느 함수에서 다음 모델 호출을 시작할까요?'],
    context: ['inspection', '모델에 실제로 전달된 메시지는 무엇이고, 이전 요청에서 무엇이 달라졌을까요?'],
    search: ['inspection', '모델이 고른 검색어가 어떤 세션을 찾고, 그 결과가 다음 요청에 어떻게 들어갈까요?'],
    tools: ['inspection', '모델에 공개한 스키마부터 호출 인자, Hook 판정, 반환값까지 따라갑니다.'],
    approval: ['decision', '어떤 정책에 걸려 실행이 멈췄는지 확인하고, 승인 또는 거절을 선택합니다.'],
    guard: ['decision', '업무 도구와 터미널 명령이 각각 어디에서 검사되고 어떤 판정을 받는지 비교합니다.'],
    skill: ['inspection', '모델이 Skill 관리 도구에 보낸 인자와 실제 생성 결과를 확인합니다.'],
    delegate: ['sequence', '부모가 일을 나누는 지점부터 각 실행의 결과가 돌아오는 지점까지 따라갑니다.'],
    graph: ['sequence', 'Agent Graph가 어떤 노드를 거쳐 모델과 도구를 호출하는지 확인합니다.'],
    deps: ['inspection', '모델 요청과 Python 도구에 주입된 접근 범위를 각각 확인합니다.'],
    conversation: ['inspection', '이전 메시지를 복원해 모델에 보내고 새 이력을 저장하는 과정을 봅니다.'],
    outputs: ['comparison', '같은 업무 요청에 네 가지 출력 모드를 적용해 실제 요청과 결과를 비교합니다.'],
    end: ['comparison', '같은 첫 모델 응답에서 종료 정책에 따라 어떤 도구가 실행되는지 비교합니다.'],
    core: ['comparison', '앱이 작성한 업무 코드와 PydanticAI가 처리하는 실행 단계를 구분합니다.'],
    harness: ['inspection', 'Harness Memory가 연결된 실행에서 실제 기억 관련 호출을 확인합니다.'],
    delegation: ['sequence', '상위 Agent의 위임과 하위 실행에서 관측한 데이터를 따라갑니다.'],
};

const roleNames = {system: '시스템 지시', developer: '개발자 지시', user: '사용자 입력', assistant: '모델 메시지', tool: '도구 결과'};
const fields = {
    bin_id: '검사 BIN', tested: '검사 수량', failed: '불량 수량', defect_rate: '불량률',
    snapshot: '데이터 버전', requested: '요청 BIN', allowed_bins: '허용 BIN', tenant: '테넌트',
    query: '검색어', role_filter: '검색 역할', limit: '조회 한도', command: '명령',
    pattern_key: '매칭 규칙', decision: '판정', approved: '승인 여부', expired: '시간 초과',
    finish_reason: '종료 이유', session: '세션', run_step: '실행 단계', message_count: '메시지 수',
    final_response: '최종 답변', completed: '완료', error: '오류', result: '반환값',
    arguments: '호출 인자', name: '이름', mode: '출력 모드', model: '모델', action: '동작',
    skill_name: 'Skill 이름', goal: '위임 목표', description: '설명', bytes: '저장 크기 (bytes)',
    expected: '기대값', actual: '실제값',
};

function element(tag, content, className) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (content !== undefined) node.textContent = content;
    return node;
}

function raw(label, value, key) {
    const details = element('details');
    if (key) details.dataset.key = key;
    details.append(element('summary', label), element('pre', typeof value === 'string' ? value : JSON.stringify(value, null, 2)));
    return details;
}

function compact(value) {
    if (typeof value === 'string') return value;
    return JSON.stringify(value) ?? '';
}

function parseValue(value) {
    if (typeof value !== 'string') return value;
    try { return JSON.parse(value); } catch { return value; }
}

function facts(value) {
    const data = parseValue(value);
    const list = element('dl', undefined, 'facts');
    for (const [key, item] of Object.entries(data ?? {})) {
        if (!Object.hasOwn(fields, key) || item == null) continue;
        const display = key === 'defect_rate' && typeof item === 'number'
            ? new Intl.NumberFormat('ko-KR', {style: 'percent', maximumFractionDigits: 4}).format(item)
            : typeof item === 'boolean' ? (item ? '예' : '아니요') : compact(item);
        if (display.length > 240) continue;
        list.append(element('dt', fields[key]), element('dd', display));
    }
    return list;
}

function preview(event) {
    const value = event.value;
    if (event.category === 'context') return (value?.messages?.length ?? 0) + '개 메시지 / ' + (value?.tools?.length ?? 0) + '개 도구';
    if (Array.isArray(value) && event.category === 'tool') {
        const names = value.map(item => item?.function?.name ?? item?.name ?? (typeof item === 'string' ? item : null)).filter(Boolean);
        if (names.length) return names.join(', ');
    }
    const v = parseValue(value?.result ?? value);
    if (typeof v?.defect_rate === 'number') return [v.bin_id, (v.defect_rate * 100).toLocaleString('ko-KR') + '%', Number.isFinite(v.failed) && Number.isFinite(v.tested) ? v.failed + '/' + v.tested + '개' : null].filter(Boolean).join(' / ');
    return compact(v?.query ?? v?.decision ?? v?.final_response ?? v?.requested ?? v?.name ?? (typeof v === 'string' ? v : event.title)).slice(0, 105);
}

function messageView(card, event, events) {
    const payload = event.value ?? {};
    const messages = payload.messages ?? [];
    const previous = events.findLast(item => item.n < event.n && item.category === 'context'
        && item.scope && item.scope === event.scope);
    const before = previous?.value?.messages ?? [];
    let common = 0;
    while (common < before.length && common < messages.length
        && compact(before[common]) === compact(messages[common])) common++;
    if (previous) card.append(element('p', '같은 HTTP 클라이언트의 앞선 전송과 비교 · 앞 ' + common + '개 유지 · 현재 변경 구간 ' + (messages.length - common)
        + '개 · 이전 변경 구간 ' + (before.length - common) + '개', 'fixture'));
    const list = element('ol', undefined, 'messages');
    messages.forEach((message, index) => {
        const item = element('li');
        item.dataset.role = message.role;
        const label = (index + 1) + '. ' + (roleNames[message.role] ?? message.role ?? '메시지');
        const content = message.tool_calls ?? parseValue(message.content);
        const details = raw('메시지 원문', message, event.n + '-msg-' + index);
        const sample = typeof content === 'string' ? content : compact(content);
        const heading = element('div', undefined, 'message-heading');
        heading.append(element('strong', label));
        if (previous && index >= common) {
            item.dataset.changed = 'true';
            heading.append(element('span', '이전 요청과 다름', 'change-marker'));
        }
        const metrics = facts(content);
        item.append(heading, metrics.children.length ? metrics
            : element('p', sample ? sample.slice(0, 180) + (sample.length > 180 ? '…' : '') : '본문 없음'), details);
        list.append(item);
    });
    card.append(list);
    const {messages: ignoredMessages, tools, ...options} = payload;
    if (tools) card.append(raw('공개 Tool 스키마 ' + tools.length + '개', tools, event.n + '-schema'));
    card.append(raw('모델 옵션과 출력 계약', options, event.n + '-options'));
}

function relatedEvents(card, event, events) {
    const value = event.value;
    const ids = new Set((Array.isArray(value) ? value : [value]).flatMap(item => [
        item?.call_id, item?.tool_call_id, item?.id,
    ]).filter(Boolean));
    const related = events.filter(item => item.n !== event.n && (
        (event.request_id && item.request_id === event.request_id)
        || (event.function_call_id && item.function_call_id === event.function_call_id)
        || (ids.size && (ids.has(item.value?.id) || ids.has(item.value?.call_id)
            || item.value?.messages?.some(message => ids.has(message.tool_call_id))))
    ));
    if (!related.length) return;
    const group = element('details');
    group.dataset.key = event.n + '-related';
    group.append(element('summary', '같은 요청·함수 호출의 관측값 ' + related.length + '건'));
    for (const item of related) group.append(raw('#' + item.n + ' ' + item.title, item.value, event.n + '-related-' + item.n));
    card.append(group);
}

function comparisonView(key, events) {
    const cases = events.filter(event => event.category === 'case' && event.value?.mode);
    if (key !== 'outputs' || !cases.length) return null;
    const columns = element('div', undefined, 'comparison');
    cases.forEach((entry, index) => {
        // The runner executes and awaits each mode before opening the next case.
        const segment = events.filter(event => event.n > entry.n && event.n < (cases[index + 1]?.n ?? Infinity));
        const first = segment.find(event => event.category === 'context');
        const output = segment.findLast(event => event.category === 'result' || event.category === 'error');
        const contract = first?.value?.response_format ?? first?.value?.tools?.filter(tool =>
            tool.function?.name !== 'read_fab_bin');
        const column = element('section');
        column.append(element('h4', entry.value.mode));
        column.append(element('p', first ? '공개 도구 ' + (first.value.tools?.length ?? 0)
            + '개 / response_format ' + (first.value.response_format?.type ?? '없음') : '모델 전송 미관측'));
        if (output) column.append(element('p', compact(output.value), 'answer'));
        if (first) column.append(raw('실제 출력 계약과 요청', {
            contract, messages: first.value.messages,
        }, entry.n + '-contract'));
        columns.append(column);
    });
    return columns;
}

function eventCard(event, events) {
    const card = element('article', undefined, 'observation');
    card.append(element('h3', event.title), element('p', '#' + event.n + ' · ' + event.thread
        + (event.request_id ? ' · 모델 요청 ' + event.request_id : ''), 'meta'));
    if (event.category === 'context') messageView(card, event, events);
    else {
        const value = event.value;
        const visible = facts(parseValue(value?.result ?? value));
        if (visible.children.length) card.append(visible);
        if (event.category === 'result' && (value?.final_response || typeof value === 'string')) {
            card.append(element('p', value.final_response ?? value, 'answer'));
        } else if (Array.isArray(value) && event.category === 'tool') {
            const tools = element('ul', undefined, 'tool-list');
            value.forEach((item, index) => {
                const li = element('li');
                li.append(raw(item?.function?.name ?? item?.name ?? compact(item).slice(0, 85), item, event.n + '-tool-' + index));
                tools.append(li);
            });
            card.append(tools);
        } else if (event.category === 'case' && /정책별 실제 실행 비교|Core 구성/.test(event.title)) {
            const comparison = element('div', undefined, 'comparison');
            for (const [name, outcome] of Object.entries(value)) {
                const column = element('section');
                column.append(element('h4', name));
                for (const [key, item] of Object.entries(outcome)) {
                    column.append(element('p', Array.isArray(outcome) ? compact(item) : key + '  ' + (compact(item) || '—')));
                }
                comparison.append(column);
            }
            card.append(comparison);
        } else if (!visible.children.length) {
            card.append(element('p', preview(event), 'preview'));
        }
    }
    relatedEvents(card, event, events);
    if (event.function) card.append(element('p', event.function + ' · 정의 ' + event.source_line + '행 · ' + event.phase, 'meta'));
    card.append(raw('원본 이벤트 값', event.value, event.n + '-raw'));
    return card;
}

let trace = [], stageIndex, eventNumber, done = false, runScenario;

function observationSequence(key, observations, selected, chosen) {
    const showNodes = ['graph', 'loop'].includes(key) && selected === 0;
    const showWorkers = ['delegate', 'delegation'].includes(key) && selected === 1;
    if ((!showNodes && !showWorkers) || observations.length < 2) return null;
    const groups = new Map();
    for (const event of observations) {
        const group = showWorkers ? event.thread : '실행 순서';
        if (!groups.has(group)) groups.set(group, []);
        groups.get(group).push(event);
    }
    const sequence = element('div', undefined, 'sequence');
    for (const [label, events] of groups) {
        const row = element('section');
        row.append(element('h3', label));
        const list = element('ol');
        for (const event of events.slice(-12)) {
            const item = element('li');
            const button = element('button', '#' + event.n + ' ' + event.title);
            button.type = 'button';
            button.dataset.event = event.n;
            button.setAttribute('aria-pressed', String(chosen.n === event.n));
            button.onclick = () => {
                stageIndex = selected;
                eventNumber = event.n;
                drawFlow();
                $('observation').querySelector('[data-event="' + event.n + '"]')?.focus();
            };
            item.append(button);
            list.append(item);
        }
        row.append(list);
        sequence.append(row);
    }
    return sequence;
}

let timelineNumber;
function timelineEvents() {
    const categories = config.scenarios[runScenario ?? scenario][2];
    return trace.filter(event => categories.includes(event.category)
        || ['approval', 'result', 'error'].includes(event.category));
}
function drawTimeline(selectedNumber) {
    const events = timelineEvents();
    const select = $('timeline-select');
    const key = (runScenario ?? scenario) + '/' + events.length;
    if (select.dataset.key !== key) {
        select.dataset.key = key;
        select.replaceChildren(...events.map(event => {
            const option = element('option', '#' + event.n + ' ' + (labels[event.category] ?? event.category) + ' / ' + event.title);
            option.value = event.n;
            return option;
        }));
    }
    const index = events.findIndex(event => event.n === selectedNumber);
    select.value = events[index]?.n ?? '';
    $('event-prev').disabled = index <= 0;
    $('event-next').disabled = index < 0 || index >= events.length - 1;
    $('timeline').hidden = events.length === 0;
    $('follow').setAttribute('aria-pressed', String(timelineNumber === undefined && stageIndex === undefined));
}
function inspectEvent(number) {
    timelineNumber = number;
    const event = trace.find(item => item.n === number);
    const stages = flows[runScenario ?? scenario] ?? [];
    stageIndex = stages.findIndex(([, category, pattern]) => event.category === category && pattern.test(event.title));
    eventNumber = number;
    drawFlow();
}
$('timeline-select').onchange = event => inspectEvent(Number(event.target.value));
for (const [id, delta] of [['event-prev', -1], ['event-next', 1]]) {
    $(id).onclick = () => {
        const events = timelineEvents();
        const index = events.findIndex(event => event.n === Number($('timeline-select').value));
        const next = events[index + delta];
        if (next) inspectEvent(next.n);
    };
}
$('follow').onclick = () => {
    timelineNumber = stageIndex = eventNumber = undefined;
    drawFlow();
};

function drawFlow() {
    const flow = $('flow');
    const key = runScenario ?? scenario;
    const stages = flows[key] ?? [];
    const [view, description] = views[key] ?? [];
    $('workspace').dataset.view = view ?? 'sequence';
    $('question').textContent = description ?? '';
    $('flow-title').textContent = view === 'comparison' ? '비교 항목' : '실행 흐름';
    $('flow-note').textContent = view === 'comparison'
        ? '비교 항목을 선택하면 실제 실행 결과를 볼 수 있습니다.'
        : '화살표는 대표 경로입니다. 단계를 선택하면 실제 실행에서 관측한 값을 볼 수 있습니다.';
    const matches = stages.map(([, category, pattern]) => trace.filter(event =>
        category === event.category && pattern.test(event.title)));
    const latest = Math.max(0, ...matches.map(events => events.at(-1)?.n ?? 0));
    const comparisonStage = done && key === 'end' && matches[1]?.length ? 1
        : done && key === 'outputs' && matches[0]?.length ? 0 : undefined;
    const selected = stageIndex ?? comparisonStage ?? (latest ? matches.findIndex(events => events.at(-1)?.n === latest) : 0);
    const buttons = flow.querySelectorAll('button');
    if (buttons.length !== stages.length || flow.dataset.scenario !== key) {
        flow.replaceChildren();
        flow.dataset.scenario = key;
        stages.forEach(([label], index) => {
            const li = element('li');
            const button = element('button');
            button.type = 'button';
            button.append(element('strong', label), element('span', '', 'step-status'), element('span', '', 'step-value'));
            button.onclick = () => { timelineNumber = undefined; stageIndex = index; eventNumber = undefined; drawFlow(); };
            li.append(button);
            flow.append(li);
        });
    }
    flow.querySelectorAll('button').forEach((button, index) => {
        const observations = matches[index];
        button.setAttribute('aria-pressed', String(index === selected));
        button.dataset.observed = String(Boolean(observations.length));
        button.children[1].textContent = observations.length ? '관측 ' + observations.length + '건'
            : done ? '미관측' : '관측 대기';
        button.children[2].textContent = observations.length ? preview(observations.at(-1)) : '';
    });
    const panel = $('observation');
    const observations = matches[selected] ?? [];
    const chosen = timelineNumber === undefined
        ? observations.find(event => event.n === eventNumber) ?? observations.at(-1)
        : trace.find(event => event.n === timelineNumber);
    drawTimeline(chosen?.n);
    const comparison = selected === 0 ? comparisonView(key, trace) : null;
    const stamp = (comparison || chosen?.request_id || chosen?.category === 'tool' ? trace.length + '/' : '') + key + '/' + selected + '/' + observations.length + '/' + (chosen?.n ?? 0);
    if (panel.dataset.stamp === stamp) return;
    panel.dataset.stamp = stamp;
    const opened = new Set([...panel.querySelectorAll('details[open][data-key]')].map(detail => detail.dataset.key));
    panel.replaceChildren();
    if (!chosen) {
        panel.append(element('p', done ? '이번 실행에서는 이 단계의 데이터가 기록되지 않았습니다.' : '실행하면 이 단계에서 오간 데이터가 표시됩니다.', 'meta'));
        return;
    }
    if (comparison) panel.append(comparison);
    const sequence = observationSequence(key, observations, selected, chosen);
    if (sequence) panel.append(sequence);
    if (observations.length > 1 && timelineNumber === undefined) {
        const label = element('label', '관측 지점 ');
        const select = element('select');
        observations.forEach(event => {
            const option = element('option', '#' + event.n + ' ' + event.title + ' / ' + preview(event));
            option.value = event.n;
            select.append(option);
        });
        select.value = chosen.n;
        select.onchange = () => {
            stageIndex = selected;
            eventNumber = Number(select.value);
            drawFlow();
            panel.querySelector('select')?.focus();
        };
        label.append(select);
        panel.append(label);
    }
    panel.append(eventCard(chosen, trace));
    panel.querySelectorAll('details[data-key]').forEach(detail => { detail.open = opened.has(detail.dataset.key); });
}

const visible = new Set(['error', 'result', 'approval']);

async function request(path, data) {
    const options = data === undefined ? {} : {
        method: 'POST', headers: {'Content-Type': 'application/json', 'X-Demo': '1'},
        body: JSON.stringify(data),
    };
    const response = await fetch(path, options);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || '요청 실패');
    return payload;
}

function choose() {
    const key = location.hash.slice(1);
    if ($('run').disabled) {
        history.replaceState(null, '', '#' + scenario);
        return;
    }
    trace = [];
    done = false;
    runScenario = stageIndex = eventNumber = timelineNumber = undefined;
    $('observation').dataset.stamp = '';
    $('events').replaceChildren();
    $('outcome').hidden = true;
    $('status').textContent = '';
    scenario = Object.hasOwn(config.scenarios, key) ? key : Object.keys(config.scenarios)[0];
    const [title, prompt] = config.scenarios[scenario];
    $('title').textContent = title;
    $('prompt').value = prompt;
    $('sessionRow').hidden = scenario !== 'conversation';
    for (const link of $('scenarios').children) {
        if (link.hash === '#' + scenario) link.setAttribute('aria-current', 'page');
        else link.removeAttribute('aria-current');
    }
    filter();
    drawFlow();
}

function filter() {
    const categories = config.scenarios[scenario][2];
    for (const row of $('events').children) {
        const kind = row.dataset.category;
        row.hidden = !$('all').checked && !visible.has(kind) && !categories.includes(kind);
    }
}

function render(event) {
    const row = document.createElement('li');
    row.dataset.category = event.category;
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = String(event.n).padStart(2, '0') + ' · ' + (labels[event.category] || event.category);
    summary.append(tag, document.createTextNode(event.title + ' · ' + event.thread));
    const body = document.createElement('pre');
    body.textContent = typeof event.value === 'string' ? event.value : JSON.stringify(event.value, null, 2);
    details.append(summary, body);
    row.append(details);
    $('events').append(row);
    if (event.category === 'approval' && event.value?.id) {
        pending = event.value.id;
        $('approval-text').textContent = event.value.details?.description || '승인 여부를 결정하세요.';
        $('approval').hidden = false;
    }
    if (event.category === 'approval' && typeof event.value?.approved === 'boolean') {
        pending = undefined;
        $('approval').hidden = true;
    }
}

async function poll() {
    try {
        const state = await request('/api/runs/' + active);
        trace = state.events;
        done = state.done;
        for (const event of trace.slice(received)) render(event);
        drawFlow();
        const final = trace.findLast(event => event.category === 'result');
        const error = trace.findLast(event => event.category === 'error');
        $('outcome').hidden = ['outputs', 'end'].includes(runScenario) || (!final && !error);
        $('outcome-text').textContent = error ? error.title + ' · ' + preview(error)
            : final ? compact(final.value?.final_response ?? final.value) : '';
        received = state.events.length;
        filter();
        if (!state.done) {
            $('status').textContent = pending ? '승인 응답 대기 중' : '실행 중 · ' + received + '개 이벤트';
            setTimeout(poll, 550);
            return;
        }
        $('status').textContent = state.events.some(e => e.category === 'error') ? '종료 · 오류 기록 확인' : '실행 완료';
    } catch (error) {
        $('status').textContent = '실행 상태 연결 재시도 중 · ' + error.message;
        setTimeout(poll, 2000);
        return;
    }
    $('run').disabled = false;
    $('approval').hidden = true;
    active = pending = undefined;
}

$('form').addEventListener('submit', async (event) => {
    event.preventDefault();
    $('run').disabled = true;
    $('status').textContent = '실행 시작 중';
    $('events').replaceChildren();
    received = 0;
    trace = [];
    done = false;
    runScenario = scenario;
    stageIndex = eventNumber = timelineNumber = undefined;
    $('outcome').hidden = true;
    $('observation').dataset.stamp = '';
    drawFlow();
    try {
        const response = await request('/api/runs', {scenario, prompt: $('prompt').value, session: $('session').value});
        active = response.id;
        poll();
    } catch (error) {
        $('status').textContent = error.message;
        $('run').disabled = false;
    }
});

for (const [key, allow] of [['allow', true], ['deny', false]]) {
    $(key).addEventListener('click', async () => {
        if (!active || !pending) return;
        try {
            await request('/api/approve/' + active, {id: pending, allow});
            $('approval').hidden = true;
            pending = undefined;
        } catch (error) {
            $('status').textContent = error.message;
        }
    });
}

request('/api/config').then((data) => {
    config = data;
    $('engine').textContent = data.engine === 'hermes' ? 'Hermes' : 'PydanticAI';
    $('endpoint').textContent = '모델 연결 ' + new URL(data.modelEndpoint).host;
    for (const [key, item] of Object.entries(data.scenarios)) {
        const link = document.createElement('a');
        link.href = '#' + key;
        link.textContent = item[0];
        $('scenarios').append(link);
    }
    window.addEventListener('hashchange', choose);
    $('all').addEventListener('change', filter);
    choose();
}).catch(error => $('status').textContent = error.message);
