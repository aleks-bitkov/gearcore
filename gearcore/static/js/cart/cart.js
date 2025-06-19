class CartManager {
    constructor() {
        this.cartWrapper = null;
        this.init();
    }

    init() {
        document.addEventListener("DOMContentLoaded", () => {
            this.cartWrapper = document.querySelector('#cartWrapper');

            if (!this.cartWrapper) {
                console.warn('Не вдалося знайти cartWrapper');
                return;
            }

            this.bindCartEvents();
        });
    }

    bindCartEvents() {
        // Remove existing listeners to prevent duplicates
        const forms = document.querySelectorAll(".formChangeCount, .fromRemoveCart, .fromAddCart");

        forms.forEach(form => {
            // Clone node to remove all event listeners
            const newForm = form.cloneNode(true);
            form.parentNode.replaceChild(newForm, form);
        });

        // Add new listeners
        const newForms = document.querySelectorAll(".formChangeCount, .fromRemoveCart, .fromAddCart");
        newForms.forEach(form => {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        });
    }

    handleFormSubmit(event) {
        event.preventDefault();

        const form = event.target;
        const csrfToken = this.getCsrfToken(form);

        if (!csrfToken) {
            console.error('CSRF токен не знайдено');
            return;
        }

        const formType = this.getFormType(form);

        switch (formType) {
            case 'changeCount':
                this.handleCartQuantityChange(form, event, csrfToken);
                break;
            case 'remove':
                this.handleCartRemoval(form, csrfToken);
                break;
            case 'add':
                this.handleCartAdd(form, csrfToken);
                break;
            default:
                console.error('Невідомий тип форми');
        }
    }

    getCsrfToken(form) {
        const csrfTokenInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
        return csrfTokenInput ? csrfTokenInput.value : null;
    }

    getFormType(form) {
        if (form.classList.contains('formChangeCount')) return 'changeCount';
        if (form.classList.contains('fromRemoveCart')) return 'remove';
        if (form.classList.contains('fromAddCart')) return 'add';
        return null;
    }

    async makeRequest(url, data, csrfToken) {
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
            this.showError('Відбулася помилка при оновленні кошика');
            throw error;
        }
    }

    handleResponse(data) {
        if (data.status === 200) {
            this.cartWrapper.innerHTML = data.html;
            this.bindCartEvents();
        } else {
            console.error('Помилка сервера:', data.debug_message);
            this.showError('Відбулася невідома помилка, вибачте');
        }
    }

    showError(message) {
        alert(message);
    }

    async handleCartQuantityChange(form, event, csrfToken) {
        const action = event.submitter?.dataset?.action;
        const cartId = form.dataset.cartId;
        const url = form.getAttribute('action');

        if (!action || !cartId || !url) {
            console.error('Відсутні необхідні дані для зміни кількості');
            return;
        }

        try {
            const data = await this.makeRequest(url, {
                action: action,
                id_cart: parseInt(cartId)
            }, csrfToken);

            this.handleResponse(data);
        } catch (error) {
            // Error already handled in makeRequest
        }
    }

    async handleCartRemoval(form, csrfToken) {
        const cartId = form.dataset.cartId;
        const url = form.getAttribute('action');

        if (!cartId || !url) {
            console.error('Відсутні необхідні дані для видалення');
            return;
        }

        try {
            const data = await this.makeRequest(url, {
                id_cart: parseInt(cartId)
            }, csrfToken);

            this.handleResponse(data);
        } catch (error) {
            // Error already handled in makeRequest
        }
    }

    async handleCartAdd(form, csrfToken) {
        const productSlug = form.dataset.productSlug;
        const url = form.getAttribute('action');

        if (!productSlug || !url) {
            console.error('Відсутні необхідні дані для додавання');
            return;
        }

        try {
            const data = await this.makeRequest(url, {
                slug: productSlug
            }, csrfToken);

            this.handleResponse(data);
        } catch (error) {
            // Error already handled in makeRequest
        }
    }
}

// Initialize the cart manager
const cartManager = new CartManager();
// document.addEventListener("DOMContentLoaded", function () {
//     const cartWrapper = document.querySelector('#cartWrapper');
//
//     if (!cartWrapper) {
//         console.warn('Не вдалося знайти cartWrapper');
//         return;
//     }
//
//     function bindCartEvents() {
//         const formsChangeCount = document.querySelectorAll(".formChangeCount, .fromRemoveCart, .fromAddCart");
//
//         formsChangeCount.forEach(form => {
//             form.removeEventListener('submit', handleFormSubmit);
//             form.addEventListener('submit', handleFormSubmit);
//         });
//     }
//
//     function handleFormSubmit(event) {
//         event.preventDefault();
//
//         const form = event.target;
//         const csrfTokenInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
//
//
//         if (!csrfTokenInput) {
//             console.error('CSRF токен не знайдено');
//             return;
//         }
//
//         const csrf_token = csrfTokenInput.value;
//
//
//         if (form.classList.contains('formChangeCount')) {
//             handleCartQuantityChange(form, event, csrf_token)
//         } else if (form.classList.contains('fromRemoveCart')) {
//             handleCartRemoval(form, csrf_token)
//         } else if (form.classList.contains('fromAddCart')){
//             handleCartAdd(form, csrf_token)
//         }else{
//             console.error('Не зрозуміла дія')
//         }
//     }
//
//     function handleCartQuantityChange(form, event, csrf_token) {
//         const action = event.submitter.dataset.action;
//         const cartId = form.dataset.cartId;
//         const url = form.getAttribute('action');
//
//
//         fetch(url, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrf_token,
//             },
//             body: JSON.stringify({
//                 "action": action,
//                 "id_cart": parseInt(cartId)
//             })
//         })
//             .then((response) => {
//                 if (!response.ok) {
//                     throw new Error(`HTTP error! status: ${response.status}`);
//                 }
//                 return response.json();
//             })
//             .then((data) => {
//
//                 if (data.status === 200) {
//                     cartWrapper.innerHTML = data.html;
//                     bindCartEvents();
//                 } else {
//                     console.error('Помилка сервера:', data.debug_message);
//                     alert('Відбулася невідома помилка, вибачте')
//                 }
//             })
//             .catch((error) => {
//                 console.error('Помилка запиту:', error);
//                 alert('Відбулася помилка при оновлені кошика');
//             });
//     }
//
//     function handleCartRemoval(form, csrf_token) {
//         const cartId = form.dataset.cartId;
//         const url = form.getAttribute('action');
//
//
//         fetch(url, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrf_token,
//             },
//             body: JSON.stringify({
//                 "id_cart": parseInt(cartId)
//             })
//         })
//             .then((response) => {
//                 if (!response.ok) {
//                     throw new Error(`HTTP error! status: ${response.status}`);
//                 }
//                 return response.json();
//             })
//             .then((data) => {
//
//                 if (data.status === 200) {
//                     cartWrapper.innerHTML = data.html;
//                     bindCartEvents();
//                 } else {
//                     console.error('Помилка сервера:', data.debug_message);
//                     alert('Відбулася невідома помилка, вибачте')
//                 }
//             })
//             .catch((error) => {
//                 console.error('Помилка запиту:', error);
//                 alert('Відбулася помилка при оновлені кошика');
//             });
//     }
//
//     function handleCartAdd(form, csrf_token) {
//         const productSlug = form.dataset.productSlug;
//         const url = form.getAttribute('action');
//
//
//         fetch(url, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrf_token,
//             },
//             body: JSON.stringify({
//                 "slug": productSlug
//             })
//         })
//             .then((response) => {
//                 if (!response.ok) {
//                     throw new Error(`HTTP error! status: ${response.status}`);
//                 }
//                 return response.json();
//             })
//             .then((data) => {
//
//                 if (data.status === 200) {
//                     cartWrapper.innerHTML = data.html;
//                     bindCartEvents();
//                 } else {
//                     console.error('Помилка сервера:', data.debug_message);
//                     alert('Відбулася невідома помилка, вибачте')
//                 }
//             })
//             .catch((error) => {
//                 console.error('Помилка запиту:', error);
//                 alert('Відбулася помилка при оновлені кошика');
//             });
//     }
//
//     bindCartEvents();
// });
