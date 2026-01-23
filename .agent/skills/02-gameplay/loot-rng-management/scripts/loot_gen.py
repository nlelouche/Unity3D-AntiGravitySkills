import argparse
import sys
import os

def generate_loot(namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    with open(os.path.join(templates_dir, "DropTable.cs.txt"), 'r') as f:
        content = f.read()
    
    content = content.replace("{NAMESPACE}", namespace)
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "DropTable.cs"), 'w') as f:
        f.write(content)
        
    print(f"Generated Loot System in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--namespace", default="Game.Loot")
    parser.add_argument("--output", default="Assets/Scripts/Loot")
    args = parser.parse_args()
    
    generate_loot(args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
