window.addEventListener("orientationchange", fixBackgroundLayout, false);

window.addEventListener("load", fixBackgroundLayout, false)

function fixBackgroundLayout() {
    $('#background').css({'height': '100%'});
    var h = $('#background').height();
    $('#background').css({'height': h + 'px'});
}