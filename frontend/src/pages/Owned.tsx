import { useEffect, useState } from "react";
import PageShell from "../components/PageShell";
import { apiGet, apiPost } from "../app/api";

type OwnedItem = {
  id: string;
  title: string;
  author?: string | null;
  format: string;
  is_favorite: boolean;
  acquired_at?: string | null;
  notes?: string | null;
  created_at: string;
};

const formats = ["hardcover", "paperback", "ebook", "audiobook", "other"] as const;

export default function Owned() {
  const [items, setItems] = useState<OwnedItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [format, setFormat] = useState<(typeof formats)[number]>("hardcover");
  const [favorite, setFavorite] = useState(false);
  const [notes, setNotes] = useState("");

  async function load() {
    setError(null);
    setLoading(true);
    try {
      const data = await apiGet<OwnedItem[]>("/owned");
      setItems(data);
    } catch (err: any) {
      setError(err?.message ?? "Failed to load Owned shelf.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function addOwned(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!title.trim()) {
      setError("Title is required.");
      return;
    }

    try {
      await apiPost("/owned", {
        title,
        author: author || null,
        format,
        is_favorite: favorite,
        notes: notes || null,
      });

      setTitle("");
      setAuthor("");
      setFormat("hardcover");
      setFavorite(false);
      setNotes("");

      await load();
    } catch (err: any) {
      setError(err?.message ?? "Failed to add Owned item.");
    }
  }

  const trophies = items.filter((x) => x.is_favorite);
  const shelf = items.filter((x) => !x.is_favorite);

  return (
    <PageShell title="Owned">
      <div className="space-y-6">

        {/* Add Form */}
        <form onSubmit={addOwned} className="rounded-2xl border bg-white p-4 shadow-sm space-y-3">
          <div>
            <label className="block text-sm font-medium">Title</label>
            <input
              className="mt-2 w-full rounded-xl border px-3 py-2"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. A Court of Mist and Fury"
            />
          </div>

          <div>
            <label className="block text-sm font-medium">Author</label>
            <input
              className="mt-2 w-full rounded-xl border px-3 py-2"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              placeholder="e.g. Sarah J. Maas"
            />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-sm font-medium">Format</label>
              <select
                className="mt-2 w-full rounded-xl border px-3 py-2 bg-white"
                value={format}
                onChange={(e) => setFormat(e.target.value as any)}
              >
                {formats.map((f) => (
                  <option key={f} value={f}>{f}</option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              <label className="inline-flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={favorite}
                  onChange={(e) => setFavorite(e.target.checked)}
                />
                Add to Trophy Case 🏆
              </label>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium">Notes (optional)</label>
            <textarea
              className="mt-2 w-full rounded-xl border px-3 py-2 min-h-[90px]"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Signed copy, why you bought it, etc."
            />
          </div>

          {error && <p className="text-sm text-red-600">{error}</p>}

          <button type="submit" className="w-full rounded-xl bg-slate-900 px-4 py-2 text-white">
            Add to Shelf
          </button>
        </form>

        {/* Trophy Case */}
        {trophies.length > 0 && (
          <div className="rounded-2xl border bg-white p-4 shadow-sm">
            <h2 className="text-base font-semibold text-slate-900">Trophy Case</h2>

            <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {trophies.map((i) => (
                <div key={i.id} className="rounded-2xl border bg-slate-50 p-4 shadow-sm">
                  <div className="text-base font-semibold">
                    {i.title} 🏆
                  </div>
                  {i.author && <div className="text-sm text-slate-600">{i.author}</div>}
                  <div className="mt-2 text-xs text-slate-500">{i.format}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Shelf */}
        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h2 className="text-base font-semibold text-slate-900">Shelf</h2>

          {shelf.length === 0 ? (
            <p className="mt-3 text-slate-700">No owned books yet.</p>
          ) : (
            <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {shelf.map((i) => (
                <div key={i.id} className="rounded-2xl border bg-white p-4 shadow-sm">
                  <div className="text-base font-semibold">{i.title}</div>
                  {i.author && <div className="text-sm text-slate-600">{i.author}</div>}
                  <div className="mt-2 text-xs text-slate-500">{i.format}</div>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </PageShell>
  );
}
