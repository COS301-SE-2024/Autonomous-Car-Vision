const sveltePreprocess = require('svelte-preprocess');
// const adapter = require('@sveltejs/adapter-auto');

module.exports = {
  preprocess: sveltePreprocess({
    postcss: {
      plugins: [require('tailwindcss'), require('autoprefixer')],
    },
  }),
  // kit: {
  //   adapter: adapter(),
  //   vite: {},
  // },
};
