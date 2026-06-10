import Link from 'next/link';

const FOOTER_LINKS = [
  ['FAQ', '/faq'],
  ['Help Centre', '/help'],
  ['Account', '/account'],
  ['Media Centre', '/press'],
  ['Investor Relations', '/ir'],
  ['Jobs', '/jobs'],
  ['Terms of Use', '/terms'],
  ['Privacy', '/privacy'],
  ['Cookie Preferences', '/cookies'],
  ['Corporate Information', '/corporate'],
  ['Contact Us', '/contact'],
];

export function Footer() {
  return (
    <footer className="bg-[#141414] border-t border-zinc-800 px-4 sm:px-8 lg:px-12 py-12 mt-auto">
      <div className="max-w-4xl mx-auto">
        <p className="text-zinc-400 text-sm mb-6">
          Questions? Call{' '}
          <a href="tel:1-800-000-0000" className="hover:underline">
            1-800-000-0000
          </a>
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 mb-8">
          {FOOTER_LINKS.map(([label, href]) => (
            <Link
              key={href}
              href={href}
              className="text-zinc-500 text-xs hover:text-zinc-300 transition-colors underline"
            >
              {label}
            </Link>
          ))}
        </div>

        <div className="mb-6">
          <select className="bg-transparent border border-zinc-600 text-zinc-400 text-sm px-3 py-1.5 rounded">
            <option value="en">English</option>
            <option value="es">Español</option>
            <option value="fr">Français</option>
          </select>
        </div>

        <p className="text-zinc-600 text-xs">
          &copy; {new Date().getFullYear()} StreamFlix, Inc.
        </p>
      </div>
    </footer>
  );
}
