console.log("Skript partial načítání načten");

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

document.addEventListener('DOMContentLoaded', () => {
  const partialLinks = document.querySelectorAll('a[data-template]');
  console.log('Registrováno odkazů načítajících partial:', partialLinks.length);

  partialLinks.forEach(link => {
    // Vynechání logout odkazu
    if (link.getAttribute('href').includes('/logout/')) {
      return;
    }

    link.addEventListener('click', event => {
      event.preventDefault();
      console.log('Kliknutí na partial odkaz zachyceno.');

      const url = event.currentTarget.getAttribute('href');
      fetch(url)
        .then(response => {
          if (!response.ok) {
            throw new Error('Chyba při načítání šablony');
          }
          return response.text();
        })
        .then(html => {
          const container = document.querySelector('.content-wrapper');
          if (container) {
            container.innerHTML = html;
          } else {
            console.error('Element .content-wrapper nebyl nalezen!');
          }
        })
        .catch(error => {
          console.error('Došlo k chybě:', error);
        });
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // Registrovat event pro načtení partial šablon (např. přihlašovací formulář)
  const partialLinks = document.querySelectorAll('a[data-template]');
  console.log("Registrováno odkazů načítajících partial:", partialLinks.length);

  partialLinks.forEach(link => {
    link.addEventListener("click", event => {
      event.preventDefault();
      const url = event.currentTarget.getAttribute("href");
      fetch(url)
        .then(response => {
          if (!response.ok) {
            throw new Error("Chyba při načítání šablony");
          }
          return response.text();
        })
        .then(html => {
          const container = document.querySelector(".content-wrapper");
          if (container) {
            container.innerHTML = html;
            // Po načtení partial formuláře zaregistrujeme event pro jeho odeslání
            registerLoginForm();
          } else {
            console.error("Element .content-wrapper nebyl nalezen!");
          }
        })
        .catch(error => {
          console.error("Došlo k chybě:", error);
        });
    });
  });

  // Funkce pro registraci event listeneru na přihlašovací formulář
  function registerLoginForm() {
    const loginForm = document.querySelector(".login-form");
    if (loginForm) {
      loginForm.addEventListener("submit", event => {
        event.preventDefault();
        const formData = new FormData(loginForm);
        // Odeslání AJAX požadavku pro přihlášení
        fetch(loginForm.action, {
          method: "POST",
          body: formData,
          headers: {
            "X-Requested-With": "XMLHttpRequest"
          }
        })
          .then(response => response.json())
          .then(result => {
            if (result.success) {
              // Aktualizace odkazu v navigaci – změníme jej na odhlášení
              const authLink = document.getElementById("auth-link");
              if (authLink) {
                authLink.href = "/logout/";
                authLink.textContent = "Odhlásit se";
              }
              // Odstraníme přihlašovací formulář z .content-wrapper
              const container = document.querySelector(".content-wrapper");
              if (container) {
                container.innerHTML = "";
              }
              // Můžeme případně provést další úpravy stránky, např. zobrazit homepage nebo další obsah
              console.log("Přihlášení proběhlo úspěšně!");
            } else {
              // Zobrazení chybové hlášky, např. alert nebo vložení hlášky do stránky
              alert(result.error);
            }
          })
          .catch(error => {
            console.error("Chyba při AJAX přihlášení:", error);
          });
      });
    }
  }
});
document.addEventListener("DOMContentLoaded", () => {
  const authLink = document.getElementById("auth-link");

  if (authLink && authLink.textContent.trim() === "Odhlásit se") {
    authLink.addEventListener("click", event => {
      event.preventDefault(); // zabrání standardní navigaci

      fetch(authLink.href, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        }
      })
        .then(response => response.json())
        .then(result => {
          if (result.success) {
            // Aktualizace odkazu na login, bez práce s nějakým containerem
            authLink.href = "/login_partial/"; // nebo jakákoliv odpovídající URL pro partial formulář
            authLink.textContent = "Přihlásit se";
            console.log("Odhlášení proběhlo úspěšně.");
          } else {
            console.error("Chyba při odhlašování:", result);
          }
        })
        .catch(error => {
          console.error("Chyba při odhlašování:", error);
        });
    });
  }
});