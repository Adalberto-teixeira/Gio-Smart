(function ($) {
    "use strict";
	
	var $window = $(window); 
	var $body = $('body'); 

	/* Slick Menu JS */
	$('#menu').slicknav({
		label : '',
		prependTo : '.responsive-menu'
	});

	/* Mobile header: visible at the top and whenever the user scrolls upward */
	var mobileHeader = document.querySelector(".header-sticky");
	var lastMobileScroll = window.pageYOffset;
	var mobileScrollTicking = false;

	function updateMobileHeader() {
		if (!mobileHeader) return;
		if (window.innerWidth > 991) {
			mobileHeader.classList.remove("active", "hide");
			lastMobileScroll = window.pageYOffset;
			return;
		}

		var currentScroll = Math.max(window.pageYOffset, 0);
		var menuIsOpen = document.querySelector(".slicknav_btn.slicknav_open");

		if (currentScroll <= 90) {
			mobileHeader.classList.remove("active", "hide");
		} else {
			mobileHeader.classList.add("active");
			if (menuIsOpen || currentScroll < lastMobileScroll - 5) {
				mobileHeader.classList.remove("hide");
			} else if (currentScroll > lastMobileScroll + 5) {
				mobileHeader.classList.add("hide");
			}
		}

		lastMobileScroll = currentScroll;
	}

	window.addEventListener("scroll", function () {
		if (!mobileScrollTicking) {
			window.requestAnimationFrame(function () {
				updateMobileHeader();
				mobileScrollTicking = false;
			});
			mobileScrollTicking = true;
		}
	}, { passive: true });
	window.addEventListener("resize", updateMobileHeader);
	updateMobileHeader();

	/* client slider box JS */
	if ($('.client-slider-box').length) {
		const client_slider_box = new Swiper('.client-slider-box .swiper', {
			slidesPerView : 1,
			speed: 2000,
			spaceBetween: 30,
			loop: true,
			autoplay: {
				delay: 3000,
			},
			breakpoints: {
				768:{
				  	slidesPerView: 2,
				},
				991:{
				  	slidesPerView: 2,
				}
			}
		});
	}

	/* Skill Bar */
	if ($('.skills-progress-bar').length) {
		$('.skills-progress-bar').waypoint(function() {
			$('.skillbar').each(function() {
				$(this).find('.count-bar').animate({
				width:$(this).attr('data-percent')
				},2000);
			});
		},{
			offset: '50%'
		});
	}

	/* Init Counter */
	if ($('.counter').length) {
		$('.counter').counterUp({ delay: 6, time: 3000 });
	}

	if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && $('.text-anime-style-3').length) {
		let	animatedTextElements = document.querySelectorAll('.text-anime-style-3');
		
		 animatedTextElements.forEach((element) => {
			//Reset if needed
			if (element.animation) {
				element.animation.progress(1).kill();
				element.split.revert();
			}

			element.split = new SplitText(element, {
				type: "lines,words,chars",
				linesClass: "split-line",
			});
			gsap.set(element, { perspective: 400 });

			gsap.set(element.split.chars, {
				opacity: 0,
				x: "50",
			});

			element.animation = gsap.to(element.split.chars, {
				scrollTrigger: { trigger: element,	start: "top 90%" },
				x: "0",
				y: "0",
				rotateX: "0",
				opacity: 1,
				duration: 1,
				ease: Back.easeOut,
				stagger: 0.02,
			});
		});		
	}

	/* Parallaxie js */
	var $parallaxie = $('.parallaxie');
	if($parallaxie.length && ($window.width() > 991))
	{
		if ($window.width() > 768) {
			$parallaxie.parallaxie({
				speed: 0.55,
				offset: 0,
			});
		}
	}

	/* Contact form -> WhatsApp or email */
	var $whatsappform = $("#whatsappForm");
	if ($whatsappform.length) {
		var WHATSAPP_NUMBER = "33670424876"; // Gio Smart - 06 70 42 48 76
		var selectedContactMethod = "whatsapp";
		var $contactButtons = $whatsappform.find("[data-contact-method]");

		$whatsappform.find("[data-contact-method]").on("click", function () {
			selectedContactMethod = $(this).data("contact-method");
		});

		$whatsappform.on("submit", async function (event) {
			event.preventDefault();
			var submitter = event.originalEvent && event.originalEvent.submitter;
			var contactMethod = submitter && submitter.dataset.contactMethod
				? submitter.dataset.contactMethod
				: selectedContactMethod;

			var fname = $("#fname").val().trim();
			var lname = $("#lname").val().trim();
			var email = $("#email").val().trim();
			var phone = $("#phone").val().trim();
			var city = $("#city").val().trim();
			var serviceType = $("#serviceType").val();
			var preferredDate = $("#preferredDate").val();
			var message = $("#message").val().trim();
			var website = $("#website").val().trim();

			if (!fname || !lname || !phone || !city || !serviceType || !message) {
				submitMSG(false, "Merci de remplir tous les champs avant d'envoyer.");
				return;
			}
			if (contactMethod === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
				submitMSG(false, "Merci d’indiquer une adresse e-mail valide.");
				$("#email").trigger("focus");
				return;
			}

			var text = "Bonjour Gio Smart, je m'appelle " + fname + " " + lname +
				".\nTéléphone : " + phone +
				(email ? "\nE-mail : " + email : "") +
				"\nVille : " + city +
				"\nService souhaité : " + serviceType +
				(preferredDate ? "\nDate souhaitée : " + preferredDate : "") +
				"\n\nDétails : " + message;

			if (contactMethod === "email") {
				$contactButtons.prop("disabled", true);
				$whatsappform.attr("aria-busy", "true");
				submitMSG(true, "Envoi de votre demande en cours...");
				try {
					var response = await fetch("/api/contact", {
						method: "POST",
						headers: { "Content-Type": "application/json", "Accept": "application/json" },
						body: JSON.stringify({
							fname: fname,
							lname: lname,
							email: email,
							phone: phone,
							city: city,
							serviceType: serviceType,
							preferredDate: preferredDate,
							message: message,
							website: website
						})
					});
					var result = await response.json().catch(function () { return {}; });
					if (!response.ok) {
						throw new Error(result.error || "L’envoi a échoué.");
					}
					$whatsappform[0].reset();
					selectedContactMethod = "whatsapp";
					submitMSG(true, "Merci ! Votre demande a bien été envoyée par e-mail.");
				} catch (error) {
					submitMSG(false, error.message || "L’envoi a échoué. Utilisez WhatsApp ou réessayez plus tard.");
				} finally {
					$contactButtons.prop("disabled", false);
					$whatsappform.removeAttr("aria-busy");
				}
				return;
			}

			var url = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text);
			var whatsappWindow = window.open(url, "_blank");
			if (whatsappWindow) {
				whatsappWindow.opener = null;
			} else {
				window.location.href = url;
			}
			submitMSG(true, "Redirection vers WhatsApp...");
		});
	}
	/* Contact form end */

	function submitMSG(valid, msg){
		if(valid){
			var msgClasses = "h4 text-success";
		} else {
			var msgClasses = "h4 text-danger";
		}
		$("#msgSubmit").removeClass().addClass(msgClasses).text(msg);
	}

	/* Animated Wow Js */
	if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
		new WOW().init();
	} else {
		$('.wow').css('visibility', 'visible');
	}

	/* Popup Video */
	if ($('.popup-video').length) {
		$('.popup-video').magnificPopup({
			type: 'iframe',
			mainClass: 'mfp-fade',
			removalDelay: 160,
			preloader: false,
			fixedContentPos: true
		});
	}
	
})(jQuery);

/* Progressive Web App registration */
if ("serviceWorker" in navigator) {
	window.addEventListener("load", function () {
		navigator.serviceWorker.register("/sw.js").catch(function () {
			// The website remains fully functional when service workers are unavailable.
		});
	});
}
