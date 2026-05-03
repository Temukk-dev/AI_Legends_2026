import { useState } from "react";
import { AlertTriangle, ArrowUpRight } from "lucide-react";
import Hero from "./components/Hero.jsx";
import SectionTitle from "./components/SectionTitle.jsx";
import Workflow from "./components/Workflow.jsx";
import FeatureCards from "./components/FeatureCards.jsx";
import RiskRules from "./components/RiskRules.jsx";
import DecisionLogic from "./components/DecisionLogic.jsx";
import UploadDemo from "./components/UploadDemo.jsx";
import QASection from "./components/QASection.jsx";
import Outputs from "./components/Outputs.jsx";
import Footer from "./components/Footer.jsx";
import MotionSection from "./components/MotionSection.jsx";
import SideDrawer from "./components/SideDrawer.jsx";
import TopNav from "./components/TopNav.jsx";
import { content } from "./data/projectContent.js";

function App() {
  const [language, setLanguage] = useState("mn");
  const [drawerOpen, setDrawerOpen] = useState(false);
  const copy = content[language];

  return (
    <div className="min-h-screen overflow-hidden bg-[#fbf8f1] text-stone-950 selection:bg-emerald-200 selection:text-stone-950">
      <div className="page-ambient" />
      <TopNav
        copy={copy.nav}
        language={language}
        onLanguageChange={setLanguage}
        onMenu={() => setDrawerOpen(true)}
      />
      <SideDrawer
        groups={copy.drawer}
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      />

      <main id="top">
        <Hero content={copy.hero} />

        <MotionSection className="section-pad" id="problem">
          <div className="mx-auto max-w-[1480px] px-5 sm:px-8 lg:px-12">
            <SectionTitle
              eyebrow={copy.problem.eyebrow}
              title={copy.problem.title}
              description={copy.problem.description}
            />
            <div className="mt-12 grid gap-5 md:grid-cols-3">
              {copy.problem.cards.map((item) => {
                const Icon = item.icon;
                return (
                  <article className="pain-card" key={item.title}>
                    <div className="icon-soft">
                      <Icon size={20} />
                    </div>
                    <h3>{item.title}</h3>
                    <p>{item.text}</p>
                  </article>
                );
              })}
            </div>
          </div>
        </MotionSection>

        <Workflow content={copy.workflowSection} />
        <FeatureCards content={copy.featuresSection} />
        <RiskRules content={copy.riskSection} />
        <DecisionLogic content={copy.decisionSection} />
        <UploadDemo content={copy.upload} />
        <QASection content={copy.qaSection} />
        <Outputs content={copy.outputsSection} />

        <MotionSection className="section-pad" id="submission">
          <div className="mx-auto grid max-w-[1480px] gap-10 px-5 sm:px-8 lg:grid-cols-[0.8fr_1.2fr] lg:px-12">
            <SectionTitle
              eyebrow={copy.submission.eyebrow}
              title={copy.submission.title}
              description={copy.submission.description}
            />
            <div className="grid gap-4 sm:grid-cols-2">
              {copy.submission.items.map((item) => (
                <div className="submission-item" key={item}>
                  <span className="icon-soft">
                    <ArrowUpRight size={18} />
                  </span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>
        </MotionSection>

        <MotionSection className="px-5 pb-12 sm:px-8 lg:px-12" id="links-preview">
          <div className="mx-auto max-w-[1480px]">
            <div className="notice-panel">
              <div className="flex items-start gap-3">
                <AlertTriangle className="mt-0.5 shrink-0 text-emerald-700" size={19} />
                <p>{copy.notice.text}</p>
              </div>
              <a className="secondary-soft-button" href="#demo">
                {copy.notice.button}
              </a>
            </div>
          </div>
        </MotionSection>
      </main>

      <Footer content={copy.footer} />
    </div>
  );
}

export default App;
