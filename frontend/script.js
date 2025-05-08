const boardEl      = document.getElementById('board');
const statusEl     = document.getElementById('status');
const resetButton  = document.getElementById('reset');
const themeToggle  = document.getElementById('toggle-theme');

const AI_DELAY     = 600;

let gameEnded = false;
let scores    = { player: 0, ai: 0 };

function updateScores() {
  document.getElementById('player-score').textContent = scores.player;
  document.getElementById('ai-score').textContent     = scores.ai;
}

function renderBoard(cells) {
  boardEl.innerHTML = '';
  cells.forEach((c,i) => {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.dataset.index = i;
    if (c !== ' ') {
      cell.textContent = c;
      cell.dataset.player = c;
      cell.style.pointerEvents = 'none';
    } else if (!gameEnded) {
      cell.addEventListener('click', () => makeMove(i));
    }
    boardEl.appendChild(cell);
  });
}

function fetchBoard() {
  fetch('/board')
    .then(r => r.json())
    .then(data => {
      renderBoard(data.board);
      if (data.winner) endGame(data.winner === 'X' ? 'You win!' : 'AI wins!');
    });
}

function makeMove(square) {
  if (gameEnded) return;
  statusEl.textContent = 'Processing...';
  document.querySelectorAll('.cell').forEach(c => c.style.pointerEvents = 'none');

  fetch('/move', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ square, player: 'X' })
  })
  .then(r => r.json())
  .then(data => {
    renderBoard(data.board);
    if (data.winner === 'X') {
      endGame('You win!'); scores.player++; updateScores();
    } else {
      statusEl.textContent = 'AI is thinking...';
      setTimeout(() => {
        renderBoard(data.board);
        if (data.winner === 'O') {
          endGame('AI wins!'); scores.ai++; updateScores();
        } else {
          statusEl.textContent = 'Your turn!';
          document.querySelectorAll('.cell').forEach(c => {
            if (!c.textContent) c.style.pointerEvents = 'auto';
          });
        }
      }, AI_DELAY);
    }
  });
}

function endGame(msg) {
  gameEnded = true;
  statusEl.textContent = msg;
  document.querySelectorAll('.cell').forEach(c => c.style.pointerEvents = 'none');
}

resetButton.addEventListener('click', () => {
  fetch('/reset', { method: 'POST' })
    .then(r => r.json())
    .then(data => {
      gameEnded = false;
      statusEl.textContent = 'Your turn!';
      renderBoard(data.board);
    });
});

themeToggle.addEventListener('click', () =>
  document.body.classList.toggle('dark-mode')
);

// initial load
fetchBoard();
updateScores();
