// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: [
//     "./**/*.html",
//     "./templates/**/*.html",
//   ],
//   theme: {
//     extend: {
//       colors: {
// brand: '#3471eb',   // Primary Blue
// accent: '#2563EB',  // Royal Blue
//       },
//       fontFamily: {
//         display: ['Playfair Display', 'serif'],
//         body: ['Inter', 'sans-serif'],
//       },
//     },
//   },
//   plugins: [],
// }


/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.html",
    "./templates/**/*.html",
  ],

  theme: {
    extend: {
      colors: {
        brand: "#3471eb",
        accent: "#2563EB",

        primary: "#0A1E5E",
        success: "#22C55E",
        warning: "#F59E0B",
        danger: "#EF4444",
        bgpage: "#F8FAFC",
        bordercolor: "#E5E7EB",
        textprimary: "#111827",
        textsecondary: "#6B7280",
      },

      fontFamily: {
        display: ["Playfair Display", "serif"],
        body: ["Inter", "sans-serif"],
        sans: ["Inter", "sans-serif"],
      },

      borderRadius: {
        xl: "12px",
      },
    },
  },

  plugins: [],
};