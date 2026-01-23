import argparse
import sys
import os

def generate_service(name, namespace, output_dir):
    """
    Generates Interface and Mock Implementation.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    # 1. Read Templates
    with open(os.path.join(templates_dir, "IService.cs.txt"), 'r') as f:
        interface_content = f.read()
        
    # 2. Replace Placeholders
    interface_content = interface_content.replace("{NAMESPACE}", namespace).replace("{SERVICE_NAME}", name).replace("{DATA_TYPE}", "string")
    
    # 3. Write Files
    os.makedirs(output_dir, exist_ok=True)
    
    interface_file = os.path.join(output_dir, f"I{name}.cs")
    
    with open(interface_file, 'w') as f:
        f.write(interface_content)
        
    print(f"Generated Service '{name}' at {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Service Generator")
    parser.add_argument("--name", required=True, help="Name of the service (e.g. AuthService)")
    parser.add_argument("--namespace", default="Game.Services", help="C# Namespace")
    parser.add_argument("--output", default="Assets/Scripts/Services", help="Output Directory")
    
    args = parser.parse_args()
    
    generate_service(args.name, args.namespace, args.output)
    return 0

if __name__ == "__main__":
    sys.exit(main())
