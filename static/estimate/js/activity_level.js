
$(document).ready(function() {

    var form = $('#ActivityLevelForm')
    var formSubmitBtn = $('#submit_btn')

    var slideBtn = $('.slideSelectBtn')

    var advBtn = $('.adv_btn')

    slideBtn.click(function() {
      
      toggleNextButton($("#submit_btn"))

      var selectedId = $(this).attr('id')
      var selectedNum = selectedId.match(/\d+/g)
      var selectedAlert = $('#slideSelectAlert'+selectedNum)

      selectedAlert.removeClass("hidden")

      slideBtn.each(function()
      {
        var thisID = $(this).attr('id')
        var thisAlert = $('#slideSelectAlert'+thisID.match(/\d+/g))

        if (thisID != selectedId)
        {
          thisAlert.addClass("hidden")
        };

      });

      $('#id_activity_level').val( $(this).val())
    });

    advBtn.click(function() {

      $(this).addClass("btn-active");
      $(this).siblings().removeClass("btn-active")

      $('#id_activity_sub_level').val($(this).val())

    });

    formSubmitBtn.click(function() {

        form.submit()

    });
});
