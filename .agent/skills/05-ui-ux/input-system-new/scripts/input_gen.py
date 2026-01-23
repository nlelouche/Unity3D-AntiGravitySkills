import argparse
import sys
import os

def generate_input(name, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    with open(os.path.join(templates_dir, "InputReader.cs.txt"), 'r') as f:
        content = f.read()
    
    content = content.replace("{NAMESPACE}", namespace)
    # Note: 'GameInput' is hardcoded in template as assumption of generated class name.
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "InputReader.cs"), 'w') as f:
        f.write(content)
        
    print(f"Generated Input Reader in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--namespace", default="Game.Input")
    parser.add_argument("--output", default="Assets/Scripts/Input")
    args = parser.parse_args()
    
    generate_input(args.name, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
