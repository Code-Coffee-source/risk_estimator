
$(document).ready(function() {

    var form = $("#VentilationForm")
    var formSubmitBtn = $('#submit_btn')

    $(".presetBtn").click(function() {
        var preset_val = $(this).val();
        $("#id_ventilation").val(preset_val);
    });

    formSubmitBtn.click(function() {
        form.submit();
    });

});