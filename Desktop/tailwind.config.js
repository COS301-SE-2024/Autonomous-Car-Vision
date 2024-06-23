module.exports = {
    purge: ['./src/**/*.svelte'],
    darkMode: false,
    theme: {
      extend: {},
      fontFamily: {
        custom: ['var(--font-custom)', 'sans-serif'],
        heading: ['var(--font-heading)', 'sans-serif'],
        special: ['var(--font-special)', 'sans-serif'],
        body: ['var(--font-body)', 'sans-serif'],
        light: ['var(--font-light)', 'sans-serif'],
        lighter: ['var(--font-light-light)', 'sans-serif'],
      },
      colors: {
        'theme-green': {
          light:'#343434', //Timber wolf
          dark:'#D3D3D3', //Jet
          primary: '#094400',
          secondary: '#07873A',
        },
        'theme-blue': {
          light:'#343434', //Timber wolf
          dark:'#D3D3D3', //Jet
          primary: '#0C3E63',
          secondary: '#5078A0',
        },
        'theme-red': {
          light:'#343434', //Timber wolf
          dark:'#D3D3D3', //Jet
          primary: '#730D0D',
          secondary: '#9B1D1D',
        },
        'theme-keith':{
          jet: '#D3D3D3',
          timber: '#343434',
          primary: '#344e41',
          secondary:'#3a5a40',
          accentone:'#588157',
          accenttwo:'#a3b18a',
          highlight:'#dad7cd',
        },
        'theme-purple': {
          light:'#343434', //Timber wolf
          dark:'#D3D3D3', //Jet
          primary: '#400F65',
          secondary: '#83468F',
        },
        'white': '#FFFF',
        'black': '#000',
      },
    },
    variants: {
      extend: {},
    },
    plugins: [
    ],
  };
  