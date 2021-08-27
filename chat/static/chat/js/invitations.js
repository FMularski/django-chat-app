(function(){
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