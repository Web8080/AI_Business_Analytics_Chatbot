"use client";
import Link from "next/link";

export function NavBar() {
  return (
    <header className="sticky top-0 z-10 border-b border-sky-200 bg-white shadow-sm">
      <nav className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <QueryLensLogoSvg />
          <span className="text-xl font-bold tracking-tight text-sky-900">
            AI QueryLens
          </span>
        </div>
        <ul className="flex items-center gap-1">
          <li>
            <Link
              href="/"
              className="rounded-lg px-4 py-2 text-sm font-medium text-sky-800 transition-colors hover:bg-sky-50"
            >
              Dashboard
            </Link>
          </li>
          <li>
            <Link
              href="/"
              className="rounded-lg px-4 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-sky-50 hover:text-sky-800"
            >
              New analysis
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}

function QueryLensLogoSvg() {
  return (
    <svg
      width="36"
      height="36"
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="shrink-0"
      aria-hidden
    >
      <circle
        cx="16"
        cy="14"
        r="8"
        stroke="currentColor"
        strokeWidth="2.5"
        className="text-sky-700"
        fill="none"
      />
      <path
        d="M20 18l6 6"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        className="text-sky-700"
      />
      <path
        d="M10 22v4h2.5v-4M13 22v4h2.5v-4M16 22v4h2.5v-4"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        className="text-sky-600"
      />
    </svg>
  );
}
