// 'I Refuse' web application
// Copyright (C) 2017  Jacob Delgado
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
// """
$(document).ready(function () {
    $('#failedRegistration').hide();

    $('form input').keyup(function () {
        var empty = false;
        $('form input').each(function () {
            if ($(this).val() === '') {
                empty = true;
            }
        });

        // $('#inputUsername').mouseenter(function () {
        //     $('[data-toggle="usernameTooltip"]').tooltip('hide');
        // });
        // $('#inputUsername').mouseleave(function () {
        //     $('[data-toggle="usernameTooltip"]').tooltip('hide');
        // });
        // $('#inputPassword').mouseenter(function () {
        //     $('[data-toggle="passwordTooltip"]').tooltip('hide');
        // });
        // $('#inputPassword').mouseleave(function () {
        //     $('[data-toggle="passwordTooltip"]').tooltip('hide');
        // });
        // $('#inputVerifyPassword').mouseenter(function () {
        //     $('[data-toggle="inputVerifyPassword"]').tooltip('hide');
        // });
        // $('#inputVerifyPassword').mouseleave(function () {
        //     $('[data-toggle="inputVerifyPassword"]').tooltip('hide');
        // });
        // if ($('#inputUsername').val().length >= 3 && $('#inputUsername').val().length <= 12) {
        //     $('[data-toggle="usernameTooltip"]').tooltip('hide');
        // } else {
        //     $('[data-toggle="usernameTooltip"]').tooltip('show');
        //     empty = true;
        // }
        //
        // if (!empty) {
        //     if ($('#inputPassword').val().length >= 6 && $('#inputPassword').val().length <= 16) {
        //         $('[data-toggle="passwordTooltip"]').tooltip('hide');
        //     } else {
        //         $('[data-toggle="passwordTooltip"]').tooltip('show');
        //         empty = true;
        //     }
        // }
        //
        // if (!empty) {
        //     var password = $('#inputPassword').val();
        //     var verifyPassword = $('#inputVerifyPassword').val();
        //     if (password !== verifyPassword) {
        //         $('[data-toggle="passwordMatchTooltip"]').tooltip('show');
        //         empty = true;
        //     } else {
        //         $('[data-toggle="passwordMatchTooltip"]').tooltip('hide');
        //     }
        // }

        if (empty) {
            $('#registerBtn').attr('disabled', 'disabled');
        } else {
            $('#registerBtn').removeAttr('disabled');
        }
    });

    $('#register').submit(function () {
            event.preventDefault();
            var username = $('#inputUsername').val();
            var password = $('#inputPassword').val();
            var verifyPassword = $('#inputVerifyPassword').val();
            if (username.length >= 3 && username.length <= 12) {
                $('#failedRegistration').hide();

            } else {
                $('#failedRegistration').hide();
                $('#failedRegistrationText').html("Username must be between" +
                    "3 and 16 characters long");
                $('#failedRegistration').show();
                return
            }
            if (password === verifyPassword) {
                if (password.length >= 6 && password.length <= 16) {
                    $.ajax({
                        url: "/register",
                        type: "POST",
                        data: JSON.stringify({
                            username: username,
                            password: password
                        }),
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
                    $('#failedRegistration').hide();
                    $('#failedRegistrationText').html("Password must be" +
                        " between 6 and 16 characters");
                    $('#failedRegistration').show();
                }
            } else {
                $('#failedRegistration').hide();
                $('#failedRegistrationText').html("Passwords do not match");
                $('#failedRegistration').show();
            }
        }
    );
});