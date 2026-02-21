"use client";

const FOOTER_LINK = "https://xtxinnovations.com";

export function Footer() {
  return (
    <footer className="mt-auto border-t border-sky-200 bg-white py-4 text-center text-sm text-slate-600">
      <p>
        Created with love by Victor Ibhafidon for XTX_Innovations. Visit{" "}
        <a
          href={FOOTER_LINK}
          target="_blank"
          rel="noopener noreferrer"
          className="font-medium text-sky-700 underline decoration-sky-300 underline-offset-2 hover:text-sky-800"
        >
          xtxinnovations.com
        </a>{" "}
        for more AI tools like this.
      </p>
    </footer>
  );
}
