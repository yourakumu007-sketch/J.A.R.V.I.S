import os
import glob
from pathlib import Path

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace('J.A.R.V.I.S', 'J.A.R.V.I.S').replace('J.A.R.V.I.S', 'J.A.R.V.I.S')
        
        # specific fixes for Github URL that shouldn't be altered if it had J.A.R.V.I.S in it (though it's 'ultronmain' and 'J.A.R.V.I.S' in the zip path)
        new_content = new_content.replace('morphhyyy-cpu/ULTRON', 'morphhyyy-cpu/ULTRON')
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Skipped {filepath}: {e}")

extensions = ['*.py', '*.html', '*.bat', '*.md', '*.json']
root_dir = r"c:\Codeing\ultronmain-main"

for ext in extensions:
    for filepath in glob.glob(os.path.join(root_dir, '**', ext), recursive=True):
        if 'node_modules' in filepath or '.git' in filepath:
            continue
        replace_in_file(filepath)

# Also rename files
files_to_rename = [
    ('START_J.A.R.V.I.S.bat', 'START_JARVIS.bat'),
    ('Start_J.A.R.V.I.S_Wake_Word.bat', 'Start_JARVIS_Wake_Word.bat'),
    ('JARVIS_SETUP.py', 'JARVIS_SETUP.py')
]

for old, new in files_to_rename:
    old_path = os.path.join(root_dir, old)
    new_path = os.path.join(root_dir, new)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed {old} to {new}")
