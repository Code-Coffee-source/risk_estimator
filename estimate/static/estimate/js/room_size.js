
$(document).ready(function() {

     var form = $("#RoomSizeForm")
    var formSubmitBtn = $('#submit_btn')

    formSubmitBtn.click(function() {
        $('#id_length').val($('#room_length').val())
        $('#id_height').val($('#room_height').val())
        $('#id_width').val($('#room_width').val())

        form.submit()

    });
});


