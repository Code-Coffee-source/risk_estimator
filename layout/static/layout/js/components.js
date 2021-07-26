$(document).ready(function() {

    console.log('ready')


    // main menu toggle
    $("#mobile_menu_button").click(function() {
        $("#mobile-menu").toggleClass('hidden block')
        $("#mobile_menu_open").toggleClass('hidden block')
        $("#mobile_menu_close").toggleClass('hidden block')
    });

});