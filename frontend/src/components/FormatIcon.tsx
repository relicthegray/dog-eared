import { Book, BookOpen, Headphones, Tablet } from "lucide-react";

type Props = {
  format?: string | null; // "Hardcover" | "Paperback" | "Kindle" | "Audiobook" etc
  className?: string;
};

export function FormatIcon({ format, className }: Props) {
  const f = (format ?? "").toLowerCase();

  if (f.includes("audio")) return <Headphones className={className} aria-label="Audiobook" />;
  if (f.includes("kindle") || f.includes("ebook") || f.includes("e-book")) return <Tablet className={className} aria-label="Ebook" />;
  if (f.includes("paper")) return <BookOpen className={className} aria-label="Paperback" />;
  if (f.includes("hard")) return <Book className={className} aria-label="Hardcover" />;

  return <Book className={className} aria-label="Book" />;
}
