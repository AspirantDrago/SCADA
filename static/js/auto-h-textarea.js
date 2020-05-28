function textarea_resize(event, line_height, min_line_count)
{
  var min_line_height = min_line_count * line_height;
  var obj = document.getElementById('text_area');
  var div = document.getElementById('text_area_div');
  div.innerHTML = obj.value;
  var obj_height = div.offsetHeight;
  if (event && event.keyCode == 13)
    obj_height += line_height;
  else if (obj_height < min_line_height)
    obj_height = min_line_height;
  obj.style.height = obj_height + 'px';
}

textarea_resize(null, 21, 5);
