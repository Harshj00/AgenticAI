const chatBox = document.getElementById('chatBox');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');

function addMessage(content, role) {
  const bubble = document.createElement('div');
  bubble.className = `message ${role}`;
  bubble.textContent = content;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const text = messageInput.value.trim();
  if (!text) return;

  addMessage(text, 'user');
  messageInput.value = '';
  addMessage('Thinking...', 'assistant');

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    const lastBubble = chatBox.querySelector('.message.assistant:last-child');
    if (lastBubble) {
      lastBubble.textContent = data.reply || 'No reply received.';
    }
  } catch (error) {
    const lastBubble = chatBox.querySelector('.message.assistant:last-child');
    if (lastBubble) {
      lastBubble.textContent = 'Something went wrong. Please try again.';
    }
  }
});
