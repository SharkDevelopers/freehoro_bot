// main.js

$(document).ready(function() {
    // Загружаем чаты
    loadChats();

    // Обработка отправки сообщения
    $('#send-message-button').click(function() {
        const messageText = $('#message-input').val().trim();
        const userId = $('#chat-header h2').text().replace('Chat with User ID: ', '').trim();

        if (messageText && userId) {
            const activeChatId = localStorage.getItem('activeChat');

            sendMessage(activeChatId, messageText);
            $('#message-input').val('');
        } else {
            alert('Cannot send message. User ID or message text is invalid.');
        }
    });
});

