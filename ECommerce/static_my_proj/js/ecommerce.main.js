$(document).ready(function () {


	function redirectToNext(nextPath, timeoffset){
		if(nextPath){
			setTimeout(function(){
				window.location.href = nextPath
			}, timeoffset)
		}
	}

	var paymentDiv = $('.payment-div')
	var paymentTemplate = $.templates("#payment-template")
	var paymentBtnTitle = paymentDiv.attr('data-btn-title') || "Add Card"
	var paymentNextUrl = paymentDiv.attr('data-next-url')


	var paymentTemplateContext = {
		nextUrl:paymentNextUrl,
		btnTitle: paymentBtnTitle
	}
	var paymentTemplateHtml = paymentTemplate.render(paymentTemplateContext)
	paymentDiv.html(paymentTemplateHtml)

	var paymentForm = $(".payment-form")
	var payBtn = $("#payBtn")
	var payBtnClasses = payBtn.attr('class')
	var payBtnHtml = payBtn.html()


	if (paymentForm.length > 1){
		console.log("MORE THAN 1")
		alert("Only one payment form is allowed per page")
		paymentForm.css("display", "none")
	}
	else if(paymentForm.length == 1){
		payBtn.on('click' , function(event){
			event.preventDefault();

			var btn = payBtn
			var loadTime=1500
			btn.blur()
			var errorHtml= "<i class='fa fa-warning'></i> An error occured" 
			var errorClasses= "btn btn-danger disabled my-3" 
			var loadHtml= "<i class='fa fa-spin fa-spinner'></i> Loading..." 
			var loadClasses= "btn btn-success disabled my-3" 
			var currentTimeout;

			var nextUrl = paymentForm.attr("data-next-url")
			console.log("SENT CARD INFO")
			var paymentMethodEndpoint = "/billing/payment-method/create/"

			var cardHolder = $('#card-holder-name').val()
			var cardNumber = $('#card-number').val()
			var expiryMonth = $('#expiry-month').val()
			var expiryYear = $('#expiry-year').val()
			var brand = "Visa/MasterCard"
			var country = "Lebanon"
							
			var data = {
				"cardHolder": cardHolder,
				"last4": cardNumber,//cardNumber[cardNumber.length - 4],
				"expY": expiryYear,
				"expM": expiryMonth,
				"brand": brand,
				"country": country,
			}
				currentTimeout = displayBtnStatus(
						loadHtml,
						loadClasses, 
						1500, 
						loadTime)

			$.ajax({
				data: data,
				url: paymentMethodEndpoint,
				method:"POST",
				success: function(data){

					var successMsg = data.message || "Success! You card was added!"
					$(':input','.payment-form')
					.not(':button, :submit, :reset, :hidden')
					.val('')
					.prop('checked', false)
					.prop('selected', false);		
					if(nextUrl){
						successMsg = successMsg + "<br/><br/><i class=\"fa fa-spin fa-spinner\"></i> Redirecting..."
					}
					if ($.alert){
						$.alert(successMsg)
					}else{
						alert(successMsg)
					}

					redirectToNext(nextUrl, 5000)

				},
				error: function(errorData){
					console.log(errorData)
					$.alert({title: "An error occured.", content:"Please try again."})
					currentTimeout = displayBtnStatus(
						errorHtml,
						errorClasses, 
						1500, 
						loadTime)
				}
			})
		})
	}
	function displayBtnStatus(newHtml, newClasses, loadTime, timeout) {

			if (!loadTime)
			{
				loadTime=1500
			}
			
			payBtn.html(newHtml)
			payBtn.removeClass(payBtnClasses)
			payBtn.addClass(newClasses)
			return setTimeout(function(){
				payBtn.html(payBtnHtml)
				payBtn.removeClass(newClasses)
				payBtn.addClass(payBtnClasses)
			}, loadTime)
		}	

})
