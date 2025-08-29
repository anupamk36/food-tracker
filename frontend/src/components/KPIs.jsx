export default function KPIs({ series = [] }) {
    if (!series.length) return null;

    const last7 = series.slice(-7);
    const sum = (arr, k) => arr.reduce((a, b) => a + Number(b?.[k] || 0), 0);

    const kcal7 = sum(last7, "calories");
    const protein7 = sum(last7, "protein_g");
    const carbs7 = sum(last7, "carbs_g");
    const fat7 = sum(last7, "fat_g");

    const avg = (v, d) => (d ? Math.round((v / d)) : 0);

    const cards = [
        { label: "Avg calories (7d)", value: avg(kcal7, last7.length) },
        { label: "Protein total (7d, g)", value: Math.round(protein7) },
        { label: "Carbs total (7d, g)", value: Math.round(carbs7) },
        { label: "Fat total (7d, g)", value: Math.round(fat7) },
    ];

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {cards.map((c) => (
                <div key={c.label} className="card">
                    <div className="text-sm text-gray-500">{c.label}</div>
                    <div className="text-2xl font-semibold mt-1">{c.value}</div>
                </div>
            ))}
        </div>
    );
}
