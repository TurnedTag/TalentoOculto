(function() {
  const THEME_KEY = 'site_theme';

  function applySavedTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    const theme = saved === 'dark' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);

    const sel = document.getElementById('theme-select');
    if (sel) sel.value = theme;
  }

  function changeTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
  }

  function initListeners() {
    const sel = document.getElementById('theme-select');
    if (sel) {
      sel.addEventListener('change', function() {
        changeTheme(this.value);
      });
    }
  }

  applySavedTheme();
  initListeners();
})();
