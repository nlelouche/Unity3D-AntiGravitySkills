import argparse
import sys
import os

def generate_controller(name, namespace, output_dir, type_):
    """
    Generates a Character Controller based on type.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    template_map = {
        "kinematic-3d": "KinematicController3D.cs.txt",
        "rigidbody-3d": "RigidbodyController3D.cs.txt"
    }
    
    template_file = template_map.get(type_)
    if not template_file:
        print(f"Error: Unknown controller type '{type_}'. Available: {list(template_map.keys())}")
        return 1

    # 1. Read Template
    with open(os.path.join(templates_dir, template_file), 'r') as f:
        content = f.read()
        
    # 2. Replace Placeholders
    content = content.replace("{NAMESPACE}", namespace).replace("{CONTROLLER_NAME}", name)
    
    # 3. Write File
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{name}.cs")
    
    with open(file_path, 'w') as f:
        f.write(content)
        
    print(f"Generated {type_} controller '{name}' at {file_path}")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Character Controller Generator")
    parser.add_argument("--name", required=True, help="Class name")
    parser.add_argument("--namespace", default="Game.Gameplay", help="C# Namespace")
    parser.add_argument("--type", default="kinematic-3d", choices=["kinematic-3d", "rigidbody-3d"], help="Controller Type")
    parser.add_argument("--output", default="Assets/Scripts/Player", help="Output path")
    
    args = parser.parse_args()
    
    return generate_controller(args.name, args.namespace, args.output, args.type)

if __name__ == "__main__":
    sys.exit(main())
