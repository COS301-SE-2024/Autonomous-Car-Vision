module.exports = {
    purge: ['./src/**/*.svelte'],
    darkMode: false,
    theme: {
      extend: {
        colors: {
          'theme-dark': {
            lightText: '#FFFFFF', // white
            background: '#181818', // offBlack
            primary: '#0099ff', // techBlue
            secondary: '#007acc', // techBlueDark
            highlight: '#0066cc', // highlight
            error: '#ff0000', // error
          },
          'theme-light': {
            lightText: '#FFFFFF',
            background: '#d9d9d9', // Timberwolf background
            primary: '#28a745', // primary
            secondary: '#218838', // secondary
            error: '#ff0000', // error
          },
        },
        boxShadow: {
          'tech-blue': '0 4px 8px rgba(0, 153, 255, 0.2), 0 6px 20px rgba(0, 153, 255, 0.19)', // shadow-blue
          'tech-green': '0 10px 20px #218838, 0 6px 20px #218838', // shadow-green
        },
      },
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
  