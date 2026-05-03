import MotionSection from "./MotionSection.jsx";
import PremiumCard from "./PremiumCard.jsx";
import SectionTitle from "./SectionTitle.jsx";

function Outputs({ content }) {
  return (
    <MotionSection className="section-pad section-tint" id="outputs">
      <div className="mx-auto grid max-w-[1480px] gap-12 px-5 sm:px-8 lg:grid-cols-[0.8fr_1.2fr] lg:px-12">
        <SectionTitle
          eyebrow={content.eyebrow}
          title={content.title}
          description={content.description}
        />

        <div className="grid gap-5 sm:grid-cols-2">
          {content.files.map((file) => {
            const Icon = file.icon;
            return (
              <PremiumCard key={file.name}>
                <div className="flex items-center justify-between gap-4">
                  <div className="icon-soft">
                    <Icon size={20} />
                  </div>
                  <span className="csv-pill">{file.badge || "CSV"}</span>
                </div>
                <h3 className="mt-6 font-mono text-base font-semibold text-stone-950">
                  {file.name}
                </h3>
                <p className="mt-3 text-sm leading-7 text-stone-500">
                  {file.detail}
                </p>
              </PremiumCard>
            );
          })}
        </div>
      </div>
    </MotionSection>
  );
}

export default Outputs;
