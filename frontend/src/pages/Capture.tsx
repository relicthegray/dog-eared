import { useEffect, useState } from "react";
import PageShell from "../components/PageShell";
import { apiGet, apiPost } from "../app/api";
import { useNavigate } from "react-router-dom";

type Source = {
  id: string;
  type: string;
  name: string;
  url?: string | null;
};

export default function Capture() {
  const nav = useNavigate();

  const [rawText, setRawText] = useState("");
  const [postUrl, setPostUrl] = useState("");

  const [sources, setSources] = useState<Source[]>([]);
  const [sourceId, setSourceId] = useState<string>("");

  const [quickSourceName, setQuickSourceName] = useState("");
  const [quickSourceType, setQuickSourceType] = useState("tiktok");

  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  async function loadSources() {
    try {
      const data = await apiGet<Source[]>("/sources");
      setSources(data);
      if (!sourceId && data.length > 0) setSourceId(data[0].id);
    } catch {
      // You can still capture without a source
    }
  }

  useEffect(() => {
    loadSources();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function onQuickAddSource() {
    setError(null);
    if (!quickSourceName.trim()) {
      setError("Enter a source name (e.g. Erin, TikTok - @name).");
      return;
    }
    try {
      const created = await apiPost<Source>("/sources", {
        type: quickSourceType,
        name: quickSourceName,
      });
      const next = [created, ...sources];
      setSources(next);
      setSourceId(created.id);
      setQuickSourceName("");
    } catch (err: any) {
      setError(err?.message ?? "Failed to create source.");
    }
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!rawText.trim()) {
      setError("Paste a book recommendation first.");
      return;
    }

    try {
      setSaving(true);
      await apiPost("/intake", {
        raw_text: rawText,
        source_id: sourceId || null,
        source_post_url: postUrl || null,
      });
      setRawText("");
      setPostUrl("");
      nav("/", { replace: true });
    } catch (err: any) {
      setError(err?.message ?? "Failed to save intake item.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <PageShell title="Capture">
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="rounded-2xl border bg-white p-4 shadow-sm space-y-4">
          <div>
            <label className="block text-sm font-medium">Source</label>
            <select
              className="mt-2 w-full rounded-xl border px-3 py-2 bg-white"
              value={sourceId}
              onChange={(e) => setSourceId(e.target.value)}
            >
              <option value="">(No source)</option>
              {sources.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>

            <div className="mt-3 grid grid-cols-3 gap-2">
              <select
                className="col-span-1 rounded-xl border px-3 py-2 bg-white text-sm"
                value={quickSourceType}
                onChange={(e) => setQuickSourceType(e.target.value)}
              >
                <option value="tiktok">TikTok</option>
                <option value="family">Family</option>
                <option value="friend">Friend</option>
                <option value="booktube">BookTube</option>
                <option value="other">Other</option>
              </select>

              <input
                className="col-span-2 rounded-xl border px-3 py-2 text-sm"
                placeholder="Quick add source (e.g. Erin, TikTok - @name)"
                value={quickSourceName}
                onChange={(e) => setQuickSourceName(e.target.value)}
              />
            </div>

            <button
              type="button"
              onClick={onQuickAddSource}
              className="mt-2 w-full rounded-xl border bg-white px-4 py-2 text-sm shadow-sm hover:bg-slate-50"
            >
              + Add Source
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium">Paste recommendation</label>
            <textarea
              className="mt-2 w-full rounded-xl border px-3 py-2 min-h-[140px]"
              placeholder="Paste TikTok caption, a note, or 'Title by Author'..."
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium">Post URL (optional)</label>
            <input
              className="mt-2 w-full rounded-xl border px-3 py-2"
              placeholder="https://www.tiktok.com/..."
              value={postUrl}
              onChange={(e) => setPostUrl(e.target.value)}
            />
          </div>

          {error && <p className="text-sm text-red-600">{error}</p>}

          <button
            type="submit"
            disabled={saving}
            className="w-full rounded-xl bg-slate-900 px-4 py-2 text-white disabled:opacity-60"
          >
            {saving ? "Saving..." : "Add to Inbox"}
          </button>
        </div>
      </form>
    </PageShell>
  );
}
