export default function TypingIndicator() {
  return (
    <div className="flex items-center gap-2 text-sm italic text-gray-500 dark:text-gray-400 animate-pulse">
      <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75" />
      <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150" />
      <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-300" />
      <span>L'assistant écrit...</span>
    </div>
  );
}