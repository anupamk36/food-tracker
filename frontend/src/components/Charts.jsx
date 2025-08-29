import {
    ResponsiveContainer,
    AreaChart, Area,
    LineChart, Line,
    BarChart, Bar,
    CartesianGrid, XAxis, YAxis, Tooltip, Legend,
} from "recharts";

// ---- helpers ----
function fmtDate(d) { return d?.slice?.(5) || d; }     // "2025-08-29" -> "08-29"
function ma(series, key, window = 7) {
    const out = [];
    let sum = 0;
    for (let i = 0; i < series.length; i++) {
        const v = Number(series[i]?.[key] || 0);
        sum += v;
        if (i >= window) sum -= Number(series[i - window]?.[key] || 0);
        out.push({ ...series[i], [`${key}_ma${window}`]: i + 1 >= window ? +(sum / window).toFixed(1) : null });
    }
    return out;
}

// ---- unified tooltip content (simple) ----
function SimpleTooltip({ label, payload }) {
    if (!payload || !payload.length) return null;
    return (
        <div className="rounded-lg bg-white shadow px-3 py-2 text-sm">
            <div className="font-medium mb-1">{label}</div>
            {payload.map((p, i) => (
                <div key={i}>{p.name}: {p.value}</div>
            ))}
        </div>
    );
}

// ---- Calories (Area) + Moving Average + Goal line ----
export function CaloriesChart({ data = [], goal = 2200 }) {
    const trimmed = data.slice(-30);              // last 30
    const withMA = ma(trimmed, "calories", 7);    // add calories_ma7

    // Inject goal line samples (as a second series via Line using same x)
    const goalSeriesKey = "goal";
    const withGoal = withMA.map(d => ({ ...d, [goalSeriesKey]: goal }));

    return (
        <div className="w-full h-64">
            <ResponsiveContainer>
                <ComposedCalories data={withGoal} />
            </ResponsiveContainer>
        </div>
    );
}

function ComposedCalories({ data }) {
    return (
        <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tickFormatter={fmtDate} />
            <YAxis />
            <Tooltip content={<SimpleTooltip />} />
            <Area type="monotone" dataKey="calories" name="Calories" />
            <Line type="monotone" dataKey="calories_ma7" name="7-day MA" dot={false} />
            <Line type="monotone" dataKey="goal" name="Goal" dot={false} strokeDasharray="4 4" />
        </AreaChart>
    );
}

// ---- Stacked Macros per day ----
export function MacroStackedChart({ data = [] }) {
    const trimmed = data.slice(-14); // last 2 weeks
    return (
        <div className="w-full h-64">
            <ResponsiveContainer>
                <BarChart data={trimmed}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tickFormatter={fmtDate} />
                    <YAxis />
                    <Tooltip content={<SimpleTooltip />} />
                    <Legend />
                    <Bar dataKey="protein_g" stackId="m" name="Protein (g)" />
                    <Bar dataKey="carbs_g" stackId="m" name="Carbs (g)" />
                    <Bar dataKey="fat_g" stackId="m" name="Fat (g)" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}

// ---- Top items bar (horizontal) ----
export function TopItemsChart({ data = [] }) {
    const top = data.slice(0, 10).map(d => ({ ...d, label: (d.name || "").slice(0, 18) }));
    return (
        <div className="w-full h-64">
            <ResponsiveContainer>
                <BarChart data={top} layout="vertical" margin={{ left: 24 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" allowDecimals={false} />
                    <YAxis dataKey="label" type="category" width={100} />
                    <Tooltip content={<SimpleTooltip />} />
                    <Bar dataKey="count" name="Count" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
