module.exports = {
    purge: ['./src/**/*.svelte'],
    darkMode: false,
    theme: {
      extend: {
        colors: {
          'theme-dark': {
            textHover: "#4D4D4D",
            white: '#FFFFFF', // white
            lightText: '#FFFFFF', // white
            background: '#001524', // offBlack
            backgroundBlue: '#0C003C',
            bgHover: '#1C008D',
            primary: '#0099ff', // techBlue
            secondary: '#007acc', // techBlueDark
            highlight: '#0066cc', // highlight
            error: '#ff0000', // error
            download: "#181818e0"
          },
          'theme-light': {
            lightText: '#FFFFFF',
            background: '#001524', // Timberwolf background
            primary: '#28a745', // primary
            secondary: '#218838', // secondary
            error: '#ff0000', // error
          },
        },
        boxShadow: {
          'tech-blue': '0 10px 20px #0C003C, 0 6px 20px #0C003C', // shadow-blue
          'card-blue': '6px 6px 10px rgba(0.15, 40, 145, 0.2), 6px 6px 10px rgba(0.15, 40, 145, 0.2)', // shadow-card
          'tech-green': '0 10px 20px #218838, 0 6px 20px #218838', // shadow-green
          'card-white': '6px 6px 10px rgba(0.15, 244, 244, 0.2), 6px 6px 10px rgba(0.15, 40, 145, 0.2)'
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
        'dark' : {
          background: '#011C27', // '#03254E',  // '#001524', '#011C27'
          primary: '#0099ff',
          secondary: '#007acc' ,// '#3EFF8B',
          hover: '#012A3B',
          background_secondary: '#000000',
          fill: '#001524'
        },
        'modal': '#0000009f', 
        'white': '#FFFF',
        'black': '#000',
        'red' : '#f44336',
        'green-80' : '#37FF8B80',
        'greeen' : '#37FF8B',
        'red-hover': '#FF1C0C',
      },
    },
    variants: {
      extend: {},
    },
    plugins: [
    ],
  };
  