
document.getElementById("menuButton").addEventListener("click", function() {
  var menu = document.getElementById("sideMenu");
  if (menu.style.width === "0px") {
    menu.style.width = "250px";
  } else {
    menu.style.width = "0px";
  }
});
