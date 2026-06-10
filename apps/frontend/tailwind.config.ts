import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#e50914',
          50: '#fff1f1',
          100: '#ffe1e1',
          200: '#ffc7c7',
          300: '#ffa0a0',
          400: '#ff6b6b',
          500: '#f83b3b',
          600: '#e50914',
          700: '#c10b13',
          800: '#a00d15',
          900: '#840f16',
        },
        surface: {
          DEFAULT: '#1a1a2e',
          50: '#f5f5f7',
          100: '#e8e8ed',
          200: '#d0d0db',
          300: '#aeaec2',
          400: '#8585a0',
          500: '#666685',
          600: '#52526b',
          700: '#444457',
          800: '#3a3a4a',
          900: '#141414',
          950: '#0a0a0f',
        },
        netflix: {
          black: '#141414',
          dark: '#181818',
          gray: '#808080',
          'light-gray': '#b3b3b3',
          red: '#e50914',
          'dark-red': '#b20710',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      aspectRatio: {
        video: '16 / 9',
        poster: '2 / 3',
      },
    },
  },
  plugins: [],
};

export default config;
