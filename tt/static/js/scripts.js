$(function () {
    var default_error_message = 'Server error, please try again later.';

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });

    $(document).ajaxError(function (event, request, settings) {
        var message = null;
        if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
            message = request.responseJSON.message;
        } else if (request.responseText) {
            var IS_JSON = true;
            try {
                var data = JSON.parse(request.responseText);
            }
            catch (err) {
                IS_JSON = false;
            }
            if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
                message = JSON.parse(request.responseText).message;
            } else {
                message = default_error_message;
            }
        } else {
            message = default_error_message;
        }
        toast(message, 'error');
    });

    var flash = null;

    function toast(body, category) {
        clearTimeout(flash);
        var $toast = $('#toast');
        if (category === 'error') {
            $toast.css('background-color', 'red')
        } else {
            $toast.css('background-color', '#333')
        }
        $toast.text(body).fadeIn();
        flash = setTimeout(function () {
            $toast.fadeOut();
        }, 3000);
    }

    var hover_timer = null;

    function show_profile_popover(e) {
        var $el = $(e.target);

        hover_timer = setTimeout(function () {
            hover_timer = null;
            $.ajax({
                type: 'GET',
                url: $el.data('href'),
                success: function (data) {
                    $el.popover({
                        html: true,
                        content: data,
                        trigger: 'manual',
                        animation: false
                    });
                    $el.popover('show');
                    $('.popover').on('mouseleave', function () {
                        setTimeout(function () {
                            $el.popover('hide');
                        }, 200);
                    });
                }
            });
        }, 500);
    }

    function hide_profile_popover(e) {
        var $el = $(e.target);

        if (hover_timer) {
            clearTimeout(hover_timer);
            hover_timer = null;
        } else {
            setTimeout(function () {
                if (!$('.popover:hover').length) {
                    $el.popover('hide');
                }
            }, 200);
        }
    }

    $('.profile-popover').hover(show_profile_popover.bind(this), hide_profile_popover.bind(this));


});
