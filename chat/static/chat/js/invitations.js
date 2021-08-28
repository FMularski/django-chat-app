(function(){

    function handleInvitation(action, msg) {
        const handleBtns = document.querySelectorAll('.' + action);
    
        handleBtns.forEach(function(btn) {
    
            btn.addEventListener('click', function(){
                const senderId = btn.getAttribute('invite-id');
                const invitationToRemove = document.querySelector('#invitation-' + senderId);
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
                $.ajax({
                    url: '/ajax/' + action +'/' + senderId + '/',
                    method: 'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    dataType: 'json',
                    success: function(response) {
                        invitationToRemove.remove();
                        const flash = document.createElement('div');
                        flash.classList.add('popup');
                        flash.classList.add('success');
                        flash.innerHTML = '<h4><i class="fas fa-check-circle"></i> Success</h4>' + 
                        '<b>' + msg +'</b></div>';
                        document.querySelector('body').append(flash);
    
                        const invitationsCount = document.querySelectorAll('.invitation').length;
    
                        if(!invitationsCount) {
                            const p = document.createElement('p');
                            p.id = 'no-invitations';
                            p.innerText = 'No pending invitations.';
                            document.querySelector('#invitations').append(p);
                        }
                        
                        const invitesCount = document.querySelector('#invitations-count');
                        invitesCount.innerText = parseInt(invitesCount.innerText) - 1;
                        
                        if (action == 'decline') return;

                        const friendsCount = document.querySelector('#friends-count');
                        friendsCount.innerText = parseInt(friendsCount.innerText) + 1;


                        const friendsSection = document.querySelector('#my-friends');
                        friendsSection.innerHTML += 
                        '<div class="friend-record">' +
                            '<img src="' + response.senderProfileImg + '"/>' + 
                            '<span>' + response.senderUsername + '</span>'; + 
                        '</div>';                        
                    }
                })
            })
    
        })
        
    }

    // decline invitation
    handleInvitation('decline', 'The invitation has been declined.');
    handleInvitation('accept', 'The invitation has been accepted.');

})();