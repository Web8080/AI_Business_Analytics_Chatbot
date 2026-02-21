"use client";
/* Victor.I - Chat input and send; triggers onSend(question). */
import { useState, useCallback } from "react";

type Props = {
  disabled?: boolean;
  onSend: (question: string) => void;
};

export function ChatInput({ disabled, onSend }: Props) {
  const [value, setValue] = useState("");
  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      const q = value.trim();
      if (!q || disabled) return;
      onSend(q);
      setValue("");
    },
    [value, disabled, onSend]
  );
  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mt-4">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Ask a question about your data..."
        className="flex-1 rounded-lg border border-sky-200 bg-white px-4 py-2 text-slate-900 placeholder-slate-400 focus:border-sky-400 focus:outline-none focus:ring-1 focus:ring-sky-400"
        disabled={disabled}
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Send
      </button>
    </form>
  );
}
