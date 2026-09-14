import os

filepath = r"c:\Codeing\ultronmain-main\dashboard\static\app.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Fix Javascript function names that got corrupted
content = content.replace("setJ.A.R.V.I.STheme", "setJarvisTheme")
content = content.replace("speakJ.A.R.V.I.SEmergency", "speakJarvisEmergency")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Fixed JS identifiers in {filepath}")
