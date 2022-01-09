$(document).ready(function() {

  var inputObj = $('input[name="chk[]"]');
  var consentBtn = $('#consent_btn');

  inputObj.change(function() {

    var checkedInputObj = $('input[name="chk[]"]:checked');

    console.log(checkedInputObj.length)

    if (checkedInputObj.length == inputObj.length) {
      consentBtn.attr('disabled', false)
    } else {
      if (consentBtn.attr('disabled', false)) {
        consentBtn.attr('disabled', true);
      };
    };
  });

});
