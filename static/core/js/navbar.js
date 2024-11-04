// Определяем все нужные элементы один раз при загрузке
const mobileMenu = document.querySelector('.mobile-menu');
const hamburger = document.querySelector('.hamburger');
const overlay = document.querySelector('.overlay');
const body = document.body;

// Обработчик для мобильного меню
function toggleMenu() {
    if (!mobileMenu || !hamburger || !overlay) return;

    mobileMenu.classList.toggle('-translate-x-full');
    hamburger.classList.toggle('active');
    overlay.classList.toggle('hidden');
    body.style.overflow = !mobileMenu.classList.contains('-translate-x-full') ? 'hidden' : '';
}

// Обработчик для профиля
function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    const menuContent = menu.querySelector('div:last-child');

    if (menu.classList.contains('hidden')) {
        // Открываем меню
        menu.classList.remove('hidden');
        // Даем время для анимации появления
        setTimeout(() => {
            menuContent.classList.remove('translate-x-full');
        }, 10);
        body.style.overflow = 'hidden';
    } else {
        // Закрываем меню
        menuContent.classList.add('translate-x-full');
        // Ждем окончания анимации перед скрытием
        setTimeout(() => {
            menu.classList.add('hidden');
            body.style.overflow = '';
        }, 300);
    }
}

// Обработчик для жанров
function toggleGenres() {
    const submenu = document.querySelector('.genres-submenu');
    const arrow = document.querySelector('.genre-arrow');

    if (!submenu || !arrow) return;

    submenu.classList.toggle('hidden');
    arrow.style.transition = 'transform 0.3s ease';
    arrow.style.transform = submenu.classList.contains('hidden') ? '' : 'rotate(180deg)';
}

// Закрытие меню при нажатии ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const menu = document.getElementById('profileMenu');
        if (!menu.classList.contains('hidden')) {
            toggleProfileMenu();
        }

        if (!mobileMenu.classList.contains('-translate-x-full')) {
            toggleMenu();
        }
    }
});

// Закрытие меню при клике вне его
document.addEventListener('click', (e) => {
    // Для мобильного меню
    if (mobileMenu && !mobileMenu.classList.contains('-translate-x-full')) {
        const isClickInsideMenu = mobileMenu.contains(e.target);
        const isHamburgerClick = hamburger.contains(e.target);

        if (!isClickInsideMenu && !isHamburgerClick) {
            toggleMenu();
        }
    }

    // Для меню профиля
    const profileMenu = document.getElementById('profileMenu');
    if (!profileMenu.classList.contains('hidden')) {
        const menuContent = profileMenu.querySelector('div:last-child');
        const isClickInsideProfileMenu = menuContent.contains(e.target);
        const isProfileButtonClick = e.target.closest('[onclick="toggleProfileMenu()"]');

        if (!isClickInsideProfileMenu && !isProfileButtonClick) {
            toggleProfileMenu();
        }
    }
});

// Закрытие меню при изменении размера экрана
window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) {
        if (!mobileMenu.classList.contains('-translate-x-full')) {
            toggleMenu();
        }

        const profileMenu = document.getElementById('profileMenu');
        if (!profileMenu.classList.contains('hidden')) {
            toggleProfileMenu();
        }
    }
});

// Добавляем CSS для анимаций
const style = document.createElement('style');
style.textContent = `
    .mobile-menu {
        transition: transform 0.3s ease-in-out;
    }

    .genre-arrow {
        transition: transform 0.3s ease-in-out;
    }

    .overlay {
        transition: opacity 0.3s ease-in-out;
    }
`;
document.head.appendChild(style);