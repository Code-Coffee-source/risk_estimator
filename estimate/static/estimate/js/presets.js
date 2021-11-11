
$(document).ready(function() {

    $(".presetBtn").click(function() {
        var preset_val = $(this).val();
        $("#id_activity").val(preset_val);
    });

    $("#submitBtn").click(function() {
        $("#ActivityForm").submit();
    });

});