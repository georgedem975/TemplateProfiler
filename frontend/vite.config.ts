import { defineConfig } from 'vite'
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
  }
})
