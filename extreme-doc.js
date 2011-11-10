$(document).ready(function() {
    addHideShowCheckbox();
    showOrHideNegativeComments(false);
  });

function showOrHideNegativeComments(show) {
  var colorProperty =  show ? "#b0b0b0" : "#ffffff";
  var visibilityProperty =  show ? "visible" : "hidden";
  var displayProperty = show ? "block" : "none";
  //$(".cn").css("color", colorProperty);
  $(".cn").css("visibility", visibilityProperty);
  $(".cn-line").css("display", displayProperty);
}

function addHideShowCheckbox() {
  $("body").prepend("<div><span class = 'showNegatives'>Show negative comments<input id = 'showNegatives' type = 'checkbox'></span></div>");
  $("#showNegatives").change(function(event) {
      showOrHideNegativeComments(event.target.checked);
    });
}
