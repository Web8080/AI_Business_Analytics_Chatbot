"use client";
/* Victor.I - Data preview and column list. */
export interface ColumnType {
  name: string;
  type: string;
}

type Props = {
  rows: Record<string, unknown>[];
  columns: string[];
  columnTypes?: ColumnType[];
  rowsCount: number;
  colsCount: number;
};

export function PreviewTable({
  rows,
  columns,
  columnTypes,
  rowsCount,
  colsCount,
}: Props) {
  return (
    <div className="space-y-4">
      <p className="text-sm text-slate-500">
        {rowsCount} rows x {colsCount} columns
      </p>
      <details className="group" open>
        <summary className="cursor-pointer font-medium text-slate-700">
          Preview Data
        </summary>
        <div className="mt-2 overflow-x-auto rounded-lg border border-sky-200">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-sky-50">
                {columns.map((col) => (
                  <th
                    key={col}
                    className="px-3 py-2 text-left font-medium text-sky-900"
                  >
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.slice(0, 10).map((row, i) => (
                <tr key={i} className="border-t border-sky-100">
                  {columns.map((col) => (
                    <td key={col} className="px-3 py-2 text-slate-600">
                      {String(row[col] ?? "")}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
      <details className="group">
        <summary className="cursor-pointer font-medium text-slate-700">
          Columns
        </summary>
        <ul className="mt-2 space-y-1 text-sm text-slate-600">
          {(columnTypes || columns.map((c) => ({ name: c, type: "Text" }))).map(
            (ct) => (
              <li key={ct.name}>
                {ct.name} ({ct.type})
              </li>
            )
          )}
        </ul>
      </details>
    </div>
  );
}
