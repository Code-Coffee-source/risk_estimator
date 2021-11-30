
$(document).ready(function() {

    var form = $('#ActivityLevelForm')
    var formSubmitBtn = $('#submit_btn')

    formSubmitBtn.click(function() {
        var levels = {
            1: "Resting",
            2: "Standing",
            3: "Light Exercise",
            4: "Heavy Exercise"
        }

        $('#id_activity_level').val(levels[$('#maskSlider').val()])

        form.submit()

    });
});

function showVal(val) {

    var image = $('#activity_image')

    var title = $('#activity_level_title')

    var desc = $('#activity_level_desc')

    var levels = {
        1 : {
                "title": "Resting",
                "description": "An activity that requires you to stay in a relaxed position. Examples: Sitting down and sleeping.",
                "image": "Resting.png",
                "code": "R"
            },

        2 : {
                "title": "Mostly Standing",
                "description": "An activity that requires you to mostly stay in an idle position. Examples: Talking while teaching a class, and waiting for a bus stop.",
                "image": "Standing.png",
                "code": "S"
            },

        3 : {
                "title": "Light Exercise",
                "description": "An activity that requires little or no effort to exert. Examples would be walking, strolling down the street, and grocery shopping",
                "image": "Light_Exercise.png",
                "code": "LE"
            },

        4 : {
                "title": "Heavy Exercise",
                "description": "An activity that requires maximum effort to exert. Examples would be running, exercising in a gym, and swimming.",
                "image": "Heavy_Exercise.png",
                "code": "HE"
            },
    }

    title.text(levels[val]["title"])
    desc.text(levels[val]["description"])
    image.attr("src", "/static/estimate/resources/image/activity_level/"+levels[val]["image"])


};



