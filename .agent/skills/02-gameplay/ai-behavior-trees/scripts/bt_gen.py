import argparse
import sys
import os

def generate_bt(actions, namespace, output_dir):
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    
    # 1. Core Nodes
    core_files = ["Node.cs.txt", "Selector.cs.txt", "Sequence.cs.txt"]
    os.makedirs(output_dir, exist_ok=True)
    
    for tpl_name in core_files:
        with open(os.path.join(templates_dir, tpl_name), 'r') as f:
            content = f.read()
        content = content.replace("{NAMESPACE}", namespace)
        
        real_name = tpl_name.replace(".txt", "")
        with open(os.path.join(output_dir, real_name), 'w') as f:
            f.write(content)

    # 2. Generate Action Nodes Stubs
    if actions:
        action_list = actions.split(",")
        for action in action_list:
            action_class = f"Task{action.strip()}"
            content = f"""using UnityEngine;
using {namespace};

namespace {namespace}
{{
    public class {action_class} : Node
    {{
        private Transform _transform;

        public {action_class}(Transform transform)
        {{
            _transform = transform;
        }}

        public override NodeState Evaluate()
        {{
            // TODO: Implement {action} logic
            return NodeState.Success;
        }}
    }}
}}"""
            with open(os.path.join(output_dir, f"{action_class}.cs"), 'w') as f:
                f.write(content)

    print(f"Generated Behavior Tree Framework in {output_dir}")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--actions", help="Comma separated list of actions (e.g. Patrol,Attack)")
    parser.add_argument("--namespace", default="Game.AI")
    parser.add_argument("--output", default="Assets/Scripts/AI")
    args = parser.parse_args()
    
    generate_bt(args.actions, args.namespace, args.output)

if __name__ == "__main__":
    sys.exit(main())
