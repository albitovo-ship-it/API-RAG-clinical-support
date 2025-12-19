const API_URL = '/ask_question';
const chatContainer = document.getElementById('chatContainer');
const queryInput = document.getElementById('queryInput');
const sendButton = document.getElementById('sendButton');
let conversationHistory = [];

// Auto-resize textarea
queryInput.addEventListener('input', function() {
    this.style.height = '52px';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Send on Enter (Shift+Enter for new line)
queryInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendButton.addEventListener('click', sendMessage);

function addMessage(text, isUser) {
    // Remove welcome message if exists
    const welcomeMsg = chatContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    chatContainer.scrollTop = chatContainer.scrollHeight;

    conversationHistory.push({
        role: isUser ? 'user' : 'assistant',
        content: text
    });
}

function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.id = 'loadingIndicator';
    
    const loadingContent = document.createElement('div');
    loadingContent.className = 'loading';
    loadingContent.innerHTML = `
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
    `;
    
    loadingDiv.appendChild(loadingContent);
    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function hideLoading() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }
}

async function sendMessage() {
    const question = queryInput.value.trim();
    
    if (!question) return;

    // Add user message
    addMessage(question, true);
    
    // Clear input
    queryInput.value = '';
    queryInput.style.height = '52px';
    
    // Disable input and button
    queryInput.disabled = true;
    sendButton.disabled = true;
    sendButton.classList.add('sending');
    
    // Show loading
    showLoading();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Hide loading
        hideLoading();
        
        // Add assistant response
        addMessage(data.response, false);

    } catch (error) {
        hideLoading();
        addMessage('Lo siento, ocurrió un error al procesar tu consulta. Por favor, intenta nuevamente.', false);
        console.error('Error:', error);
    } finally {
        // Re-enable input and button
        queryInput.disabled = false;
        sendButton.disabled = false;
        sendButton.classList.remove('sending');
        queryInput.focus();
    }
}