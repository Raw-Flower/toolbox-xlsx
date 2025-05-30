const app_field = document.getElementById('id_app')
app_field.addEventListener('change', function () {
    getModels(app_field.value)
})

function getModels(app_name) {
    const model_field = document.getElementById('id_model')
    model_field.innerHTML = ''
    if (app_name != '') {
        fetch(`../get-models/${app_name}`)
            .then(response => response.json())
            .then(data => {
                model_field.innerHTML += '<option value selected>-- Select model --</option><option'
                for (let model of data.models) {
                    model_field.innerHTML += `<option value="${model[0]}">${model[1]}</option><option`
                }
            })
            .catch(error => {
                alert('Error while getting the models from apps, please contact system administrator.')
            })
    } else {
        model_field.innerHTML += '<option value selected>Select an app first</option><option'
    }
}