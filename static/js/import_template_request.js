const button = document.getElementById('import_request')

button.addEventListener('click', function () {
    // Disabled button
    button.disabled = true
    button.innerHTML = 'Processing...'

    // Get token from form
    const token = document.getElementsByName('csrfmiddlewaretoken')

    // Prepare other parameters to send request to back-end
    params2send = new FormData()
    params2send.append('csrfmiddlewaretoken',token[0].value)
    params2send.append('app',button.dataset.app)
    params2send.append('model',button.dataset.model)

    // Send fech request
    fetch('../import-request/',{
        method: 'POST',
        body: params2send
    })
    .then(response => response.json())
    .then(data => {
        // Enable button
        button.disabled = false
        button.innerText = 'Add/Update template'

        //Processing request
        if(data.result){
            alert('Import template was created/updated sucucesffully.')
        }else{
            alert(`ERROR: ${data.error_message}`)
        }
    })
    .catch(error => {
        // Enable button
        button.disabled = false;
        button.innerText = 'Add/Update template'
        console.error('Error fetching data:', error)
    });
})