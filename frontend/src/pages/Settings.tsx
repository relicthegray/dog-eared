import PageShell from "../components/PageShell";

export default function Settings() {
  return (
    <PageShell title="Settings">
      <div className="rounded-2xl border bg-white p-4 shadow-sm">
        <p className="text-slate-700">Account, sources, and (admin) invite management will live here.</p>
      </div>
    </PageShell>
  );
}
