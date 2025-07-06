import { defineConfig } from 'vite'
import preact from '@preact/preset-vite'

export default defineConfig({
  plugins: [preact()],
  build: {
    outDir: '../static/dist',
    emptyOutDir: false,
    rollupOptions: {
      input: 'src/main.jsx',
      output: {
        entryFileNames: 'app.js',
        chunkFileNames: 'chunks/[name].js',
        assetFileNames: 'assets/[name].[ext]'
      }
    }
  },
  server: {
    proxy: {
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      },
      '/pointcalc': 'http://localhost:8000'
    }
  }
})