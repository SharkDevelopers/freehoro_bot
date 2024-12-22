// websocket.js

let socket;
const reconnectInterval = 5000;  // Интервал для переподключения (5 секунд)

// Функция для подключения к WebSocket серверу
function connectWebSocket() {
    socket = new WebSocket(`ws://localhost:8005/ws/conn/example_user`);

    socket.onopen = function() {
        console.log("WebSocket connection established.");
    };

    socket.onmessage = function(event) {
        const parsedMessage = JSON.parse(event.data);

        switch (parsedMessage.event_type) {
            case 'new_message':
                handleNewMessage(parsedMessage);
                break;
            case 'new_chat':
                handleNewChat(parsedMessage);
                break;
            default:
                console.log("Unknown event type:", parsedMessage.event_type);
        }
    };

    socket.onclose = function() {
        console.log("WebSocket connection closed.");
        setTimeout(connectWebSocket, reconnectInterval);
    };

    socket.onerror = function(error) {
        console.log("WebSocket error:", error);
        socket.close();
    };
}

// Обработка новых сообщений
function handleNewMessage(message) {
    console.log("New message:", message.data);
    const userId = message.user_id;

    if ($('#chat-header').text().includes(`User ID: ${userId}`)) {
        loadChatMessages(userId);
    }
    loadChats();
}

// Обработка новых чатов
function handleNewChat(message) {
    console.log("New chat:", message.data);
    loadChats();
}

// Инициализация WebSocket подключения
connectWebSocket();

