"use client";

import { useState, useRef, useEffect } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
  sql_queries?: string[];
  isLoading?: boolean;
};

const EXAMPLES = [
  "Who are the top 5 customers by total spending?",
  "What is the best-selling product by quantity?",
  "How many orders were placed per country?",
  "Which product category generates the most revenue?",
];

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (question: string) => {
    if (!question.trim() || loading) return;

    const userMessage: Message = { role: "user", content: question };
    const loadingMessage: Message = { role: "assistant", content: "", isLoading: true };

    setMessages((prev) => [...prev, userMessage, loadingMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("https://sqlagent-production-f7d2.up.railway.app/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { role: "assistant", content: data.answer, sql_queries: data.sql_queries },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { role: "assistant", content: "Failed to connect to the API. Make sure the backend is running on port 8000." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 61px)", maxWidth: 720, margin: "0 auto", width: "100%", padding: "24px 16px", gap: 16 }}>

      {/* Empty state */}
      {messages.length === 0 && (
        <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 24, textAlign: "center" }}>
          <div>
            <h2 style={{ fontSize: 20, fontWeight: 600, color: "white", marginBottom: 8 }}>Ask anything about your data</h2>
            <p style={{ color: "#9ca3af", fontSize: 14 }}>No SQL knowledge needed. Just type in plain English.</p>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, width: "100%" }}>
            {EXAMPLES.map((ex) => (
              <button
                key={ex}
                onClick={() => sendMessage(ex)}
                style={{ textAlign: "left", fontSize: 13, background: "#111827", border: "1px solid #374151", borderRadius: 12, padding: "12px 16px", color: "#d1d5db", cursor: "pointer" }}
                onMouseOver={(e) => { (e.currentTarget as HTMLButtonElement).style.borderColor = "#10b981"; (e.currentTarget as HTMLButtonElement).style.color = "white"; }}
                onMouseOut={(e) => { (e.currentTarget as HTMLButtonElement).style.borderColor = "#374151"; (e.currentTarget as HTMLButtonElement).style.color = "#d1d5db"; }}
              >
                {ex}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 16, overflowY: "auto" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ display: "flex", justifyContent: msg.role === "user" ? "flex-end" : "flex-start" }}>
            {msg.role === "user" ? (
              <div style={{ background: "#059669", color: "white", borderRadius: "18px 18px 4px 18px", padding: "10px 16px", maxWidth: "80%", fontSize: 14 }}>
                {msg.content}
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 6, maxWidth: "90%" }}>
                {msg.isLoading ? (
                  <div style={{ background: "#111827", border: "1px solid #1f2937", borderRadius: "18px 18px 18px 4px", padding: "12px 16px" }}>
                    <div style={{ display: "flex", gap: 4 }}>
                      {[0, 150, 300].map((delay) => (
                        <div key={delay} style={{ width: 8, height: 8, background: "#10b981", borderRadius: "50%", animation: `bounce 1s ${delay}ms infinite` }} />
                      ))}
                    </div>
                  </div>
                ) : (
                  <>
                    <div style={{ background: "#111827", border: "1px solid #1f2937", borderRadius: "18px 18px 18px 4px", padding: "12px 16px", fontSize: 14, color: "#f3f4f6", whiteSpace: "pre-wrap" }}>
                      {msg.content}
                    </div>
                    {msg.sql_queries && msg.sql_queries.length > 0 && <SQLBlock queries={msg.sql_queries} />}
                  </>
                )}
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div style={{ display: "flex", gap: 8, alignItems: "flex-end" }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              sendMessage(input);
            }
          }}
          placeholder="Ask a question about your data..."
          rows={1}
          style={{ flex: 1, background: "#111827", border: "1px solid #374151", borderRadius: 12, padding: "12px 16px", fontSize: 14, color: "white", resize: "none", outline: "none", fontFamily: "inherit" }}
          onFocus={(e) => (e.currentTarget.style.borderColor = "#10b981")}
          onBlur={(e) => (e.currentTarget.style.borderColor = "#374151")}
        />
        <button
          onClick={() => sendMessage(input)}
          disabled={loading || !input.trim()}
          style={{ background: loading || !input.trim() ? "#064e3b" : "#059669", color: "white", border: "none", borderRadius: 12, padding: "12px 20px", fontSize: 14, fontWeight: 500, cursor: loading || !input.trim() ? "not-allowed" : "pointer", opacity: loading || !input.trim() ? 0.5 : 1, transition: "all 0.2s" }}
        >
          {loading ? "..." : "Send"}
        </button>
      </div>

      <style>{`@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }`}</style>
    </div>
  );
}

function SQLBlock({ queries }: { queries: string[] }) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ fontSize: 12 }}>
      <button onClick={() => setOpen(!open)} style={{ background: "none", border: "none", color: "#6b7280", cursor: "pointer", display: "flex", alignItems: "center", gap: 4 }}>
        <span>{open ? "▾" : "▸"}</span>
        <span>Generated SQL ({queries.length} {queries.length === 1 ? "query" : "queries"})</span>
      </button>
      {open && (
        <div style={{ marginTop: 4, display: "flex", flexDirection: "column", gap: 4 }}>
          {queries.map((q, i) => (
            <pre key={i} style={{ background: "#030712", border: "1px solid #1f2937", borderRadius: 8, padding: "8px 12px", color: "#34d399", overflowX: "auto", whiteSpace: "pre-wrap", margin: 0, fontSize: 12 }}>
              {q}
            </pre>
          ))}
        </div>
      )}
    </div>
  );
}