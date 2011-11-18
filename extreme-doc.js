$(document).ready(function() {
    addHideShowCheckboxes();
    setNegativeCommentsVisible(false);
    setExtremeCommentsVisible(false);
  });

function setNegativeCommentsVisible(visible) {
  var displayProperty = visible ? "block" : "none";
  $(".cn-line").css("display", displayProperty);
}

function setExtremeCommentsVisible(visible) {
  var displayProperty = visible ? "block" : "none";
  $(".ce-line").css("display", displayProperty);
}

function addHideShowCheckboxes() {
  $("body").prepend("<div><span class = 'showCommentsCheckboxes'>" + 
                    "<span class = 'checkbox'>Show negative comments<input id = 'showNegatives' type = 'checkbox'>" + 
                    "</span>" + 
                    "<span class = 'checkbox'>Show extreme comments<input id = 'showExtremes' type = 'checkbox'>" + 
                    "</span></span></div>");
  $("#showNegatives").change(function(event) {
      setNegativeCommentsVisible(event.target.checked);
    });
  $("#showExtremes").change(function(event) {
      setExtremeCommentsVisible(event.target.checked);
    });
}
