(function(){

    function handleInvitation(action, msg) {
        const handleBtns = document.querySelectorAll('.' + action);
    
        handleBtns.forEach(function(btn) {
    
            btn.addEventListener('click', function(){
                const invitationId = btn.getAttribute('invite-id');
                const invitationToRemove = document.querySelector('#invitation-' + invitationId);
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
                const invitesCount = document.querySelector('#invitations-count');
                invitesCount.innerText = parseInt(invitesCount.innerText) - 1;

                invitationToRemove.style.animation = 'shrink-record 0.3s ease';
                invitationToRemove.addEventListener('animationend', function() {

                    invitationToRemove.remove() 

                    const invitationsCount = document.querySelectorAll('.invitation').length;
                    if (invitationsCount) return;
    
                    const p = document.createElement('p');
                    p.id = 'no-invitations';
                    p.innerText = 'No pending invitations.';
                    document.querySelector('#invitations').append(p);
                });

                
                $.ajax({
                    url: '/ajax/' + action +'/' + invitationId + '/',
                    method: 'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    dataType: 'json',
                    success: function(response) {
                        const flash = document.createElement('div');
                        flash.classList.add('popup');
                        flash.classList.add('success');
                        flash.innerHTML = '<h4><i class="fas fa-check-circle"></i> Success</h4>' + 
                        '<b>' + msg +'</b></div>';
                        document.querySelector('body').append(flash);
    
                        
                        if (action == 'decline') return;

                        const friendsCount = document.querySelector('#friends-count');
                        friendsCount.innerText = parseInt(friendsCount.innerText) + 1;

                        const friendsSection = document.querySelector('#my-friends');
                        friendsSection.innerHTML += 
                        '<div class="friend-record flex-between">' +
                            '<div>' +
                                '<img src="' + response.senderProfileImg + '"/>' + 
                                '<span>' + response.senderUsername + '</span>' +
                            '</div>' +
                            '<i class="delete-btn delete-btn-' + response.senderId + ' fas fa-minus hover-scale"' +
                            'del-username="' + response.senderUsername + '"' +
                            'del-id="' + response.senderId + '"></i>' +
                        '</div>';                        
                        
                        const newDeleteBtn = document.querySelector('.delete-btn-' + response.senderId);
                        newDeleteBtn.addEventListener('click', function() {
                            document.querySelector('#dark').classList.add('active');
                            document.querySelector('#confirm-delete').classList.add('active');

                            document.querySelector('#delete-username').innerText = newDeleteBtn.getAttribute('del-username');
                            document.querySelector('#confirm-delete-btn').setAttribute('del-id', newDeleteBtn.getAttribute('del-id'));
                            
                            newDeleteBtn.parentElement.classList.add('to-be-removed');
                        })
                    }
                })
            })
    
        })
        
    }

    // decline invitation
    handleInvitation('decline', 'The invitation has been declined.');
    handleInvitation('accept', 'The invitation has been accepted.');

})();