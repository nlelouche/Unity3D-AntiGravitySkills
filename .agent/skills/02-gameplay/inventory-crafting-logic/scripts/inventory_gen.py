import argparse
import sys
import os

def generate_inventory(name, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    # 1. Read
    with open(os.path.join(templates_dir, "ItemData.cs.txt"), 'r') as f:
        item_tpl = f.read()
    with open(os.path.join(templates_dir, "InventoryModel.cs.txt"), 'r') as f:
        model_tpl = f.read()
        
    # 2. Replace
    item_tpl = item_tpl.replace("{NAMESPACE}", namespace)
    model_tpl = model_tpl.replace("{NAMESPACE}", namespace).replace("{INVENTORY_NAME}", name)
    
    # 3. Write
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "ItemData.cs"), 'w') as f:
        f.write(item_tpl)
    with open(os.path.join(output_dir, f"{name}Model.cs"), 'w') as f:
        f.write(model_tpl)
        
    print(f"Generated Inventory System '{name}'")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--namespace", default="Game.Inventory")
    parser.add_argument("--output", default="Assets/Scripts/Inventory")
    args = parser.parse_args()
    
    generate_inventory(args.name, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
