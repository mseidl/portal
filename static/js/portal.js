$(function() {¬
  $('.portal-summary-row').click(function() {
    var id = $(this).data('res-id');
    $('.portal-detail-row[data-res-id=' + id + ']').slideToggle();
  });
})
