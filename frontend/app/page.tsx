"use client";
import { useState, useCallback } from "react";
import { uploadCsv, query, getPreview, type UploadResponse, type ChartData } from "@/lib/api";
import { UploadSection } from "@/components/UploadSection";
import { PreviewTable } from "@/components/PreviewTable";
import { ChatMessage } from "@/components/ChatMessage";
import { ChartDisplay } from "@/components/ChartDisplay";
import { ChatInput } from "@/components/ChatInput";

type Message = {
  role: "user" | "assistant";
  content: string;
  chartData?: ChartData | null;
  confidence?: number;
};

export default function DashboardPage() {
  const [dataset, setDataset] = useState<UploadResponse | null>(null);
  const [preview, setPreview] = useState<{ rows: Record<string, unknown>[]; columns: string[] } | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const handleUploaded = useCallback(async (result: UploadResponse) => {
    setDataset(result);
    try {
      const p = await getPreview(result.dataset_id);
      setPreview(p);
    } catch {
      setPreview({ rows: [], columns: result.column_names || [] });
    }
  }, []);

  const handleSend = useCallback(
    async (question: string) => {
      if (!dataset) return;
      setMessages((m) => [...m, { role: "user", content: question }]);
      setLoading(true);
      try {
        const res = await query(dataset.dataset_id, question);
        setMessages((m) => [
          ...m,
          {
            role: "assistant",
            content: res.answer,
            chartData: res.chart_data,
            confidence: res.confidence,
          },
        ]);
      } catch (e) {
        setMessages((m) => [
          ...m,
          {
            role: "assistant",
            content: e instanceof Error ? e.message : "Request failed.",
          },
        ]);
      } finally {
        setLoading(false);
      }
    },
    [dataset]
  );

  return (
    <div className="min-h-full flex flex-col">
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 p-6">
        <aside className="lg:col-span-1 space-y-6 rounded-xl border border-sky-200 bg-white p-5 shadow-md">
          <UploadSection onUploaded={handleUploaded} uploadCsv={uploadCsv} />
          {dataset && preview && (
            <PreviewTable
              rows={preview.rows}
              columns={preview.columns}
              columnTypes={dataset.column_types}
              rowsCount={dataset.rows}
              colsCount={dataset.columns}
            />
          )}
        </aside>
        <section className="lg:col-span-2 flex flex-col rounded-xl border border-neutral-200 bg-white p-5 shadow-sm">
          {!dataset ? (
            <div className="flex flex-1 items-center justify-center text-slate-500">
              Upload a CSV file to start asking questions.
            </div>
          ) : (
            <>
              <div className="flex-1 overflow-y-auto space-y-4 min-h-0">
                {messages.length === 0 && dataset.suggested_questions && dataset.suggested_questions.length > 0 && (
                  <div className="rounded-lg border border-sky-200 bg-sky-50/50 p-4">
                    <p className="mb-2 text-sm font-medium text-sky-900">Try asking</p>
                    <div className="flex flex-wrap gap-2">
                      {dataset.suggested_questions.map((q, i) => (
                        <button
                          key={i}
                          type="button"
                          onClick={() => handleSend(q)}
                          disabled={loading}
                          className="rounded-full border border-sky-300 bg-white px-3 py-1.5 text-sm text-sky-800 shadow-sm hover:bg-sky-50 disabled:opacity-50"
                        >
                          {q}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                {messages.map((msg, i) => (
                  <div key={i}>
                    <ChatMessage
                      role={msg.role}
                      content={msg.content}
                      confidence={msg.confidence}
                    />
                    {msg.chartData && (
                      <ChartDisplay chartData={msg.chartData} />
                    )}
                  </div>
                ))}
                {loading && (
                  <p className="text-sm text-sky-600">Analyzing...</p>
                )}
              </div>
              <ChatInput disabled={loading} onSend={handleSend} />
            </>
          )}
        </section>
      </div>
    </div>
  );
}
