function toggleSideBar() {
    var sideBar = document.getElementById("sidebar");
    var content = document.querySelector(".content");


    if (sideBar.style.width !== "48px") {
        sideBar.style.width = "48px";
        content.style.marginLeft = "48px";
    } else {
        sideBar.style.width = "280px";
        content.style.marginLeft = "280px";
    }

}



$(document).ready(function() {
    $(".app_sidebar_button.active").on("click", function() {
        var sideBar = $(".app_sidebar");
        var content = $(".app_content");

        if (sideBar.width() !== 48) {
            sideBar.css("width", "48px");
            content.css("margin-left", "48px");
        } else {
            sideBar.css("width", "280px");
            content.css("margin-left", "280px");
        }
    });
});
