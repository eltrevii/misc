$(window).on("load", function(){
    imgArr = []
    imgArr[0] = ""
    //$("body").css("background-color", "black")
    $('#video')[0].addEventListener('ended',myHandler,false);
    function myHandler(e) {
        $("#intro").fadeOut()
    }
        imgArr[1] = new Image();
        imgArr[2] = new Image();
        imgArr[3] = new Image();
        
        imgArr[1].src = "https://source.unsplash.com/random/7680x4320?img=1";
        imgArr[1].onload = function() {
            console.log("1 ready")
            imgArr[2].src = "https://source.unsplash.com/random/7680x4320?img=2";
            imgArr[2].onload = function() {
                console.log("2 ready")
                imgArr[3].src = "https://source.unsplash.com/random/7680x4320?img=3";
                imgArr[3].onload = function() {
                    console.log("3 ready")
                    img_sel(1)
                    hide()
                }
            }
        }
    var matches = document.querySelectorAll('.radio1');
    for (match in matches) {
        matches[match].onchange = function() {
        img_sel(this.value)
       }
    }
});

hide = function() {
    $("#page")[0].style.display = "block";
    $("#loader-parent").fadeOut(750);
}

img_sel = function(img) {
    $("body").css("background", "linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.5)), url(" + imgArr[img].src + ")")
}