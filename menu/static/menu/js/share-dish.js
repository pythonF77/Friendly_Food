(() => {
  const shareButton = document.getElementById("share-native");
  const telegramLink = document.getElementById("share-telegram");
  const copyButton = document.getElementById("share-copy");
  const status = document.getElementById("share-status");
  if (!shareButton || !telegramLink || !copyButton || !status) return;

  const url = window.location.href.split("#", 1)[0];
  const title = document.querySelector(".detail-copy h1")?.textContent.trim() || document.title;
  const message = `${title} — Do‘stlik oshxonasi`;
  telegramLink.href = `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(message)}`;

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(url);
    } catch {
      const field = document.createElement("textarea");
      field.value = url;
      field.setAttribute("readonly", "");
      field.style.position = "fixed";
      field.style.opacity = "0";
      document.body.appendChild(field);
      field.select();
      document.execCommand("copy");
      field.remove();
    }
    status.textContent = "Taom havolasi nusxalandi. Endi uni Instagram yoki boshqa chatga yuboring.";
  };

  copyButton.addEventListener("click", copyLink);
  shareButton.addEventListener("click", async () => {
    if (!navigator.share) {
      await copyLink();
      return;
    }
    try {
      await navigator.share({ title: message, text: `${title} — Do‘stlik oshxonasidagi taom`, url });
    } catch (error) {
      if (error.name !== "AbortError") await copyLink();
    }
  });
})();
