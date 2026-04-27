import type { BenchmarkResult } from '../types';

const API_URL = import.meta.env.VITE_API_URL;
const BASE = `${API_URL}/benchmarks`;

export async function saveBenchmark(
    data: Omit<BenchmarkResult, 'id' | 'created_at'>
): Promise<BenchmarkResult> {

  const body = JSON.stringify({
    template_engine: data.template_engine,
    render_time_ms: data.render_time_ms.toFixed(3),
    payload: data.payload
  });

  const res = await fetch(BASE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body
  });

  if (!res.ok) {
    throw new Error(`Failed to save: ${res.status}`);
  }

  return res.json();
}

export async function fetchBenchmarks(): Promise<BenchmarkResult[]> {
  const res = await fetch(BASE);

  if (!res.ok) {
    throw new Error(`Failed to fetch: ${res.status}`);
  }

  return res.json();
}