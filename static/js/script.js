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
    console.log("Kliknutí na a.anchoresidebar zachyceno.");

    // Odstraníme aktivní třídu ze všech li elementů v celé oblasti sidebaru
    document.querySelectorAll("#sidebar li.active").forEach(li => li.classList.remove("active"));

    // Získáme rodičovský li element pro kliknutý odkaz
    let currentLi = link.closest("li");
    if (!currentLi) {
      currentLi = link.parentElement.closest("li");
    }
    if (currentLi) {
      // Přidáme aktivní třídu přímo na rodičovský li
      currentLi.classList.add("active");

      // Rekurzivně procházíme všechny rodičovské li elementy a přidáme jim aktivní třídu
      let parentLi = currentLi.parentElement.closest("li");
      while (parentLi) {
        parentLi.classList.add("active");
        parentLi = parentLi.parentElement.closest("li");
      }
    }

    // Načteme obsah přes AJAX
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
          // Tohle zajistí znovuinicializaci HTMX na vloženém HTML obsahu
          if(typeof htmx !== 'undefined') {
              htmx.process(container);
              console.log("HTMX inicializován pro nový obsah");
          } else {
              console.warn("HTMX objekt není načten, překontrolujte načtení knihovny HTMX");
          }

          // Přeregistrace eventů po načtení partial šablony
          registerAjaxLinks();
          registerLoginForm();
          registerFilterForm();
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
              registerFilterForm();
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
            console.log("Přihlášení bylo úspěšné.");
            // Přesměrujeme na home
            window.location.href = '/';
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
  function registerLogoutLink() {
  const logoutLink = document.querySelector("a.logout");
  if (logoutLink) {
    logoutLink.addEventListener("click", event => {
      event.preventDefault();
      fetch(logoutLink.href, {
        method: "GET",
        headers: { "X-Requested-With": "XMLHttpRequest" }
      })
        .then(response => response.json())
        .then(result => {
          if (result.success) {
            console.log("Odhlášení bylo úspěšné.");
            window.location.href = result.redirect_url || '/';
          } else {
            console.error("Odhlášení selhalo.");
          }
        })
        .catch(error => {
          console.error("Došlo k chybě při odesílání požadavku na odhlášení:", error);
        });
      });
    }
  }
  function registerFilterForm() {
    console.log("Spouštím registerFilterForm");

  const filterForm = document.getElementById("filter-form");
  if (!filterForm) {
    console.log("Element s id 'filter-form' nebyl nalezen.");
    return;
  }


  // Volitelně: odstraníme již zavěšený listener,
  // pokud jej máme uloženého na vlastnosti elementu.
  if (filterForm._submitListener) {
    filterForm.removeEventListener("submit", filterForm._submitListener);
  }

  const submitListener = event => {
    console.log("Odeslání filtru zachyceno.");
    event.preventDefault();

    // Serializace formuláře do query stringu
    const formData = new FormData(filterForm);
    const params = new URLSearchParams(formData);
    const url = filterForm.getAttribute("action") + "?" + params.toString();
    console.log("Odesílám URL:", url);

    // AJAX fetch požadavku
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
      .then(response => {
        if (!response.ok) throw new Error("Chyba při filtrování");
        return response.text();
      })
      .then(html => {
        console.log("Data načtena, aktualizuji obsah.");
        const container = document.querySelector(".content-wrapper");
        if (container) {
          container.innerHTML = html;
          // Znovu zavěsit události na nové prvky z partial šablony
          registerAjaxLinks();
          registerFilterForm();
        } else {
          console.error("Element .content-wrapper nenalezen!");
        }
      })
      .catch(error => {
        console.error("Došlo k chybě při načtení filtrovaných dat:", error);
      });
    };

  // Uložíme listener do vlastnosti elementu pro možnost budoucího odstranění
  filterForm._submitListener = submitListener;
  filterForm.addEventListener("submit", submitListener);
  }

  document.addEventListener("DOMContentLoaded", () => {
  const themeToggleBtn = document.getElementById("theme-toggle");

  if (!themeToggleBtn) {
    console.warn("Tlačítko 'theme-toggle' nebylo nalezeno.");
    return;
  }

  // Inicializace tlačítka pro přepínání témat
  themeToggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("light-mode");

    // Uložení volby do localStorage pro zachování stavu při opětovném načtení stránky
    if (document.body.classList.contains("light-mode")) {
      localStorage.setItem("theme", "light");
    } else {
      localStorage.setItem("theme", "dark");
    }
  });

  // Při načtení stránky nastavíme téma dle uložené volby
  const userTheme = localStorage.getItem("theme");
  if (userTheme === "light") {
    document.body.classList.add("light-mode");
  }
});

  // Po načtení DOM zaregistrujeme AJAX odkazy (paginátor) a formulář
  registerAjaxLinks();
  registerLoginForm();
  registerFilterForm();
  registerLogoutLink();
});