/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        quantum: {
          950: '#060a12',
          900: '#0b1329',
          850: '#101c3d',
          800: '#18274f',
          700: '#263b73',
          glow: '#06b6d4',
          accent: '#8b5cf6',
          purple: '#a855f7',
          teal: '#14b8a6',
          amber: '#f59e0b'
        }
      },
      fontFamily: {
        mono: ['Fira Code', 'JetBrains Mono', 'Consolas', 'monospace']
      }
    },
  },
  plugins: [],
}
