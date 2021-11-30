$(document).ready(function() {

    var timeUnit = $('#id_t_unit')
    var minBtn = $('#minBtn')
    var hrsBtn = $('#hrsBtn')

    var form = $('#TimeAndPeopleForm')
    var formSubmitBtn = $('#submit_btn')

    timeUnit.val('hours');

    hrsBtn.click( function() {
        switchBtnState($(this), minBtn);
        timeUnit.val($(this).val());
    });

    minBtn.click( function() {
        switchBtnState($(this), hrsBtn);
        timeUnit.val($(this).val());
    });

    formSubmitBtn.click(function() {
        $('#id_time').val($('#time_input').val())

        $('#id_people').val($('#people_input').val())

        form.submit()

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

