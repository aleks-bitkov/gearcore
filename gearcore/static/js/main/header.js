const profileToggle = document.getElementById('profileToggle');
const profileMenu = document.getElementById('profileMenu');

document.addEventListener('click', function (e) {
    const isClickInside = profileToggle.contains(e.target) || profileMenu.contains(e.target);

    if (isClickInside) {
        profileMenu.style.display = profileMenu.style.display === 'flex' ? 'none' : 'flex';
    } else {
        profileMenu.style.display = 'none';
    }
});


