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
                    console.log(result);
                    resultsBox.innerHTML += 
                    '<div class="result"><div>' +
                    '<img src="' + result.profile_img + '">' + 
                    '<span>' + result.username + '</span></div>' + 
                    '<i class="fas fa-user-plus hover-scale"></i>' + 
                    '</div>';
                })
            }
        })


    })
})();