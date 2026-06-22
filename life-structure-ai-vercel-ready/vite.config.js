import { resolve } from "node:path";

export default {
  root: "frontend",
  build: {
    outDir: "../dist",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "frontend/index.html"),
        payQr: resolve(__dirname, "frontend/pay_qr.html"),
        contentGenerator: resolve(__dirname, "frontend/content_generator.html")
      }
    }
  }
};
