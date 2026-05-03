import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import PremiumCard from "./PremiumCard.jsx";
import SearchCTA from "./SearchCTA.jsx";
import TempleHero from "./TempleHero.jsx";

function Hero({ content }) {
  return (
    <section className="hero-section" id="home">
      <div className="mx-auto grid max-w-[1680px] items-center gap-12 px-5 pb-20 pt-8 sm:px-8 lg:grid-cols-[0.95fr_1.05fr] lg:px-12 lg:pb-24 lg:pt-16">
        <motion.div
          className="order-2 mx-auto w-full max-w-3xl text-center lg:order-1 lg:mx-0 lg:text-left"
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.75, ease: [0.22, 1, 0.36, 1] }}
        >
          <p className="hero-greeting">{content.greeting}</p>
          <h1 className="hero-title">{content.title}</h1>
          <p className="hero-subtitle">{content.subtitle}</p>

          <div className="mt-9">
            <SearchCTA
              placeholder={content.searchPlaceholder}
              action={content.searchAction}
            />
          </div>

          <div className="mt-5 flex flex-wrap justify-center gap-2 lg:justify-start">
            {content.quickTags.map((tag) => (
              <span className="quick-pill" key={tag}>
                {tag}
              </span>
            ))}
          </div>
        </motion.div>

        <div className="order-1 lg:order-2">
          <TempleHero />
        </div>
      </div>

      <div className="mx-auto grid max-w-[1480px] gap-6 px-5 pb-16 sm:px-8 md:grid-cols-3 lg:px-12">
        {content.cards.map((card) => {
          const Icon = card.icon;
          return (
            <PremiumCard className="hero-link-card" key={card.title}>
              <div className="icon-disc">
                <Icon size={28} />
              </div>
              <div className="min-w-0 flex-1">
                <h3>{card.title}</h3>
                <p>{card.text}</p>
              </div>
              <a className="arrow-link" href={card.href} aria-label={card.title}>
                <ArrowRight size={24} />
              </a>
            </PremiumCard>
          );
        })}
      </div>
    </section>
  );
}

export default Hero;
