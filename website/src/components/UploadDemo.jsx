import { useEffect, useRef, useState } from "react";
import {
  CheckCircle2,
  FileImage,
  FileText,
  Loader2,
  UploadCloud,
  XCircle,
} from "lucide-react";
import MotionSection from "./MotionSection.jsx";
import SectionTitle from "./SectionTitle.jsx";

const acceptedExtensions = [".pdf", ".jpg", ".jpeg", ".png"];

function formatBytes(bytes) {
  if (!bytes) return "0 KB";
  return `${Math.max(bytes / 1024, 1).toFixed(1)} KB`;
}

function isAccepted(file) {
  const lowerName = file.name.toLowerCase();
  return acceptedExtensions.some((extension) => lowerName.endsWith(extension));
}

function nextStatus(status) {
  if (status === "queued") return "extracting";
  if (status === "extracting") return "validating";
  if (status === "validating") return "ready";
  return status;
}

function UploadDemo({ content }) {
  const inputRef = useRef(null);
  const [files, setFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!files.some((file) => file.status !== "ready")) return;

    const timer = window.setInterval(() => {
      setFiles((current) =>
        current.map((file) => ({ ...file, status: nextStatus(file.status) })),
      );
    }, 900);

    return () => window.clearInterval(timer);
  }, [files]);

  function handleFileList(fileList) {
    const nextFiles = Array.from(fileList);
    const accepted = nextFiles.filter(isAccepted);
    const rejected = nextFiles.length - accepted.length;

    if (accepted.length) {
      const mapped = accepted.map((file, index) => ({
        id: `${file.name}-${file.size}-${Date.now()}-${index}`,
        name: file.name,
        size: file.size,
        type: file.type || "invoice file",
        status: "queued",
      }));
      setFiles((current) => [...mapped, ...current].slice(0, 6));
      setMessage(`${accepted.length} ${content.acceptedMessage}`);
    }

    if (rejected) {
      setMessage(`${rejected} ${content.rejectedMessage}`);
    }
  }

  function handleDrop(event) {
    event.preventDefault();
    setIsDragging(false);
    handleFileList(event.dataTransfer.files);
  }

  return (
    <MotionSection className="section-pad" id="demo">
      <div className="mx-auto max-w-[1480px] px-5 sm:px-8 lg:px-12">
        <SectionTitle
          eyebrow={content.eyebrow}
          title={content.title}
          description={content.description}
        />

        <div className="demo-shell mt-12">
          <div
            className={`upload-zone ${isDragging ? "upload-zone-active" : ""}`}
            onDragEnter={() => setIsDragging(true)}
            onDragLeave={() => setIsDragging(false)}
            onDragOver={(event) => event.preventDefault()}
            onDrop={handleDrop}
          >
            <input
              ref={inputRef}
              className="sr-only"
              type="file"
              multiple
              accept=".pdf,.jpg,.jpeg,.png,application/pdf,image/jpeg,image/png"
              onChange={(event) => handleFileList(event.target.files)}
            />
            <div className="upload-icon">
              <UploadCloud size={28} />
            </div>
            <h3>{content.dropTitle}</h3>
            <p>{content.dropText}</p>
            <button
              className="primary-soft-button mt-7"
              type="button"
              onClick={() => inputRef.current?.click()}
            >
              <FileText size={18} />
              {content.chooseFiles}
            </button>
            {message && (
              <p className="mt-5 text-sm font-medium text-emerald-700" role="status">
                {message}
              </p>
            )}
          </div>

          <div className="file-panel">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="eyebrow">{content.localPreview}</p>
                <h3 className="mt-2 text-2xl font-semibold tracking-tight text-stone-950">
                  {content.uploadedList}
                </h3>
              </div>
              <span className="soft-label">{content.noBackend}</span>
            </div>

            <div className="mt-7 space-y-3">
              {files.length === 0 ? (
                <div className="empty-state">{content.empty}</div>
              ) : (
                files.map((file) => (
                  <div className="file-row" key={file.id}>
                    <span className="icon-soft shrink-0">
                      <FileImage size={18} />
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-semibold text-stone-950">
                        {file.name}
                      </p>
                      <p className="text-xs text-stone-400">
                        {formatBytes(file.size)} · {file.type}
                      </p>
                    </div>
                    <StatusBadge status={file.status} labels={content.status} />
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        <div className="result-table mt-6">
          <div className="border-b border-stone-200/80 px-6 py-5">
            <p className="eyebrow">{content.mockTable}</p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px] text-left text-sm">
              <thead>
                <tr>
                  {content.tableHeaders.map((header) => (
                    <th key={header}>{header}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {content.mockResults.map((row) => (
                  <tr key={row.file}>
                    <td className="font-semibold text-stone-950">{row.file}</td>
                    <td>{row.vendor}</td>
                    <td>{row.total}</td>
                    <td>{row.risk}</td>
                    <td>
                      <DecisionPill decision={row.decision} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </MotionSection>
  );
}

function StatusBadge({ status, labels }) {
  const ready = status === "ready";
  return (
    <span className={ready ? "status-ready" : "status-working"}>
      {ready ? <CheckCircle2 size={14} /> : <Loader2 className="animate-spin" size={14} />}
      {labels[status]}
    </span>
  );
}

function DecisionPill({ decision }) {
  const styles = {
    AUTO_POST: "decision-success",
    HUMAN_APPROVAL: "decision-warning",
    DENY: "decision-danger",
  };

  return (
    <span className={`decision-badge ${styles[decision]}`}>
      {decision === "DENY" ? <XCircle size={14} /> : <CheckCircle2 size={14} />}
      {decision}
    </span>
  );
}

export default UploadDemo;
