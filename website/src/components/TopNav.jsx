import { Menu } from "lucide-react";
import LanguageSwitcher from "./LanguageSwitcher.jsx";

function TopNav({ copy, language, onLanguageChange, onMenu }) {
  const links = [
    { label: copy.workflow, href: "#workflow" },
    { label: copy.features, href: "#features" },
    { label: copy.results, href: "#results" },
    { label: copy.links, href: "#project-links" },
  ];

  return (
    <header className="topbar">
      <nav className="mx-auto grid max-w-[1680px] grid-cols-[auto_1fr_auto] items-center gap-5 px-5 py-5 sm:px-8 lg:px-12">
        <button className="hamburger-button" type="button" onClick={onMenu} aria-label={copy.menuLabel}>
          <Menu size={28} strokeWidth={1.9} />
        </button>

        <div className="hidden justify-center gap-14 md:flex">
          {links.map((link) => (
            <a className="topnav-link" href={link.href} key={link.href}>
              {link.label}
            </a>
          ))}
        </div>

        <div className="flex items-center justify-end gap-3">
          <LanguageSwitcher
            language={language}
            label={copy.languageLabel}
            onLanguageChange={onLanguageChange}
          />
          <button className="signin-button" type="button">
            {copy.signIn}
          </button>
        </div>
      </nav>
    </header>
  );
}

export default TopNav;
