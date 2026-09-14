import os
import glob

def fix_python_identifiers(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace('JarvisUI', 'JarvisUI')
        new_content = new_content.replace('JarvisWebWindow', 'JarvisWebWindow')
        new_content = new_content.replace('JarvisLive', 'JarvisLive')
        new_content = new_content.replace('JARVIS_SETUP', 'JARVIS_SETUP')
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed identifiers in: {filepath}")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

root_dir = r"c:\Codeing\ultronmain-main"
extensions = ['*.py', '*.bat', '*.md']

for ext in extensions:
    for filepath in glob.glob(os.path.join(root_dir, '**', ext), recursive=True):
        if 'node_modules' in filepath or '.git' in filepath:
            continue
        fix_python_identifiers(filepath)
