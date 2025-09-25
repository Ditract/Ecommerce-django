document.addEventListener("DOMContentLoaded", () => {
  /* -------------------------
     Ver más / Ver menos integrado (mejorado, accesible)
  --------------------------*/
  const botones = document.querySelectorAll(".ver-mas-btn");
  botones.forEach((btn) => {
    btn.addEventListener("click", () => {
      const descId = btn.getAttribute("aria-controls");
      const descripcion = document.getElementById(descId);
      if (!descripcion) return;

      // Toggle clase expandida en la descripción
      descripcion.classList.toggle("expandida");

      // Toggle aria-expanded en el botón
      const isExpanded = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!isExpanded));

      // Actualizar texto label
      const label = btn.querySelector(".label");
      if (label) {
        label.textContent = !isExpanded ? "Ver menos" : "Ver más";
      }
    });
  });
});