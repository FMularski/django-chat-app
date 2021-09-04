(function(){
    const filterInput = document.querySelector('#filter-input');
    const filterSpinner = document.querySelector('#filter-spinner');
    const friendRecords = document.querySelectorAll('.friend-record');


    filterInput.addEventListener('keyup', function(){

        // filterSpinner.innerHTML = '<i class="fas fa-spinner spinning"></i>';

        if (filterInput.value) {
            friendRecords.forEach(function(record){
                const username = record.children[0].children[1].innerText;
                
                if(!username.startsWith(filterInput.value))
                    record.classList.add('hidden');
                else 
                    record.classList.remove('hidden');
            })
        } else {
            friendRecords.forEach(function(record){
                record.classList.remove('hidden');
            })
        }

        // $.ajax({
        //     url: '/ajax/filter/' + (filterInput.value ? filterInput.value  + '/' : ''),
        //     method: 'GET',
        //     dataType: 'json',
        //     success: function(response) {
        //         const friendRecords = document.querySelectorAll('.friend-record');

        //         friendRecords.forEach(function(record){
        //             if (response.idsToHide.includes(parseInt(record.getAttribute('id').split('-')[2]))) {
        //                 record.classList.add('hidden');
        //             } else {
        //                 record.classList.remove('hidden');
        //             }
        //         })

        //         filterSpinner.innerHTML = '';
        //     }
        // });
    });



})();