import MotionSection from "./MotionSection.jsx";
import PremiumCard from "./PremiumCard.jsx";
import ResultSummary from "./ResultSummary.jsx";
import SectionTitle from "./SectionTitle.jsx";

const toneClass = {
  success: "decision-success",
  warning: "decision-warning",
  danger: "decision-danger",
};

function DecisionLogic({ content }) {
  return (
    <MotionSection className="section-pad section-tint" id="decision">
      <div className="mx-auto max-w-[1480px] px-5 sm:px-8 lg:px-12">
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-end">
          <SectionTitle
            eyebrow={content.eyebrow}
            title={content.title}
            description={content.description}
          />
          <ResultSummary items={content.summary} />
        </div>

        <div className="mt-12 grid gap-5 lg:grid-cols-3" id="results">
          {content.decisions.map((decision) => {
            const Icon = decision.icon;
            return (
              <PremiumCard className="decision-card" key={decision.label}>
                <div className="flex items-center justify-between gap-4">
                  <span className={`decision-badge ${toneClass[decision.tone]}`}>
                    <Icon size={17} />
                    {decision.label}
                  </span>
                </div>
                <h3>{decision.title}</h3>
                <p>{decision.text}</p>
              </PremiumCard>
            );
          })}
        </div>

        {content.rules?.length ? (
          <div className="mt-10 rounded-panel p-5 sm:p-6">
            <p className="eyebrow">Decision rules</p>
            <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
              {content.rules.map((rule) => (
                <span className={`soft-label ${toneClass[rule.tone]}`} key={rule.label}>
                  {rule.label}
                </span>
              ))}
            </div>
          </div>
        ) : null}
      </div>
    </MotionSection>
  );
}

export default DecisionLogic;
