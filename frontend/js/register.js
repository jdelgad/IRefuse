$(document).ready(function () {
    $('#failedRegistration').hide();
    $('#invalidPassword').hide();
    $('#register').submit(function () {
        event.preventDefault();
        var username = $('#inputUsername').val();
        var password = $('#inputPassword').val();
        var verifyPassword = $('#inputVerifyPassword').val();
        if (password === verifyPassword) {
            $.ajax({
                url: "/register",
                type: "POST",
                data: JSON.stringify({username: username, password: password}),
                dataType: "json",
                contentType: "application/json",
                success: function () {
                    window.location.href = "/";
                },
                error: function () {
                    $('#failedRegistration').show();
                    $('input[type="text"]').css({
                        "border": "1px solid red",
                        "box-shadow": "0 0 3px red"
                    });
                    $('input[type="password"]').css({
                        "border": "1px solid red",
                        "box-shadow": "0 0 3px red"
                    });
                }
            });
        } else {
            $('#invalidPassword').show();
        }
    });
});