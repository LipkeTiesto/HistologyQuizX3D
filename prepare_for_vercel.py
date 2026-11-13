# -*- coding: utf-8 -*-
"""
Prepare project for production Vercel hosting:
1. Normalize images into clean, web-safe 'images/' directory
2. Update slides_db.js to point to clean image paths
3. Create root 'index.html'
4. Create 'vercel.json' configuration
5. Create 'package.json' for npm / Vercel detection
6. Create '.gitignore'
"""
import os
import json
import shutil
import re

print("Starting Vercel preparation...")

# 1. Read slides_db.js
with open("slides_db.js", "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r"const SLIDES_DB\s*=\s*(\[.*\]);", content, re.DOTALL)
if not m:
    raise ValueError("Could not parse SLIDES_DB from slides_db.js")

slides = json.loads(m.group(1))

# 2. Prepare images/ directory
os.makedirs("images", exist_ok=True)
copied_count = 0

for slide in slides:
    orig_file = slide.get("file", "")
    # Find extension
    ext = os.path.splitext(orig_file)[1].lower()
    if not ext:
        ext = ".jpg"
    
    clean_name = f"{slide['id']}{ext}"
    dest_path = os.path.join("images", clean_name)
    
    # Try copying from original path
    if os.path.exists(orig_file):
        shutil.copy2(orig_file, dest_path)
        slide["file"] = f"images/{clean_name}"
        copied_count += 1
    else:
        # Check if already exists in images/
        if os.path.exists(dest_path):
            slide["file"] = f"images/{clean_name}"
            copied_count += 1
        else:
            print(f"Warning: File not found: {orig_file}")

print(f"Successfully processed {copied_count} slide images into images/")

# 3. Save updated slides_db.js
with open("slides_db.js", "w", encoding="utf-8") as f:
    f.write("// Histology Master Database for Vercel\n")
    f.write("const SLIDES_DB = " + json.dumps(slides, ensure_ascii=False, indent=2) + ";\n")

print("Updated slides_db.js with clean paths.")

# 4. Copy histology_quiz_app.html -> index.html (Vercel default entry point)
shutil.copy2("histology_quiz_app.html", "index.html")
print("Generated root index.html")

# 5. Create vercel.json
vercel_config = {
    "version": 2,
    "name": "histology-master-quiz",
    "cleanUrls": True,
    "trailingSlash": False,
    "headers": [
        {
            "source": "/(.*)",
            "headers": [
                {
                    "key": "X-Content-Type-Options",
                    "value": "nosniff"
                },
                {
                    "key": "X-Frame-Options",
                    "value": "DENY"
                },
                {
                    "key": "X-XSS-Protection",
                    "value": "1; mode=block"
                }
            ]
        },
        {
            "source": "/images/(.*)",
            "headers": [
                {
                    "key": "Cache-Control",
                    "value": "public, max-age=31536000, immutable"
                }
            ]
        },
        {
            "source": "/(.*)\\.js",
            "headers": [
                {
                    "key": "Content-Type",
                    "value": "application/javascript; charset=utf-8"
                },
                {
                    "key": "Cache-Control",
                    "value": "public, max-age=3600"
                }
            ]
        }
    ]
}

with open("vercel.json", "w", encoding="utf-8") as f:
    json.dump(vercel_config, f, ensure_ascii=False, indent=2)
print("Created vercel.json")

# 6. Create package.json (allows 'npx vercel', 'npm run dev', and auto-detection)
package_json = {
    "name": "histology-quiz-app",
    "version": "1.0.0",
    "description": "Interactive Histology Quiz Application with 3 Training Modes",
    "main": "index.html",
    "scripts": {
        "dev": "serve .",
        "start": "serve ."
    },
    "devDependencies": {
        "serve": "^14.2.4"
    },
    "keywords": [
        "histology",
        "medical-education",
        "quiz",
        "interactive-microscopy",
        "vercel"
    ],
    "author": "Department of Histology",
    "license": "MIT"
}

with open("package.json", "w", encoding="utf-8") as f:
    json.dump(package_json, f, ensure_ascii=False, indent=2)
print("Created package.json")

# 7. Create .gitignore
gitignore_content = """# OS & Editor files
.DS_Store
Thumbs.db
*.tmp
*.log
.vscode/
.idea/

# Node & Vercel
node_modules/
.vercel/

# Heavy raw docx (optional, keep if needed)
# *.docx
"""

with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(gitignore_content.strip() + "\n")
print("Created .gitignore")

print("All Vercel preparation tasks completed successfully!")
