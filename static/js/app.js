(() => {
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
})();
