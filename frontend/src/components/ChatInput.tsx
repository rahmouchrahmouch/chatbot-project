type Props = {
  input: string;
  setInput: (value: string) => void;
  handleSend: () => void;
  handleKeyDown: (e: React.KeyboardEvent) => void;
};

export default function ChatInput({ input, setInput, handleSend, handleKeyDown }: Props) {
  return (
    <div className="mt-4 flex gap-2">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={1}
        placeholder="Écris ta question ici..."
        aria-label="Zone de saisie"
        className="flex-1 resize-none rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        onClick={handleSend}
        disabled={!input.trim()}
        className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl transition disabled:bg-blue-300"
      >
        Envoyer
      </button>
    </div>
  );
}