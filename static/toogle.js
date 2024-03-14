// theme-switch.js

function toggleTheme() {
    const currentTheme = document.getElementById('themeStylesheet').getAttribute('href');
    const isLightTheme = currentTheme.includes('home-light');
  
    if (isLightTheme) {
      document.getElementById('themeStylesheet').href = 'home-dark.css';
    } else {
      document.getElementById('themeStylesheet').href = 'home-light.css';
    }
  }
  