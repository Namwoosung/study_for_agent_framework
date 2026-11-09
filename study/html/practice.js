const status = document.querySelector('#copy-status');

for (const button of document.querySelectorAll('[data-copy]')) {
  const code = button.closest('figure').querySelector('code');
  let resetLabel;
  button.hidden = false;
  button.addEventListener('click', async () => {
    clearTimeout(resetLabel);
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = '복사됨';
      status.textContent = '코드를 복사했습니다.';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = '코드 선택됨';
      status.textContent = '선택한 코드를 복사 단축키로 복사하세요.';
    }
    resetLabel = setTimeout(() => {
      button.textContent = '코드 복사';
      status.textContent = '';
    }, 2500);
  });
}
