import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { BenchmarkResults } from './BenchmarkResults'; // Importa el original

// Simulamos la API
vi.mock('../api/benchmarks', () => ({
  fetchBenchmarks: vi.fn(() => Promise.resolve([])),
}));

describe('BenchmarkResults Component', () => {
  it('debe mostrar el mensaje cuando no hay resultados', async () => {
    render(<BenchmarkResults />);
    const message = await screen.findByText(/No results yet/i);
    expect(message).toBeInTheDocument();
  });
});