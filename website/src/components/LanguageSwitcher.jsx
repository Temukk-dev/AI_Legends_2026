import { Globe2 } from "lucide-react";
import { languages } from "../data/projectContent.js";

function LanguageSwitcher({ language, onLanguageChange }) {
  return (
    <div className="language-switch" aria-label="Available languages are Mongolian and English">
      <Globe2 className="hidden text-stone-900 sm:block" size={20} strokeWidth={2} />
      {languages.map((item) => {
        const active = item.code === language;
        return (
          <button
            className={active ? "language-pill-active" : "language-pill"}
            key={item.code}
            type="button"
            aria-pressed={active}
            title={item.label}
            onClick={() => onLanguageChange(item.code)}
          >
            {item.nativeLabel}
          </button>
        );
      })}
    </div>
  );
}

export default LanguageSwitcher;
