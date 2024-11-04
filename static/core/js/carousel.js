document.addEventListener("DOMContentLoaded", () => {
    const carouselConfig = {
        autoplayInterval: 5000
    };

    const prevButton = document.querySelector('.carousel-nav-button.prev');
    const nextButton = document.querySelector('.carousel-nav-button.next');
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;


    let dotsContainer = document.querySelector('.carousel-dots');
    if (!dotsContainer) {
        dotsContainer = document.createElement('div');
        dotsContainer.className = 'carousel-dots';
        document.querySelector('.carousel-container').appendChild(dotsContainer);
    }


    const createDots = () => {
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('button');
            dot.className = `dot ${i === 0 ? 'active' : ''}`;
            dot.dataset.slide = i;
            dotsContainer.appendChild(dot);
        }
    };

    let currentSlide = 0;
    let touchStartX = 0;
    let autoplayInterval;
    const carousel = document.querySelector("#carousel");

    const showSlide = (index) => {

        currentSlide = (index + totalSlides) % totalSlides;


        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === currentSlide);
            slide.style.transform = `translateX(${(i - currentSlide) * 100}%)`;
        });

        document.querySelectorAll('.dot').forEach((dot, i) => {
            dot.classList.toggle('active', i === currentSlide);
        });
    };

    const showSwipeIndicator = () => {
        const indicator = document.querySelector('.swipe-indicator');
        if (indicator) {
            indicator.classList.add('active');
            setTimeout(() => indicator.classList.remove('active'), 1000);
        }
    };

    const handleSwipe = (touchEndX) => {
        const swipeDistance = touchEndX - touchStartX;
        if (Math.abs(swipeDistance) > 50) {
            if (swipeDistance > 0) {
                showSlide(currentSlide - 1);
            } else {
                showSlide(currentSlide + 1);
            }
            if (window.innerWidth < 1024) {
                showSwipeIndicator();
            }
        }
    };


    createDots();

    prevButton.addEventListener('click', () => {
        showSlide(currentSlide - 1);
        clearInterval(autoplayInterval);
        autoplayInterval = setInterval(() => showSlide(currentSlide + 1), carouselConfig.autoplayInterval);
    });

    nextButton.addEventListener('click', () => {
        showSlide(currentSlide + 1);
        clearInterval(autoplayInterval);
        autoplayInterval = setInterval(() => showSlide(currentSlide + 1), carouselConfig.autoplayInterval);
    });


    carousel.addEventListener("touchstart", (e) => {
        touchStartX = e.touches[0].clientX;
        clearInterval(autoplayInterval);
    }, { passive: true });

    carousel.addEventListener("touchend", (e) => {
        handleSwipe(e.changedTouches[0].clientX);
        autoplayInterval = setInterval(() => showSlide(currentSlide + 1), carouselConfig.autoplayInterval);
    });

    document.querySelectorAll('.dot').forEach(dot => {
        dot.addEventListener('click', () => {
            const slideIndex = parseInt(dot.dataset.slide);
            showSlide(slideIndex);
            clearInterval(autoplayInterval);
            autoplayInterval = setInterval(() => showSlide(currentSlide + 1), carouselConfig.autoplayInterval);
        });
    });

    autoplayInterval = setInterval(() => showSlide(currentSlide + 1), carouselConfig.autoplayInterval);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            showSlide(currentSlide - 1);
        } else if (e.key === 'ArrowRight') {
            showSlide(currentSlide + 1);
        }
    });
});