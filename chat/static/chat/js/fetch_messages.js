(function(){
    const messagesBox = document.querySelector('#messages');
    const roomPK = document.querySelector('#chat-room-header').getAttribute('room-pk');
    const newMsgBtn = document.querySelector('#new-msg-btn');
    const spinner = document.querySelector('#fetch-msg-spinner');
    spinner.innerHTML = '<i class="fas fa-spinner spinning"></i>';


    newMsgBtn.addEventListener('click', function(){
        $('#messages').animate({ scrollTop: messages.scrollHeight}, 'slow');
        newMsgBtn.classList.add('hidden');
    })

    function fetch_messages(scrollSpeed) {
        const scroll = messagesBox.scrollTop === (messagesBox.scrollHeight - messagesBox.offsetHeight);
        const msgCountBefore = document.querySelectorAll('.message').length;

        $.ajax({
            url: '/ajax/fetch_messages/' + roomPK + '/',
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                messagesBox.innerHTML = ''
                spinner.innerHTML = ''

                response.messages.forEach(function(message) {
                    messagesBox.innerHTML += 
                    '<div class="message hover-scale ' + message.cssClass + '">' + 
                        '<p>' + 
                            '<img src="' + message.senderProfileImg + '" class="user-portrait">' + 
                            '<span class="chat-room-record-username"><b>' + message.senderUsername + '</b> ' + 
                            '<i>' + message.createdAt + '</i></span>' + 
                        '</p>' + 
                        '<hr/>' + 
                        '<p class="message-text">' + message.text +'</p>' + 
                        // '<img class="message-img" src="' + message.attachedImg + '" alt="">' + 
                        '<div class="message-likes">' + 
                            '<i class="fas fa-heart"></i>' + 
                            '<span class="likes-count"> ' + message.likes + '</span>' + 
                        '</div>' + 
                    '</div>'
                });

                if (scroll) 
                    $('#messages').animate({ scrollTop: messages.scrollHeight}, scrollSpeed);
                else {
                    const msgCountAfter = document.querySelectorAll('.message').length;
                    if (msgCountAfter > msgCountBefore)
                        newMsgBtn.classList.remove('hidden');
                } 
            }
        })
    }

    fetch_messages(1); // initial fetch, instant scroll

    setInterval(function(){
        fetch_messages('slow');
    }, 5000);

})();