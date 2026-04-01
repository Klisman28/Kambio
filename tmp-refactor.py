import os
import re

theme_dir = r"c:\dev\Finances\frontend\src\theme"

def refactor_at_imports(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace lines like: import { X } from "@/stores..."
    # and: import '@/assets...'
    # -> to: "@/theme/stores..." and "@/theme/assets..."
    # also handle single quotes
    
    # regex to match: "@/something" -> "@/theme/something"
    new_content = re.sub(r'([\"\'])\@\/', r'\1@/theme/', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Refactored: {filepath}")

for root, _, files in os.walk(theme_dir):
    for filename in files:
        if filename.endswith(".vue") or filename.endswith(".ts") or filename.endswith(".js"):
            filepath = os.path.join(root, filename)
            refactor_at_imports(filepath)
