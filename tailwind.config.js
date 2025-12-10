export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],  // ← SCANS your files for classes
  theme: {
    extend: {
      colors: {
        crewai: {
          500: '#3B82F6',  // Brand blue for agent status
        }
      }
    },
  },
  plugins: []
};
