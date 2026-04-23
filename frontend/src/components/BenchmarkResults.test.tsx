import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { BenchmarkResults } from './BenchmarkResults'; // Importa el original

// Simulamos la API
vi.mock('../api/benchmarks', () => ({
  fetchBenchmarks: vi.fn(() => Promise.resolve([])),
}));

describe('BenchmarkResults Component', () => {
  it('it needs to display a massege when there not  result', async () => {
    render(<BenchmarkResults />);
    const message = await screen.findByText(/No results yet/i);
    expect(message).toBeInTheDocument();
  });
});

it('Show the title', () => {
  render(<BenchmarkResults />);
  // Buscamos el encabezado h2 que tienes en tu código
  const title = screen.getByText(/Сохранённые результаты/i);
  expect(title).toBeInTheDocument();
});