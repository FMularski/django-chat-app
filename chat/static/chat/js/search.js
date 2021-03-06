(function(){
    const searchInput = document.querySelector('#search-input');
    const resultsBox = document.querySelector('#search-results');
    const spinner = document.querySelector('#spinner');

    searchInput.addEventListener('keyup', function() {

        if(!searchInput.value) {
            resultsBox.innerHTML = '';
            return;
        } 

        spinner.innerHTML = '<i class="fas fa-spinner spinning"></i>';
        
        $.ajax({
            url: '/ajax/search/' + (searchInput.value ? searchInput.value + '/' : ''),
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                spinner.innerHTML = '';
                resultsBox.innerHTML = '';

                if (!response.length) {
                    resultsBox.innerHTML = '<p id="no-results"><i class="fas fa-times-circle"></i> No results found.</p>';
                    return;
                }

                response.forEach(function(result) {
                    resultsBox.innerHTML += 
                    '<div id="result-' + result.pk + '" class="result"><div>' +
                    '<img src="' + result.profile_img + '">' + 
                    '<span>' + result.username + '</span></div>' + 
                    '<i class="hover-scale invite-btn ' +
                    (result.status == 'pending' ? 'disabled pending far fa-clock' : 
                    (result.status == 'is_friend' ? 'disabled accepted fas fa-user-check' : 'fas fa-user-plus')) + 
                    '" invite-id="' + result.pk + '"></i>' + 
                    '</div>';
                })

                // inviting vvv

                const inviteBtns = document.querySelectorAll('.invite-btn');

                inviteBtns.forEach(function(btn) {
                    btn.addEventListener('click', function(){
                        const recordToRemove = document.querySelector('#result-' + btn.getAttribute('invite-id'));

                        recordToRemove.style.animation = 'shrink-record 0.3s ease';
                        recordToRemove.addEventListener('animationend', function() {
                            recordToRemove.remove()
                        })
       
                        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                        const flyingMsg = document.createElement('img');
                        flyingMsg.setAttribute('src', 'https://django-chat-app-bucket.s3.eu-central-1.amazonaws.com/chat/img/message.png');
                        flyingMsg.setAttribute('class', 'flying-invitation');
                        flyingMsg.addEventListener('animationend', function() {
                            this.remove();
                        })

                        document.querySelector('body').append(flyingMsg);

                        $.ajax({
                            url: '/ajax/invite/' + btn.getAttribute('invite-id') + '/',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                            method: 'POST',
                            dataType: 'json',
                            success: function(response) {
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

})();