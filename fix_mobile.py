import os

filepath = r"dashboard\static\app.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Add viewport-fit=cover and link manifest
html = html.replace(
    '<meta name="viewport" content="width=device-width,initial-scale=1">',
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<link rel="manifest" href="/manifest.json">'
)

# Add media queries for mobile
css_addition = """
/* --- MOBILE RESPONSIVENESS --- */
@media (max-width: 1023px) {
  #app {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto auto;
    gap: 8px;
    padding: max(12px, env(safe-area-inset-top)) max(12px, env(safe-area-inset-right)) max(12px, env(safe-area-inset-bottom)) max(12px, env(safe-area-inset-left));
    height: auto;
    min-height: 100%;
  }
  #webgl { position: fixed; }
  .top { grid-row: 1; flex-direction: column; align-items: stretch; text-align: center; }
  .tele { justify-content: center; margin: 8px 0; }
  .core { grid-row: 2; margin: 20px 0; min-height: 250px; }
  .side { grid-row: 3; display: flex; flex-direction: column; gap: 8px; }
  .bottom { grid-row: 4; flex-direction: column; gap: 8px; align-items: stretch; margin-top: 15px; }
  .bottom .dock { flex-wrap: wrap; justify-content: center; }
  
  /* Make buttons touch friendly */
  .btn, .input { min-height: 44px; padding: 12px 16px; font-size: 13px; }
  
  /* Collapsible panels for mobile */
  .panel .title { cursor: pointer; padding-bottom: 5px; border-bottom: 1px solid var(--h); position: relative; }
  .panel .title::after { content: "+"; position: absolute; right: 0; }
  .panel.open .title::after { content: "-"; }
  .panel:not(.open) .data, .panel:not(.open) .bar, .panel:not(.open) .events, .panel:not(.open) > div:not(.title) { display: none !important; }
  
  /* Chat modal on mobile */
  .modal { padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left); align-items: flex-end; }
  .card { width: 100vw; height: 100%; max-height: calc(100vh - env(safe-area-inset-top)); border-radius: 8px 8px 0 0; display: flex; flex-direction: column; }
  .feed { flex: 1; max-height: none; overflow-y: auto; }
}
"""

if "/* --- MOBILE RESPONSIVENESS --- */" not in html:
    html = html.replace("</style>", css_addition + "\n</style>")

# Add JS for toggling panels on mobile
js_addition = """
// Mobile panel collapse logic
document.querySelectorAll('.panel .title').forEach(t => {
  t.addEventListener('click', () => {
    if (window.innerWidth <= 1023) {
      t.parentElement.classList.toggle('open');
    }
  });
});
"""

if "Mobile panel collapse logic" not in html:
    html = html.replace("})();", js_addition + "\n})();")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated app.html with mobile responsiveness")
