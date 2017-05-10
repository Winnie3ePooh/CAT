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
});
