#!/usr/bin/env python3
"""
ScriptableObject Generator
Generates SO data containers and event channels.

Usage:
  python so_gen.py --type data --name WeaponConfig --fields "float Damage,float FireRate"
  python so_gen.py --type event --name OnPlayerDamaged --fields "float Amount,Vector3 Position"
  python so_gen.py --type runtimeset --name EnemySet --item_type Enemy
"""

import argparse
from pathlib import Path


def generate_data_so(name: str, fields: str, namespace: str, output_dir: Path):
    """Generate a data container SO."""
    field_lines = []
    property_lines = []
    
    for field in fields.split(','):
        field = field.strip()
        if not field:
            continue
        parts = field.split()
        if len(parts) >= 2:
            field_type = parts[0]
            field_name = parts[1]
            private_name = f"_{field_name[0].lower()}{field_name[1:]}"
            field_lines.append(f"        [SerializeField] private {field_type} {private_name};")
            property_lines.append(f"        public {field_type} {field_name} => {private_name};")
    
    content = f'''using UnityEngine;

namespace {namespace}
{{
    [CreateAssetMenu(fileName = "New{name}", menuName = "Game/Data/{name}")]
    public class {name}SO : ScriptableObject
    {{
        [Header("Configuration")]
{chr(10).join(field_lines)}
        
{chr(10).join(property_lines)}
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{name}SO.cs").write_text(content, encoding='utf-8')
    print(f"✓ Generated {name}SO.cs")


def generate_event_so(name: str, fields: str, namespace: str, output_dir: Path):
    """Generate an event channel SO with typed payload."""
    field_defs = []
    for field in fields.split(','):
        field = field.strip()
        if field:
            field_defs.append(field)
    
    has_payload = len(field_defs) > 0
    
    if has_payload:
        content = f'''using System;
using System.Collections.Generic;
using UnityEngine;

namespace {namespace}
{{
    [Serializable]
    public struct {name}Data
    {{
{chr(10).join([f"        public {f};" for f in field_defs])}
    }}
    
    [CreateAssetMenu(fileName = "{name}", menuName = "Game/Events/{name}")]
    public class {name}EventSO : ScriptableObject
    {{
        private readonly List<Action<{name}Data>> _listeners = new();
        
        public void Raise({name}Data data)
        {{
            for (int i = _listeners.Count - 1; i >= 0; i--)
                _listeners[i]?.Invoke(data);
        }}
        
        public void Subscribe(Action<{name}Data> listener) => _listeners.Add(listener);
        public void Unsubscribe(Action<{name}Data> listener) => _listeners.Remove(listener);
    }}
}}
'''
    else:
        content = f'''using System;
using System.Collections.Generic;
using UnityEngine;

namespace {namespace}
{{
    [CreateAssetMenu(fileName = "{name}", menuName = "Game/Events/{name}")]
    public class {name}EventSO : ScriptableObject
    {{
        private readonly List<Action> _listeners = new();
        
        public void Raise()
        {{
            for (int i = _listeners.Count - 1; i >= 0; i--)
                _listeners[i]?.Invoke();
        }}
        
        public void Subscribe(Action listener) => _listeners.Add(listener);
        public void Unsubscribe(Action listener) => _listeners.Remove(listener);
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{name}EventSO.cs").write_text(content, encoding='utf-8')
    print(f"✓ Generated {name}EventSO.cs")


def generate_runtime_set(name: str, item_type: str, namespace: str, output_dir: Path):
    """Generate a runtime set SO."""
    content = f'''using UnityEngine;

namespace {namespace}
{{
    [CreateAssetMenu(fileName = "{name}", menuName = "Game/RuntimeSets/{name}")]
    public class {name}SO : RuntimeSetSO<{item_type}>
    {{
        // Optional: Add custom methods for this specific set
        // public {item_type} GetClosestTo(Vector3 position) {{ ... }}
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{name}SO.cs").write_text(content, encoding='utf-8')
    print(f"✓ Generated {name}SO.cs")


def main():
    parser = argparse.ArgumentParser(description='Generate ScriptableObject components')
    parser.add_argument('--type', '-t', choices=['data', 'event', 'runtimeset'],
                        required=True, help='SO type')
    parser.add_argument('--name', '-n', required=True, help='Name (without SO suffix)')
    parser.add_argument('--fields', '-f', default='', help='Comma-separated fields')
    parser.add_argument('--item_type', '-i', default='MonoBehaviour', help='Item type for runtimeset')
    parser.add_argument('--namespace', '-ns', default='Game.Data', help='Namespace')
    parser.add_argument('--output', '-o', default='Assets/Scripts/ScriptableObjects', help='Output')
    
    args = parser.parse_args()
    output_dir = Path(args.output)
    
    if args.type == 'data':
        generate_data_so(args.name, args.fields, args.namespace, output_dir)
    elif args.type == 'event':
        generate_event_so(args.name, args.fields, args.namespace, output_dir)
    elif args.type == 'runtimeset':
        generate_runtime_set(args.name, args.item_type, args.namespace, output_dir)
    
    return 0


if __name__ == '__main__':
    exit(main())
