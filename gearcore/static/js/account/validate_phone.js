const phoneInput = document.getElementById('phone')

phoneInput.value = '+38';

phoneInput?.addEventListener('input', function (e) {
    let x = e.target.value.replace(/\D/g, '')
        .match(/(\d{0,2})(\d{0,3})(\d{0,3})(\d{0,2})(\d{0,2})(\d{0,3})/);

    if (!x[1]) {
        e.target.value = '+38';
        return;
    }

    if (!x[2]) {
        e.target.value = `+38`;
        return;
    }

    e.target.value = `+38 (${x[2]}`
        + (x[3] ? `) ${x[3]}` : '')
        + (x[4] ? ` ${x[4]}` : '')
        + (x[5] ? ` ${x[5]}` : '');
});
