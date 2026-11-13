import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3200,
    open: false,
  },
  build: {
    outDir: "build", // keep the same output directory as CRA used
  },
  preview: {
    port: 3200,
  },
});



