// ui.js
function displayChatMessages(chat) {
    const messages = chat.messages;
    const chatContent = $('#chat-body');
    const chatHeader = $('#chat-header');
    const chatUserName = $('#chat-user-name');
    const chatFooter = $('#chat-footer');
    
    chatContent.empty();
    
    // Скрываем элементы, если сообщений нет
    if (messages && messages.length > 0) {
        chatHeader.show();
        chatFooter.show();
        chatContent.show();
        chatHeader.find('h2').html(`
            <span class="chat-header-user">${chat.full_name}</span><br>
            <span class="chat-header-username">@${chat.username}</span>
        `);
    } else {
        chatHeader.hide();
        chatFooter.hide();
        chatContent.append('<p>No messages found.</p>');
    }

    if (messages) {
        messages.forEach(function(message) {
            const messageElement = $('<div></div>').addClass('chat-message');
            messageElement.addClass(message.direction);
            
            // Если сообщение от вас (outgoing)
            if (message.direction === 'outgoing') {
                messageElement.addClass('you-message');
            } else {
                messageElement.addClass('user-message');
            }

            // Добавляем текст и время
            messageElement.html(`
                <span class="chat-timestamp">${message.created_at}</span><br>
                ${message.text}
            `);

            // Сжимаем сообщение, убираем лишние отступы
            messageElement.css({
                'padding': '8px 12px',
                'margin-bottom': '8px',
                'font-size': '15px',
                'line-height': '1.4',
                'border-radius': '8px',
                'box-shadow': '0 2px 5px rgba(0, 0, 0, 0.1)',
                'transition': 'transform 0.2s ease-in-out, opacity 0.2s ease-in-out'
            });

            // Плавное появление сообщений
            messageElement.css('opacity', '0');
            chatContent.append(messageElement);
            messageElement.animate({ opacity: 1, transform: 'translateY(0)' }, 400);  // Анимация появления

            // Цвет фона для входящих и исходящих сообщений
            if (message.direction === 'incoming') {
                messageElement.css('background-color', '#e0f7fa');
            } else {
                messageElement.css('background-color', '#c8e6c9');
            }
        });
    }

    scrollToBottom();
}

// Установка активного чата
function setActiveChat(userId) {
    $('#chat-list li').removeClass('active').css({
        'backgroundColor': '#2d2d2d', // Цвет для неактивных чатов
        'boxShadow': '0 2px 6px rgba(0, 0, 0, 0.15)',
    });

    $('#chat-list li').filter(function() {
        return $(this).text().includes(`id: ${userId}`);
    }).addClass('active').css({
        'backgroundColor': '#3b83bd', // Цвет для активного чата
        'color': '#fff', // Белый текст для активного чата
        'boxShadow': '0 4px 12px rgba(0, 123, 255, 0.3)', // Более яркая тень
    });

    // Сохраняем активный чат в localStorage
    localStorage.setItem('activeChat', userId);
}

// Прокрутка до конца чата
function scrollToBottom() {
    const chatBody = $('#chat-body');
    chatBody.scrollTop(chatBody[0].scrollHeight);
}

