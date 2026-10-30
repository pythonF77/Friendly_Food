(function () {
  const greetingKey = "dostlik-welcome-spoken-v3";
  const greeting = "Assalomu alaykum! Do‘stlik oshxonamiz saytiga xush kelibsiz. O‘zingizga yoqqan taomni tanlang va fikrlaringizni biz bilan bo‘lishing. Va yana bir narsa, yoqimli ishtaha!";

  function speakOnce() {
    if (localStorage.getItem(greetingKey)) return;
    localStorage.setItem(greetingKey, "1");

    const welcomeAudio = new Audio("/static/menu/audio/welcome.mp3");
    welcomeAudio.play().catch(() => {
      if ("speechSynthesis" in window && "SpeechSynthesisUtterance" in window) {
        speakWithBrowserVoice();
      }
    });
  }

  function speakWithBrowserVoice() {
    const voices = window.speechSynthesis.getVoices();
    const uzbekVoice = voices.find((voice) => voice.lang.toLowerCase().startsWith("uz"));
    const femaleVoice = voices.find((voice) => /female|woman|zira|dilnoza|madina|gulnora/i.test(voice.name));
    const utterance = new SpeechSynthesisUtterance(greeting);
    utterance.lang = "uz-UZ";
    utterance.rate = 0.92;
    utterance.pitch = 1.08;
    utterance.voice = uzbekVoice || femaleVoice || null;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  }

  window.addEventListener("pointerdown", speakOnce, { once: true, passive: true });
  window.addEventListener("keydown", speakOnce, { once: true });
})();
