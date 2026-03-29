import { useState, useEffect } from 'react';
import { fetchBenchmarks } from '../api/benchmarks';
import type { BenchmarkResult } from '../types';
import { ENGINE_LABELS } from '../engines';

export function BenchmarkResults() {
  const [results, setResults] = useState<BenchmarkResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchBenchmarks();
      setResults(data);
    } catch {
      setError('Failed to load results. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-800">Saved Benchmark Results</h2>
        <button
          onClick={load}
          disabled={loading}
          className="px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50 transition-colors disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {error && (
        <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 rounded-md px-4 py-3 text-sm">
          {error}
        </div>
      )}

      {!loading && !error && results.length === 0 && (
        <p className="text-gray-500 text-sm">No results yet. Run a benchmark and save it.</p>
      )}

      {results.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg overflow-hidden">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Engine</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time (ms)</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Payload</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created At</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {results.map((r, i) => (
                <tr key={r.id ?? i} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-500">{r.id ?? '—'}</td>
                  <td className="px-4 py-3 text-sm font-medium text-indigo-700">
                    {ENGINE_LABELS[r.template_engine] ?? r.template_engine}
                  </td>
                  <td className="px-4 py-3 text-sm font-mono text-gray-800">{r.render_time_ms}</td>
                  <td className="px-4 py-3 text-sm text-gray-600 max-w-xs truncate font-mono">{r.payload}</td>
                  <td className="px-4 py-3 text-sm text-gray-500">{r.created_at ?? '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
