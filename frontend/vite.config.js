// https://vitejs.dev/config/

import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue'
import process from 'process';
global.window = global.window || {};

window.process = process;
// const fs = require('fs')

// export default defineConfig({
export default ({ mode }) => {
  // if (typeof process !== 'undefined') {
  //   process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };
  // }
  return  defineConfig({
    plugins: [
      vue(),
    //   new webpack.DefinePlugin({
    // 'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
    //   }),
    ],
    resolve: {
      alias: {
        '@': '/src',
      },
    },
    server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
    devServer: {
      // https: {
      //   key: fs.readFileSync('./certs/example.com+5-key.pem'),
      //   cert: fs.readFileSync('./certs/example.com+5.pem'),
      // },
      public: 'https://localhost/v1:8443/'
    }
  })
}
