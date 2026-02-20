import { useEffect, useState } from "react";
import PageShell from "../components/PageShell";
import { apiGet, apiPost } from "../app/api";

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

  // Quick Capture state
  const [tiktokUrl, setTiktokUrl] = useState("");
  const [notes, setNotes] = useState("");
  const [saving, setSaving] = useState(false);

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

  async function createFromQuickCapture() {
    setError(null);

    const url = tiktokUrl.trim();
    const noteText = notes.trim();

    if (!url && !noteText) {
      setError("Paste a TikTok URL or add a note.");
      return;
    }

    // V1 behavior (per feature doc):
    // - URL only => raw_text = "TikTok capture"
    // - Notes only => raw_text = notes
    // - Both => raw_text = notes
    const raw_text = noteText || (url ? "TikTok capture" : "");

    setSaving(true);
    try {
      await apiPost("/intake", {
        raw_text,
        source_post_url: url || null,
        source_id: null,
      });

      setTiktokUrl("");
      setNotes("");
      await load();
    } catch (err: any) {
      setError(err?.message ?? "Failed to save capture.");
    } finally {
      setSaving(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <PageShell title="Inbox">
      <div className="space-y-3">
        {/* Quick Capture Card */}
        <div className="space-y-3 rounded-2xl border bg-white p-4 shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-medium text-slate-900">Quick Capture</h2>
            <span className="text-xs text-slate-500">TikTok-friendly</span>
          </div>

          <div className="space-y-2">
            <label className="block text-xs text-slate-600">TikTok URL</label>
            <input
              value={tiktokUrl}
              onChange={(e) => setTiktokUrl(e.target.value)}
              placeholder="https://www.tiktok.com/..."
              className="w-full rounded-xl border px-3 py-2 text-sm"
            />
          </div>

          <div className="space-y-2">
            <label className="block text-xs text-slate-600">Notes (optional)</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Title hint, author, why you saved it..."
              className="w-full rounded-xl border px-3 py-2 text-sm"
              rows={3}
            />
          </div>

          <button
            onClick={createFromQuickCapture}
            disabled={saving}
            className="w-full rounded-xl border bg-white px-4 py-2 text-sm shadow-sm hover:bg-slate-50 disabled:opacity-60"
          >
            {saving ? "Saving..." : "Save to Inbox"}
          </button>
        </div>

        {/* Existing Refresh Button */}
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
                <span className="inline-flex items-center rounded-full border bg-slate-50 px-2 py-1 text-slate-700">
                  {i.source_name ??
                    (i.source_post_url && /tiktok\.com/i.test(i.source_post_url)
                      ? "TikTok"
                      : "Source")}
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
