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

        document.querySelector('#filter-friends').value = '';
        document.querySelector('#id_name').value = '';
        document.querySelector('#uncheck-btn').click();
        document.querySelectorAll('.add-friend-record').forEach(function(record){
            record.classList.remove('hidden');
        })
    })

    const filterInput = document.querySelector('#filter-friends');
    const addFriendRecords = document.querySelectorAll('.add-friend-record');
    const filterSpinner = document.querySelector('#filter-spinner');

    filterInput.addEventListener('keyup', function(){

        if (filterInput.value) {
            addFriendRecords.forEach(function(record){
                const username = record.children[1].children[1].innerText;
                
                if(!username.startsWith(filterInput.value))
                    record.classList.add('hidden');
                else 
                    record.classList.remove('hidden');
            })
        } else {
            addFriendRecords.forEach(function(record){
                record.classList.remove('hidden');
            })
        }

        // if (!filterInput.value) {
        //     addFriendRecords.forEach(function(record) {
        //         record.classList.remove('hidden');
        //     });
        //     filterSpinner.innerHTML = '';
        //     return;
        // }

        // filterSpinner.innerHTML = '<i class="fas fa-spinner spinning"></i>';
        // $.ajax({
        //     url: '/ajax/filter/' + filterInput.value + '/',
        //     method: 'GET',
        //     dataType: 'json',
        //     success: function(response) {
        //         addFriendRecords.forEach(function(record){
        //             if (response.idsToHide.includes(parseInt(record.getAttribute('id').split('-')[2]))) {
        //                 record.classList.add('hidden');
        //             } else {
        //                 record.classList.remove('hidden');
        //             }

        //             filterSpinner.innerHTML = '';
        //         })
        //     }
        // })

    });

    const uncheckBtn = document.querySelector('#uncheck-btn');
    uncheckBtn.addEventListener('click', function(){
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(function(cb) {
            cb.checked = false;
        })
    })

})();