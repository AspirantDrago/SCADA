window.addEventListener("orientationchange", fixBackgroundLayout, false);

window.addEventListener("load", fixBackgroundLayout, false)

function fixBackgroundLayout() {
    var h = $('#background').height();
    $('#background').css({'height': h + 'px'});
}