let img = document.getElementById("heatmap_img");
let p = document.getElementById("get_picture");

if (p.textContent == "") {
  img.classList.add("d-none");
} else {
  img.classList.remove("d-none");
}