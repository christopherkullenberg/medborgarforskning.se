$(document).ready(function(){
    if ($(".accordion__item__header").length > 0) {
      var active = "active";
      $(".accordion__item__header").click(function () {
        $(this).toggleClass(active);
        console.log($(this).next("div")[0]);
        $(this).next("div").toggle(200);

      });
    }
});
