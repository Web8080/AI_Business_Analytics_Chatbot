import type { Metadata } from "next";
import "./globals.css";
import { NavBar } from "@/components/NavBar";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "AI QueryLens – Conversational Analytics",
  description: "Ask questions about your data in plain language. AI QueryLens.",
  icons: {
    icon: "/querylens-logo.png",
    apple: "/querylens-logo.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/querylens-logo.png" sizes="32x32" type="image/png" />
      </head>
      <body className="min-h-screen flex flex-col">
        <NavBar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
