import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import postcss from 'rollup-plugin-postcss';
import { terser } from 'rollup-plugin-terser';
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';

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
    resolve({
      browser: true,
      dedupe: ['svelte']
    }),
    commonjs(),
    production && terser()
  ],
  watch: {
    clearScreen: false
  }
};
