document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const loadingIndicator = document.getElementById('loading-indicator');
    const errorBanner = document.getElementById('error-banner');
    const clearBtn = document.getElementById('clear-btn');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');

    // Handle suggestion chip clicks
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', () => {
            userInput.value = chip.innerText;
            chatForm.dispatchEvent(new Event('submit'));
        });
    });

    // Handle clearing the chat
    clearBtn.addEventListener('click', () => {
        // Keep only the initial greeting
        const initialMessage = chatMessages.firstElementChild;
        chatMessages.innerHTML = '';
        if (initialMessage) {
            chatMessages.appendChild(initialMessage);
        }
        hideError();
    });

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const messageText = userInput.value.trim();
        if (!messageText) return;

        // 1. Add User Message to UI
        appendMessage(messageText, 'user');
        userInput.value = '';
        
        // 2. Show loading state
        showLoading();
        hideError();

        try {
            // 3. Make POST request to API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageText })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // 4. Add Assistant Message to UI
            appendMessage(data.answer, 'assistant', data.intent);

        } catch (error) {
            console.error('Error fetching chat response:', error);
            showError("Unable to reach the server. Please try again.");
            appendMessage("I'm sorry, I'm having trouble connecting to my systems right now.", 'assistant', 'SYSTEM_ERROR');
        } finally {
            hideLoading();
        }
    });

    function appendMessage(text, sender, intent = null) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', `${sender}-message`, 'slide-in');

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');

        // Optional: show a tiny badge for the intent on bot messages to show off the backend logic
        if (sender === 'assistant' && intent && intent !== 'UNKNOWN' && intent !== 'SYSTEM_ERROR') {
            const badge = document.createElement('span');
            badge.classList.add('intent-badge');
            badge.innerText = `Matched Intent: ${intent.replace('_', ' ')}`;
            bubbleDiv.appendChild(badge);
        }

        const textNode = document.createTextNode(text);
        bubbleDiv.appendChild(textNode);
        
        msgDiv.appendChild(bubbleDiv);
        chatMessages.appendChild(msgDiv);
        
        scrollToBottom();
    }

    function showLoading() {
        loadingIndicator.classList.remove('hidden');
        scrollToBottom();
    }

    function hideLoading() {
        loadingIndicator.classList.add('hidden');
    }

    function showError(msg) {
        errorBanner.innerText = msg;
        errorBanner.classList.remove('hidden');
    }

    function hideError() {
        errorBanner.classList.add('hidden');
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
