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