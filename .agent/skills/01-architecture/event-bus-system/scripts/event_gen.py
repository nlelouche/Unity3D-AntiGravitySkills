#!/usr/bin/env python3
"""
Event Generator
Generates event definitions and event bus components.

Usage:
  python event_gen.py --event PlayerDamaged --fields "float DamageAmount,float CurrentHealth"
  python event_gen.py --listener HealthUI --event PlayerDamaged
"""

import argparse
from pathlib import Path


def generate_event(event_name: str, fields: str, namespace: str, output_dir: Path):
    """Generate an event struct."""
    field_lines = []
    for field in fields.split(','):
        field = field.strip()
        if field:
            field_lines.append(f"    public readonly {field};")
    
    content = f'''using UnityEngine;

namespace {namespace}
{{
    /// <summary>
    /// Event: {event_name}
    /// </summary>
    public struct {event_name}Event : IEvent
    {{
{chr(10).join(field_lines)}
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{event_name}Event.cs"
    output_path.write_text(content, encoding='utf-8')
    
    print(f"✓ Generated {event_name}Event.cs")


def generate_listener(listener_name: str, event_name: str, namespace: str, output_dir: Path):
    """Generate a listener component."""
    content = f'''using UnityEngine;

namespace {namespace}
{{
    /// <summary>
    /// Listens to {event_name}Event and responds.
    /// </summary>
    public class {listener_name} : EventListenerBase<{event_name}Event>
    {{
        protected override void OnEventReceived({event_name}Event evt)
        {{
            // TODO: Implement response to event
            Debug.Log($"[{listener_name}] Received {event_name}Event");
        }}
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{listener_name}.cs"
    output_path.write_text(content, encoding='utf-8')
    
    print(f"✓ Generated {listener_name}.cs")


def main():
    parser = argparse.ArgumentParser(description='Generate event components')
    parser.add_argument('--event', '-e', help='Event name to generate')
    parser.add_argument('--fields', '-f', default='', help='Comma-separated fields')
    parser.add_argument('--listener', '-l', help='Listener name to generate')
    parser.add_argument('--namespace', '-ns', default='Game.Events', help='Namespace')
    parser.add_argument('--output', '-o', default='Assets/Scripts/Events', help='Output dir')
    
    args = parser.parse_args()
    output_dir = Path(args.output)
    
    if args.event:
        generate_event(args.event, args.fields, args.namespace, output_dir)
    
    if args.listener and args.event:
        generate_listener(args.listener, args.event, args.namespace, output_dir)
    
    return 0


if __name__ == '__main__':
    exit(main())
