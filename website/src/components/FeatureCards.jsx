import MotionSection from "./MotionSection.jsx";
import PremiumCard from "./PremiumCard.jsx";
import SectionTitle from "./SectionTitle.jsx";

function FeatureCards({ content }) {
  return (
    <MotionSection className="section-pad section-tint" id="features">
      <div className="mx-auto max-w-[1480px] px-5 sm:px-8 lg:px-12">
        <SectionTitle
          eyebrow={content.eyebrow}
          title={content.title}
          description={content.description}
        />

        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {content.cards.map((feature) => {
            const Icon = feature.icon;
            return (
              <PremiumCard key={feature.title}>
                <div className="icon-soft">
                  <Icon size={20} />
                </div>
                <h3 className="mt-6 text-lg font-semibold tracking-tight text-stone-950">
                  {feature.title}
                </h3>
                <p className="mt-3 text-sm leading-7 text-stone-500">
                  {feature.text}
                </p>
              </PremiumCard>
            );
          })}
        </div>
      </div>
    </MotionSection>
  );
}

export default FeatureCards;
