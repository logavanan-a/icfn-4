$(document).ready(function(){
	$('.menuhamburger a').on('click', function(event){
		if($(this).hasClass('active')){
			$(this).removeClass('active');
			$('.main_menutoggle').removeClass('toggleshow');
			$('.submenu_mainmenu').removeClass('toggleshow_sub');
			$('.main_menutoggle .main_navlinktop').removeClass('active');
		} else {
			$(this).addClass('active');
			$('.main_menutoggle').addClass('toggleshow');
		}
	});
	$('.main_menutoggle .main_navlinktop').on('click', function(event){
		if($(this).hasClass('active')){
			$(this).removeClass('active');
			$(this).next().removeClass('toggleshow_sub');
		} else {
			$(this).addClass('active');
			$(this).next().addClass('toggleshow_sub');
		}
	});
	$('.searchbottombybtm a').on('click', function(event){
		event.stopPropagation();
		$('.searchbottomsearchbar').removeClass('active_slide');
		$(this).next().toggleClass('active_slide');
	});
	$(document).on('click',function(){
		$('.searchbottomsearchbar').removeClass('active_slide');
	});
	$('.searchbottomsearchbar').on('click', function(event){
		event.stopPropagation();
	});
	$('#sliderlogos').owlCarousel({
	    loop:true,
	    margin:10,
	    nav:false,
	    items:1,
	    dots:true,
	    autoplay:true,
	});
	$('#associatedwith').owlCarousel({
	    loop:true,
	    margin:20,
	    nav:false,
	    autoplay:true,
	    responsive:{
            0:{
                items:1
            },
            1180:{
                items:4
            }
        },
	    dots:true,
	});
	$('#mainslidercarousel').owlCarousel({
	    loop:true,
	    margin:10,
	    nav:false,
	    items:1,
	    dots:true,
	    animateOut: 'fadeOut',
	    autoplay:true,
	    mouseDrag:false,
	    touchDrag:false,
	    pullDrag:false,
	    freeDrag:false,
	});
	if($(window).width() < 1180){
		// $('.menuhamburger a').removeClass('active');
		// $('.main_menutoggle').removeClass('toggleshow')
		$('.menuhamburger a').click();
	}
	$('.fixed_icon .sharebutton').on('click', function(){
		$(this).next().toggle();
	});
	var currentActivestatus = true;
	$(window).scroll(function() {
		var Scrolcounter = $('.carouselimg').height()/3;
		if ($(window).scrollTop() > Scrolcounter){
			if(currentActivestatus == true){
				$('.numberCounter').each(function () {
					$(this).prop('Counter',0).animate({
						Counter: $(this).text()
					},{
						duration: 4000,
						easing: 'swing',
						step: function (now) {
							$(this).text(Math.ceil(now));
						}
					});
				});
				currentActivestatus = false;
			}
		}
	});
});


function customfilesel(obj){
	var current_text = $(obj).val();
	$(obj).prev().prev().val(current_text);
}
$('.askque_box').on('click', function(){
	$(this).next().stop().slideToggle();
	$('.askque_box .link_img ').removeClass('img_plus').addClass('img_minus');
	$(this).find('.link_img ').removeClass('img_minus').addClass('img_plus');
});
$('.text_part').on('click', function(){
	$(this).next().stop().slideToggle();
});
$('.pusername').on('click', function(){
	$(this).next().stop().slideToggle();
	$(this).find('img').toggleClass('toggle');
});