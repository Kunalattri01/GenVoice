/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.html",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        brand: '#2d8c57',
        accent: '#1e6040',
      },
      fontFamily: {
        display: ['Playfair Display', 'serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}