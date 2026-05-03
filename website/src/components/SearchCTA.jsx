import { Mic, Plus, Sparkles } from "lucide-react";

function SearchCTA({ placeholder, action }) {
  return (
    <a className="search-cta" href="#workflow" aria-label={action}>
      <span className="search-plus">
        <Plus size={23} strokeWidth={2.1} />
      </span>
      <span className="search-placeholder">{placeholder}</span>
      <span className="search-divider" />
      <span className="search-spark">
        <Sparkles size={23} strokeWidth={2.1} />
      </span>
      <span className="search-mic">
        <Mic size={23} strokeWidth={2.1} />
      </span>
    </a>
  );
}

export default SearchCTA;
