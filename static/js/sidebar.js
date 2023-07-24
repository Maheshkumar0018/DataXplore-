/* Open the sidebar */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  document.querySelector(".sidebar").classList.add("open-nav");
  document.querySelector(".container").style.marginLeft = "250px";
  document.querySelector(".box1").style.backgroundColor = "transparent";
  /*document.querySelector(".box2").style.marginLeft = "250px";*/
}

/* Close the sidebar */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.querySelector(".sidebar").classList.remove("open-nav");
  document.querySelector(".container").style.marginLeft = "0";
  document.querySelector(".box1").style.backgroundColor = "#F8F8F8";
  document.querySelector(".box1").style.marginLeft = '50px';
  document.querySelector(".box2").style.marginLeft = "0";
}
