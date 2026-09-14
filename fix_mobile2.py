import os

filepath = r"dashboard\static\app.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Make sure messages break words on mobile
if "word-break: break-word;" not in html:
    html = html.replace('.msg{', '.msg{word-break: break-word; ')
    
with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Added word-break")
