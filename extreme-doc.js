$(document).ready(function() {
    // alert("Hello world from extreme-doc.js");
    $(".cn").addClass("cnHide");
    addHideShowCheckbox();
  });

function addHideShowCheckbox() {
  $("body").prepend("<div>Show negative comments<input id = 'showNegatives' type = 'checkbox'></div>");
  $("#showNegatives").change(function(event) {
      if (event.target.checked) {
        $(".cn").addClass("cnShow");
        $(".cn").removeClass("cnHide");
      }
      else {
        $(".cn").addClass("cnHide");
        $(".cn").removeClass("cnShow");
      }
    });
        
}
