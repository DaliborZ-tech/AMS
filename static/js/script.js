
document.addEventListener("DOMContentLoaded", () => {
  // Zúžení sidebaru + otočení toggle tlačítka
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("toggle-btn");

  toggleBtn.addEventListener("click", () => {
    // Změna stavu sidebaru
    sidebar.classList.toggle("close");
    toggleBtn.classList.toggle("active");

    // Zavřít všechna submenu a vrátit ikony do výchozího stavu
    const allDropdownBtns = document.querySelectorAll(".dropdown-btn");
    allDropdownBtns.forEach((btn) => {
      const subMenu = btn.nextElementSibling;
      const arrowIcon = btn.querySelector(".bi-arrow-bar-down");

      if (subMenu && subMenu.classList.contains("show")) {
        subMenu.classList.remove("show");
      }
      if (arrowIcon && arrowIcon.classList.contains("rotated")) {
        arrowIcon.classList.remove("rotated");
      }
    });
  });

  // Rozbalování submenu a otáčení šipky – pouze jedno otevřené současně
  const dropdownButtons = document.querySelectorAll(".dropdown-btn");

  dropdownButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const subMenu = btn.nextElementSibling;
      const arrowIcon = btn.querySelector(".bi-arrow-bar-down");

      // Zavřít ostatní rozbalená submenu
      document.querySelectorAll(".dropdown-btn").forEach((otherBtn) => {
        if (otherBtn !== btn) {
          const otherSubMenu = otherBtn.nextElementSibling;
          const otherArrow = otherBtn.querySelector(".bi-arrow-bar-down");

          if (otherSubMenu && otherSubMenu.classList.contains("show")) {
            otherSubMenu.classList.remove("show");
          }
          if (otherArrow && otherArrow.classList.contains("rotated")) {
            otherArrow.classList.remove("rotated");
          }
        }
      });

      // Otevřít / zavřít kliknuté submenu
      if (subMenu) {
        subMenu.classList.toggle("show");
      }
      if (arrowIcon) {
        arrowIcon.classList.toggle("rotated");
      }
    });
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("toggle-btn");

  document.querySelectorAll(".dropdown-btn").forEach((btn) => {
    const arrowIcon = btn.querySelector(".bi-arrow-bar-down");
    btn.addEventListener("click", () => {
      if (btn.nextElementSibling) {
        btn.nextElementSibling.classList.toggle("show");
      }
      if (arrowIcon) {
        arrowIcon.classList.toggle("rotated");
      }
      if (sidebar.classList.contains("close")) {
        sidebar.classList.toggle("close");
        toggleBtn.classList.toggle("active");
      }
    });
  });
});
