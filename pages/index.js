import Head from "next/head";
import Chatbot from "../components/Chatbot";

export default function Home() {
  return (
    <>
      <Head>
        <title>Chatbot IA Générative</title>
      </Head>
      <main className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
        <Chatbot />
      </main>
    </>
  );
}
