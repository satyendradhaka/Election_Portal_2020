$(document).ready(function () {
    ids = $(".hover-effect");
    $.each(ids, function(index, value) {
      $(this).hover(
        function () {
          $(".index_" + $(this).attr('id')).addClass("hidden");
          $(".text_" + $(this).attr('id')).removeClass("hidden");
        },
        function () {
          $(".index_" + $(this).attr('id')).removeClass("hidden");
          $(".text_" + $(this).attr('id')).addClass("hidden");
        }
      );
    });
});