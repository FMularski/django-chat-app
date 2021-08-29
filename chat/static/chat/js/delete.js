(function(){
    const dark = document.querySelector('#dark');
    const confirmDelete = document.querySelector('#confirm-delete');
    const confirmDeleteBtn = document.querySelector('#confirm-delete-btn');
    let friendRecord;
    
    const deleteBtns = document.querySelectorAll('.delete-btn');
    deleteBtns.forEach(function(btn) {
        btn.addEventListener('click', function(){
            dark.classList.add('active');
            confirmDelete.classList.add('active');

            document.querySelector('#delete-username').innerText = btn.getAttribute('del-username');
            confirmDeleteBtn.setAttribute('del-id', btn.getAttribute('del-id'));
            btn.parentElement.classList.add('to-be-removed');
        })
    });

    const cancelDeleteBtn = document.querySelector('#cancel-delete-btn');
    cancelDeleteBtn.addEventListener('click', function(){
        dark.classList.remove('active');
        confirmDelete.classList.remove('active');
        document.querySelector('.to-be-removed').classList.remove('.to-be-removed');
    });

    confirmDeleteBtn.addEventListener('click', function(){
        dark.classList.remove('active');
        confirmDelete.classList.remove('active');
        document.querySelector('.to-be-removed').remove();
        const friendsCount = document.querySelector('#friends-count');
        friendsCount.innerText = parseInt(friendsCount.innerText) - 1;

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            url: '/ajax/delete_friend/' + this.getAttribute('del-id') + '/',
            headers : {'X-CSRFToken': csrftoken },
            method: 'POST',
            dataType: 'json',
            success: function(response) {
            }
        })
    });

})();