const chatForm = document.querySelector('.chat-input-form');
        const chatInput = document.querySelector('.chat-input');
        const chatMessages = document.getElementById('chatMessages');
        const chatSendBtn = document.querySelector('.chat-send-btn');

        // Auto-scroll to bottom when new messages arrive
        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Add message to chat UI
        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'message-user' : 'message-ai'}`;
            
            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'message-bubble';
            bubbleDiv.textContent = content;
            
            messageDiv.appendChild(bubbleDiv);
            chatMessages.appendChild(messageDiv);
            scrollToBottom();
        }

        // Show typing indicator
        function showTypingIndicator() {
            chatSendBtn.disabled = true;
            chatSendBtn.innerHTML = '<span>●●●</span>';
            
            // Add typing indicator message
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message message-ai typing-indicator';
            typingDiv.innerHTML = '<div class="message-bubble">Sky is typing...</div>';
            chatMessages.appendChild(typingDiv);
            scrollToBottom();
        }

        // Hide typing indicator
        function hideTypingIndicator() {
            chatSendBtn.disabled = false;
            chatSendBtn.innerHTML = '<span>Send</span>';
            
            // Remove typing indicator
            const typingIndicator = document.querySelector('.typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }

        // Handle form submission with AJAX
        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault(); // Prevent form from submitting normally
            
            const message = chatInput.value.trim();
            if (!message) return;

            // Add user message immediately
            addMessage(message, true);
            
            // Clear input and show typing indicator
            chatInput.value = '';
            showTypingIndicator();

            try {
                // Send message to backend via AJAX
                const formData = new FormData();
                formData.append('message', message);

                const response = await fetch('/chat', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                
                hideTypingIndicator();

                if (data.success) {
                    // Add AI response
                    addMessage(data.ai_response, false);
                } else {
                    addMessage('Sorry, there was an error processing your message.', false);
                }
            } catch (error) {
                hideTypingIndicator();
                addMessage('Sorry, there was a connection error.', false);
                console.error('Chat error:', error);
            }

            // Focus back on input
            chatInput.focus();
        });

        // Allow Enter key to send message
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });

        // Auto-scroll to bottom on page load
        document.addEventListener('DOMContentLoaded', function() {
            scrollToBottom();
            chatInput.focus();
        });

        // Add smooth scroll behavior
        if (chatMessages) {
            chatMessages.style.scrollBehavior = 'smooth';
        }
