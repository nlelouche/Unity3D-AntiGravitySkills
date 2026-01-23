#!/usr/bin/env python3
"""
Design Patterns Generator
Generates boilerplate code for common design patterns in Unity.

Usage:
  python pattern_gen.py --pattern strategy --name EnemyBehavior --namespace Game.AI
  python pattern_gen.py --pattern factory --name Projectile --namespace Game.Combat
  python pattern_gen.py --pattern observer --name PlayerStats --namespace Game.Core
  python pattern_gen.py --pattern command --name PlayerAction --namespace Game.Input
"""

import argparse
import os
from pathlib import Path
from datetime import datetime

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

def get_template(filename: str) -> str:
    """Load a template file."""
    template_path = TEMPLATES_DIR / filename
    if template_path.exists():
        return template_path.read_text(encoding='utf-8')
    return ""

def replace_placeholders(content: str, replacements: dict) -> str:
    """Replace template placeholders."""
    for key, value in replacements.items():
        content = content.replace(f"{{{{{{key}}}}}", value)
        content = content.replace(f"{{{{{key}}}}}", value)  # Handle both formats
    return content

def generate_strategy(name: str, namespace: str, output_dir: Path):
    """Generate Strategy pattern files."""
    replacements = {"NAMESPACE": namespace, "NAME": name}
    
    # Generate interface
    interface_content = get_template("IStrategy.cs.txt")
    interface_content = replace_placeholders(interface_content, replacements)
    
    # Generate concrete strategy
    concrete = f'''using UnityEngine;

namespace {namespace}.Strategies
{{
    /// <summary>
    /// Concrete implementation of {name} strategy.
    /// TODO: Implement your specific behavior logic.
    /// </summary>
    public class {name}Strategy : IStrategy<{name}Context>
    {{
        public void Execute({name}Context context)
        {{
            // TODO: Implement strategy logic
            Debug.Log($"[{name}Strategy] Executing with context");
        }}
    }}
    
    /// <summary>
    /// Context data for {name} strategies.
    /// </summary>
    public class {name}Context
    {{
        // TODO: Add context properties needed by strategies
        public Transform Target {{ get; set; }}
        public float Speed {{ get; set; }}
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    (output_dir / f"I{name}Strategy.cs").write_text(interface_content, encoding='utf-8')
    (output_dir / f"{name}Strategy.cs").write_text(concrete, encoding='utf-8')
    
    print(f"✓ Generated Strategy pattern for '{name}'")
    print(f"  - I{name}Strategy.cs")
    print(f"  - {name}Strategy.cs")

def generate_factory(name: str, namespace: str, output_dir: Path):
    """Generate Factory pattern files."""
    factory_content = f'''using UnityEngine;

namespace {namespace}.Factories
{{
    /// <summary>
    /// Factory for creating {name} instances.
    /// Uses object pooling for performance.
    /// </summary>
    public class {name}Factory : PooledFactory<{name}>
    {{
        protected override void OnInstanceCreated({name} instance)
        {{
            // TODO: Configure the instance after retrieval from pool
            instance.Initialize();
        }}
        
        protected override void OnInstanceReturned({name} instance)
        {{
            // TODO: Reset the instance before returning to pool
            instance.Reset();
        }}
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{name}Factory.cs").write_text(factory_content, encoding='utf-8')
    
    print(f"✓ Generated Factory pattern for '{name}'")
    print(f"  - {name}Factory.cs")

def generate_observer(name: str, namespace: str, output_dir: Path):
    """Generate Observer pattern files."""
    subject_content = f'''using System;
using System.Collections.Generic;
using UnityEngine;

namespace {namespace}.Events
{{
    /// <summary>
    /// Subject that broadcasts {name} changes to observers.
    /// Remember to unsubscribe in OnDisable/OnDestroy!
    /// </summary>
    public class {name}Subject : MonoBehaviour, ISubject<{name}Data>
    {{
        private readonly List<IObserver<{name}Data>> _observers = new();
        
        public event Action<{name}Data> OnChanged;
        
        public void Subscribe(IObserver<{name}Data> observer)
        {{
            if (!_observers.Contains(observer))
                _observers.Add(observer);
        }}
        
        public void Unsubscribe(IObserver<{name}Data> observer)
        {{
            _observers.Remove(observer);
        }}
        
        public void NotifyObservers({name}Data data)
        {{
            foreach (var observer in _observers)
            {{
                observer.OnNotify(data);
            }}
            OnChanged?.Invoke(data);
        }}
        
        private void OnDestroy()
        {{
            _observers.Clear();
            OnChanged = null;
        }}
    }}
    
    /// <summary>
    /// Data structure for {name} notifications.
    /// </summary>
    [Serializable]
    public struct {name}Data
    {{
        // TODO: Add your data fields
        public float Value;
        public string Message;
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{name}Subject.cs").write_text(subject_content, encoding='utf-8')
    
    print(f"✓ Generated Observer pattern for '{name}'")
    print(f"  - {name}Subject.cs")

def generate_command(name: str, namespace: str, output_dir: Path):
    """Generate Command pattern files."""
    command_content = f'''using UnityEngine;

namespace {namespace}.Commands
{{
    /// <summary>
    /// Command for {name} action with undo support.
    /// </summary>
    public class {name}Command : IReversibleCommand
    {{
        private readonly object _receiver;
        private object _previousState;
        
        public bool CanUndo => _previousState != null;
        
        public {name}Command(object receiver)
        {{
            _receiver = receiver;
        }}
        
        public void Execute()
        {{
            // TODO: Save previous state for undo
            // _previousState = _receiver.GetState();
            
            // TODO: Execute the command
            Debug.Log($"[{name}Command] Executing");
        }}
        
        public void Undo()
        {{
            if (!CanUndo) return;
            
            // TODO: Restore previous state
            Debug.Log($"[{name}Command] Undoing");
        }}
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{name}Command.cs").write_text(command_content, encoding='utf-8')
    
    print(f"✓ Generated Command pattern for '{name}'")
    print(f"  - {name}Command.cs")

GENERATORS = {
    'strategy': generate_strategy,
    'factory': generate_factory,
    'observer': generate_observer,
    'command': generate_command,
}

def main():
    parser = argparse.ArgumentParser(description='Generate design pattern boilerplate')
    parser.add_argument('--pattern', '-p', choices=GENERATORS.keys(), required=True,
                        help='Pattern type to generate')
    parser.add_argument('--name', '-n', required=True,
                        help='Base name for the pattern (e.g., Enemy, Projectile)')
    parser.add_argument('--namespace', '-ns', default='Game',
                        help='C# namespace (default: Game)')
    parser.add_argument('--output', '-o', default='Assets/Scripts/Patterns',
                        help='Output directory (default: Assets/Scripts/Patterns)')
    
    args = parser.parse_args()
    
    output_dir = Path(args.output) / args.pattern.capitalize()
    
    print(f"\n🔧 Generating {args.pattern.upper()} pattern...")
    print(f"   Name: {args.name}")
    print(f"   Namespace: {args.namespace}")
    print(f"   Output: {output_dir}\n")
    
    GENERATORS[args.pattern](args.name, args.namespace, output_dir)
    
    print(f"\n✅ Pattern generated successfully!")
    return 0

if __name__ == '__main__':
    exit(main())
