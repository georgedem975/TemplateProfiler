import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'


export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/benchmarks': 'http://localhost:5000'
    }
  },
  resolve: {
    alias: {
      'node:fs': 'src/shims/empty.ts',
      'node:path': 'src/shims/path.ts',
    }

  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts', 
  },
})


