import argparse
import sys
import os

def generate_ability_system(name, namespace, output_dir):
    """
    Generates AbilityData and AbilitySystem scripts.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    # 1. Read Templates
    with open(os.path.join(templates_dir, "AbilityData.cs.txt"), 'r') as f:
        data_tpl = f.read()
    with open(os.path.join(templates_dir, "AbilitySystem.cs.txt"), 'r') as f:
        sys_tpl = f.read()
        
    # 2. Replace Placeholders
    data_tpl = data_tpl.replace("{NAMESPACE}", namespace)
    sys_tpl = sys_tpl.replace("{NAMESPACE}", namespace).replace("{SYSTEM_NAME}", name)
    
    # 3. Write Files
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, "AbilityData.cs"), 'w') as f:
        f.write(data_tpl)
    with open(os.path.join(output_dir, f"{name}.cs"), 'w') as f:
        f.write(sys_tpl)
        
    print(f"Generated Ability System in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Ability System Generator")
    parser.add_argument("--name", required=True, help="System Class Name")
    parser.add_argument("--namespace", default="Game.Combat", help="C# Namespace")
    parser.add_argument("--output", default="Assets/Scripts/Abilities", help="Output Directory")
    
    args = parser.parse_args()
    
    generate_ability_system(args.name, args.namespace, args.output)
    return 0

if __name__ == "__main__":
    sys.exit(main())
