import Image from "next/image";

type Props = {
  author: "user" | "bot";
  text: string;
  sources?: string[];
};

export default function ChatBubble({ author, text, sources }: Props) {
  const isUser = author === "user";
  const avatarSrc = isUser ? "/avatar-user.png" : "/avatar-bot.png";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div className="flex items-start gap-2 max-w-[80%]">
        {!isUser && (
          <Image
            src={avatarSrc}
            alt="Bot avatar"
            width={32}
            height={32}
            className="rounded-full"
          />
        )}

        <div
          className={`rounded-xl px-4 py-2 text-sm shadow ${
            isUser
              ? "bg-blue-600 text-white rounded-br-none"
              : "bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-bl-none"
          }`}
        >
          <div>{text}</div>
          {Array.isArray(sources) && sources.length > 0 && (
            <div className="text-xs mt-2 text-blue-400">
              Source(s): {sources.join(", ")}
            </div>
          )}
        </div>

        {isUser && (
          <Image
            src={avatarSrc}
            alt="User avatar"
            width={32}
            height={32}
            className="rounded-full"
          />
        )}
      </div>
    </div>
  );
}