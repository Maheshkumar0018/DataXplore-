/* Open the sidebar */
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.querySelector(".sidebar").classList.add("open-nav");
  }
  
  /* Close the sidebar */
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.querySelector(".sidebar").classList.remove("open-nav");
  }
  