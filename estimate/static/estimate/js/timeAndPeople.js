
$(document).ready(function() {

    $('#id_t_unit').val('hours');

    $('#hrsBtn').click( function() {
        switchBtnState($(this), $('#minBtn'));
        $('#id_t_unit').val($(this).val());
    });

    $('#minBtn').click( function() {
        switchBtnState($(this), $('#hrsBtn'));
        $('#id_t_unit').val($(this).val());
    });

    $('#submitBtn').click(function() {
        $('#id_time').val($('#time_input').val())

        $('#id_people').val($('#people_input').val())

        $('#timeAndPeopleForm').submit()

    });
});

function switchBtnState(btn1, btn2) {

    if (btn1.hasClass('inactive')) {
            activateBtn(btn1);
            deactivateBtn(btn2);
        };

    function activateBtn(inactiveBtn) {
        inactiveBtn.switchClass('inactive', 'active')
        inactiveBtn.switchClass('bg-transparent', 'bg-dirty-white')
        inactiveBtn.switchClass('text-gray-400', 'text-charlotte-blue')
    };

    function deactivateBtn(activeBtn) {
        activeBtn.switchClass('active', 'inactive')
        activeBtn.switchClass('bg-dirty-white', 'bg-transparent')
        activeBtn.switchClass('text-charlotte-blue','text-gray-400')
    };

};

