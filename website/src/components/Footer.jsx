import { ArrowUpRight } from "lucide-react";
import MotionSection from "./MotionSection.jsx";
import PremiumCard from "./PremiumCard.jsx";

function Footer({ content }) {
  return (
    <footer className="section-pad" id="project-links">
      <div className="mx-auto max-w-[1480px] px-5 sm:px-8 lg:px-12">
        <MotionSection>
          <div className="grid gap-10 lg:grid-cols-[0.8fr_1.2fr]">
            <div>
              <p className="eyebrow">{content.eyebrow}</p>
              <h2 className="section-title">{content.title}</h2>
              <p className="section-description">{content.description}</p>
            </div>

            <div className="grid gap-5 sm:grid-cols-2">
              {content.links.map((link) => {
                const Icon = link.icon;
                return (
                  <PremiumCard className="link-card" key={link.label}>
                    <div className="flex items-center justify-between gap-4">
                      <div className="icon-soft">
                        <Icon size={20} />
                      </div>
                      {link.disabled ? (
                        <span className="csv-pill">TODO</span>
                      ) : (
                        <a
                          className="arrow-link"
                          href={link.href}
                          aria-label={link.label}
                          target={link.href?.startsWith("http") ? "_blank" : undefined}
                          rel="noreferrer"
                        >
                          <ArrowUpRight size={20} />
                        </a>
                      )}
                    </div>
                    <h3>{link.label}</h3>
                    <p>{link.detail}</p>
                    <span>{link.disabled ? content.placeholder : link.href}</span>
                  </PremiumCard>
                );
              })}
            </div>
          </div>
        </MotionSection>

        <div className="mt-16 flex flex-col gap-4 border-t border-stone-200 pt-8 text-sm text-stone-400 sm:flex-row sm:items-center sm:justify-between">
          <span>{content.brand}</span>
          <span>{content.note}</span>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
