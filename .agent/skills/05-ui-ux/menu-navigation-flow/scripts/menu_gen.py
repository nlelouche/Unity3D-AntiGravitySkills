import argparse
import sys
import os

def generate_menu(name, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    with open(os.path.join(templates_dir, "MenuManager.cs.txt"), 'r') as f:
        content = f.read()
    
    content = content.replace("{NAMESPACE}", namespace).replace("{MANAGER_NAME}", name)
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{name}.cs"), 'w') as f:
        f.write(content)
        
    print(f"Generated Menu System in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--namespace", default="Game.UI")
    parser.add_argument("--output", default="Assets/Scripts/UI")
    args = parser.parse_args()
    
    generate_menu(args.name, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
