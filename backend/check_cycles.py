import json

with open("c:\\AI-Career-Assistant\\backend\\core\\skill_dependency_database.json") as f:
    db = json.load(f)

def check_cycles():
    visited = set()
    stack = set()
    
    def dfs(node):
        node = node.lower()
        if node in stack:
            print(f"CYCLE DETECTED AT: {node}")
            return True
        if node in visited:
            return False
            
        visited.add(node)
        stack.add(node)
        
        for k, deps in db.items():
            if k.lower() == node:
                for dep in deps:
                    if dfs(dep):
                        return True
                        
        stack.remove(node)
        return False
        
    for k in db.keys():
        if dfs(k):
            return True
    return False

if check_cycles():
    print("Graph has cycles!")
else:
    print("No cycles found.")
