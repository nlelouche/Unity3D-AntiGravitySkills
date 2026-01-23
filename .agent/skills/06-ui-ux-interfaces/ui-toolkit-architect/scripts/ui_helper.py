import argparse
import sys
import os

def generate_ui_panel(name, namespace, output_dir):
    """
    Generates UXML, USS, and Controller for a UI Panel.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    # 1. Read Templates
    with open(os.path.join(templates_dir, "PanelTemplate.uxml.txt"), 'r') as f:
        uxml = f.read()
    with open(os.path.join(templates_dir, "PanelStyle.uss.txt"), 'r') as f:
        uss = f.read()
    with open(os.path.join(templates_dir, "PanelController.cs.txt"), 'r') as f:
        ctrl = f.read()
        
    # 2. Replace Placeholders
    title = name.replace("Panel", "")
    
    uxml = uxml.replace("{PANEL_NAME}", name).replace("{PANEL_TITLE}", title)
    # uss usually doesn't need replacement unless we want unique class names, usually shared is better.
    ctrl = ctrl.replace("{NAMESPACE}", namespace).replace("{PANEL_NAME}", name)
    
    # 3. Write Files
    # UI Toolkit assets are best kept together
    panel_dir = os.path.join(output_dir, name)
    os.makedirs(panel_dir, exist_ok=True)
    
    with open(os.path.join(panel_dir, f"{name}.uxml"), 'w') as f:
        f.write(uxml)
    with open(os.path.join(panel_dir, f"{name}.uss"), 'w') as f:
        f.write(uss)
    with open(os.path.join(panel_dir, f"{name}Controller.cs"), 'w') as f:
        f.write(ctrl)
        
    print(f"Generated UI Panel '{name}' at {panel_dir}")

def main():
    parser = argparse.ArgumentParser(description="UI Toolkit Generator")
    parser.add_argument("--name", required=True, help="Name of the panel (e.g. MainMenuPanel)")
    parser.add_argument("--namespace", default="Game.UI", help="C# Namespace")
    parser.add_argument("--output", default="Assets/UI", help="Output Directory")
    
    args = parser.parse_args()
    
    generate_ui_panel(args.name, args.namespace, args.output)
    return 0

if __name__ == "__main__":
    sys.exit(main())
