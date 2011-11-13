$(document).ready(function() {
    addHideShowCheckbox();
    setNegativeCommentsVisible(false);
  });

function setNegativeCommentsVisible(visible) {
  var displayProperty = visible ? "block" : "none";
  $(".cn-line").css("display", displayProperty);
}

function addHideShowCheckbox() {
  $("body").prepend("<div><span class = 'showNegatives'>Show negative comments<input id = 'showNegatives' type = 'checkbox'></span></div>");
  $("#showNegatives").change(function(event) {
      setNegativeCommentsVisible(event.target.checked);
    });
}
