function toggleMenu() {
    const mobileMenu = document.querySelector('.mobile-menu');
    const hamburger = document.querySelector('.hamburger');
    const overlay = document.querySelector('.overlay');

    if (mobileMenu && hamburger && overlay) {
        mobileMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
        overlay.classList.toggle('hidden');

        // Prevent body scroll when menu is open
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    }
}

function toggleCategories() {
    const submenu = document.querySelector('.categories-submenu');
    const arrow = document.querySelector('.category-arrow');

    if (submenu && arrow) { // Проверка наличия элементов
        submenu.classList.toggle('hidden');
        arrow.style.transform = submenu.classList.contains('hidden') ? '' : 'rotate(90deg)';
    }
}
