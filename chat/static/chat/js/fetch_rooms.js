(function(){
    const rooms = document.querySelector('#rooms-list');
    const filterInput = document.querySelector('#filter-room-input');
    const spinner = document.querySelector('#filter-room-spinner');
    spinner.innerHTML = '<i class="fas fa-spinner spinning"></i>';

    function fetchRooms() {
        $.ajax({
            url: '/ajax/fetch_rooms/',
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                spinner.innerHTML = '';
                rooms.innerHTML = ''

                response.rooms.forEach(function(room) {

                    const showAfterFilter = filterInput.value ? room.name.startsWith(filterInput.value) : true;

                    rooms.innerHTML += 
                    '<a href="/chat_rooms/' + room.pk + '" class="chat-room-record-a transition-activator ' + (showAfterFilter ? '' : 'hidden') + '">' + 
                        '<div class="chat-room-record" id="room-record-' + room.pk + '">' + 
                            '<p class="chat-room-record-name"><b>' + room.name + 
                            '</b> <span class="chat-room-record-users-count">(' + room.members + ' users)</span></p>' + 
                            '<div class="chat-preview flex-start">' + 
                                '<img src="' + room.senderProfileImg + '" class="user-portrait">' + 
                                '<div class="flex-between-column">' + 
                                    '<span class="chat-room-record-username"><b>' + room.senderUsername + '</b> <i>' + room.lastMsgAt + '</i></span>' + 
                                    '<span class="chat-room-record-message">' + room.lastMsgText + '</span>' + 
                                '</div>' + 
                            '</div>' + 
                        '</div>' + 
                    '</a>';
                })
            }
        })
    }

    fetchRooms();
    setInterval(fetchRooms, 5000);

})();