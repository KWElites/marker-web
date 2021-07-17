var gallery = undefined

function setupGallery() {
    gallery = $('.gallery-slider').slick({
      slidesToShow: 4,
      slidesToScroll: 3,
      dots: true,
      arrows: false,
      responsive: [
        {
          breakpoint: 992,
          settings: {
            slidesToShow: 4,
            slidesToScroll: 4,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 767,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 575,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2
          }
        }
      ]
    });
}

function openPage(no) {
    if(no == 1) {
      if(gallery == undefined) {
        setupGallery();
      } else {
        $('.gallery-slider').slick('unslick');
        setupGallery();
      }    
    }

    $('.cd-hero-slider li').hide();
    $('.cd-hero-slider li[data-page-no="' + no + '"]')
      .fadeIn();
}

$(window).on('load', function() {
    $('body').addClass('loaded');
    openPage(1);
});



