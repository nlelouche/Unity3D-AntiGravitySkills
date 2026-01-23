#!/usr/bin/env python3
"""
State Machine Generator
Generates state machine components and individual states.

Usage:
  python state_gen.py --context PlayerController --states Idle,Walk,Run,Jump --namespace Game.Player
"""

import argparse
from pathlib import Path


def generate_state(state_name: str, context_name: str, namespace: str) -> str:
    """Generate a single state class."""
    return f'''using UnityEngine;

namespace {namespace}
{{
    public class {state_name}State : StateBase<{context_name}>
    {{
        public override void Enter({context_name} ctx)
        {{
            Debug.Log($"[{state_name}State] Enter");
            // TODO: Initialize state (play animation, reset timers, etc.)
        }}
        
        public override void Update({context_name} ctx)
        {{
            // TODO: Check transition conditions
            // Example: if (condition) TransitionTo<OtherState>();
        }}
        
        public override void FixedUpdate({context_name} ctx)
        {{
            // TODO: Physics-related logic
        }}
        
        public override void Exit({context_name} ctx)
        {{
            // TODO: Cleanup (stop effects, etc.)
        }}
    }}
}}
'''


def generate_context(context_name: str, state_names: list, namespace: str) -> str:
    """Generate the context controller with state machine."""
    add_states = '\n'.join([f'        _stateMachine.AddState(new {s}State());' for s in state_names])
    first_state = state_names[0] if state_names else 'Idle'
    
    return f'''using UnityEngine;

namespace {namespace}
{{
    public class {context_name} : MonoBehaviour
    {{
        private StateMachine<{context_name}> _stateMachine;
        
        // TODO: Add context properties that states need access to
        // public Rigidbody Rigidbody {{ get; private set; }}
        // public Animator Animator {{ get; private set; }}
        // public InputData Input {{ get; set; }}
        
        private void Awake()
        {{
            _stateMachine = new StateMachine<{context_name}>(this);
            
            // Register states
{add_states}
            
            // Set initial state
            _stateMachine.ChangeState<{first_state}State>();
        }}
        
        private void Update()
        {{
            _stateMachine.Update();
        }}
        
        private void FixedUpdate()
        {{
            _stateMachine.FixedUpdate();
        }}
        
        public bool IsInState<T>() where T : IState<{context_name}>
        {{
            return _stateMachine.IsInState<T>();
        }}
    }}
}}
'''


def main():
    parser = argparse.ArgumentParser(description='Generate state machine components')
    parser.add_argument('--context', '-c', required=True, help='Context class name')
    parser.add_argument('--states', '-s', required=True, help='Comma-separated state names')
    parser.add_argument('--namespace', '-ns', default='Game', help='Namespace')
    parser.add_argument('--output', '-o', default='Assets/Scripts/States', help='Output dir')
    
    args = parser.parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    state_names = [s.strip() for s in args.states.split(',')]
    
    # Generate context
    context_content = generate_context(args.context, state_names, args.namespace)
    (output_dir / f"{args.context}.cs").write_text(context_content, encoding='utf-8')
    print(f"✓ Generated {args.context}.cs")
    
    # Generate each state
    states_dir = output_dir / "States"
    states_dir.mkdir(exist_ok=True)
    
    for state_name in state_names:
        state_content = generate_state(state_name, args.context, args.namespace)
        (states_dir / f"{state_name}State.cs").write_text(state_content, encoding='utf-8')
        print(f"✓ Generated States/{state_name}State.cs")
    
    print(f"\n✅ State machine generated with {len(state_names)} states!")
    return 0


if __name__ == '__main__':
    exit(main())
