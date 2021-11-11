
$(document).ready(function() {

    // main menu toggle
    $('#menu-button').click(function() {
        if ($('#regions-menu').hasClass('closed')) {
            $('#regions-menu').toggleClass('ease-in ease-out');
            $('#regions-menu').toggleClass('duration-75 duration-100');
            $('#regions-menu').toggleClass('opacity-0 opacity-100');
            $('#regions-menu').toggleClass('scale-0 scale-100');
            $('#regions-menu').toggleClass('h-0 h-auto');
        };

        console.log($('#id_location').val())

    });

    $('.menuItem').click(function() {

        var activity_val = $(this).val()

        $('#menu-text').text($(this).text())

        $("#id_location").val(activity_val);
    });
});