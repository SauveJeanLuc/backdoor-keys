 
 /*------------------------------*/
/*	Page loader
/*------------------------------*/


 $(window).load(function() {
	$(".loader-item").delay(500).fadeOut();
	$("#pageloader").delay(1000).fadeOut("slow");
	});


 /*------------------------------*/
/*	Slider
/*------------------------------*/

	setTimeout(function(){
		$('.home .flexslider').height($(window).height()).flexslider({
			slideshowSpeed: 6000,
			after : function(slider){
				$('.flexslider .big, .flexslider .middle, .flexslider .small').css('opacity',0);
				var next = $('.flex-active-slide', slider);
				sliderAnimate(next);
			}
		});
		$(window).resize(function(){
			$('.home .flexslider, .home .flexslider .slides img').height($(window).height());
		})
		sliderAnimate($('.flex-active-slide'));
		function sliderAnimate(next){
			if(next.hasClass('first')){
				var time = -200;
				$('.big', next).each(function(){
					var thiz = $(this);
					time += 200;
					setTimeout(function(){							
						thiz.addClass('flipInX animated').css('opacity','1');
						thiz.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
							thiz.removeClass('flipInX animated');
						});
					}, time);
				});
				setTimeout(function(){
					$('.middle', next).addClass('bounceIn animated').css('opacity','1');
					$('.middle', next).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
						$('.middle', next).removeClass('bounceIn animated');
					});
					$('.small', next).addClass('fadeIn animated').css('opacity','1');
					$('.small', next).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
						$('.small', next).removeClass('fadeIn animated');
					});
				}, 400)
			}else if(next.hasClass('secondary')){

				$('.big', next).addClass('bounceInDown animated');
				$('.big', next).css('opacity','1');
				$('.big', next).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
					$('.big', next).removeClass('bounceInDown animated');
				});

				setTimeout(function(){
					$('.middle', next).addClass('bounceInRight animated').css('opacity','1');
					$('.middle', next).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
						$('.middle', next).removeClass('bounceInRight animated');
					});
					$('.small', next).addClass('bounceInLeft animated').css('opacity','1');
					$('.small', next).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
						$('.small', next).removeClass('bounceInLeft animated');
					});
				}, 400)
			}else if(next.hasClass('third')){
				var time = -200;
				$('.big', next).each(function(){
					var thiz = $(this);
					time += 200;
					setTimeout(function(){							
						thiz.addClass('fadeInDown animated').css('opacity','1');
						thiz.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
							thiz.removeClass('fadeInDown animated');
						});
					}, time);
				});
				setTimeout(function(){
					$('.middle', next).addClass('fadeInRight animated').css('opacity','1');
					$('.middle', next).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
						$('.middle', next).removeClass('fadeInRight animated');
					});
					$('.small', next).addClass('fadeInLeft animated').css('opacity','1');
					$('.small', next).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
						$('.small', next).removeClass('fadeInLeft animated');
					});
					
				}, 400)
			}
		}

		$('.flex-next').addClass('fa fa-angle-right').text('');
		$('.flex-prev').addClass('fa fa-angle-left').text('');

		$('.home li > img').each(function(){
			$(this).css('background-image', 'url(' + $(this).attr('src') + ')')
				   .attr('src', '../images/1x1-blue.png')
				   .height($(window).height());
		});
	},0)

