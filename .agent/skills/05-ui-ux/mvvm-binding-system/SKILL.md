---
name: mvvm-binding-system
description: "Implements a full Model-View-ViewModel (MVVM) architecture for Unity UI Toolkit. Features reactive data binding, INotifyPropertyChanged integration, and the [CreateProperty] source generator workflow."
version: 2.0.0
tags: ["ui", "mvvm", "ui-toolkit", "data-binding", "reactive", "architecture", "uss", "uxml"]
argument-hint: "action='generate' name='HealthBar' model='PlayerModel' OR action='bind' viewmodel='InventoryViewModel'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies:
    - "com.unity.ui"
    - "com.unity.properties"
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for:
    - "com.unity.properties"
    - "com.unity.ui"
performance_budget:
  gc_alloc_per_frame: "0 bytes (binding system batches dirty checks)"
  max_update_cost: "O(dirty_props) — only changed properties trigger UI updates"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
  - mcp_unityMCP_manage_ui
---

# MVVM Binding System (UI Toolkit)

## Overview
**MVVM** separates game data (Model) from display logic (ViewModel) from rendering (View). In Unity 6, UI Toolkit's native data binding system makes this first-class: bind a C# property directly to a UXML element attribute with zero boilerplate. This skill generates the complete M-V-VM triad: the data Model, the observable ViewModel, and the UXML/USS View.

## When to Use
- Use for **HUDs** (health bars, ammo counters, stamina) that react to game state.
- Use for **menus and panels** with dynamic content (inventory lists, shop panels).
- Use for **settings screens** where binding goes both directions (toggle → config).
- ❌ Do NOT use for world-space UI on 3D objects — use Canvas + traditional binding there.
- ❌ Do NOT use for single-display static text (`TextMeshPro` on a prefab is simpler).

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│                    MVVM TRIAD                             │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  MODEL                  VIEWMODEL             VIEW        │
│  ┌───────────────┐      ┌──────────────────┐  ┌───────┐  │
│  │ PlayerModel   │      │HealthBarViewModel│  │ UXML  │  │
│  │               │      │                  │  │       │  │
│  │ float Health  │─────▶│[CreateProperty]  │◀─│bind:  │  │
│  │ float MaxHealth│     │ float Health     │  │health │  │
│  │               │      │ float FillRatio  │  │-value │  │
│  │ (Plain POCO)  │      │ (Observable)     │  └───────┘  │
│  └───────────────┘      └──────────────────┘             │
│                                │                         │
│                       INotifyBindablePropertyChanged      │
│                       (Unity 6 runtime binding)          │
└───────────────────────────────────────────────────────────┘
```

## MVVM Layer Contracts

| Layer | Class Type | Responsibility |
|-------|-----------|----------------|
| **Model** | Plain C# class / ScriptableObject | Holds raw game data. No Unity UI references. |
| **ViewModel** | Plain C# class implementing `INotifyBindablePropertyChanged` | Transforms Model data into bindable properties. Contains display logic. |
| **View** | UXML + USS + `UIDocument` component | Renders properties. Zero game logic. |

## TDD Contract

```csharp
// Test the ViewModel independently — no Unity editor required
[Test]
public void HealthBarViewModel_WhenHealthChanges_FillRatioUpdates()
{
    var model = new PlayerModel { Health = 50f, MaxHealth = 100f };
    var vm = new HealthBarViewModel(model);

    model.Health = 25f;
    vm.RefreshFromModel(); // Explicit refresh (or use events)

    Assert.AreApproximatelyEqual(0.25f, vm.FillRatio, 0.001f);
}

[Test]
public void HealthBarViewModel_WhenHealthZero_FillRatioIsZero()
{
    var model = new PlayerModel { Health = 0f, MaxHealth = 100f };
    var vm = new HealthBarViewModel(model);
    Assert.AreApproximatelyEqual(0f, vm.FillRatio, 0.001f);
}
```

## Procedure

1.  **Define the Model** (plain POCO — no Unity API):
    ```csharp
    public class PlayerModel
    {
        public float Health    { get; set; }
        public float MaxHealth { get; set; }
    }
    ```

2.  **Create the ViewModel** (implements `INotifyBindablePropertyChanged`):
    ```csharp
    using Unity.Properties;
    using UnityEngine.UIElements;

    public partial class HealthBarViewModel : INotifyBindablePropertyChanged
    {
        public event EventHandler<BindablePropertyChangedEventArgs> propertyChanged;

        private readonly PlayerModel _model;
        private float _fillRatio;

        [CreateProperty]
        public float FillRatio
        {
            get => _fillRatio;
            private set
            {
                if (Mathf.Approximately(_fillRatio, value)) return;
                _fillRatio = value;
                Notify(nameof(FillRatio));
            }
        }

        public HealthBarViewModel(PlayerModel model)
        {
            _model = model;
            RefreshFromModel();
        }

        public void RefreshFromModel()
        {
            FillRatio = _model.MaxHealth > 0f ? _model.Health / _model.MaxHealth : 0f;
        }

        private void Notify(string property) =>
            propertyChanged?.Invoke(this, new BindablePropertyChangedEventArgs(property));
    }
    ```

3.  **Create the View (UXML)**:
    ```xml
    <!-- HealthBarView.uxml -->
    <ui:UXML xmlns:ui="UnityEngine.UIElements">
        <ui:VisualElement class="health-bar-container">
            <ui:ProgressBar name="health-bar"
                            binding-path="FillRatio"
                            low-value="0"
                            high-value="1" />
            <ui:Label name="health-label" binding-path="HealthText" />
        </ui:VisualElement>
    </ui:UXML>
    ```

4.  **Wire the Binding in MonoBehaviour**:
    ```csharp
    using UnityEngine;
    using UnityEngine.UIElements;

    [RequireComponent(typeof(UIDocument))]
    public class HealthBarView : MonoBehaviour
    {
        private UIDocument _document;
        private HealthBarViewModel _viewModel;

        // Injected or resolved via ServiceLocator
        [SerializeField] private PlayerModel _model;

        private void Awake()
        {
            _document  = GetComponent<UIDocument>();
            _viewModel = new HealthBarViewModel(_model);
        }

        private void OnEnable()
        {
            _document.rootVisualElement.dataSource = _viewModel;
        }

        private void OnDisable()
        {
            _document.rootVisualElement.dataSource = null;
        }
    }
    ```

## Best Practices

- ✅ **ViewModel is pure C#** — test it without entering Play Mode.
- ✅ Use `[CreateProperty]` — triggers source generation for the binding path.
- ✅ Guard against redundant notifications: `if (value == _field) return;`
- ✅ Set `dataSource` in `OnEnable`, clear in `OnDisable` to prevent memory leaks.
- ✅ Keep USS separate from UXML — styles in `.uss` files, structure in `.uxml`.
- ❌ **NEVER** put game logic (physics, collision) in the ViewModel.
- ❌ **NEVER** reference `MonoBehaviour` from the Model or ViewModel.
- ❌ **NEVER** update UI directly from the Model — always go through the ViewModel.

## Few-Shot Examples

### Example 1: Ammo Counter HUD
**User**: "Create an ammo counter that updates when I shoot."

**Agent**: Generates `AmmoModel`, `AmmoCounterViewModel` with `[CreateProperty] int CurrentAmmo`, and a UXML `<Label binding-path="CurrentAmmo" />`. Subscribes to `WeaponSystem.OnFired` → updates model → ViewModel notifies → binding updates label.

### Example 2: Two-Way Settings Binding
**User**: "Bind a toggle to the mute audio setting."

**Agent**: Creates `AudioSettingsViewModel` with `[CreateProperty] bool IsMuted { get; set; }` where the setter calls `AudioMixer.SetFloat("Volume", value ? -80f : 0f)`. The UXML `<Toggle binding-path="IsMuted"/>` updates bidirectionally.

## Performance Notes

| Approach | Update Cost | GC Alloc |
|----------|:-----------:|:---------:|
| Direct UI update in Update() | O(all_elements)/frame | High |
| Event-driven dirty flags | O(changed_only) | Low |
| MVVM native binding (Unity 6) | O(dirty_props)/frame | 0 bytes |

## Related Skills

- `@ui-toolkit-modern` — UXML/USS authoring foundations
- `@responsive-ui-design` — Multi-resolution layout
- `@event-bus-system` — Model mutation events
- `@service-locator-pattern` — Inject Model into View

## Template Files

- `templates/ModelTemplate.cs.txt` — Pure POCO data model
- `templates/ViewModelTemplate.cs.txt` — INotifyBindablePropertyChanged + [CreateProperty]
- `templates/ViewTemplate.uxml` — UXML with binding-path examples
- `templates/ViewMonoBehaviour.cs.txt` — UIDocument wiring
