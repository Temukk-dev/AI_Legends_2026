import {
  AlertTriangle,
  BadgeCheck,
  Ban,
  BarChart3,
  BookOpen,
  BrainCircuit,
  CheckCircle2,
  CircleDollarSign,
  ClipboardCheck,
  Clock3,
  Database,
  FileArchive,
  FileCheck2,
  FileImage,
  FileSearch,
  FileText,
  Github,
  Layers3,
  ListChecks,
  PlayCircle,
  ScanLine,
  ShieldAlert,
  ShieldCheck,
  Table2,
  UploadCloud,
  WalletCards,
  XCircle,
} from "lucide-react";

const icons = {
  alert: AlertTriangle,
  badge: BadgeCheck,
  ban: Ban,
  bar: BarChart3,
  book: BookOpen,
  brain: BrainCircuit,
  check: CheckCircle2,
  circleDollar: CircleDollarSign,
  clipboard: ClipboardCheck,
  clock: Clock3,
  database: Database,
  archive: FileArchive,
  fileCheck: FileCheck2,
  fileImage: FileImage,
  fileSearch: FileSearch,
  fileText: FileText,
  github: Github,
  layers: Layers3,
  list: ListChecks,
  play: PlayCircle,
  scan: ScanLine,
  shieldAlert: ShieldAlert,
  shieldCheck: ShieldCheck,
  table: Table2,
  upload: UploadCloud,
  wallet: WalletCards,
  xCircle: XCircle,
};

export const languages = [
  { code: "mn", label: "Mongolian", nativeLabel: "MN" },
  { code: "en", label: "English", nativeLabel: "EN" },
];

const commonLinks = [
  {
    label: "Open Kaggle Notebook",
    detail: "Final pipeline, extraction, validation, and Q&A",
    href: "https://www.kaggle.com/code/temuulenmunkhochir/ai-legends-2026-final-ipynb",
    icon: icons.book,
  },
  {
    label: "View GitHub Repository",
    detail: "Repository with notebook, docs, and CSV outputs",
    href: "https://github.com/Temukk-dev/AI_Legends_2026",
    icon: icons.github,
  },
  {
    label: "View Outputs folder",
    detail: "all_results.csv, summary, and exported batch files",
    href: "#outputs",
    icon: icons.table,
  },
  {
    label: "Watch Demo Video",
    detail: "TODO — public video URL pending",
    href: "#project-links",
    icon: icons.play,
    disabled: true,
  },
  {
    label: "Read Kaggle Writeup",
    detail: "TODO — public writeup URL pending",
    href: "#project-links",
    icon: icons.fileText,
    disabled: true,
  },
];

export const content = {
  en: {
    nav: {
      workflow: "Workflow",
      features: "Features",
      results: "Results",
      links: "Links",
      signIn: "Sign in",
      languageLabel: "Language",
      menuLabel: "Open menu",
    },
    drawer: [
      {
        title: "Project",
        items: [
          { label: "Overview", href: "#top" },
          { label: "Source Files", href: "#project-links" },
          { label: "Notebook", href: "#project-links" },
          { label: "README", href: "#project-links" },
          { label: "Writeup", href: "#project-links" },
        ],
      },
      {
        title: "Workspace",
        items: [
          { label: "Upload Demo", href: "#demo" },
          { label: "Processing History", href: "#results" },
          { label: "Result Table", href: "#demo" },
          { label: "Q&A Console", href: "#qa" },
          { label: "Decision Logs", href: "#decision" },
        ],
      },
      {
        title: "Outputs",
        items: [
          { label: "final_results.csv", href: "#outputs" },
          { label: "clean_invoices.csv", href: "#outputs" },
          { label: "suspicious_invoices.csv", href: "#outputs" },
          { label: "failed_files.csv", href: "#outputs" },
        ],
      },
      {
        title: "External Links",
        items: commonLinks.map((link) => ({
          label: link.label,
          href: link.href,
          disabled: link.disabled,
        })),
      },
    ],
    hero: {
      greeting: "Hello, how can I help?",
      title: "Automate invoice workflows with AI.",
      subtitle:
        "Extract data, validate with confidence, assess risk, and make smarter financial decisions faster.",
      detail: "",
      searchPlaceholder: "Ask anything about invoices...",
      searchAction: "Explore workflow",
      quickTags: ["Vision/OCR extraction", "Risk detection", "CSV outputs"],
      cards: [
        {
          title: "GitHub",
          text: "Explore the code, models, and automation pipelines.",
          href: "#project-links",
          icon: icons.github,
        },
        {
          title: "Analytics",
          text: "Monitor decisions, trends, and financial insights.",
          href: "#results",
          icon: icons.bar,
        },
        {
          title: "Live Demo",
          text: "Experience the AI invoice workflow with demo files.",
          href: "#demo",
          icon: icons.play,
        },
      ],
    },
    problem: {
      eyebrow: "Problem",
      title: "Manual invoice review slows finance teams down.",
      description:
        "The project turns messy invoice files into evidence-backed decisions before accounting teams spend time on manual checks.",
      cards: [
        {
          title: "Manual checking is slow",
          text:
            "Accountants lose hours opening files, copying values, checking totals, and searching master data.",
          icon: icons.clock,
        },
        {
          title: "Small errors become risk",
          text:
            "Human review can miss wrong totals, vendor names, invoice dates, bank accounts, or duplicated invoices.",
          icon: icons.fileSearch,
        },
        {
          title: "Large batches are hard to inspect",
          text:
            "When hundreds of invoices arrive together, teams need automatic triage before human approval.",
          icon: icons.layers,
        },
      ],
    },
    workflowSection: {
      eyebrow: "Agent Workflow",
      title: "From uploaded invoice to business decision.",
      description:
        "The workflow is transparent enough for a Kaggle notebook and practical enough for a finance review process.",
      steps: [
        {
          title: "PDF/JPG/PNG Upload",
          detail: "Batch files are staged for the agent without manual copy-paste.",
          icon: icons.upload,
        },
        {
          title: "Vision/OCR Extraction",
          detail:
            "Groq Vision extracts vendor, dates, totals, line items, and account fields.",
          icon: icons.scan,
        },
        {
          title: "Database Validation",
          detail:
            "Extracted values are checked against master vendor and item records.",
          icon: icons.database,
        },
        {
          title: "Risk Flagging",
          detail:
            "The agent marks suspicious records before money movement happens.",
          icon: icons.shieldAlert,
        },
        {
          title: "Final Decision",
          detail: "Each invoice receives AUTO_POST, HUMAN_APPROVAL, or DENY.",
          icon: icons.clipboard,
        },
        {
          title: "CSV Output + Q&A",
          detail:
            "Clean outputs and aggregate questions summarize the full invoice batch.",
          icon: icons.table,
        },
      ],
    },
    featuresSection: {
      eyebrow: "Features",
      title: "A focused feature set for invoice automation.",
      description:
        "Every capability maps to a practical finance workflow: read the file, validate facts, separate risk, and produce usable outputs.",
      cards: [
        {
          title: "PDF/JPG/PNG invoice processing",
          text: "Handles common invoice formats used in accounting workflows.",
          icon: icons.fileImage,
        },
        {
          title: "Groq Vision field extraction",
          text:
            "Extracts key invoice fields from document images with vision-first parsing.",
          icon: icons.brain,
        },
        {
          title: "Vendor validation",
          text: "Checks vendor identity against registered master records.",
          icon: icons.badge,
        },
        {
          title: "Item validation",
          text:
            "Compares invoice line items with allowed product or service references.",
          icon: icons.list,
        },
        {
          title: "Amount mismatch detection",
          text: "Flags subtotal, tax, total, and line-item inconsistencies.",
          icon: icons.circleDollar,
        },
        {
          title: "Duplicate invoice detection",
          text:
            "Detects repeated invoice numbers or vendor/date/amount patterns.",
          icon: icons.layers,
        },
        {
          title: "Clean, suspicious, failed separation",
          text: "Routes processed files into clean, review, and failed outputs.",
          icon: icons.archive,
        },
        {
          title: "Final decision logic",
          text:
            "Turns extraction and validation evidence into business-ready outcomes.",
          icon: icons.shieldCheck,
        },
      ],
    },
    riskSection: {
      eyebrow: "Risk Detection Rules",
      title: "Explainable checks before final posting.",
      description:
        "The agent does not only extract text. It turns each invoice into a validation record with transparent risk reasons.",
      rules: [
        {
          title: "Unregistered vendor",
          text:
            "Vendor name, tax ID, or supplier code is missing from trusted master data.",
          icon: icons.shieldAlert,
        },
        {
          title: "Amount mismatch",
          text: "Line items, tax, subtotal, or grand total do not reconcile cleanly.",
          icon: icons.circleDollar,
        },
        {
          title: "Duplicate invoice",
          text:
            "Invoice number or vendor/date/amount fingerprint appears more than once.",
          icon: icons.layers,
        },
        {
          title: "Invalid or missing date",
          text:
            "Invoice date is empty, malformed, or outside the expected accounting window.",
          icon: icons.alert,
        },
        {
          title: "Missing required fields",
          text:
            "Required fields such as invoice number, vendor, total, or currency are absent.",
          icon: icons.fileSearch,
        },
        {
          title: "Bank/account mismatch",
          text: "Payment account does not match the approved vendor account.",
          icon: icons.wallet,
        },
      ],
    },
    decisionSection: {
      eyebrow: "Final Decision Logic",
      title: "Clear outcomes for business action.",
      description:
        "The notebook uses deterministic business rules rather than a second LLM for the final label.",
      rules: [
        { label: "No risks → AUTO_POST", tone: "success" },
        { label: "Amount mismatch → HUMAN_APPROVAL", tone: "warning" },
        { label: "Invalid date → HUMAN_APPROVAL", tone: "warning" },
        { label: "Unregistered vendor → HUMAN_APPROVAL", tone: "warning" },
        { label: "Low-confidence extraction → HUMAN_APPROVAL", tone: "warning" },
        { label: "Extraction failed → HUMAN_APPROVAL", tone: "warning" },
        { label: "Bank account mismatch → DENY", tone: "danger" },
        { label: "Duplicate → DENY", tone: "danger" },
      ],
      decisions: [
        {
          label: "AUTO_POST",
          title: "No risks and valid totals",
          text: "Clean invoice, trusted vendor, and valid totals pass automatic posting.",
          icon: icons.check,
          tone: "success",
        },
        {
          label: "HUMAN_APPROVAL",
          title: "Reviewable risk cases",
          text: "Amount mismatch, invalid date, unregistered vendor, low-confidence extraction, and extraction failure route here.",
          icon: icons.alert,
          tone: "warning",
        },
        {
          label: "DENY",
          title: "High-risk invoice",
          text: "Bank account mismatch and duplicate invoices are denied.",
          icon: icons.xCircle,
          tone: "danger",
        },
      ],
      summary: [
        { label: "Total", value: "100", tone: "success", subtext: "Final verified run" },
        { label: "Clean", value: "68", tone: "success", subtext: "AUTO_POST-ready invoices" },
        { label: "Suspicious", value: "32", tone: "warning", subtext: "Needs review or deny" },
        { label: "AUTO_POST", value: "68", tone: "success", subtext: "Automatic posting" },
        { label: "HUMAN_APPROVAL", value: "15", tone: "warning", subtext: "Manual review queue" },
        { label: "DENY", value: "17", tone: "danger", subtext: "Blocked from posting" },
      ],
    },
    upload: {
      eyebrow: "Demo Upload UI",
      title: "A frontend-only processing preview.",
      description:
        "Drag files into the interface to preview the experience. Files stay in your browser state only, and this static demo does not send invoices to any backend.",
      dropTitle: "Drop invoice files here",
      dropText:
        "Accepts PDF, JPG, and PNG. This demo shows local file names, simulated processing status, and mock decision output.",
      chooseFiles: "Choose files",
      acceptedMessage: "demo file staged for local preview.",
      rejectedMessage: "file ignored. Accepted formats: PDF, JPG, PNG.",
      localPreview: "Local preview",
      uploadedList: "Uploaded file list",
      noBackend: "Demo mode — files are not sent to a backend.",
      empty:
        "No files staged yet. Add an invoice to see fake processing statuses appear here.",
      mockTable: "Mock result table",
      tableHeaders: ["File", "Vendor", "Total", "Risk", "Decision"],
      status: {
        queued: "Queued",
        extracting: "Extracting",
        validating: "Validating",
        ready: "Decision ready",
      },
      mockResults: [
        {
          file: "invoice_1042.pdf",
          vendor: "Nomad Office Supply",
          total: "$2,840.00",
          risk: "Clean",
          decision: "AUTO_POST",
        },
        {
          file: "invoice_1043.png",
          vendor: "Unknown Vendor",
          total: "$1,290.50",
          risk: "Unregistered vendor",
          decision: "HUMAN_APPROVAL",
        },
        {
          file: "invoice_1044.jpg",
          vendor: "Urban Logistics LLC",
          total: "$5,800.00",
          risk: "Duplicate invoice",
          decision: "DENY",
        },
      ],
    },
    qaSection: {
      eyebrow: "Aggregate Q&A",
      title: "Deterministic Mini Q&A Agent.",
      description:
        "The Mini Q&A Agent is deterministic and reads from `final_results_df` and `summary_df`, not from another LLM.",
      aggregateLabel: "Aggregate questions",
      invoiceLabel: "Invoice fact checks",
      questions: [
        {
          question: "Хэдэн invoice AUTO_POST болсон бэ?",
          answer: "AUTO_POST болсон invoice: 68.",
        },
        {
          question: "Хэдэн invoice HUMAN_APPROVAL болсон бэ?",
          answer: "HUMAN_APPROVAL шаардлагатай invoice: 15.",
        },
        {
          question: "Хэдэн invoice DENY болсон бэ?",
          answer: "DENY болсон invoice: 17.",
        },
        {
          question: "Хэдэн invoice duplicate байсан бэ?",
          answer: "Duplicate invoice: 10.",
        },
        {
          question: "Хэдэн invoice бүртгэлгүй vendor-той байсан бэ?",
          answer: "Unregistered vendor count: 0.",
        },
        {
          question: "Хэдэн invoice amount mismatch-тэй байсан бэ?",
          answer: "Amount mismatch count: 6.",
        },
        {
          question: "Аль category хамгийн их байна вэ?",
          answer: "AUTO_POST is the largest category in the verified final run.",
        },
      ],
      invoiceQuestions: [
        {
          question: "invoice_001.pdf final decision юу вэ?",
          answer: "invoice_001.pdf-ийн final decision: HUMAN_APPROVAL. Risk flags: AMOUNT_MISMATCH.",
        },
        {
          question: "invoice_095.png extraction status юу вэ?",
          answer: "invoice_095.png-ийн extraction status: FAILED.",
        },
        {
          question: "niit heden invoice burtgesen be?",
          answer: "Нийт 100 invoice байна.",
        },
      ],
    },
    outputsSection: {
      eyebrow: "Outputs",
      title: "CSV files ready for notebook, README, and review.",
      description:
        "The agent separates processed results so clean files, suspicious files, failed files, and final decisions are easy to inspect.",
      files: [
        {
          name: "all_results.csv",
          detail: "The full 100-invoice result table from the final notebook run.",
          icon: icons.table,
          badge: "CSV",
        },
        {
          name: "final_results.csv",
          detail:
            "Complete batch output with extraction fields, risk flags, and final decisions.",
          icon: icons.table,
          badge: "CSV",
        },
        {
          name: "clean_invoices.csv",
          detail: "Invoices that qualify for AUTO_POST after validation.",
          icon: icons.fileCheck,
          badge: "CSV",
        },
        {
          name: "suspicious_invoices.csv",
          detail: "Invoices routed to HUMAN_APPROVAL for accounting review.",
          icon: icons.alert,
          badge: "CSV",
        },
        {
          name: "failed_files.csv",
          detail: "Unreadable or invalid files that could not be processed reliably.",
          icon: icons.ban,
          badge: "CSV",
        },
        {
          name: "aggregate_summary.csv",
          detail: "One-row summary with the final notebook counts and metrics.",
          icon: icons.bar,
          badge: "CSV",
        },
        {
          name: "invoice_automation_final_outputs.zip",
          detail: "Notebook export bundle for judging, sharing, or download.",
          icon: icons.archive,
          badge: "ZIP",
        },
      ],
    },
    submission: {
      eyebrow: "Submission Narrative",
      title: "Built for Kaggle project storytelling.",
      description:
        "The website connects README structure, notebook flow, writeup sections, and demo video planning into one polished presentation surface.",
      items: [
        "README-ready project structure",
        "Kaggle writeup section mapping",
        "YouTube demo timeline support",
        "Business decision vocabulary",
      ],
    },
    notice: {
      text:
        "This website is a frontend presentation demo. The real invoice extraction, validation, decision logic, CSV export, and Mini Q&A Agent are implemented in the Kaggle notebook.",
      button: "Open demo UI",
    },
    footer: {
      eyebrow: "Project Links",
      title: "Ready for GitHub Pages deployment.",
      description:
        "The first three links are live. Demo video and Kaggle writeup remain disabled until their public URLs are ready.",
      placeholder: "TODO",
      brand: "Invoice Automation AI Agent",
      note: "Static demo site for Kaggle project submission.",
      links: commonLinks,
    },
  },
  mn: {
    nav: {
      workflow: "Workflow",
      features: "Features",
      results: "Results",
      links: "Links",
      signIn: "Нэвтрэх",
      languageLabel: "Хэл",
      menuLabel: "Цэс нээх",
    },
    drawer: [
      {
        title: "Project",
        items: [
          { label: "Overview", href: "#top" },
          { label: "Source Files", href: "#project-links" },
          { label: "Notebook", href: "#project-links" },
          { label: "README", href: "#project-links" },
          { label: "Writeup", href: "#project-links" },
        ],
      },
      {
        title: "Workspace",
        items: [
          { label: "Upload Demo", href: "#demo" },
          { label: "Processing History", href: "#results" },
          { label: "Result Table", href: "#demo" },
          { label: "Q&A Console", href: "#qa" },
          { label: "Decision Logs", href: "#decision" },
        ],
      },
      {
        title: "Outputs",
        items: [
          { label: "final_results.csv", href: "#outputs" },
          { label: "clean_invoices.csv", href: "#outputs" },
          { label: "suspicious_invoices.csv", href: "#outputs" },
          { label: "failed_files.csv", href: "#outputs" },
        ],
      },
      {
        title: "External Links",
        items: commonLinks.map((link) => ({
          label: link.label,
          href: link.href,
          disabled: link.disabled,
        })),
      },
    ],
    hero: {
      greeting: "Сайн байна уу танд хэрхэн туслах вэ ?",
      title: "Invoice workflow-оо AI-аар автоматжуул.",
      subtitle:
        "Өгөгдөл уншиж, итгэлтэй баталгаажуулж, эрсдэлийг үнэлээд санхүүгийн шийдвэрийг хурдан гаргана.",
      detail: "",
      searchPlaceholder: "Invoice-ийн талаар асуугаарай...",
      searchAction: "Workflow үзэх",
      quickTags: ["Vision/OCR уншилт", "Эрсдэл илрүүлэлт", "CSV гаралт"],
      cards: [
        {
          title: "GitHub",
          text: "Код, model, automation pipeline-уудыг үзэх.",
          href: "#project-links",
          icon: icons.github,
        },
        {
          title: "Analytics",
          text: "Шийдвэр, trend, санхүүгийн insight-уудыг хянах.",
          href: "#results",
          icon: icons.bar,
        },
        {
          title: "Live Demo",
          text: "Demo file ашиглан AI invoice workflow-г турших.",
          href: "#demo",
          icon: icons.play,
        },
      ],
    },
    problem: {
      eyebrow: "Асуудал",
      title: "Гараар invoice шалгах нь санхүүгийн багийг удаашруулдаг.",
      description:
        "Энэ төсөл нь эмх замбараагүй invoice файлуудыг нягтлангийн гараар шалгалтаас өмнө нотолгоотой бизнес шийдвэр болгон хувиргана.",
      cards: [
        {
          title: "Гараар шалгах нь удаан",
          text:
            "Нягтлангууд файл нээх, утга хуулах, нийт дүн шалгах, мастер дата хайхад олон цаг зарцуулдаг.",
          icon: icons.clock,
        },
        {
          title: "Жижиг алдаа эрсдэл болдог",
          text:
            "Нийт дүн, vendor нэр, invoice огноо, банкны данс, давхардсан invoice зэрэг алдааг хүн анзаарахгүй өнгөрч болно.",
          icon: icons.fileSearch,
        },
        {
          title: "Олон файлыг шалгах хэцүү",
          text:
            "Олон invoice зэрэг ирэх үед хүний баталгаажуулалтаас өмнө автомат triage хэрэгтэй.",
          icon: icons.layers,
        },
      ],
    },
    workflowSection: {
      eyebrow: "Agent Workflow",
      title: "Файлаас бизнес шийдвэр хүртэл.",
      description:
        "Workflow нь Kaggle notebook-д тайлбарлахад ил тод, санхүүгийн review process-д ашиглахад практик байна.",
      steps: [
        {
          title: "PDF/JPG/PNG Upload",
          detail: "Batch файлуудыг гараар хуулалгүй агент руу оруулна.",
          icon: icons.upload,
        },
        {
          title: "Vision/OCR Extraction",
          detail:
            "Groq Vision vendor, огноо, нийт дүн, line item, дансны талбаруудыг уншина.",
          icon: icons.scan,
        },
        {
          title: "Database Validation",
          detail:
            "Уншсан талбаруудыг vendor болон item-ийн мастер дататай тулгана.",
          icon: icons.database,
        },
        {
          title: "Risk Flagging",
          detail:
            "Мөнгө шилжихээс өмнө сэжигтэй invoice бүрийг эрсдэлийн шалтгаанаар тэмдэглэнэ.",
          icon: icons.shieldAlert,
        },
        {
          title: "Final Decision",
          detail: "Invoice бүр AUTO_POST, HUMAN_APPROVAL, DENY гэсэн шийдвэр авна.",
          icon: icons.clipboard,
        },
        {
          title: "CSV Output + Q&A",
          detail:
            "Цэвэр гаралтууд болон aggregate questions нь batch-ийн үр дүнг нэгтгэнэ.",
          icon: icons.table,
        },
      ],
    },
    featuresSection: {
      eyebrow: "Онцлогууд",
      title: "Invoice automation-д зориулсан төвлөрсөн боломжууд.",
      description:
        "Файлыг унших, бизнес өгөгдөл баталгаажуулах, эрсдэлийг ялгах, ашиглахад бэлэн гаралт үүсгэх ажлуудыг хамарна.",
      cards: [
        {
          title: "PDF/JPG/PNG invoice боловсруулах",
          text: "Нягтлан бодох үйл ажиллагаанд түгээмэл хэрэглэгддэг файлуудыг дэмжинэ.",
          icon: icons.fileImage,
        },
        {
          title: "Groq Vision field extraction",
          text:
            "Document image-ээс invoice-ийн гол талбаруудыг vision-first аргаар уншина.",
          icon: icons.brain,
        },
        {
          title: "Vendor validation",
          text: "Vendor-ийн мэдээллийг бүртгэлтэй мастер дататай тулгана.",
          icon: icons.badge,
        },
        {
          title: "Item validation",
          text: "Invoice line item-уудыг зөвшөөрөгдсөн бараа, үйлчилгээтэй харьцуулна.",
          icon: icons.list,
        },
        {
          title: "Amount mismatch detection",
          text: "Subtotal, tax, total, line-item зөрүүг илрүүлнэ.",
          icon: icons.circleDollar,
        },
        {
          title: "Duplicate invoice detection",
          text: "Invoice дугаар эсвэл vendor/огноо/дүнгийн давхардсан pattern илрүүлнэ.",
          icon: icons.layers,
        },
        {
          title: "Clean, suspicious, failed separation",
          text: "Файлуудыг clean, review, failed гаралтын бүлэгт ангилна.",
          icon: icons.archive,
        },
        {
          title: "Final decision logic",
          text: "Уншилт ба validation нотолгоог бизнес шийдвэр болгон хувиргана.",
          icon: icons.shieldCheck,
        },
      ],
    },
    riskSection: {
      eyebrow: "Risk Detection Rules",
      title: "Final posting хийхээс өмнөх тайлбарлагдах шалгалтууд.",
      description:
        "Агент зөвхөн текст уншихгүй. Invoice бүрийг ил тод эрсдэлийн шалтгаантай validation record болгоно.",
      rules: [
        {
          title: "Бүртгэлгүй vendor",
          text: "Vendor нэр, tax ID, supplier code нь итгэмжлэгдсэн мастер датад байхгүй.",
          icon: icons.shieldAlert,
        },
        {
          title: "Amount mismatch",
          text: "Line item, tax, subtotal, grand total цэвэр таарахгүй байна.",
          icon: icons.circleDollar,
        },
        {
          title: "Duplicate invoice",
          text: "Invoice дугаар эсвэл vendor/огноо/дүнгийн fingerprint давхардсан байна.",
          icon: icons.layers,
        },
        {
          title: "Огноо буруу эсвэл дутуу",
          text: "Invoice огноо хоосон, формат буруу, эсвэл accounting window-оос гадуур байна.",
          icon: icons.alert,
        },
        {
          title: "Шаардлагатай талбар дутуу",
          text: "Invoice number, vendor, total, currency зэрэг талбарууд байхгүй байна.",
          icon: icons.fileSearch,
        },
        {
          title: "Bank/account mismatch",
          text: "Төлбөрийн данс vendor-ийн баталгаажсан данстай таарахгүй байна.",
          icon: icons.wallet,
        },
      ],
    },
    decisionSection: {
      eyebrow: "Final Decision Logic",
      title: "Бизнес үйлдэлд зориулсан тодорхой шийдвэр.",
      description:
        "Final label нь Kaggle notebook доторх deterministic rule set-ээр гарна.",
      rules: [
        { label: "No risks → AUTO_POST", tone: "success" },
        { label: "Amount mismatch → HUMAN_APPROVAL", tone: "warning" },
        { label: "Invalid date → HUMAN_APPROVAL", tone: "warning" },
        { label: "Unregistered vendor → HUMAN_APPROVAL", tone: "warning" },
        { label: "Low-confidence extraction → HUMAN_APPROVAL", tone: "warning" },
        { label: "Extraction failed → HUMAN_APPROVAL", tone: "warning" },
        { label: "Bank account mismatch → DENY", tone: "danger" },
        { label: "Duplicate → DENY", tone: "danger" },
      ],
      decisions: [
        {
          label: "AUTO_POST",
          title: "No risks and valid totals",
          text: "Цэвэр invoice, итгэмжлэгдсэн vendor, зөв дүн нь AUTO_POST болно.",
          icon: icons.check,
          tone: "success",
        },
        {
          label: "HUMAN_APPROVAL",
          title: "Reviewable risk cases",
          text: "Amount mismatch, invalid date, unregistered vendor, low-confidence extraction, extraction failure нь review queue руу орно.",
          icon: icons.alert,
          tone: "warning",
        },
        {
          label: "DENY",
          title: "High-risk invoice",
          text: "Bank account mismatch болон duplicate invoice нь DENY болно.",
          icon: icons.xCircle,
          tone: "danger",
        },
      ],
      summary: [
        { label: "Нийт", value: "100", tone: "success", subtext: "Final verified run" },
        { label: "Clean", value: "68", tone: "success", subtext: "AUTO_POST-ready invoices" },
        { label: "Suspicious", value: "32", tone: "warning", subtext: "Needs review or deny" },
        { label: "AUTO_POST", value: "68", tone: "success", subtext: "Automatic posting" },
        { label: "HUMAN_APPROVAL", value: "15", tone: "warning", subtext: "Manual review queue" },
        { label: "DENY", value: "17", tone: "danger", subtext: "Blocked from posting" },
      ],
    },
    upload: {
      eyebrow: "Demo Upload UI",
      title: "Frontend-only invoice processing preview.",
      description:
        "Файлаа drag and drop хийж туршилтын UI-г үзнэ үү. Файлын нэр зөвхөн browser state-д хадгалагдах бөгөөд backend рүү илгээгдэхгүй.",
      dropTitle: "Invoice файлуудаа энд оруулна уу",
      dropText:
        "PDF, JPG, PNG дэмжинэ. Энэ demo нь local file name, simulated processing status, mock decision output харуулна.",
      chooseFiles: "Файл сонгох",
      acceptedMessage: "demo файл local preview-д бэлэн боллоо.",
      rejectedMessage: "файл алгасагдлаа. Зөвшөөрөх формат: PDF, JPG, PNG.",
      localPreview: "Local preview",
      uploadedList: "Оруулсан файлууд",
      noBackend: "Demo mode — files are not sent to a backend.",
      empty:
        "Одоогоор файл байхгүй. Invoice нэмэхэд fake processing status энд харагдана.",
      mockTable: "Mock result table",
      tableHeaders: ["Файл", "Vendor", "Нийт дүн", "Эрсдэл", "Шийдвэр"],
      status: {
        queued: "Дараалалд",
        extracting: "Уншиж байна",
        validating: "Шалгаж байна",
        ready: "Шийдвэр бэлэн",
      },
      mockResults: [
        {
          file: "invoice_1042.pdf",
          vendor: "Nomad Office Supply",
          total: "$2,840.00",
          risk: "Цэвэр",
          decision: "AUTO_POST",
        },
        {
          file: "invoice_1043.png",
          vendor: "Unknown Vendor",
          total: "$1,290.50",
          risk: "Бүртгэлгүй vendor",
          decision: "HUMAN_APPROVAL",
        },
        {
          file: "invoice_1044.jpg",
          vendor: "Urban Logistics LLC",
          total: "$5,800.00",
          risk: "Duplicate invoice",
          decision: "DENY",
        },
      ],
    },
    qaSection: {
      eyebrow: "Aggregate Q&A",
      title: "Deterministic Mini Q&A Agent.",
      description:
        "Mini Q&A Agent нь deterministic бөгөөд `final_results_df` болон `summary_df`-ээс уншина, өөр LLM ашиглахгүй.",
      aggregateLabel: "Aggregate questions",
      invoiceLabel: "Invoice fact checks",
      questions: [
        {
          question: "Хэдэн invoice AUTO_POST болсон бэ?",
          answer: "AUTO_POST болсон invoice: 68.",
        },
        {
          question: "Хэдэн invoice HUMAN_APPROVAL болсон бэ?",
          answer: "HUMAN_APPROVAL шаардлагатай invoice: 15.",
        },
        {
          question: "Хэдэн invoice DENY болсон бэ?",
          answer: "DENY болсон invoice: 17.",
        },
        {
          question: "Хэдэн invoice duplicate байсан бэ?",
          answer: "Duplicate invoice: 10.",
        },
        {
          question: "Хэдэн invoice бүртгэлгүй vendor-той байсан бэ?",
          answer: "Unregistered vendor count: 0.",
        },
        {
          question: "Хэдэн invoice amount mismatch-тэй байсан бэ?",
          answer: "Amount mismatch count: 6.",
        },
        {
          question: "Аль category хамгийн их байна вэ?",
          answer: "AUTO_POST is the largest category in the verified final run.",
        },
      ],
      invoiceQuestions: [
        {
          question: "invoice_001.pdf final decision юу вэ?",
          answer: "invoice_001.pdf-ийн final decision: HUMAN_APPROVAL. Risk flags: AMOUNT_MISMATCH.",
        },
        {
          question: "invoice_095.png extraction status юу вэ?",
          answer: "invoice_095.png-ийн extraction status: FAILED.",
        },
        {
          question: "niit heden invoice burtgesen be?",
          answer: "Нийт 100 invoice байна.",
        },
      ],
    },
    outputsSection: {
      eyebrow: "Outputs",
      title: "Notebook, README, review-д бэлэн CSV файлууд.",
      description:
        "Агент clean, suspicious, failed, final decision гаралтуудыг тусгаарлаж шалгахад хялбар болгоно.",
      files: [
        {
          name: "all_results.csv",
          detail: "100 invoice-ийн бүрэн нэг мөрт хүснэгт.",
          icon: icons.table,
          badge: "CSV",
        },
        {
          name: "final_results.csv",
          detail: "Extraction fields, risk flags, final decisions бүхий бүрэн batch output.",
          icon: icons.table,
          badge: "CSV",
        },
        {
          name: "clean_invoices.csv",
          detail: "Validation дараа AUTO_POST болох invoice-ууд.",
          icon: icons.fileCheck,
          badge: "CSV",
        },
        {
          name: "suspicious_invoices.csv",
          detail: "HUMAN_APPROVAL review queue руу шилжсэн invoice-ууд.",
          icon: icons.alert,
          badge: "CSV",
        },
        {
          name: "failed_files.csv",
          detail: "Найдвартай боловсруулж чадаагүй уншигдахгүй эсвэл буруу файлууд.",
          icon: icons.ban,
          badge: "CSV",
        },
        {
          name: "aggregate_summary.csv",
          detail: "Final count summary болон нийт үр дүнгийн нэг мөр файл.",
          icon: icons.bar,
          badge: "CSV",
        },
        {
          name: "invoice_automation_final_outputs.zip",
          detail: "Notebook export bundle for judging, sharing, or download.",
          icon: icons.archive,
          badge: "ZIP",
        },
      ],
    },
    submission: {
      eyebrow: "Submission Narrative",
      title: "Kaggle project storytelling-д бэлэн.",
      description:
        "README бүтэц, notebook flow, writeup sections, demo video plan-ийг нэг polished presentation surface дээр холбож өгнө.",
      items: [
        "README-д бэлэн project structure",
        "Kaggle writeup section mapping",
        "YouTube demo timeline support",
        "Business decision vocabulary",
      ],
    },
    notice: {
      text:
        "This website is a frontend presentation demo. The real invoice extraction, validation, decision logic, CSV export, and Mini Q&A Agent are implemented in the Kaggle notebook.",
      button: "Demo UI нээх",
    },
    footer: {
      eyebrow: "Project Links",
      title: "GitHub Pages deployment-д бэлэн.",
      description:
        "Notebook болон GitHub repository live link-үүд active. Demo video болон writeup link-үүд TODO байсаар байна.",
      placeholder: "TODO",
      brand: "Invoice Automation AI Agent",
      note: "Kaggle project submission-д зориулсан static demo site.",
      links: commonLinks,
    },
  },
};
