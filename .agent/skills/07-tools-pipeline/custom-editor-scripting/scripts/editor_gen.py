import argparse
import sys
import os

def generate_editor(name, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    with open(os.path.join(templates_dir, "EditorWindow.cs.txt"), 'r') as f:
        content = f.read()
    
    content = content.replace("{NAMESPACE}", namespace).replace("{WINDOW_NAME}", name)
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{name}.cs"), 'w') as f:
        f.write(content)
        
    print(f"Generated Editor Window in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--namespace", default="Game.Editor")
    parser.add_argument("--output", default="Assets/Editor") # Note: Editor folder!
    args = parser.parse_args()
    
    generate_editor(args.name, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
