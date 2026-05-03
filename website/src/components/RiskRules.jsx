import MotionSection from "./MotionSection.jsx";
import SectionTitle from "./SectionTitle.jsx";

function RiskRules({ content }) {
  return (
    <MotionSection className="section-pad" id="risk">
      <div className="mx-auto grid max-w-[1480px] gap-12 px-5 sm:px-8 lg:grid-cols-[0.8fr_1.2fr] lg:px-12">
        <SectionTitle
          eyebrow={content.eyebrow}
          title={content.title}
          description={content.description}
        />

        <div className="rounded-panel grid gap-3 p-3 sm:grid-cols-2">
          {content.rules.map((rule) => {
            const Icon = rule.icon;
            return (
              <article className="risk-row" key={rule.title}>
                <div className="icon-soft">
                  <Icon size={19} />
                </div>
                <div>
                  <h3>{rule.title}</h3>
                  <p>{rule.text}</p>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </MotionSection>
  );
}

export default RiskRules;
