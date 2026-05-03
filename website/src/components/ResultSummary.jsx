const toneClass = {
  success: "text-emerald-700 bg-emerald-50",
  warning: "text-amber-700 bg-amber-50",
  danger: "text-rose-700 bg-rose-50",
};

function ResultSummary({ items }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {items.map((item) => (
        <div className="result-tile" key={item.label}>
          <span className={`result-chip ${toneClass[item.tone]}`}>{item.label}</span>
          <strong>{item.value}</strong>
          <span>{item.subtext || "final notebook run"}</span>
        </div>
      ))}
    </div>
  );
}

export default ResultSummary;
