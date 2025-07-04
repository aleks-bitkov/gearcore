const profileToggle = document.getElementById('profileToggle');
const profileMenu = document.getElementById('profileMenu');

document.addEventListener('click', function (e) {
    if (profileToggle.contains(e.target)) {
        // Переключаем меню только при клике на toggle
        profileMenu.style.display = profileMenu.style.display === 'flex' ? 'none' : 'flex';
    } else if (!profileMenu.contains(e.target)) {
        // Скрываем меню только если клик вне его области
        profileMenu.style.display = 'none';
    }
});

const cartToggle = document.getElementById('cartToggle');
const cartWrapper = document.getElementById('cartWrapper');

document.addEventListener('click', function (e) {

    if (!cartToggle || !cartWrapper){
        console.warn('не знайдено елементи кошика')
        return;
    }

    if (cartToggle.contains(e.target)) {
        cartWrapper.style.display = cartWrapper.style.display === 'block' ? 'none' : 'block';
    } else if (!cartWrapper.contains(e.target)) {
        cartWrapper.style.display = 'none';
    }
});
