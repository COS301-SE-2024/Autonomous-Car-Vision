import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import url from '@rollup/plugin-url';
import commonjs from '@rollup/plugin-commonjs';
import postcss from 'rollup-plugin-postcss';
import { terser } from 'rollup-plugin-terser';
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';
import json from '@rollup/plugin-json';

const production = !process.env.ROLLUP_WATCH;

export default {
  input: 'src/main.js',
  output: {
    sourcemap: true,
    format: 'iife',
    name: 'app',
    file: 'public/build/bundle.js'
  },
  plugins: [
    svelte({
      dev: !production,
      css: css => {
        css.write('public/build/bundle.css');
      }
    }),
    postcss({
      extract: true,
      minimize: production,
      plugins: [
        tailwindcss,
        autoprefixer,
      ]
    }),
    // url({
    //   include: ['**/*.svg', '**/*.png', '**/*.jpg', '**/*.gif'],
    //   limit: 8192,
    //   emitFiles: true,
    //   fileName: 'assets/[name][hash][extname]',
    // }),
    resolve({
      browser: true,
      dedupe: ['svelte']
    }),
    commonjs(),
      json(),
    production && terser()
  ],
  watch: {
    clearScreen: false
  }
};
