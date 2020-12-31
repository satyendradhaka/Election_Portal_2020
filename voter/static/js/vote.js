let selected = false;
let selected_id = null;
let ids = [];

function getIds(contList) {
  for (let index = 0; index < contList.length; index++) {
    let element = contList[index];
    ids.push(element);
    console.log(element);
  }
}

$(document).ready(function () {
  $.each(ids, function(index, value) {
    $("#" + ids[index]).hover(
      function () {
        $("#index_" + ids[index]).addClass("hidden");
        $("#text_" + ids[index]).removeClass("hidden");
        console.log(index);
      },
      function () {
        $("#index_" + ids[index]).removeClass("hidden");
        $("#text_" + ids[index]).addClass("hidden");
      }
    );
    $("#" + ids[index]).click(function () {
      $(".nota-effect").css("opacity", 1);
      $(".bg-custom").css("background", "rgba(231, 105, 15, 0.1)");
      $(".text-custom").css("color", "#E7690F");

      if (
        (selected == false) &
        ((selected_id != input_id) | (input_id == null))
      ) {
        $("#" + ids[index]).delay(10).fadeOut(70).fadeIn(70).fadeOut(50).fadeIn(50);
        $("#" + ids[index]).addClass(" bg-gray-200");
        $("#action_box_container_" + ids[index]).addClass(" bg-black text-white");
        $("#action_box_container_" + ids[index]).html("<span>Voted</span>");
        selected = true;
        selected_id = ids[index];
        voteClick(selected_id);
      } else if (ids[index] == selected_id) {
        var cha = String.fromCharCode(65+ids.indexOf(selected_id));
        $("#" + selected_id).removeClass(" bg-gray-200");
        $("#action_box_container_" + selected_id).removeClass(
          " bg-black text-white"
        );
        $("#action_box_container_" + selected_id).html(
          `<span id="text_${selected_id}" class="hidden" >Vote for</span><span id="index_${selected_id}">${cha}</span>`
        );
        selected = false;
        selected_id = null;
        voteClick(selected_id);
      } else {
        var cha = String.fromCharCode(65+ids.indexOf(selected_id));
        $("#" + selected_id).removeClass(" bg-gray-200");
        $("#action_box_container_" + selected_id).removeClass(
          " bg-black text-white"
        );
        $("#action_box_container_" + selected_id).html(
          `<span id="text_${selected_id}" class="hidden" >Vote for</span><span id="index_${selected_id}">${cha}</span>`
        );
        $(this).delay(10).fadeOut(70).fadeIn(70).fadeOut(50).fadeIn(50);
        $(this).addClass(" bg-gray-200");
        $("#action_box_container_" + ids[index]).addClass(" bg-black text-white");
        $("#action_box_container_" + ids[index]).html("<span>Voted</span>");
        selected = true;
        selected_id = ids[index];
        voteClick(selected_id);
      }
      console.log(selected_id);
    });
  });

  $("#nota").click(function () {
    if (selected_id) {
      var cha = String.fromCharCode(65+ids.indexOf(selected_id));
      $("#" + selected_id).removeClass(" bg-gray-200");
      $("#action_box_container_" + selected_id).removeClass(
        " bg-black text-white"
      );
      $("#action_box_container_" + selected_id).html(
        `<span id="text_${selected_id}" class="hidden" >Vote for</span><span id="index_${selected_id}">${cha}</span>`
      );
      selected = false;
      selected_id = null;
    }
    $(".nota-effect").css("opacity", 0.5);
    $(".bg-custom").css("background", "#E7690F");
    $(".text-custom").css("color", "rgb(236, 232, 229)");
  });

  $("#info-btn").hover(
    function () {
      $("#info-txt").toggleClass("hidden");
    },
    function () {
      $("#info-txt").toggleClass("hidden");
    }
  );

  if ($(window).width() <= 560 ) {
    $("#next-btn").insertAfter("#nota");
    $("#nota").attr('class', 'float-left bg-custom text-custom h-14 w-48 text-lg text-center font-bold rounded-sm next-btn');
    $("#nota").css('margin-left', $(window).width() * 2 / 7);
    $("#next-btn").attr('class', 'float-left bg-black text-white h-14 w-48 text-lg text-center font-bold rounded-sm next-btn');
    $("#next-btn").css('margin-left', $(window).width() * 2 / 7);
  }

  $(window).resize(
    function () {
      if ($(window).width() <= 560 ) {
        $("#next-btn").insertAfter("#nota");
        $("#nota").attr('class', 'float-left bg-custom text-custom h-14 w-48 text-lg text-center font-bold rounded-sm next-btn');
        $("#nota").css('margin-left', $(window).width() * 2 / 7);
        $("#next-btn").attr('class', 'float-left bg-black text-white h-14 w-48 text-lg text-center font-bold rounded-sm next-btn');
        $("#next-btn").css('margin-left', $(window).width() * 2 / 7);
      } else {
        $("#nota").insertAfter("#next-btn");
        $("#nota").css('margin-left', 0);
        $("#next-btn").css('margin-left', 0);
        $("#nota").attr('class', 'lg:float-right relative bottom-4 mr-5 bg-custom text-custom h-14 w-48 text-lg text-center font-bold rounded-sm next-btn');
        $("#next-btn").attr('class', 'relative mr-10 sm:mr-auto float-right bg-black text-white h-14 w-48 text-lg text-center font-bold rounded-sm next-btn');
      }
    }
  );
});

let input_id = null;
$(document).ready(function () {
document.onkeyup = function (e) {
  if(e.which-65>=ids.length){
    input_id = null;
  }
  else{
    input_id = ids[e.which-65];
    $("#" + input_id).trigger("click");
    console.log(input_id);
  }
}
});