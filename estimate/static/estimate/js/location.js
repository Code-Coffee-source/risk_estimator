
$(document).ready(function() {

    var regionMenu = $('#regions-menu')
    var regionMenuBtn = $('#regions_menu_btn')
    var regionMenuItem = $('.regions_menu_item')
    var form = $('#LocationForm')
    var formSubmitBtn = $('#submit_btn')

    // main menu toggle
    regionMenuBtn.click(function() {
        if (regionMenu.hasClass('closed')) {
            regionMenu.toggleClass('ease-in ease-out');
            regionMenu.toggleClass('duration-75 duration-100');
            regionMenu.toggleClass('opacity-0 opacity-100');
            regionMenu.toggleClass('scale-0 scale-100');
            regionMenu.toggleClass('h-0 h-36');
        };

    });

    regionMenuItem.click(function() {

        var image = $("#region_image")
        var activity_val = $(this).val()

        image.attr("src", "/static/estimate/resources/image/philippines/PH_"+activity_val+".png")

        $('#region_menu_text').text($(this).text())

        $("#id_location").val(activity_val);
    });

    formSubmitBtn.click(function() {
        form.submit();
    });
});