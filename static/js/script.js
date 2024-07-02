'use strict';


/**
 * Add event listener on multiple elements
 */

const addEventOnElements = function (elements, eventType, callback) {
    for (let i = 0, len = elements.length; i < len; i++) {
        elements[i].addEventListener(eventType, callback);
    }
}


/**
 * MOBILE NAVBAR TOGGLER
 */

const navbar = document.querySelector("[data-navbar]");
const navTogglers = document.querySelectorAll("[data-nav-toggler]");

const toggleNav = () => {
    navbar.classList.toggle("active");
    document.body.classList.toggle("nav-active");
}

addEventOnElements(navTogglers, "click", toggleNav);


/**
 * HEADER ANIMATION
 * When scrolled donw to 100px header will be active
 */

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", () => {
    if (window.scrollY > 100) {
        header.classList.add("active");
        backTopBtn.classList.add("active");
    } else {
        header.classList.remove("active");
        backTopBtn.classList.remove("active");
    }
});


/**
 * SLIDER
 */

const slider = document.querySelector("[data-slider]");
const sliderContainer = document.querySelector("[data-slider-container]");
const sliderPrevBtn = document.querySelector("[data-slider-prev]");
const sliderNextBtn = document.querySelector("[data-slider-next]");

let totalSliderVisibleItems = Number(getComputedStyle(slider).getPropertyValue("--slider-items"));
let totalSlidableItems = sliderContainer.childElementCount - totalSliderVisibleItems;

let currentSlidePos = 0;

const moveSliderItem = function () {
    sliderContainer.style.transform = `translateX(-${sliderContainer.children[currentSlidePos].offsetLeft}px)`;
}

/**
 * NEXT SLIDE
 */

const slideNext = function () {
    const slideEnd = currentSlidePos >= totalSlidableItems;

    if (slideEnd) {
        currentSlidePos = 0;
    } else {
        currentSlidePos++;
    }

    moveSliderItem();
}

sliderNextBtn.addEventListener("click", slideNext);

/**
 * PREVIOUS SLIDE
 */

const slidePrev = function () {
    if (currentSlidePos <= 0) {
        currentSlidePos = totalSlidableItems;
    } else {
        currentSlidePos--;
    }

    moveSliderItem();
}

sliderPrevBtn.addEventListener("click", slidePrev);

/**
 * RESPONSIVE
 */
window.addEventListener("resize", function () {
    totalSliderVisibleItems = Number(getComputedStyle(slider).getPropertyValue("--slider-items"));
    totalSlidableItems = sliderContainer.childElementCount - totalSliderVisibleItems;

    moveSliderItem();
});

// Messages html -------------------


// // -------------------------------------- Modal Window ------------------------------------------------
// // Отримати модальні вікна
// var loginModal = document.getElementById("loginModal");
// var registerModal = document.getElementById("registerModal");
//
// // Отримати кнопки, які відкривають модальні вікна
// var loginBtn = document.getElementById("loginBtn");
// var registerBtn = document.getElementById("registerBtn");
//
// // Отримати елементи <span>, які закривають модальні вікна
// var closeButtons = document.getElementsByClassName("close");
//
// // Коли користувач натискає на кнопку Вхід, відкрити відповідне модальне вікно
// loginBtn.onclick = function () {
//     loginModal.style.display = "block";
// }
//
// // Коли користувач натискає на кнопку Реєстрація, відкрити відповідне модальне вікно
// registerBtn.onclick = function () {
//     registerModal.style.display = "block";
// }
//
// // Коли користувач натискає на <span> (x), закрити відповідне модальне вікно
// for (var i = 0; i < closeButtons.length; i++) {
//     closeButtons[i].onclick = function () {
//         loginModal.style.display = "none";
//         registerModal.style.display = "none";
//     }
// }
//
// // Коли користувач натискає в будь-якому місці за межами модального вікна, закрити його
// window.onclick = function (event) {
//     if (event.target == loginModal) {
//         loginModal.style.display = "none";
//     }
//     if (event.target == registerModal) {
//         registerModal.style.display = "none";
//     }
// }
//
// // Carousel ------------------------------
// let currentSlide = 0;
// const slides = document.querySelectorAll('.carousel-slide');
// const totalSlides = slides.length;

// function nextSlide() {
//     currentSlide = (currentSlide + 1) % totalSlides;
//     const newSlidePosition = -currentSlide * 100; // This moves the slide
//     document.getElementById('carouselSlides').style.transform = `translateX(${newSlidePosition}%)`;
// }
//
// // Change slide every 5 seconds
// setInterval(nextSlide, 5000);


// -------------Message ---------------------------------
window.onload = function () {
    setTimeout(function () {
        var messagesContainer = document.getElementById('messages-container');
        if (messagesContainer) {
            messagesContainer.style.opacity = '0'; // Початок зникнення
            setTimeout(function () {
                messagesContainer.style.display = 'none'; // Повністю прибрати елемент після зникнення
            }, 500); // Час для завершення анімації
        }
    }, 2000); // Час показу повідомлення перед початком зникнення
}






