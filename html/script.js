$(window).on("load", function(){
    var img = new Image();
    img.src = "https://source.unsplash.com/random/3840x2160";
    img.onload = function() {
        $("body").css("background", "linear-gradient(rgba(0,0,0,0.7),rgba(0,0,0,0.7)), url(" + img.src + ")")
        hide()
    }
});

hide = function() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("page").style.display = "block";
}