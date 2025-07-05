document.addEventListener('DOMContentLoaded', function() {
  const imageCarousels = document.querySelectorAll('[id^="carousel-"]');

  imageCarousels.forEach(function(imageCarousel) {
    const carouselId = imageCarousel.id.split('-')[1];
    const formsCarousel = document.getElementById('forms-carousel-' + carouselId);

    if (formsCarousel) {
      const imageBootstrapCarousel = new bootstrap.Carousel(imageCarousel, {
        interval: false
      });

      const formsBootstrapCarousel = new bootstrap.Carousel(formsCarousel, {
        interval: false
      });

      imageCarousel.addEventListener('slide.bs.carousel', function(event) {
        formsBootstrapCarousel.to(event.to);
      });
    }
  });
});
