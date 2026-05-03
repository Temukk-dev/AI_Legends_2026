import { ArrowRight } from "lucide-react";
import MotionSection from "./MotionSection.jsx";
import SectionTitle from "./SectionTitle.jsx";

function Workflow({ content }) {
  return (
    <MotionSection className="section-pad" id="workflow">
      <div className="mx-auto max-w-[1480px] px-5 sm:px-8 lg:px-12">
        <SectionTitle
          eyebrow={content.eyebrow}
          title={content.title}
          description={content.description}
          align="center"
        />

        <div className="workflow-strip mt-14">
          {content.steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div className="workflow-item" key={step.title}>
                <div className="workflow-card">
                  <span className="step-number">{String(index + 1).padStart(2, "0")}</span>
                  <div className="icon-soft">
                    <Icon size={20} />
                  </div>
                  <h3>{step.title}</h3>
                  <p>{step.detail}</p>
                </div>
                {index < content.steps.length - 1 && (
                  <ArrowRight className="workflow-arrow" size={18} />
                )}
              </div>
            );
          })}
        </div>
      </div>
    </MotionSection>
  );
}

export default Workflow;
