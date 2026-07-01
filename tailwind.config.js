/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.html",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
brand: '#3471eb',   // Primary Blue
accent: '#2563EB',  // Royal Blue
      },
      fontFamily: {
        display: ['Playfair Display', 'serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}