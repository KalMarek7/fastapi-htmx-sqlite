import os
import subprocess

# Set the paths
src_css = "templates/style.css"
dst_css = "static/css/output.css"
config_file = "tailwind.config.js"

# Create the directories if they don't exist
os.makedirs(os.path.dirname(src_css), exist_ok=True)
os.makedirs(os.path.dirname(dst_css), exist_ok=True)

# Write the Tailwind CSS source
with open(src_css, "w") as f:
    f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;")

# Run the Tailwind CSS build command
subprocess.run(["npx", "tailwindcss", "-i", src_css, "-o",
               dst_css, "--config", config_file, "--minify"], check=True)
