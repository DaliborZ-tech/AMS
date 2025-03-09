console.log("Skript partial načítání načten");

document.addEventListener("DOMContentLoaded", () => {
  // Při načtení DOM získáme potřebné elementy
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("toggle-btn");

  // Ošetření kliknutí na tlačítko pro přepínání sidebaru
  toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    toggleBtn.classList.toggle("active");

    // Zavření všech submenu a reset ikonek
    sidebar.querySelectorAll(".dropdown-btn").forEach(btn => {
      const subMenu = btn.nextElementSibling;
      const arrowIcon = btn.querySelector(".bi-arrow-bar-down");

      if (subMenu) {
        subMenu.classList.remove("show");
      }
      if (arrowIcon) {
        arrowIcon.classList.remove("rotated");
      }
    });
  });

  // Použijeme delegaci události na obsluhu kliknutí pro dropdown tlačítka v sidebaru
  sidebar.addEventListener("click", event => {
    // Hledáme kliknutí přímo na .dropdown-btn nebo u vnořeného elementu
    const btn = event.target.closest(".dropdown-btn");
    if (!btn) return;

    // Zavřeme ostatní submenu
    sidebar.querySelectorAll(".dropdown-btn").forEach(otherBtn => {
      if (otherBtn !== btn) {
        const otherSubMenu = otherBtn.nextElementSibling;
        const otherArrow = otherBtn.querySelector(".bi-arrow-bar-down");

        if (otherSubMenu) {
          otherSubMenu.classList.remove("show");
        }
        if (otherArrow) {
          otherArrow.classList.remove("rotated");
        }
      }
    });

    // Přepnutí aktuálního submenu a otáčení ikony
    const subMenu = btn.nextElementSibling;
    const arrowIcon = btn.querySelector(".bi-arrow-bar-down");

    if (subMenu) {
      subMenu.classList.toggle("show");
    }
    if (arrowIcon) {
      arrowIcon.classList.toggle("rotated");
    }

    // Pokud je sidebar zavřený, při kliknutí jej otevřeme
    if (sidebar.classList.contains("close")) {
      sidebar.classList.remove("close");
      toggleBtn.classList.remove("active");
    }
  });

  // Obsluha odkazů pro načítání partial šablon přes AJAX (sidebar)
  const partialLinks = document.querySelectorAll("a.anchoresidebar");
  console.log("Registrováno odkazů načítajících partial:", partialLinks.length);

  partialLinks.forEach(link => {
    // Vynecháme odkaz pro odhlášení
    if (link.getAttribute("href").includes("/logout/")) return;

    link.addEventListener("click", event => {
      event.preventDefault();
      console.log("Kliknutí na partial odkaz zachyceno.");

      const url = link.getAttribute("href");
      fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
      })
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
            // Po načtení partial šablony zaregistrujeme eventy znovu
            registerAjaxLinks();
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

  // Funkce pro registraci AJAX odkazů (např. paginátor)
  function registerAjaxLinks() {
    const ajaxLinks = document.querySelectorAll("a.ajax-link");
    console.log("Registrováno AJAX odkazů:", ajaxLinks.length);
    ajaxLinks.forEach(link => {
      link.addEventListener("click", event => {
        event.preventDefault();
        console.log("Kliknutí na AJAX link zachyceno.");
        const url = link.getAttribute("href");
        fetch(url, {
          headers: { "X-Requested-With": "XMLHttpRequest" }
        })
          .then(response => {
            if (!response.ok) {
              throw new Error("Chyba při načítání partial šablony");
            }
            return response.text();
          })
          .then(html => {
            const container = document.querySelector(".content-wrapper");
            if (container) {
              container.innerHTML = html;
              // Znovu zaregistrujeme AJAX odkazy a eventy formulářů
              registerAjaxLinks();
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
  }

  // Funkce pro registraci posluchače události formuláře pro přihlášení
  function registerLoginForm() {
    const loginForm = document.querySelector(".login-form");
    if (loginForm) {
      loginForm.addEventListener("submit", event => {
        event.preventDefault();
        const formData = new FormData(loginForm);

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
              // Aktualizujeme odkaz nebo provedeme další potřebné akce
              console.log("Přihlášení bylo úspěšné.");
            } else {
              console.error("Přihlášení selhalo.");
            }
          })
          .catch(error => {
            console.error("Došlo k chybě při odesílání formuláře:", error);
          });
      });
    }
  }

  // Po načtení DOM zaregistrujeme AJAX odkazy (paginátor) a formulář
  registerAjaxLinks();
  registerLoginForm();
});