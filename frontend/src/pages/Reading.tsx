import PageShell from "../components/PageShell";

export default function Reading() {
  return (
    <PageShell title="Reading">
      <div className="rounded-2xl border bg-white p-4 shadow-sm">
        <p className="text-slate-700">Your currently-reading shelf will live here.</p>
      </div>
    </PageShell>
  );
}
