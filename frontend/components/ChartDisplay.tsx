"use client";
/* Victor.I - Bar/line chart from backend chart_data. Normalizes Plotly vs simple x/y. */
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import type { ChartData } from "@/lib/api";

function normalizeChart(chart: ChartData): {
  type: string;
  title: string;
  data: { name: string; value: number }[];
} {
  const type = chart.type || "bar";
  const title = chart.title || "Chart";
  let data: { name: string; value: number }[] = [];
  if (chart.x && chart.y && Array.isArray(chart.x) && Array.isArray(chart.y)) {
    data = chart.x.map((name, i) => ({
      name: String(name),
      value: Number(chart.y![i]) || 0,
    }));
  } else if (chart.data?.data?.[0]) {
    const d = chart.data.data[0];
    const x = (d.x || []) as unknown[];
    const y = (d.y || []) as unknown[];
    if (x.length && y.length) {
      data = x.map((name, i) => ({
        name: String(name),
        value: Number(y[i]) || 0,
      }));
    } else if (d.labels && d.values) {
      data = (d.labels as unknown[]).map((name, i) => ({
        name: String(name),
        value: Number((d.values as unknown[])[i]) || 0,
      }));
    }
  }
  return { type, title, data };
}

const COLORS = ["#0284c7", "#0ea5e9", "#38bdf8", "#7dd3fc", "#0c4a6e"];

type Props = { chartData: ChartData | null };
export function ChartDisplay({ chartData }: Props) {
  if (!chartData || !chartData.type) return null;
  const { type, title, data } = normalizeChart(chartData);
  if (!data.length) return null;

  const tooltipStyle = { background: "#fff", border: "1px solid #bae6fd" };
  const gridStroke = "#bae6fd";
  const axisStroke = "#0369a1";

  return (
    <div className="my-4 rounded-xl border border-sky-200 bg-white p-4 shadow-sm">
      <h3 className="mb-3 text-sm font-medium text-sky-900">{title}</h3>
      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          {type === "pie" ? (
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {data.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={tooltipStyle} />
            </PieChart>
          ) : type === "line" ? (
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
              <XAxis dataKey="name" stroke={axisStroke} fontSize={12} />
              <YAxis stroke={axisStroke} fontSize={12} />
              <Tooltip contentStyle={tooltipStyle} />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#0284c7" strokeWidth={2} />
            </LineChart>
          ) : (
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
              <XAxis dataKey="name" stroke={axisStroke} fontSize={12} />
              <YAxis stroke={axisStroke} fontSize={12} />
              <Tooltip contentStyle={tooltipStyle} />
              <Legend />
              <Bar dataKey="value" fill="#0284c7" name="Value" radius={[4, 4, 0, 0]} />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
}
