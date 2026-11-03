const $ = (id) => document.getElementById(id);
const labels = {
    context: '요청 본문', response: '모델 응답', loop: '루프', node: 'Graph',
    tool: 'Tool', deps: 'Deps', state: '상태', hook: 'Hook', search: '검색',
    approval: '승인', skill: 'Skill', delegation: '위임', memory: '기억',
    case: '실험', result: '결과', error: '오류',
};
let config, scenario, active, received = 0, pending;
let lastRequest, requestCount = 0, toolCount = 0;
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
    details.open = ['approval', 'result', 'error', 'case'].includes(event.category);
    const summary = document.createElement('summary');
    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = String(event.n).padStart(2, '0') + ' · ' + (labels[event.category] || event.category);
    summary.append(tag, document.createTextNode(event.title + ' · ' + event.thread));
    if (event.category === 'context' && Array.isArray(event.value?.messages)) {
        const messages = event.value.messages;
        let common = 0;
        while (common < (lastRequest?.length || 0) && common < messages.length
            && JSON.stringify(lastRequest[common]) === JSON.stringify(messages[common])) common++;
        const suffix = messages.slice(common).map(message => message.role).join(' → ');
        const diff = document.createElement('p');
        diff.className = 'fixture';
        diff.textContent = '요청 ' + (++requestCount) + ' · 메시지 ' + messages.length
            + '개 · 이전 요청과 같은 앞부분 ' + common + '개'
            + (suffix ? ' · 변경 구간 ' + suffix : '');
        details.append(summary, diff);
        lastRequest = messages;
    }
    const body = document.createElement('pre');
    body.textContent = typeof event.value === 'string' ? event.value : JSON.stringify(event.value, null, 2);
    if (!summary.parentNode) details.append(summary);
    details.append(body);
    row.append(details);
    $('events').append(row);
    if (event.category === 'tool' && /실행 완료|업무 Tool 반환/.test(event.title)) toolCount++;
    $('overview').hidden = false;
    $('overview').textContent = '모델 전송 ' + requestCount + '회 · Tool 반환 관찰 ' + toolCount + '건';
    if (event.category === 'approval' && event.value?.id) {
        pending = event.value.id;
        $('approval-text').textContent = event.value.details.description || '승인 여부를 결정하세요.';
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
        for (const event of state.events.slice(received)) render(event);
        received = state.events.length;
        filter();
        if (!state.done) {
            $('status').textContent = pending ? '승인 응답 대기 중' : '실행 중 · ' + received + '개 이벤트';
            setTimeout(poll, 550);
            return;
        }
        $('status').textContent = state.events.some(e => e.category === 'error') ? '종료 · 오류 기록 확인' : '실행 완료';
    } catch (error) {
        $('status').textContent = error.message;
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
    $('empty').hidden = true;
    received = 0;
    requestCount = toolCount = 0;
    lastRequest = undefined;
    $('overview').hidden = true;
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
