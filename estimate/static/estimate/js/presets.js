
$(document).ready(function() {

    console.log('ready')
    var form = $('#ActivityForm')
    var formSubmitBtn = $('#submit_btn')

    $(".presetBtn").click(function() {
        var preset_val = $(this).val();
        $("#id_activity").val(preset_val);
    });

    formSubmitBtn.click(function() {
        form.submit();
        console.log("print")
    });

});