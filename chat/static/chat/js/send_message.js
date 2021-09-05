(function(){
    const messageTextInput = document.querySelector('#msg-text');
    const sendBtn = document.querySelector('#send-btn');
    const roomPK = document.querySelector('#chat-room-header').getAttribute('room-pk');
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const messages = document.querySelector('#messages');

    sendBtn.addEventListener('click', function() {

        if (!messageTextInput.value) return;

        const text = messageTextInput.value;
        messageTextInput.value = '';

        $.ajax({
            url: '/ajax/send_msg/',
            method: 'POST',
            headers: {'X-CSRFToken': csrfToken},
            dataType: 'json',
            data: {'text': text, 'room-pk': roomPK },
            success: function(response) {
                messages.innerHTML += 
                    '<div class="message hover-scale user-message new-msg ">' + 
                        '<p>' + 
                            '<img src="' + response.senderProfileImg + '" class="user-portrait">' + 
                            '<span class="chat-room-record-username"><b>' + response.senderUsername + '</b>' + 
                            '<i>' + response.createdAt + '</i></span>' +
                        '</p><hr>' +
                        '<p class="message-text">' + response.text + '</p>' +
                        // attached img... 
                    '</div>'

                $('#messages').animate({ scrollTop: messages.scrollHeight}, 'slow');
            }

        });
    });


    messageTextInput.addEventListener('keyup', function(e){
        if (e.key == 'Enter') {
            if (messageTextInput.value.trim())
                sendBtn.click();
        }
    })

})();