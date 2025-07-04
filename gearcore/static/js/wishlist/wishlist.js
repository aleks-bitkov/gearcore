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
        const variantId = form.dataset.productVariantId;

        const data = {
            "variantId": variantId
        }

        let response = await makeRequest(url, data, csrfToken)

        const heartButton = form.querySelector('.heart-btn');
        const icon = heartButton?.querySelector('i');

        if (heartButton && icon) {
            heartButton.classList.toggle('active');
        }else{
            console.warn('не знайдено кнопки або іконки додавання до обраних (зміни внесені на сервері)')
        }

        if (heartButton.classList.contains('active')) {
                showAlert('Товар додано до улюблених')
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill');
        } else {
            showAlert('Товар видалено з улюблених')
            icon.classList.remove('bi-heart-fill');
            icon.classList.add('bi-heart');
        }

        form.setAttribute('action', response.action)
    });
});
