$(document).ready(function() {

    var mainMenuBtn = $('#menu_btn')
    var mainMenuBtnIcon = $('#menu_btn_icon')


    // main menu toggle
    mainMenuBtn.click(function() {
        toggleMenu()
    });

    mainMenuBtnIcon.click(function() {
        toggleMenu()
    });
});

function toggleMenu() {
    var mainMenu = $('#mobile_menu')

    mainMenu.toggleClass('h-0 h-auto')
    mainMenu.toggleClass('overflow-hidden overflow-visible')
    console.log("clicked")
};

function toggleNextButton(next_button) {
  next_button.removeAttr("disabled")
  next_button.switchClass("text-gray-500", "text-white")
  next_button.switchClass("bg-gray-600", "bg-charlotte-green")
  next_button.switchClass("cursor-not-allowed", "cursor-default")
};
