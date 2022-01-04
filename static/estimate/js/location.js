$(document).ready(function() {

    var regionMenu = $('#regions-menu')
    var regionMenuItem = $('.regions_menu_item')
    var regionMenuToggle = $('#regionMenuToggle')

    var form = $('#LocationForm')
    var formSubmitBtn = $('#submit_btn')

    regionMenuItem.click(function() {

        var image = $("#region_image")
        var activity_val = $(this).val()

        image.attr("src", "/static/estimate/resources/image/philippines/PH_"+activity_val+".png")

        $('#region_menu_text').text($(this).text())

        $("#id_location").val(activity_val);

        toggleRegionsMenu()

        toggleNextButton($("#submit_btn"))
    });

    regionMenuToggle.click(function() {
      toggleRegionsMenu()
    });


    formSubmitBtn.click(function() {
        $("#next_link").val("next_page")
        form.submit();
    });


});

function toggleRegionsMenu() {
  var checkBoxes = $("#regions-modal");
  checkBoxes.prop("checked", !checkBoxes.prop("checked"));
};
