$(document).ready(function(){ //Contact Form
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")

    function displaySubmit(submitBtn, defaultText, doSubmit) {

        if (doSubmit) {
            submitBtn.addClass("disabled");
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")

        } else {
            submitBtn.removeClass("disabled");
            submitBtn.html(contactFormSubmissionTxt)
        }


    }

    contactForm.submit(function(event) {
        event.preventDefault();

        var contactFormBtn = contactForm.find("[type='submit']")
        var contactFormSubmissionTxt = contactFormBtn.text()


        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmit(contactFormBtn, "", true)
        $.ajax({
            url: contactFormEndpoint,
            method: contactFormMethod,
            data: contactFormData,
            success: function(data) {
                contactForm[0].reset()
                $.alert({
                    title: "Success",
                    content: data.message,
                    theme: "modern",
                });
                setTimeout(function() {
                    displaySubmit(contactFormBtn, contactFormSubmissionTxt, false)
                }, 500)
            },
            error: function(errorData) {
                var jsonData = errorData.responseJSON
                console.log(jsonData)
                var msg = ""
                $.each(jsonData, function(key, value) {
                    msg += key + ": " + value[0].message + "<br/>"
                })
                $.alert({
                    title: "Oops",
                    content: msg,
                    theme: "modern",
                });
                setTimeout(function() {
                    displaySubmit(contactFormBtn, contactFormSubmissionTxt, false)
                }, 500)
            },
        })
    })
         //Search
         var searchForm = $('.search-form')
         var searchInput = searchForm.find("[name='q']")
         var typingTimer;
         var typingInterval = 1500;
         var searchBtn = searchForm.find("[type='submit']")
         searchInput.keyup(function(event) {
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, typingInterval)
        })
         searchInput.keydown(function(event) {
            clearTimeout(typingTimer)
        })

         function displaySearching() {
            searchBtn.addClass("disabled");
            searchBtn.html("<i class='fa fa-spin fa-spinner'></i>Searching...")


        }

        function performSearch() {
            displaySearching()
            var query = searchInput.val()
            setTimeout(function() {
                window.location.href = "/search/?q=" + query

            }, 1000)
        }

                //Cart Add Products
                var productForm = $(".form-product-ajax")

                productForm.submit(function(event) {
                    event.preventDefault();
                    event.stopImmediatePropagation();
                    var thisForm = $(this);
                    var actionEndpoint = thisForm.attr("data-endpoint")
                    var httpMethod = thisForm.attr("method")
                    var formData = thisForm.serialize()

                    $.ajax({
                        url: actionEndpoint,
                        method: httpMethod,
                        data: formData,
                        success: function(data) {
                            console.log("Success test");
                            var submitSpan = thisForm.find(".submit-span");
                            if (data.added) {
                                submitSpan.html("<div class=\"container\"><div class=\"row\"><div class=\"col-3\"></div><div class=\"col-8\"><div class=\"input-group qAdder\"><input type=\"button\" value=\"-\" class=\"button-minus\" data-field=\"quantity\" onclick=\"decrementValue(event)\"><input type=\"number\" step=\"1\" max=\"\" value=\"1\" name=\"quantity\" class=\"quantity-field\"><input type=\"button\" value=\"+\" class=\"button-plus\" data-field=\"quantity\" onclick=\"incrementValue(event)\"></div></div></div></div>");
                            } else {
                                submitSpan.html("<button class=\"btn btn-success\" type=\"submit\" >Add To Cart</button>\n");
                            }
                            var navbarCount = $(".navbar-cart-count");
                            navbarCount.text(data.cartItemCount);
                            var currentPath = window.location.href;
                            if (currentPath.indexOf("cart") != -1) {
                                refreshCart()
                            }

                        },
                        error: function(errorData) {
                            $.alert({
                                title: "Oops",
                                content: "An error occurred. ",
                                theme: "modern",
                            });
                            console.log("error");
                            console.log(errorData);
                        }

                    })


                })






                function refreshCart() {
                    var cartTable = $('.cart-table');
                    var cartBody = cartTable.find('.cart-body');
                    var productRow = cartBody.find(".cart-product");
                    var subtotal = cartBody.find(".cart-subtotal");
                    var total = cartBody.find(".cart-total");
                    var refreshCartUrl = "/api/cart/";
                    var refreshMethod = "GET";
                    var data = {};
                    var currentUrl = window.location.href;

                    $.ajax({
                        url: refreshCartUrl,
                        method: refreshMethod,
                        data: data,
                        success: function(data) {
                            var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                            if (data.products.length > 0) {
                                productRow.html(" ");
                                var i = data.products.length
                                $.each(data.products, function(index, value) {
                                    var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                                    newCartItemRemove.css("display", "block");
                                    newCartItemRemove.find(".cart-item-product-id").val(value.id)
                                    cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>");
                                    i--;
                                });
                                subtotal.text(data.subtotal)
                                total.text(data.total)
                                window.location.href = currentUrl;

                            } else {
                                window.location.href = currentUrl;
                            }
                        },
                        error: function(errorData) {
                            $.alert({
                                title: "Oops",
                                content: "An error occurred. ",
                                theme: "modern",
                            });

                            console.log("error");
                            console.log(errorData);

                        }
                    })
                }


        function incrementValue(event) {
            event.preventDefault();
            var fieldName = $(event.target).data('field');
            var parent = $(event.target).closest('div');
            var currentVal = parseInt(parent.find('input[name=' + fieldName + ']').val(), 10);

            if (!isNaN(currentVal)) {
              parent.find('input[name=' + fieldName + ']').val(currentVal + 1);
          } else {
              parent.find('input[name=' + fieldName + ']').val(0);
          }
      }

      function decrementValue(event) {
        event.preventDefault();
        var fieldName = $(event.target).data('field');
        var parent = $(event.target).closest('div');
        var currentVal = parseInt(parent.find('input[name=' + fieldName + ']').val(), 10);

        if (!isNaN(currentVal) && currentVal > 1) {
          parent.find('input[name=' + fieldName + ']').val(currentVal - 1);
      } else {
          parent.find('input[name=' + fieldName + ']').val(0);
      }
  }
               

});
function normalizeSlideHeights() {
    $('.carousel').each(function() {
        var items = $('.carousel-item', this);
        // reset the height
        items.css('min-height', 0);
        // set the height
        var maxHeight = Math.max.apply(null,
            items.map(function() {
                return $(this).outerHeight()
            }).get());
        items.css('min-height', maxHeight + 'px');
    })
}

$(window).on('load resize orientationchange', normalizeSlideHeights);