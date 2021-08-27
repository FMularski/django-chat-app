(function(){
    const searchInput = document.querySelector('#search-input');
    const resultsBox = document.querySelector('#search-results');
    const spinner = document.querySelector('#spinner');

    searchInput.addEventListener('keyup', function() {

        if(!searchInput.value) {
            spinner.innerHTML = '';
            resultsBox.innerHTML = '';
            return;
        } 

        spinner.innerHTML = '<i class="fas fa-spinner spinning"></i>';
        
        $.ajax({
            url: '/ajax/search/' + searchInput.value,
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                spinner.innerHTML = '';
                resultsBox.innerHTML = '';

                if (!response.length) {
                    resultsBox.innerHTML = '<p id="no-results"><i class="fas fa-times-circle"></i> No results found.</p>';
                    return;
                }

                response.forEach(function(result){
                    resultsBox.innerHTML += 
                    '<div id="result-' + result.pk + '" class="result"><div>' +
                    '<img src="' + result.profile_img + '">' + 
                    '<span>' + result.username + '</span></div>' + 
                    '<i class="fas fa-user-plus hover-scale invite-btn" invite-id="' + result.pk + '"></i>' + 
                    '</div>';
                })

                // inviting vvv

                const inviteBtns = document.querySelectorAll('.invite-btn');

                inviteBtns.forEach(function(btn) {
                    btn.addEventListener('click', function(){
                        const recordToRemove = document.querySelector('#result-' + btn.getAttribute('invite-id'));
                        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                        $.ajax({
                            url: '/ajax/invite/' + btn.getAttribute('invite-id') + '/',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                            method: 'POST',
                            dataType: 'json',
                            success: function(response) {
                                recordToRemove.remove()

                                const flash = document.createElement('div');
                                flash.classList.add('popup');
                                flash.classList.add('success');
                                flash.innerHTML = '<h4><i class="fas fa-check-circle"></i> Success</h4>' + 
                                '<b>The invitation has been sent.</b></div>';
                                
                                document.querySelector('body').append(flash);
                            }
                        })
                        
                    })
                })
            }
        })
    })

    const declineInvBtns = document.querySelectorAll('.decline');

    declineInvBtns.forEach(function(btn) {

        btn.addEventListener('click', function(){
            const invitationToRemove = document.querySelector('#invitation-' + btn.getAttribute('invite-id'));
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
            $.ajax({
                url: '/ajax/decline/' + btn.getAttribute('invite-id') + '/',
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                dataType: 'json',
                success: function(response) {
                    invitationToRemove.remove();
                    const flash = document.createElement('div');
                    flash.classList.add('popup');
                    flash.classList.add('success');
                    flash.innerHTML = '<h4><i class="fas fa-check-circle"></i> Success</h4>' + 
                    '<b>The invitation has been declined.</b></div>';
                    document.querySelector('body').append(flash);

                    const invitationsCount = document.querySelectorAll('.invitation').length;

                    if(!invitationsCount) {
                        const p = document.createElement('p');
                        p.id = 'no-invitations';
                        p.innerText = 'No pending invitations.';
                        document.querySelector('#invitations').append(p);
                    }
                    
                }
            })
        })

    })

})();