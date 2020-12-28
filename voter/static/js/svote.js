var selected_ids = new Set();
let ids = [];

function getIds(contList) {
  for (let index = 0; index < contList.length; index++) {
    let element = contList[index];
    ids.push(element);
    console.log(element);
  }
}

$(document).ready(function () {
  console.log("ready!");
  console.log(l);
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
      document.getElementById("hiddenNOTA").checked = false;
//       $(".voter_list").css("opacity", 1);
      $(".nota-effect").css("opacity", 1);
      $(".bg-custom").css("background", "rgb(255, 210, 177)");
      $(".text-custom").css("color", "#E7690F");
      var selected_id = ids[index];
      if(selected_ids.has(ids[index])){
        
        var cha = String.fromCharCode(65+ids.indexOf(selected_id));
        $("#" + selected_id).removeClass(" bg-gray-200");
        $("#action_box_container_" + selected_id).removeClass(
          " bg-black text-white"
        );
        $("#action_box_container_" + selected_id).html(
          `<span id="text_${selected_id}" class="hidden" >Vote for</span><span id="index_${selected_id}">${cha}</span>`
        );
        document.getElementById("hidden"+selected_id).checked = false;
        selected_ids.delete(selected_id);
      }
      else if(selected_ids.size>=l){
        alert("you can select maximum of "+l);
      }
      else{
        console.log(selected_id);
        $("#" + ids[index]).delay(10).fadeOut(70).fadeIn(70).fadeOut(50).fadeIn(50);
        $("#" + ids[index]).addClass(" bg-gray-200");
        $("#action_box_container_" + ids[index]).addClass(" bg-black text-white");
        $("#action_box_container_" + ids[index]).html("<span>Voted</span>");
        selected_ids.add(selected_id);
        document.getElementById("hidden"+selected_id).checked = true;
      }
    });
  });

  $("#notaButton").click(function () {
    console.log("Nota ran!");
    selected_ids.forEach(function (value1, value2, set) {
      var cha = String.fromCharCode(65+ids.indexOf(value2));
      $("#" + value2).removeClass(" bg-gray-200");
      $("#action_box_container_" + value2).removeClass(
        " bg-black text-white"
      );
      $("#action_box_container_" + value2).html(
        `<span id="text_${value2}" class="hidden" >Vote for</span><span id="index_${value2}">${cha}</span>`
      );
      document.getElementById("hidden"+value2).checked = false;
    });
    document.getElementById("hiddenNOTA").checked = true;
    selected_ids.clear();
    // selected_ids.add("NOTA");    
   
    }
    $(".nota-effect").css("opacity", 0.5);
    $(".bg-custom").css("background", "#E7690F");
    $(".text-custom").css("color", "rgb(236, 232, 229)");
  });
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