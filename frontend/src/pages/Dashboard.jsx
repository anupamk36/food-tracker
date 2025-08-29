import { useEffect, useState } from "react";
import { api, setAuth } from "../services/api";
import { getToken } from "../services/auth";
import KPIs from "../components/KPIs";
import { CaloriesChart, MacroStackedChart, TopItemsChart } from "../components/Charts";

export default function Dashboard() {
  const [meals, setMeals] = useState([]);
  const [stats, setStats] = useState({ series: [], topItems: [] });
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  useEffect(() => {
    setAuth(getToken?.());
    Promise.all([api.get("/meals/"), api.get("/meals/stats")])
      .then(([m, s]) => {
        setMeals(m?.data?.items ?? []);
        setStats(s?.data ?? { series: [], topItems: [] });
      })
      .catch((e) => setErr(e))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Your dashboard</h1>
      </div>

      {err && (
        <div className="card border border-red-200">
          <div className="text-red-600 font-medium mb-1">Error</div>
          <pre className="text-sm whitespace-pre-wrap">{String(err?.message || err)}</pre>
        </div>
      )}

      {/* KPIs */}
      <KPIs series={stats?.series ?? []} />

      {/* Charts */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="card">
          <h2 className="font-medium mb-2">Calories (30d)</h2>
          <CaloriesChart data={stats?.series ?? []} goal={2200} />
        </div>
        <div className="card">
          <h2 className="font-medium mb-2">Macros per day</h2>
          <MacroStackedChart data={stats?.series ?? []} />
        </div>
        <div className="card">
          <h2 className="font-medium mb-2">Top items</h2>
          <TopItemsChart data={stats?.topItems ?? []} />
        </div>
      </div>

      {/* Meals list */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-3">Recent meals</h2>
        {loading ? <div>Loading…</div> : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {meals.map((m) => (
              <div key={m.id} className="border rounded-xl p-4 bg-white">
                <div className="text-sm text-gray-500">
                  {m.timestamp ? new Date(m.timestamp).toLocaleString() : "—"}
                </div>
                {m.image_path && (
                  <img src={m.image_path} alt="" className="mt-2 rounded-lg max-h-44 w-full object-cover" />
                )}
                <div className="mt-2">
                  <div className="text-sm text-gray-600">
                    Status: <span className="font-medium">{m.status || "unknown"}</span>
                  </div>
                  {m.nutrition && (
                    <div className="text-sm mt-2 space-y-1">
                      <div><span className="font-medium">Calories:</span> {m.nutrition.calories ?? "—"}</div>
                      <div>Protein: {m.nutrition.protein_g ?? "—"}g</div>
                      <div>Carbs: {m.nutrition.carbs_g ?? "—"}g</div>
                      <div>Fat: {m.nutrition.fat_g ?? "—"}g</div>
                    </div>
                  )}
                  {m.notes && <div className="text-sm mt-2 italic">“{m.notes}”</div>}
                </div>
              </div>
            ))}
            {!meals.length && !loading && <div className="text-gray-500">No meals yet.</div>}
          </div>
        )}
      </div>
    </div>
  );
}
