module.exports = {
    purge: ['./src/**/*.svelte'],
    darkMode: false,
    theme: {
      extend: {
        colors: {
          'theme-dark': {
            textHover: "#4D4D4D",
            white: '#FFFFFF',
            lightText: '#FFFFFF',
            background: '#001524',
            backgroundBlue: '#0C003C',
            bgHover: '#1C008D',
            primary: '#0099ff',
            secondary: '#007acc',
            highlight: '#0066cc',
            error: '#ff0000',
            download: "#181818e0"
          },
          'theme-light': {
            lightText: '#FFFFFF',
            background: '#001524',
            primary: '#28a745',
            secondary: '#218838',
            error: '#ff0000',
          },
        },
        boxShadow: {
          'tech-blue': '0 10px 20px #0C003C, 0 6px 20px #0C003C',
          'card-blue': '6px 6px 10px rgba(0.15, 40, 145, 0.2), 6px 6px 10px rgba(0.15, 40, 145, 0.2)',
          'tech-green': '0 10px 20px #218838, 0 6px 20px #218838',
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
          background: '#011C27',
          primary: '#0099ff',
          secondary: '#007acc',
          hover: '#012A3B',
          background_secondary: '#000000',
          fill: '#001524'
        },
        'highVizLight': {
          primary: '#0099FF',
          secondary: '#007ACC',
          accent: '#6CA9C3',
          neutral: '#B6D9E8',
          background: '#F8F8F8',
          info: '#6CA9C3',
          success: '#16A34A',
          warning: '#BEAB2C',
          error: '#C63939',
        },
        'highVizDark': {
          primary: '#0099FF',
          secondary: '#007ACC',
          accent: '#012A3B',
          neutral: '#00152A',
          background: '#181818',
          info: '#012A3B',
          success: '#8FFFB0',
          warning: '#C4B44E',
          error: '#FF8383',
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
  