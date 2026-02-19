import { useEffect, useState } from "react";
import PageShell from "../components/PageShell";
import { apiGet } from "../app/api";

type IntakeItem = {
  id: string;
  raw_text: string;
  status: string;
  captured_at: string;
  source_id?: string | null;
  source_name?: string | null;
  source_post_url?: string | null;
};

export default function Inbox() {
  const [items, setItems] = useState<IntakeItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    setError(null);
    setLoading(true);
    try {
      const data = await apiGet<IntakeItem[]>("/intake?status=new");
      setItems(data);
    } catch (err: any) {
      setError(err?.message ?? "Failed to load inbox.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <PageShell title="Inbox">
      <div className="space-y-3">
        <button
          onClick={load}
          className="w-full rounded-xl border bg-white px-4 py-2 text-sm shadow-sm hover:bg-slate-50"
        >
          {loading ? "Refreshing..." : "Refresh"}
        </button>

        {error && (
          <div className="rounded-2xl border bg-white p-4 shadow-sm">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        {items.length === 0 && !error && (
          <div className="rounded-2xl border bg-white p-4 shadow-sm">
            <p className="text-slate-700">Your inbox is empty. Add something from Capture.</p>
          </div>
        )}

        {items.map((i) => (
          <div key={i.id} className="rounded-2xl border bg-white p-4 shadow-sm">
            {(i.source_name || i.source_post_url) && (
              <div className="mb-2 flex items-center justify-between text-xs">
                <span className="inline-flex items-center rounded-full border px-2 py-1 text-slate-700 bg-slate-50">
                  {i.source_name ?? "Source"}
                </span>
                {i.source_post_url ? (
                  <a
                    className="text-slate-700 underline"
                    href={i.source_post_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Open
                  </a>
                ) : (
                  <span />
                )}
              </div>
            )}

            <p className="whitespace-pre-wrap text-slate-900">{i.raw_text}</p>

            <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
              <span>{new Date(i.captured_at).toLocaleString()}</span>
              <span />
            </div>
          </div>
        ))}
      </div>
    </PageShell>
  );
}
