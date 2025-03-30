/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'primary': {
          50: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 97%)',
          100: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 94%)',
          200: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 85%)',
          300: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 75%)',
          400: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 65%)',
          500: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 55%)',
          600: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 45%)',
          700: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 35%)',
          800: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 25%)',
          900: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 20%)',
          950: 'hsl(var(--primary-hue, 170), var(--primary-saturation, 80%), 10%)',
        },
        'secondary': {
          50: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 97%)',
          100: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 94%)',
          200: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 85%)',
          300: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 75%)',
          400: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 65%)',
          500: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 55%)',
          600: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 45%)',
          700: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 35%)',
          800: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 25%)',
          900: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 20%)',
          950: 'hsl(var(--secondary-hue, 220), var(--secondary-saturation, 80%), 10%)',
        },
      },
    },
  },
  plugins: [],
} 