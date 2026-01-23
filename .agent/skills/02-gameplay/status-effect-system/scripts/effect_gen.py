import argparse
import sys
import os

def generate_effects(name, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    with open(os.path.join(templates_dir, "EffectData.cs.txt"), 'r') as f:
        data_tpl = f.read()
    with open(os.path.join(templates_dir, "EffectManager.cs.txt"), 'r') as f:
        mgr_tpl = f.read()
    
    data_tpl = data_tpl.replace("{NAMESPACE}", namespace)
    mgr_tpl = mgr_tpl.replace("{NAMESPACE}", namespace).replace("{MANAGER_NAME}", name)
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "EffectData.cs"), 'w') as f:
        f.write(data_tpl)
    with open(os.path.join(output_dir, f"{name}.cs"), 'w') as f:
        f.write(mgr_tpl)
        
    print(f"Generated Effect System in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--namespace", default="Game.Combat")
    parser.add_argument("--output", default="Assets/Scripts/Combat")
    args = parser.parse_args()
    
    generate_effects(args.name, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
