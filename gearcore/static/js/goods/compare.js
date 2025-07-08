const forms = document.querySelectorAll('.formToCompare')

async function makeRequest(url, data, csrfToken, msg="") {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            showAlert(msg)
            throw new Error(`HTTP помилка! статус: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Помилка запиту:', error);
        throw error;
    }
}

function getCsrfToken(form) {
    const csrfTokenInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfTokenInput ? csrfTokenInput.value : null;
}

forms?.forEach(form=>{
    form.addEventListener('submit', async function (event){
        event.preventDefault();
        const form = event.target;

        const url = form.getAttribute('action');
        const variantId = form.dataset?.variantId
        const action = form.dataset?.actionCompare
        const csrfToken = getCsrfToken(form);

        if (!url || !variantId || !action || !csrfToken){
            showAlert("Сталася помилка при додавані товару до порівняння")
            console.warn('не отримано достатньо даних для додавання товару у порівняння')
        }

        let message_error = ""
        let message_success = ""

        if(action === "add"){
            message_error = "Невдвлося додати товар до списку порівнянь"
            message_success = "Товар було додано до списку порівнянь"
        }else{
            message_error = "Невдвлося прибрати товар зі списку порівнянь"
            message_success = "Товар було прибрано зі списку порівнянь"
        }

        await makeRequest(url, {variant_id: variantId, action: action}, csrfToken, message_error)

        showAlert(message_success)

        console.log('event submitter', event.submitter)

        if(action === "add"){
            form.dataset.actionCompare = "remove"
            event.submitter.classList.add('active', 'bg-light', 'text-dark')
        }else{
            form.dataset.actionCompare = "add"
            event.submitter.classList.remove('active', 'bg-light', 'text-dark')
        }
    })
})
