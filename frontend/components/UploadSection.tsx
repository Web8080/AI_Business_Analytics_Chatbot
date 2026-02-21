"use client";
/* Victor.I - CSV upload with drag-drop and schema summary. */
import { useCallback, useState } from "react";

const MAX_MB = 200;
const MAX_BYTES = MAX_MB * 1024 * 1024;

export interface UploadResult {
  dataset_id: string;
  filename: string;
  rows: number;
  columns: number;
  column_names: string[];
  column_types?: { name: string; type: string }[];
}

type Props = {
  onUploaded: (result: UploadResult) => void;
  uploadCsv: (file: File) => Promise<UploadResult>;
};

export function UploadSection({ onUploaded, uploadCsv }: Props) {
  const [drag, setDrag] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const doUpload = useCallback(
    async (file: File) => {
      if (!file.name.toLowerCase().endsWith(".csv")) {
        setError("Only CSV files are allowed.");
        return;
      }
      if (file.size > MAX_BYTES) {
        setError(`File too large. Limit ${MAX_MB}MB per file.`);
        return;
      }
      setError(null);
      setLoading(true);
      try {
        const result = await uploadCsv(file);
        onUploaded(result);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Upload failed.");
      } finally {
        setLoading(false);
      }
    },
    [onUploaded, uploadCsv]
  );

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDrag(false);
      const file = e.dataTransfer.files[0];
      if (file) doUpload(file);
    },
    [doUpload]
  );
  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDrag(true);
  }, []);
  const onDragLeave = useCallback(() => setDrag(false), []);

  const onFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) doUpload(file);
      e.target.value = "";
    },
    [doUpload]
  );

  return (
    <section className="space-y-3">
      <h2 className="text-lg font-semibold">Upload Data</h2>
      <div
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        className={`border-2 border-dashed rounded-xl p-6 text-center transition-colors ${
          drag ? "border-sky-400 bg-sky-50" : "border-sky-300 bg-white"
        }`}
      >
        <p className="mb-2 text-sm text-slate-500">
          Limit {MAX_MB}MB per file. CSV only.
        </p>
        <p className="mb-4 text-slate-700">Drag and drop file here</p>
        <label className="inline-block cursor-pointer rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700">
          Browse files
          <input
            type="file"
            accept=".csv"
            className="hidden"
            onChange={onFileInput}
            disabled={loading}
          />
        </label>
      </div>
      {loading && (
        <p className="text-sm text-sky-600">Uploading and parsing...</p>
      )}
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </section>
  );
}
