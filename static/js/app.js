(() => {
  const THEME_KEY = "takt-theme";
  const SIDEBAR_KEY = "takt-sidebar";
  const NAV_GROUPS_KEY = "takt-nav-groups";

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

  function readNavGroups() {
    try {
      const raw = localStorage.getItem(NAV_GROUPS_KEY);
      if (!raw) {
        return {};
      }
      const parsed = JSON.parse(raw);
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch (e) {
      return {};
    }
  }

  function writeNavGroups(state) {
    try {
      localStorage.setItem(NAV_GROUPS_KEY, JSON.stringify(state));
    } catch (e) {
      /* ignore */
    }
  }

  function setNavGroupCollapsed(group, collapsed, persist) {
    const key = group.getAttribute("data-nav-group");
    const toggle = group.querySelector("[data-nav-group-toggle]");
    group.classList.toggle("is-collapsed", collapsed);
    if (toggle) {
      toggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
      const label = collapsed
        ? toggle.getAttribute("data-expand-label")
        : toggle.getAttribute("data-collapse-label");
      if (label) {
        toggle.setAttribute("aria-label", label);
        toggle.setAttribute("title", label);
      }
    }
    if (persist && key) {
      const state = readNavGroups();
      state[key] = collapsed ? "collapsed" : "expanded";
      writeNavGroups(state);
    }
  }

  const savedGroups = readNavGroups();
  document.querySelectorAll("[data-nav-group]").forEach((group) => {
    const key = group.getAttribute("data-nav-group");
    const toggle = group.querySelector("[data-nav-group-toggle]");
    if (!toggle) {
      return;
    }
    const collapsed = savedGroups[key] === "collapsed";
    setNavGroupCollapsed(group, collapsed, false);
    toggle.addEventListener("click", () => {
      setNavGroupCollapsed(
        group,
        !group.classList.contains("is-collapsed"),
        true
      );
    });
  });
})();
