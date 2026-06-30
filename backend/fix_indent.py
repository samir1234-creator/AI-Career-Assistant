import sys

path = r"c:\AI-Career-Assistant\backend\api\v1\endpoints\roadmap_endpoint.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if 78 <= i <= 218:
        if line.startswith("    "):
            new_lines.append(line[4:])
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Indentation fixed.")
