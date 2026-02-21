"use client";
/* Victor.I - Single chat message (user or assistant) with optional confidence. */
type Props = {
  role: "user" | "assistant";
  content: string;
  confidence?: number;
};

export function ChatMessage({ role, content, confidence }: Props) {
  const isUser = role === "user";
  return (
    <div
      className={`max-w-[85%] rounded-xl p-3 ${
        isUser
          ? "ml-auto bg-sky-600 text-white"
          : "mr-auto bg-sky-50 text-slate-900 border border-sky-200"
      }`}
    >
      <p className="mb-1 text-xs font-medium opacity-80">
        {isUser ? "You" : "AI Assistant"}
      </p>
      <div className="whitespace-pre-wrap text-sm">{content}</div>
      {!isUser && confidence != null && (
        <p className="mt-2 text-xs text-sky-700">
          Confidence: {Math.round(confidence * 100)}%
        </p>
      )}
    </div>
  );
}
