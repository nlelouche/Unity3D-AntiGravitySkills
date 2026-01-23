#!/usr/bin/env python3
"""
Interface Generator
Generates common Unity interface patterns with boilerplate.

Usage:
  python interface_gen.py --type damageable --namespace Game.Interfaces
  python interface_gen.py --type interactable --namespace Game.Interfaces
  python interface_gen.py --type custom --name IControllable --methods "Move(Vector3),Stop"
"""

import argparse
from pathlib import Path

INTERFACE_TEMPLATES = {
    'damageable': '''public interface IDamageable
{{
    float CurrentHealth {{ get; }}
    float MaxHealth {{ get; }}
    bool IsAlive {{ get; }}
    void TakeDamage(float amount, GameObject source = null);
}}''',
    
    'interactable': '''public interface IInteractable
{{
    string InteractionPrompt {{ get; }}
    bool CanInteract {{ get; }}
    void Interact(GameObject interactor);
    void OnFocus();
    void OnUnfocus();
}}''',
    
    'saveable': '''public interface ISaveable
{{
    string SaveId {{ get; }}
    int SavePriority {{ get; }}
    object CaptureState();
    void RestoreState(object state);
}}''',
    
    'poolable': '''public interface IPoolable
{{
    void OnSpawnFromPool();
    void OnReturnToPool();
    void ReturnToPool();
}}''',
}


def generate_interface(interface_type: str, namespace: str, output_dir: Path):
    """Generate interface based on type."""
    if interface_type not in INTERFACE_TEMPLATES:
        print(f"Unknown interface type: {interface_type}")
        print(f"Available: {', '.join(INTERFACE_TEMPLATES.keys())}")
        return
    
    template = INTERFACE_TEMPLATES[interface_type]
    interface_name = f"I{interface_type.capitalize()}"
    
    content = f'''using UnityEngine;

namespace {namespace}
{{
    /// <summary>
    /// Auto-generated {interface_name} interface.
    /// </summary>
    {template}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{interface_name}.cs"
    output_path.write_text(content, encoding='utf-8')
    
    print(f"✓ Generated {interface_name}.cs at {output_path}")


def generate_custom_interface(name: str, methods: str, namespace: str, output_dir: Path):
    """Generate custom interface with specified methods."""
    method_lines = []
    for method in methods.split(','):
        method = method.strip()
        method_lines.append(f"    void {method}();")
    
    content = f'''using UnityEngine;

namespace {namespace}
{{
    /// <summary>
    /// Custom interface: {name}
    /// </summary>
    public interface {name}
    {{
{chr(10).join(method_lines)}
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{name}.cs"
    output_path.write_text(content, encoding='utf-8')
    
    print(f"✓ Generated {name}.cs at {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate Unity interface patterns')
    parser.add_argument('--type', '-t', choices=list(INTERFACE_TEMPLATES.keys()) + ['custom'],
                        required=True, help='Interface type')
    parser.add_argument('--namespace', '-ns', default='Game.Interfaces',
                        help='C# namespace')
    parser.add_argument('--output', '-o', default='Assets/Scripts/Interfaces',
                        help='Output directory')
    parser.add_argument('--name', '-n', help='Custom interface name (for type=custom)')
    parser.add_argument('--methods', '-m', help='Comma-separated methods (for type=custom)')
    
    args = parser.parse_args()
    output_dir = Path(args.output)
    
    if args.type == 'custom':
        if not args.name or not args.methods:
            print("Error: --name and --methods required for custom type")
            return 1
        generate_custom_interface(args.name, args.methods, args.namespace, output_dir)
    else:
        generate_interface(args.type, args.namespace, output_dir)
    
    return 0


if __name__ == '__main__':
    exit(main())
