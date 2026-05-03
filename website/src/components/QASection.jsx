import { MessageSquareText } from "lucide-react";
import MotionSection from "./MotionSection.jsx";
import SectionTitle from "./SectionTitle.jsx";

function QASection({ content }) {
  return (
    <MotionSection className="section-pad" id="qa">
      <div className="mx-auto max-w-[1480px] px-5 sm:px-8 lg:px-12">
        <SectionTitle
          eyebrow={content.eyebrow}
          title={content.title}
          description={content.description}
          align="center"
        />

        <div className="mt-12 grid gap-4 lg:grid-cols-2">
          {content.questions.map((item, index) => (
            <article className="qa-card" key={item.question}>
              <div className="icon-soft">
                <MessageSquareText size={19} />
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-stone-400">
                  Q{String(index + 1).padStart(2, "0")}
                </p>
                <h3>{item.question}</h3>
                <p>{item.answer}</p>
              </div>
            </article>
          ))}
        </div>

        {content.invoiceQuestions?.length ? (
          <div className="mt-10">
            <p className="eyebrow text-center">{content.invoiceLabel || "Invoice fact checks"}</p>
            <div className="mt-5 grid gap-4 lg:grid-cols-2">
              {content.invoiceQuestions.map((item) => (
                <article className="qa-card" key={item.question}>
                  <div className="icon-soft">
                    <MessageSquareText size={19} />
                  </div>
                  <div>
                    <h3>{item.question}</h3>
                    <p>{item.answer}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        ) : null}
      </div>
    </MotionSection>
  );
}

export default QASection;
