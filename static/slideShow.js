// // courses slideshow

// const slides = document.querySelectorAll('.slide');
// const totalSlides = slides.length;
// let currentSlide = 0;

// function showSlide(slideIndex) {
//   slides.forEach((slide) => slide.classList.remove('active'));
//   slides[slideIndex].classList.add('active');
// }

// function nextSlide() {
//   currentSlide++;
//   if (currentSlide >= totalSlides) {
//     currentSlide = 0;
//   }
//   showSlide(currentSlide);
// }

// function prevSlide() {
//   currentSlide--;
//   if (currentSlide < 0) {
//     currentSlide = totalSlides - 1;
//   }
//   showSlide(currentSlide);
// }

// showSlide(currentSlide);
// setInterval(nextSlide, 5000);
