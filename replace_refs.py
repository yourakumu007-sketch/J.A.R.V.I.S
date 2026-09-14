import os
import glob

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace('JARVIS_SETUP.py', 'JARVIS_SETUP.py')
        new_content = new_content.replace('START_JARVIS.bat', 'START_JARVIS.bat')
        new_content = new_content.replace('Start_JARVIS_Wake_Word.bat', 'Start_JARVIS_Wake_Word.bat')
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated filenames in: {filepath}")
    except Exception as e:
        pass

extensions = ['*.py', '*.html', '*.bat', '*.md']
root_dir = r"c:\Codeing\ultronmain-main"

for ext in extensions:
    for filepath in glob.glob(os.path.join(root_dir, '**', ext), recursive=True):
        if 'node_modules' in filepath or '.git' in filepath:
            continue
        replace_in_file(filepath)

