import argparse
import sys
import os

def generate_horde(name, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    with open(os.path.join(templates_dir, "WaveConfig.cs.txt"), 'r') as f:
        cfg = f.read()
    with open(os.path.join(templates_dir, "WaveManager.cs.txt"), 'r') as f:
        mgr = f.read()
    
    cfg = cfg.replace("{NAMESPACE}", namespace)
    mgr = mgr.replace("{NAMESPACE}", namespace).replace("{MANAGER_NAME}", name)
    
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "WaveConfig.cs"), 'w') as f:
        f.write(cfg)
    with open(os.path.join(output_dir, f"{name}.cs"), 'w') as f:
        f.write(mgr)
        
    print(f"Generated Wave System in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--namespace", default="Game.Combat")
    parser.add_argument("--output", default="Assets/Scripts/Combat")
    args = parser.parse_args()
    
    generate_horde(args.name, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
