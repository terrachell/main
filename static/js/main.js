// Подключаемся к серверу
const socket = io({
    transports: ['websocket', 'polling'],
    reconnection: true,
    reconnectionAttempts: 5
});

let currentChat = 1;

// DOM элементы
const create_new_chat_btn = document.getElementById('create_new_chat');
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const currentChatName = document.getElementById('current-chat-name');
const account = document.getElementById("account")


const currentUser = account.innerHTML;

// Подключение
socket.on('connect', () => {
    console.log('Подключено к серверу, SID:', socket.id);
    addSystemMessage('Подключено к чату');
    loadMessages(currentChat);
});

socket.on('connected', (data) => {
    console.log('Сервер подтвердил подключение:', data);
});

socket.on('disconnect', () => {
    console.log('Отключено от сервера');
    addSystemMessage('Потеряно соединение. Переподключение...');
});

// Получение нового сообщения
socket.on('new_message', (data) => {
    console.log('Новое сообщение:', data);
    if (data.chat_id === currentChat) {
        addMessage(data.user, data.message, data.user === currentUser, data.timestamp);
    }
    updateLastMessage(data.chat_id, data.user, data.message);
});

// Загрузка истории сообщений
function loadMessages(chatId) {
    fetch(`/api/messages/${chatId}`)
        .then(response => response.json())
        .then(messages => {
            messagesContainer.innerHTML = '';
            if (messages.length === 0) {
                messagesContainer.innerHTML = '<div class="empty-state"><p>💬 Нет сообщений</p><p>Напишите первое сообщение</p></div>';
            } else {
                messages.forEach(msg => {
                    console.log(msg)
                    const created_at = msg.created_at.match(/(\d{2}):(\d{2})/)[0];
                    addMessage(msg.username, msg.message, msg.username === currentUser, created_at);
                });
            }
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(err => console.error('Ошибка загрузки сообщений:', err));
}

// Отправка сообщения
function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    const data = {
        user: currentUser,
        message: message,
        chatid: currentChat,
    };
    
    console.log('📤 Отправка:', data);
    socket.emit('send_message', data);
    
    // Оптимистичное отображение (без ожидания сервера)
  /*   addMessage(currentUser, message, true); */
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Прокрутка вниз
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 100);
}

// Добавление сообщения в DOM
function addMessage(username, message, isSent, created_at) {
    const emptyState = messagesContainer.querySelector('.empty-state');
    if (emptyState) emptyState.remove();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isSent ? 'sent' : 'received'}`;
    messageDiv.innerHTML = `
        <div class="message-info">${username} • ${created_at}</div>
        <div class="message-bubble">${escapeHtml(message)}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Системное сообщение
function addSystemMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.style.textAlign = 'center';
    msgDiv.style.color = '#999';
    msgDiv.style.fontSize = '12px';
    msgDiv.style.margin = '10px 0';
    msgDiv.textContent = text;
    messagesContainer.appendChild(msgDiv);
}

// Экранирование HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 100) + 'px';
});

// Enter для отправки
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

// Переключение чата
document.querySelectorAll('.chat-item').forEach(chat => {
    chat.addEventListener('click', () => {
        document.querySelectorAll('.chat-item').forEach(c => c.classList.remove('active'));
        chat.classList.add('active');
        currentChat = parseInt(chat.dataset.chatId);
        currentChatName.textContent = chat.querySelector('.chat-name').textContent;
        loadMessages(currentChat);
    });
});

create_new_chat_btn.addEventListener('click', () => {
    const dark_block = document.getElementById('dark-block');
    const cancel = document.getElementById('cancel')
    cancel.addEventListener('click', () => {
        dark_block.style.display = 'none'
    })
    dark_block.style.display = 'flex'
})



// Приветствие
addSystemMessage(`Добро пожаловать, ${currentUser}!`);