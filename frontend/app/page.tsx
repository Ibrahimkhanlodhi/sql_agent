"use client";

import { useState } from "react";
import ChatInterface from "./components/ChatInterface";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 text-white flex flex-col">
      <header className="border-b border-gray-800 px-6 py-4 flex items-center gap-3">
        <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center text-sm font-bold">
          SQL
        </div>
        <div>
          <h1 className="font-semibold text-white">SQL Agent</h1>
          <p className="text-xs text-gray-400">Chat with your database in plain English</p>
        </div>
      </header>
      <ChatInterface />
    </main>
  );
}