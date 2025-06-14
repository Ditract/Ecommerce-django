document.addEventListener("DOMContentLoaded", () => {
  const botones = document.querySelectorAll(".ver-mas-btn");

  botones.forEach((btn) => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".producto-card");
      const descripcion = card.querySelector(".descripcion");

      if (descripcion.classList.contains("expandida")) {
        descripcion.classList.remove("expandida");
        btn.textContent = "Ver más";
      } else {
        descripcion.classList.add("expandida");
        btn.textContent = "Ver menos";
      }
    });
  });
});


