import { resolve } from "node:path";

export default {
  root: ".",
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        payQr: resolve(__dirname, "pay_qr.html"),
        contentGenerator: resolve(__dirname, "content_generator.html")
      }
    }
  }
};
