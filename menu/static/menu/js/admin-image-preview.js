(() => {
  const init = () => {
    const fileInput = document.querySelector('input[type="file"][name="image"]');
    if (!fileInput || fileInput.dataset.previewReady) return;
    fileInput.dataset.previewReady = "true";

    const preview = document.createElement("img");
    preview.alt = "Tanlangan taom rasmi ko‘rinishi";
    preview.hidden = true;
    preview.style.cssText = "display:block;max-width:280px;max-height:220px;object-fit:cover;border-radius:12px;margin-top:12px;border:1px solid #d5e5e9;box-shadow:0 8px 24px rgba(18,61,85,.12)";
    fileInput.insertAdjacentElement("afterend", preview);

    let previousUrl = "";
    fileInput.addEventListener("change", () => {
      if (previousUrl) URL.revokeObjectURL(previousUrl);
      const file = fileInput.files && fileInput.files[0];
      if (!file || !file.type.startsWith("image/")) {
        preview.removeAttribute("src");
        preview.hidden = true;
        return;
      }
      previousUrl = URL.createObjectURL(file);
      preview.src = previousUrl;
      preview.hidden = false;
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
