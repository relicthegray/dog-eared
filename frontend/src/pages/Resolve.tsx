import PageShell from "../components/PageShell";

export default function Resolve() {
  return (
    <PageShell title="Resolve">
      <div className="rounded-2xl border bg-white p-4 shadow-sm">
        <p className="text-slate-700">Resolve ambiguous matches by selecting the correct book candidate.</p>
      </div>
    </PageShell>
  );
}
