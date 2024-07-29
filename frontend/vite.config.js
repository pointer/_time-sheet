// https://vitejs.dev/config/

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
const fs = require('fs')

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  devServer: {
      https: {
        key: fs.readFileSync('./certs/example.com+5-key.pem'),
        cert: fs.readFileSync('./certs/example.com+5.pem'),
      },
      public: 'https://localhost:8765/'
  }  
})