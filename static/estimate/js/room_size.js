
$(document).ready(function() {

    var form = $("#RoomSizeForm")
    var formSubmitBtn = $('#submit_btn')

    var lengthField = $('#id_length')
    var widthField = $('#id_width')
    var heightField = $('#id_height')

    var lengthInput = $('#room_length')
    var widthInput = $('#room_width')
    var heightInput = $('#room_height')


    $(":input").on('edit change', function() {
      lengthField.val(lengthInput.val())
      widthField.val(widthInput.val())
      heightField.val(heightInput.val())

      if (lengthField.val() && widthField.val() && heightField.val() ) {
        toggleNextButton($("#submit_btn"))
      };

    });

    formSubmitBtn.click(function() {
        $('#id_length').val($('#room_length').val())
        $('#id_height').val($('#room_height').val())
        $('#id_width').val($('#room_width').val())

        form.submit()

    });
});

function updateFormField(input, formField) {
    formField.val(input.val())
};
