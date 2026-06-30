import re

file_path = "frontend/src/pages/RoadmapDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix React import
content = content.replace("import React, { useState", "import { useState")

# Fix getSharedRoadmap
content = content.replace(", getSharedRoadmap ", " ")

# Fix loadProgress and saveProgress
content = re.sub(r'const loadProgress = .*?\n};', '', content, flags=re.DOTALL)
content = re.sub(r'const saveProgress = .*?\n};', '', content, flags=re.DOTALL)

# Restore all catch blocks
content = content.replace("} catch {", "} catch (err) {")

# Then fix ONLY the ones that don't use 'err'
# (The one in handleShare doesn't use err, it just does setShareMsg)
content = content.replace("} catch (err) {\n      setShareMsg", "} catch {\n      setShareMsg")

# Also, if there's an empty block like try { ... } catch (err) {}
content = content.replace("} catch (err) {}", "} catch {}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Final ESLint fixes applied.")
