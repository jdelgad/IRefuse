$(document).ready(function () {
    $('#failedLogin').hide();
    $('#login').submit(function () {
        event.preventDefault();
        var email = $('#inputEmail').val();
        var password = $('#inputPassword').val();
        $.ajax({
            url: "/login",
            type: "POST",
            data: JSON.stringify({email: email, password: password}),
            dataType: "json",
            contentType: "application/json",
            success: function () {
                window.location.href = "/game";
            },
            error: function () {
                $('#failedLogin').show();
                $('input[type="email"]').css({
                    "border": "1px solid red",
                    "box-shadow": "0 0 3px red"
                });
                $('input[type="password"]').css({
                    "border": "1px solid red",
                    "box-shadow": "0 0 3px red"
                });
            }
        });
    });
});