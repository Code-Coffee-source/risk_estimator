
$(document).ready(function() {

    $(document).on('input', '#maskSlider', function() {
        $('#sliderValue').html( $(this).val() +"%" );
    });

    $(".maskBtn").click(function() {
        var mask_val = $(this).val();
        $("#id_maskType").val(mask_val);
    });

    $('#submitBtn').click(function() {
        $('#id_maskPercent').val($('#maskSlider').val())

        $('#masksForm').submit()

    });
});


