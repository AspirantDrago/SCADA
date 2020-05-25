window.addEventListener("orientationchange", fixBackgroundLayout, false);

window.addEventListener("load", fixBackgroundLayout, false)

function fixBackgroundLayout() {
    $('#background').css({'height': '100%'});
    var h = $('#background').height();
    $('#background').css({'height': h + 'px'});
}

$('body').on('click', '.control-eye', function(){
    if ($(this).hasClass('view')) {
        $(this).removeClass('view');
        $(this).parent().children('input').attr('type', 'text');
    } else {
        $(this).addClass('view');
        $(this).parent().children('input').attr('type', 'password');
    }
	return false;
});