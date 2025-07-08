type Props = {
  userId: string | null;
  chatHistory: { author: string; text: string; sources?: string[] }[];
  setMessages: (value: any) => void;
  setChatHistory: (value: any) => void;
};

export default function ChatToolbar({ userId, chatHistory, setMessages, setChatHistory }: Props) {
  const handleDownload = () => {
    if (!userId || chatHistory.length === 0) return;
    const lines = chatHistory.map((msg) => {
      const author = msg.author === "user" ? "Vous" : "Assistant";
      const sources = Array.isArray(msg.sources) && msg.sources.length > 0
        ? `\nSources: ${msg.sources.join(", ")}`
        : "";
      return `${author}: ${msg.text}${sources}\n`;
    });
    const blob = new Blob([lines.join("\n")], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "historique_chat.txt";
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleClear = () => {
    if (!userId) return;
    localStorage.removeItem(`chatHistory_${userId}`);
    setChatHistory([]);
    setMessages([]);
  };

  return (
    <div className="flex gap-2 mb-4">
      <button onClick={handleClear} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">Effacer</button>
      <button onClick={handleDownload} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Télécharger</button>
    </div>
  );
}
