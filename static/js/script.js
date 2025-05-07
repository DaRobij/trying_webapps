document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    
    // Ascultă pentru mesaje noi
    socket.on('receive_message', function(data) {
        appendMessage(data.user, data.bot);
    });
    
    // Trimite mesaj
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            socket.emit('send_message', { message: message });
            messageInput.value = '';
        }
    });
    
    // Adaugă mesaj în chat
    function appendMessage(userMessage, botResponse) {
        const messageElement = document.createElement('div');
        messageElement.className = 'flex flex-col';
        messageElement.innerHTML = `
            <div class="self-end bg-indigo-100 rounded-lg p-3 max-w-xs md:max-w-md lg:max-w-lg">
                <p class="text-gray-800">${userMessage}</p>
            </div>
            <div class="self-start bg-gray-200 rounded-lg p-3 mt-2 max-w-xs md:max-w-md lg:max-w-lg">
                <p class="text-gray-800">${botResponse}</p>
            </div>
        `;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});