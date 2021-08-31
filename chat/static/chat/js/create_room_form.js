(function(){
    const dark = document.querySelector('#dark');
    const openCreateRoomFormBtn = document.querySelector("#add-chat-room-btn");
    const createRoomForm = document.querySelector('#create-room-panel');
    const closeCreateRoomFormBtn = document.querySelector('#close-create-room-btn');

    openCreateRoomFormBtn.addEventListener('click', function(){
        createRoomForm.classList.add('active');
        dark.classList.add('active');
    });

    closeCreateRoomFormBtn.addEventListener('click', function(){
        createRoomForm.classList.remove('active');
        dark.classList.remove('active');
    })

})();