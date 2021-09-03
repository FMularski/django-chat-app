(function(){

    const filterInput = document.querySelector('#filter-room-input');
    const spinner = document.querySelector('#filter-room-spinner');

    filterInput.addEventListener('keyup', function(){

        spinner.innerHTML = '<i class="fas fa-spinner spinning"></i>';

        $.ajax({
            url: '/ajax/filter_rooms/' + (filterInput.value ? filterInput.value + '/' : ''),
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                const rooms = document.querySelectorAll('.chat-room-record');
                rooms.forEach(function(record){
                    if (response.idsToHide.includes(parseInt(record.getAttribute('id').split('-')[2]))) {
                        record.classList.add('hidden');
                    } else {
                        record.classList.remove('hidden');
                    }
                })

                spinner.innerHTML = '';
            }
        })


    });

})();