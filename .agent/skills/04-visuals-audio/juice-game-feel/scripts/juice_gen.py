import argparse
import sys
import os

def generate_juice(name, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    with open(os.path.join(templates_dir, "FeedbackController.cs.txt"), 'r') as f:
        content = f.read()
    
    content = content.replace("{NAMESPACE}", namespace).replace("{CLASS_NAME}", name)
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{name}.cs"), 'w') as f:
        f.write(content)
        
    print(f"Generated Game Feel Controller in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--namespace", default="Game.Feedback")
    parser.add_argument("--output", default="Assets/Scripts/Feedback")
    args = parser.parse_args()
    
    generate_juice(args.name, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
