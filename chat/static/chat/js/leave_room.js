(function(){
    const leaveRoomPanel = document.querySelector('#leave-room-panel');
    const cancelLeaveBtn = document.querySelector('#cancel-leave-btn');
    const leaveRoomBtn = document.querySelector('#leave-room-btn');
    const dark = document.querySelector('#dark');

    leaveRoomBtn.addEventListener('click', function(){
        leaveRoomPanel.classList.add('active');
        dark.classList.add('active');
    });

    cancelLeaveBtn.addEventListener('click', function(){
        leaveRoomPanel.classList.remove('active');
        dark.classList.remove('active');
    });

})();