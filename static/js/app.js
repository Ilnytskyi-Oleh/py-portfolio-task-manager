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
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      button.classList.toggle("is-dark", theme === "dark");
    });
  }

  document.querySelectorAll("[data-theme-set]").forEach((button) => {
    button.addEventListener("click", () => {
      setTheme(button.getAttribute("data-theme-set"));
    });
  });
  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      setTheme(currentTheme() === "dark" ? "light" : "dark");
    });
  });
  syncThemeButtons();

  const submenus = document.querySelectorAll("[data-submenu]");
  const submenuHoverMedia = window.matchMedia(
    "(hover: hover) and (pointer: fine)"
  );

  function setSubmenuOpen(menu, open) {
    const toggle = menu.querySelector("[data-submenu-toggle]");
    const panel = menu.querySelector(".sidebar-submenu-panel");
    if (!toggle || !panel) {
      return;
    }
    menu.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    panel.hidden = !open;
  }

  function closeAllSubmenus(except) {
    submenus.forEach((menu) => {
      if (menu !== except) {
        setSubmenuOpen(menu, false);
      }
    });
  }

  submenus.forEach((menu) => {
    const toggle = menu.querySelector("[data-submenu-toggle]");
    if (!toggle) {
      return;
    }
    let hoverCloseTimer = null;

    function clearHoverClose() {
      if (hoverCloseTimer) {
        window.clearTimeout(hoverCloseTimer);
        hoverCloseTimer = null;
      }
    }

    toggle.addEventListener("click", (event) => {
      event.stopPropagation();
      const next = !menu.classList.contains("is-open");
      closeAllSubmenus(menu);
      setSubmenuOpen(menu, next);
    });

    menu.addEventListener("mouseenter", () => {
      if (!submenuHoverMedia.matches) {
        return;
      }
      clearHoverClose();
      closeAllSubmenus(menu);
      setSubmenuOpen(menu, true);
    });

    menu.addEventListener("mouseleave", () => {
      if (!submenuHoverMedia.matches) {
        return;
      }
      clearHoverClose();
      // Longer grace when the panel flies beside a collapsed rail.
      const delay = isSidebarCollapsed() ? 320 : 160;
      hoverCloseTimer = window.setTimeout(() => {
        setSubmenuOpen(menu, false);
      }, delay);
    });
  });

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof Element) || !target.closest("[data-submenu]")) {
      closeAllSubmenus();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAllSubmenus();
    }
  });

  const peekMedia = window.matchMedia("(hover: hover) and (pointer: fine)");

  function isSidebarCollapsed() {
    return document.documentElement.classList.contains("sidebar-collapsed");
  }

  function setSidebarPeek(peek) {
    document.documentElement.classList.toggle("sidebar-peek", Boolean(peek));
    syncSidebarTooltips();
  }

  function isSidebarPeekZone(target) {
    if (!(target instanceof Element)) {
      return false;
    }
    // Only the empty area below menu items may open the rail.
    return Boolean(target.closest(".sidebar-peek-zone"));
  }

  function sidebarTooltipTargets() {
    return document.querySelectorAll(
      [
        ".sidebar-desktop .nav-link",
        ".sidebar-desktop .btn-logout",
        ".sidebar-desktop .btn-settings",
        ".sidebar-desktop .sidebar-toggle",
        ".sidebar-desktop .sidebar-footer .btn",
      ].join(", ")
    );
  }

  function sidebarTooltipText(el) {
    return (
      el.getAttribute("data-bs-original-title") ||
      el.getAttribute("title") ||
      ""
    );
  }

  function syncSidebarTooltipContent(el, text) {
    if (!text) {
      return;
    }
    el.setAttribute("title", text);
    el.setAttribute("data-bs-original-title", text);
    const tip = window.bootstrap?.Tooltip?.getInstance(el);
    if (tip) {
      tip.setContent({ ".tooltip-inner": text });
    }
  }

  function syncSidebarTooltips() {
    if (!window.bootstrap?.Tooltip) {
      return;
    }
    const enabled =
      isSidebarCollapsed() &&
      !document.documentElement.classList.contains("sidebar-peek");
    sidebarTooltipTargets().forEach((el) => {
      if (!sidebarTooltipText(el)) {
        return;
      }
      let tip = bootstrap.Tooltip.getInstance(el);
      if (!tip) {
        tip = new bootstrap.Tooltip(el, {
          placement: "right",
          container: "body",
          // Native title tooltips are ~0.5–1s; keep a tiny delay to avoid flicker.
          delay: { show: 50, hide: 0 },
          trigger: "hover",
        });
      }
      if (enabled) {
        tip.enable();
      } else {
        tip.hide();
        tip.disable();
      }
    });
  }

  function setSidebarCollapsed(collapsed) {
    document.documentElement.classList.toggle("sidebar-collapsed", collapsed);
    if (!collapsed) {
      setSidebarPeek(false);
    }
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
        syncSidebarTooltipContent(button, label);
      }
    });
    syncSidebarTooltips();
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

  document.querySelectorAll(".sidebar-desktop").forEach((sidebar) => {
    sidebar.addEventListener("mouseover", (event) => {
      if (!peekMedia.matches || !isSidebarCollapsed()) {
        return;
      }
      if (document.documentElement.classList.contains("sidebar-peek")) {
        return;
      }
      if (!isSidebarPeekZone(event.target)) {
        return;
      }
      setSidebarPeek(true);
    });

    sidebar.addEventListener("mouseleave", () => {
      setSidebarPeek(false);
    });
  });

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
