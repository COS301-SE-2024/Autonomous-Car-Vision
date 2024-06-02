module.exports = {
    purge: ['./src/**/*.svelte'],
    darkMode: false,
    theme: {
      extend: {},
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
          primary: '#9A0000',
          secondary: '#730D0D',
        },
        'theme-purple': {
          light:'#343434', //Timber wolf
          dark:'#D3D3D3', //Jet
          primary: '#400F65',
          secondary: '#83468F',
        },
      },
    },
    variants: {
      extend: {},
    },
    plugins: [
    ],
  };
  