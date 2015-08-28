// JQuery functions to hide form errors on keypress

$(document).ready(function () {
    $('input')
        .filter('#id_text')
        .on('keypress', function () {
        $('.has-error').hide();
    });
    
    $('input')
        .filter('#id_text')
        .on('click', function () {
        $('.has-error').hide();
    });
});
