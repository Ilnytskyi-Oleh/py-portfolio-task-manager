(() => {
  const THEME_KEY = "takt-theme";
  const SIDEBAR_KEY = "takt-sidebar";

  const rows = document.querySelectorAll("tr[data-href]");
  rows.forEach((row) => {
    row.addEventListener("click", (event) => {
      const target = event.target;
      if (
        target.closest("a, button, input, label, select, textarea")
      ) {
        return;
      }
      const href = row.getAttribute("data-href");
      if (href) {
        window.location.href = href;
      }
    });
  });

  function currentTheme() {
    const value = document.documentElement.getAttribute("data-theme");
    return value === "dark" ? "dark" : "light";
  }

  function setTheme(theme) {
    const next = theme === "dark" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    try {
      localStorage.setItem(THEME_KEY, next);
    } catch (e) {
      /* ignore */
    }
    syncThemeButtons();
  }

  function syncThemeButtons() {
    const theme = currentTheme();
    document.querySelectorAll("[data-theme-set]").forEach((button) => {
      const active = button.getAttribute("data-theme-set") === theme;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  document.querySelectorAll("[data-theme-set]").forEach((button) => {
    button.addEventListener("click", () => {
      setTheme(button.getAttribute("data-theme-set"));
    });
  });
  syncThemeButtons();

  function isSidebarCollapsed() {
    return document.documentElement.classList.contains("sidebar-collapsed");
  }

  function setSidebarCollapsed(collapsed) {
    document.documentElement.classList.toggle("sidebar-collapsed", collapsed);
    try {
      localStorage.setItem(
        SIDEBAR_KEY,
        collapsed ? "collapsed" : "expanded"
      );
    } catch (e) {
      /* ignore */
    }
    document.querySelectorAll("[data-sidebar-toggle]").forEach((button) => {
      button.setAttribute("aria-expanded", collapsed ? "false" : "true");
      const label = collapsed ? button.dataset.labelExpand : button.dataset.labelCollapse;
      if (label) {
        button.setAttribute("aria-label", label);
        button.setAttribute("title", label);
      }
    });
  }

  document.querySelectorAll("[data-sidebar-toggle]").forEach((button) => {
    const collapseLabel =
      button.getAttribute("aria-label") || "Collapse sidebar";
    button.dataset.labelCollapse = collapseLabel;
    button.dataset.labelExpand =
      button.getAttribute("data-expand-label") || "Expand sidebar";
    button.addEventListener("click", () => {
      setSidebarCollapsed(!isSidebarCollapsed());
    });
  });
  setSidebarCollapsed(isSidebarCollapsed());
})();
