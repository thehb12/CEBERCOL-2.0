function redirigir2() {
    // window.location.href = "intesolicitud.html";
      var modelo = document.getElementById("model")
      modelo.style.display="block"

  }

var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
// asdsa
// var splide = new Splide("#main-slider", {
//   width: 600,
//   height: 300,
//   pagination: false,
//   cover: true
// });

// var thumbnails = document.getElementsByClassName("thumbnail");
// var current;

// for (var i = 0; i < thumbnails.length; i++) {
//   initThumbnail(thumbnails[i], i);
// }

// function initThumbnail(thumbnail, index) {
//   thumbnail.addEventListener("click", function () {
//     splide.go(index);
//   });
// }

// splide.on("mounted move", function () {
//   var thumbnail = thumbnails[splide.index];

//   if (thumbnail) {
//     if (current) {
//       current.classList.remove("is-active");
//     }

//     thumbnail.classList.add("is-active");
//     current = thumbnail;
//   }
// });

// splide.mount();

