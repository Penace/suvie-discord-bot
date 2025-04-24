import { useEffect } from "react";

export default function KoFiWidget() {
  useEffect(() => {
    if (document.getElementById("kofi-script")) return;

    const script = document.createElement("script");
    script.id = "kofi-script";
    script.src = "https://storage.ko-fi.com/cdn/scripts/overlay-widget.js";
    script.async = true;
    script.onload = () => {
      if (window.kofiWidgetOverlay) {
        window.kofiWidgetOverlay.draw("penace", {
          type: "floating-chat",
          "floating-chat.donateButton.text": "",
          "floating-chat.donateButton.background-color": "#FF5E5B",
          "floating-chat.donateButton.text-color": "#ffffff",
          mb: "25px",
        });
      }
    };

    document.body.appendChild(script);
    return () => {
      document.getElementById("kofi-script")?.remove();
    };
  }, []);

  return null;
}
