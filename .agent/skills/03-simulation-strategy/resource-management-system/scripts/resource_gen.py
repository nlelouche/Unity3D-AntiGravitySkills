import argparse
import sys
import os

def generate_resources(name, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    with open(os.path.join(templates_dir, "ResourceType.cs.txt"), 'r') as f:
        type_tpl = f.read()
    with open(os.path.join(templates_dir, "ResourceManager.cs.txt"), 'r') as f:
        mgr_tpl = f.read()
    
    type_tpl = type_tpl.replace("{NAMESPACE}", namespace)
    mgr_tpl = mgr_tpl.replace("{NAMESPACE}", namespace).replace("{MANAGER_NAME}", name)
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "ResourceType.cs"), 'w') as f:
        f.write(type_tpl)
    with open(os.path.join(output_dir, f"{name}.cs"), 'w') as f:
        f.write(mgr_tpl)
        
    print(f"Generated Economy System in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--namespace", default="Game.Economy")
    parser.add_argument("--output", default="Assets/Scripts/Economy")
    args = parser.parse_args()
    
    generate_resources(args.name, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
