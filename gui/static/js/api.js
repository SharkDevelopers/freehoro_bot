// api.js

// Получение списка чатов
function loadChats() {
    $.ajax({
        url: '/api/chats',
        method: 'GET',
        success: function(data) {
            populateChatList(data.data);
        },
        error: function() {
            alert('Error loading chats');
        }
    });
}

// Заполнение списка чатов
function populateChatList(chats) {
    const chatList = $('#chat-list');
    chatList.empty();

    chats.forEach(function(chat) {
        const lastMessage = chat.messages[0];
        const title = chat.full_name ? chat.full_name : chat.user_id;

        // Функция для сокращения текста
        function shortenText(text, maxLength) {
            if (text.length > maxLength) {
                return text.slice(0, maxLength) + '...';
            }
            return text;
        }

        // Сокращаем титл и юзернейм
        const shortenedTitle = shortenText(title, 15);

        // Создаём элемент <li> для чата
        const chatItem = $('<li></li>')
            .click(function() {
                loadChatMessages(chat.user_id);
                setActiveChat(chat.user_id);
            })
            .css({
                'display': 'flex',
                'alignItems': 'center',  // Центрирование по вертикали
                'padding': '12px 15px',
                'marginBottom': '10px',
                'borderRadius': '12px',
                'cursor': 'pointer',
                'transition': 'all 0.3s ease',
                'backgroundColor': '#2d2d2d',  // Темный фон по умолчанию
                'boxShadow': '0 2px 6px rgba(0, 0, 0, 0.15)',
            })
            ;

        const avatarUrl = '/static/avatar.png';

        // Создаём аватарку пользователя
        const avatar = $('<img>')
            .attr('src', avatarUrl)  // Замените на путь к изображению
            .attr('alt', 'Avatar')
            .css({
                'width': '50px',
                'height': '50px',
                'borderRadius': '50%',  // Круглая аватарка
                'marginRight': '15px',
                'objectFit': 'cover',
            });

        // Создаём элемент для титла
        const titleElement = $('<span></span>')
            .text(shortenedTitle)
            .css({
                'fontWeight': 'bold',
                'fontSize': '16px',
                'textAlign': 'left',
                'display': 'block',
                'maxWidth': '200px',
                'whiteSpace': 'nowrap',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'color': '#fff', // Белый цвет для титла
            });

        // Создаём элемент для юзернейма (курсивом)
        const idElement = $('<span></span>')
            .text(`id: ${chat.user_id}`)
            .css({
                'fontStyle': 'italic',
                'fontSize': '14px',
                'color': '#bbb', // Светло-серый цвет для id
                'textAlign': 'left',
                'display': 'block',
                'maxWidth': '200px',
                'whiteSpace': 'nowrap',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            });

        // Создаём элемент для последнего сообщения
        const lastMessageElement = $('<span></span>')
            .text(`🕘${lastMessage.created_at}`)
            .css({
                'fontSize': '14px',
                'color': '#ccc', // Светло-серый для последнего сообщения
                'display': 'block',
                'maxWidth': '250px',
                'whiteSpace': 'nowrap',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            });

        // Добавляем аватарку, титл, юзернейм и сообщение в chatItem
        chatItem.append(avatar)
                .append($('<div></div>')
                    .css({
                        'display': 'flex',
                        'flexDirection': 'column',
                        'justifyContent': 'center',
                        'flexGrow': '1',
                    })
                    .append(titleElement)
                    .append(idElement)
                    .append(lastMessageElement)
                );

        // Добавляем чат в список
        chatList.append(chatItem);
    });

    const activeChatId = localStorage.getItem('activeChat');
    if (activeChatId) {
        setActiveChat(activeChatId);
        loadChatMessages(activeChatId);
    }
}


// Загрузка сообщений чата
function loadChatMessages(userId) {
    $('#chat-header').show();
    $('#chat-body').show();
    $('#chat-footer').show();

    $.ajax({
        url: `/api/chats/${userId}`,
        method: 'GET',
        success: function(chat) {
            displayChatMessages(chat);
        },
        error: function() {
            alert('Error loading chat messages.');
        }
    });
}

// Отправка сообщения
function sendMessage(userId, messageText) {
    $.ajax({
        url: `/api/chats/${userId}/send_message`,
        method: 'POST',
        data: { text: messageText },
        success: function() {
            console.log("Message sent successfully");
        },
        error: function() {
            alert('Error sending message.');
        }
    });
}

