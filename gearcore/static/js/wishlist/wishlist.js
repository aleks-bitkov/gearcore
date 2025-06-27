const heartsForm = document.querySelectorAll('.heart-form');

async function makeRequest(url, data, csrfToken) {
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

heartsForm?.forEach(form=>{
    form.addEventListener('submit', async function (event){
        event.preventDefault();

        const form = event.target;
        const csrfToken = getCsrfToken(form);

        if (!csrfToken) {
            console.error('CSRF токен не знайдено');
            return;
        }

        const url = form.getAttribute('action');
        const productSlug = form.dataset.productSlug;

        let result = await makeRequest(url, {"productSlug": productSlug}, csrfToken)

        console.log('result', result)
    });
});
