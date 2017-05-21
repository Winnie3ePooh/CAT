$('div.alert-success').hide();
$(document).ready(function() {
  $('.delete').click(function(){
    var catid;
    catid = $(this).attr('data-testid');
    $.ajax({
        url: '/tests/delete/',
        data: {
          'test_id': catid
        },
        dataType: 'json',
        success: function (data) {
          if (data.rdy) {
            $('div#'+catid).get(0).remove();
            $('div.alert-success').fadeIn(1000).show(0);
            $('div.alert-success').delay(2000).fadeOut(1000).hide(0);
            return( false );
          }
        }
      });
  });

  $('.edit').click(function(){
    var catid;
    catid = $(this).attr('data-questtid');
    $.ajax({
        url: '/tests/questionEdit/',
        type: "GET",
        data: {
          'questionID': catid
        },
        success: function (data) {
          $('.modal-body').html(data);
        }
      });
  });

  $('.getStats').click(function(){
  	var pathname = window.location.pathname.split("/");
    var catid = $('.select2-selection__rendered').text();
    var cUrl = ($(this).attr('data-type') == 'group') ? 'groupsTestDetails':'usersTestDetails';
    alert(cUrl);
    $.ajax({
        url: '/tests/'+cUrl+'/'+pathname[pathname.length-2]+'/',
        type: "POST",
        data: {
          'group': catid
        },
        success: function (data) {
          $('#groupRender').html(data);
        },
        error: function (data){
        	alert('NOPE');
        }
      });
  });

  $('.add').click(function(){
    $.ajax({
        url: '/tests/questionCreate/',
        type: "GET",
        success: function (data) {
          $('.modal-body').html(data);
        }
      });
  });
  $('.remove-it').click(function(){
    var catid;
    catid = $(this).attr('data-questtid');
    alert('catid');
    $.ajax({
        url: '/tests/questionDelete/',
        type: "GET",
        data: {
          'questionID': catid
        },
        success: function (data) {
          if (data.rdy) {
            $('div#'+catid).get(0).remove();
            $('div.alert-success').fadeIn(1000).show(0);
            $('div.alert-success').delay(2000).fadeOut(1000).hide(0);
            return( false );
          }
        }
      });
  });

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

  $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip();
  });
});
