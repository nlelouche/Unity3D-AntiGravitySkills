import argparse
import sys
import os

def generate_state_machine(name, namespace, output_dir):
    """
    Generates a generic HFSM implementation.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    # 1. Read Templates
    with open(os.path.join(templates_dir, "StateBase.cs.txt"), 'r') as f:
        state_base_content = f.read()
    with open(os.path.join(templates_dir, "StateMachineController.cs.txt"), 'r') as f:
        controller_content = f.read()
        
    # 2. Replace Placeholders
    state_base_content = state_base_content.replace("{NAMESPACE}", namespace).replace("{STATE_MACHINE_NAME}", name)
    controller_content = controller_content.replace("{NAMESPACE}", namespace).replace("{STATE_MACHINE_NAME}", name)
    
    # 3. Write Files
    os.makedirs(output_dir, exist_ok=True)
    
    base_file = os.path.join(output_dir, f"{name}State.cs")
    ctrl_file = os.path.join(output_dir, f"{name}Controller.cs")
    
    with open(base_file, 'w') as f:
        f.write(state_base_content)
    
    with open(ctrl_file, 'w') as f:
        f.write(controller_content)
        
    print(f"Generated State Machine for '{name}' at {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="OOP Patterns Generator")
    parser.add_argument("--pattern", default="state-machine", help="Design Pattern to generate")
    parser.add_argument("--name", required=True, help="Name of the system (e.g. PlayerLocomotion)")
    parser.add_argument("--namespace", default="Game.Systems", help="C# Namespace")
    parser.add_argument("--output", default="Assets/Scripts/Generated", help="Output Directory")
    
    args = parser.parse_args()
    
    if args.pattern == "state-machine":
        generate_state_machine(args.name, args.namespace, args.output)
    else:
        print(f"Unknown pattern: {args.pattern}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
