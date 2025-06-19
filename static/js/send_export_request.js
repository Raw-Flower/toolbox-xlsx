const button = document.getElementById('generate_export')

button.addEventListener('click', function () {
    // Disabled button
    button.disabled = true
    button.innerHTML = 'Processing...'

    // Get query parameters from URL
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const params2send = new FormData()
    const token = document.getElementsByName('csrfmiddlewaretoken')

    // Add query parameters into body request
    for(param of urlParams) {
        params2send.append(param[0],param[1])
    }

    // Prepare other parameters to send request to back-end
    params2send.append('csrfmiddlewaretoken',token[0].value)
    params2send.append('app',button.dataset.app)
    params2send.append('model',button.dataset.model)

    // Send fech request
    fetch('../get-xlsx-file/',{
        method: 'POST',
        body: params2send
    })
    .then(response => response.json())
    .then(data => {
        // Enable button
        button.disabled = false
        button.innerText = 'Export'
        if(data.result){
            window.location.href = data.file_path;
        }else{
            console.log(data)
            if(data.error_message){
                alert(data.error_message)
            }else if(data.form_errors){
                let message = 'Your request has been failed, please review the following errors: \n'
                for(const error of data.form_errors){
                    message+=`* ${error}\n` 
                }
                alert(message)
            }
            else{
                alert('File generation has been failed, please contact system administrator.')
            }
        }
    })
    .catch(error => {
        // Enable button
        button.disabled = false;
        button.innerText = 'Export'
        console.error('Error fetching data:', error)
    });
})