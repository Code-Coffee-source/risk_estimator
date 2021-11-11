module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      'lato' : ['Lato', 'sans-serif']
    },

    extend: {
      transitionProperty: {
        'height':'height'
      },
      colors: {
        'charlotte-green': '337970',
        'charlotte-gold': 'b1a36a',
        'charlotte-blue': '333d51',
        'orange': 'd6974',
        'dirty-white': 'e3e7f0',
        'blue-stained-white': 'd6e4f5'
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.25rem',
        '4xl': '1.5rem',
        '6xl': '2rem',
        '7xl': '2.5rem',
        '8xl': '3rem',
      },
      letterSpacing : {
        widest2x: '.25rem',
        widest3x: '.50rem',
      }
    },
  },
  variants: {
    height: ['responsive', 'hover', 'focus'],
  },
  plugins: [],
}
