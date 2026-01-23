import argparse
import sys
import os

def generate_bootstrap(name, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    # Check for Unitask requirement or fallback
    # For now, we assume simple templates
    
    with open(os.path.join(templates_dir, "IInitializable.cs.txt"), 'r') as f:
        tf_init = f.read()
    with open(os.path.join(templates_dir, "Bootstrapper.cs.txt"), 'r') as f:
        tf_boot = f.read()
    
    tf_init = tf_init.replace("{NAMESPACE}", namespace)
    tf_boot = tf_boot.replace("{NAMESPACE}", namespace).replace("{CLASS_NAME}", name)
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "IInitializable.cs"), 'w') as f:
        f.write(tf_init)
    with open(os.path.join(output_dir, f"{name}.cs"), 'w') as f:
        f.write(tf_boot)
        
    print(f"Generated Bootstrap Architecture in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--namespace", default="Game.Core")
    parser.add_argument("--output", default="Assets/Scripts/Core")
    args = parser.parse_args()
    
    generate_bootstrap(args.name, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
