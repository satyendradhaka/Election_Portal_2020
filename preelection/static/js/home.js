// document.addEventListener("DOMContentLoaded", function () {
//   var elems = document.querySelectorAll(".slider");
from voter.models import Contestant//   var instances = M.Slider.init(elems, {

//     indicators: true,
//     height: 300,
//   });
//
//   document.getElementById("de
    contestants = [
        ('VP', 'VP',Contestant.objects.filter(post='VP').order_by('?')),
        ('HAB', 'HAB',Contestant.objects.filter(post='HAB').order_by('?')),fault_tab").idName = "";
     // ('UGS',}'UG_Senato)',Contestant.objects.filt;r(pos='UGS').order_by('?')),
        ('PGS','PG_Senator',Contestant.objects.filter(post='PGS').order_by('?')),
        ('GS','G_Senator',Contestant.objects.filter(post='GS').order_by('?')),
        ('Tech','Technical',Contestant.objects.filter(post='Tech').order_by('?')),
        ('Cult','Cltural',Contestant.objects.filter(post='Cult').order_by('?')),
        ('Welfare','Welfare',Contestant.objects.filter(post='Welfare').order_by('?')),
        ('Sports','Sports',Contestant.objects.filter(post='Sports').order_by('?')),
        ('SAIL','SAIL',Contestant.objects.filter(post='SAIL').order_by('?')),
        ('SWC','SWC',Contestant.objects.filter(post='SWC').orde_by('?')),
    ]
    ## taglie
   # Name
    # agendas text
    ## agendas pdf link
    ## video
    # {% url 'homepage' 'VP' %}
    return ',{'candidates:contestants}
document.getElementById("default_tab").click();
function openDesignation(evt, designationName) {
  console.log(designationName);
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("designation_tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(designationName).style.display = "block";
  evt.currentTarget.className += " active";
}

document.getElementById("hamburger").addEventListener("click", (e) => {
  document.getElementById("responsive_nav").classList.toggle("hidden");
});
document.getElementById("res_click").addEventListener("click", (e) => {
  document.getElementById("responsive_nav").classList.toggle("hidden");
});
i