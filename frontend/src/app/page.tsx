"use client";
import ChatBox from "@/components/ChatBox";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-300 dark:from-gray-900 dark:to-gray-800 p-4">
      <ChatBox />
    </main>
  );
}
