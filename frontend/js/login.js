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
    $('#failedLogin').hide();
    $('#inputUsername').keyup(function () {
        if ($(this).val().length < 3 || $(this).val().length > 12) {
            $('#inputUsername').tooltip('show');
        } else {
            $('#inputUsername').tooltip('hide');
        }
    });
    $('#inputUsername').mouseenter(function () {
        $('[data-toggle="usernameTooltip"]').tooltip('hide');
    });
    $('#inputUsername').mouseleave(function () {
        $('[data-toggle="usernameTooltip"]').tooltip('hide');
    });
    $('#inputPassword').mouseenter(function () {
        $('[data-toggle="passwordTooltip"]').tooltip('hide');
    });
    $('#inputPassword').mouseleave(function () {
        $('[data-toggle="passwordTooltip"]').tooltip('hide');
    });
    $('#inputPassword').keyup(function () {
        if ($(this).val().length >= 6 && $(this).val().length <= 16) {
            $('[data-toggle="passwordTooltip"]').tooltip('hide');
        } else {
            $('[data-toggle="passwordTooltip"]').tooltip('show');
        }
    });
    $('form input').keyup(function () {
        var empty = false;
        $('form input').each(function () {
            if ($(this).val() === '') {
                empty = true;
            }
        });

        if ($('#inputUsername').val().length >= 3 && $('#inputUsername').val().length <= 12) {
            $('#usernamePrompt').attr('class', 'form-group has-success');
        } else {
            $('#usernamePrompt').attr('class', 'form-group has-error');
            empty = true;
        }

        if ($('#inputPassword').val().length >= 6 && $('#inputPassword').val().length <= 16) {
            $('#passwordPrompt').attr('class', 'form-group has-success');
        } else {
            $('#passwordPrompt').attr('class', 'form-group has-error');
            empty = true;
        }

        if (empty) {
            $('#signIn').attr('disabled', 'disabled');
            $('#signIn').attr('class', 'btn btn-lg btn-default btn-block');
        } else {
            $('#signIn').removeAttr('disabled');
            $('#signIn').attr('class', 'btn btn-lg btn-primary btn-block');
        }
    });
    $('#login').submit(function () {
        event.preventDefault();
        var username = $('#inputUsername').val();
        var password = $('#inputPassword').val();
        $.ajax({
            url: "/login",
            type: "POST",
            data: JSON.stringify({username: username, password: password}),
            dataType: "json",
            contentType: "application/json",
            success: function () {
                window.location.href = "/";
            },
            error: function () {
                $('#failedLogin').show();
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
    });
});