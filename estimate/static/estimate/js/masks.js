
$(document).ready(function() {

    var form = $('#MasksForm')
    var formSubmitBtn = $('#submit_btn')

    $(document).on('input', '#maskSlider', function() {
        $('#sliderValue').html( $(this).val() +"%" );
    });

    $(".maskBtn").click(function() {
        var mask_val = $(this).val();
        $("#id_maskType").val(mask_val);
    });

    formSubmitBtn .click(function() {
        $('#id_maskPercent').val($('#maskSlider').val())

        form.submit()

    });
});


