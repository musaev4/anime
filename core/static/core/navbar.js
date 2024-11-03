// Определяем все нужные элементы один раз при загрузке
const mobileMenu = document.querySelector('.mobile-menu');
const hamburger = document.querySelector('.hamburger');
const overlay = document.querySelector('.overlay');
const body = document.body;

// Обработчик для мобильного меню

function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    const menuContent = menu.querySelector('.absolute.right-0');

    if (menu.classList.contains('hidden')) {
        // Открываем меню
        menu.classList.remove('hidden');
        // Даем время для анимации появления
        setTimeout(() => {
            menuContent.classList.remove('translate-x-full');
        }, 10);
    } else {
        // Закрываем меню
        menuContent.classList.add('translate-x-full');
        // Ждем окончания анимации перед скрытием
        setTimeout(() => {
            menu.classList.add('hidden');
        }, 300);
    }
}

// Закрытие меню при нажатии ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const menu = document.getElementById('profileMenu');
        if (!menu.classList.contains('hidden')) {
            toggleProfileMenu();
        }
    }
});
function toggleMenu() {
    if (!mobileMenu || !hamburger || !overlay) return;

    // Переключаем классы для анимации
    mobileMenu.classList.toggle('active');
    mobileMenu.classList.toggle('-translate-x-full');
    hamburger.classList.toggle('active');
    overlay.classList.toggle('hidden');

    // Управление скроллом body
    body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';

    // Добавляем плавную анимацию гамбургера
    const lines = hamburger.querySelectorAll('.hamburger-line');
    lines.forEach(line => line.classList.toggle('active'));
}

// Обработчик для жанров
function toggleGenres() {
    const submenu = document.querySelector('.genres-submenu');
    const arrow = document.querySelector('.genre-arrow');

    if (!submenu || !arrow) return;

    submenu.classList.toggle('hidden');

    // Плавная анимация стрелки
    arrow.style.transition = 'transform 0.3s ease';
    arrow.style.transform = submenu.classList.contains('hidden') ? '' : 'rotate(90deg)';
}

// Закрытие меню при клике вне его
document.addEventListener('click', (e) => {
    if (mobileMenu && mobileMenu.classList.contains('active')) {
        const isClickInsideMenu = mobileMenu.contains(e.target);
        const isHamburgerClick = hamburger.contains(e.target);

        if (!isClickInsideMenu && !isHamburgerClick) {
            toggleMenu();
        }
    }
});

// Закрытие меню при изменении размера экрана
window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024 && mobileMenu.classList.contains('active')) {
        toggleMenu();
    }
});

// Добавляем CSS для анимаций
const style = document.createElement('style');
style.textContent = `
    .mobile-menu {
        transition: transform 0.3s ease-in-out;
    }

    .hamburger-line {
        transition: all 0.3s ease-in-out;
    }

    .hamburger.active .line1 {
        transform: rotate(45deg) translate(5px, 5px);
    }

    .hamburger.active .line2 {
        opacity: 0;
    }

    .hamburger.active .line3 {
        transform: rotate(-45deg) translate(5px, -5px);
    }

    .overlay {
        transition: opacity 0.3s ease-in-out;
    }

    .category-arrow {
        transition: transform 0.3s ease-in-out;
    }
`;
document.head.appendChild(style);