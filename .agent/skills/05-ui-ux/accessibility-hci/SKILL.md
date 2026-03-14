---
name: accessibility-hci
description: "Implements accessibility (A11y) standards for Unity games: WCAG 2.1 color contrast, font scaling, colorblind modes, motor-impaired input remapping, and audio cues for visually impaired players."
version: 2.0.0
tags: ["ui", "accessibility", "a11y", "wcag", "colorblind", "inclusive-design", "hci", "ux"]
argument-hint: "feature='colorblind|font-scale|remapping|audio-cues' action='implement'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies:
    - "com.unity.ui"
    - "com.unity.inputsystem"
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for:
    - "com.unity.inputsystem"
performance_budget:
  gc_alloc_per_frame: "0 bytes (settings applied at startup, no per-frame cost)"
  max_update_cost: "O(1)"
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - write_to_file
---

# Accessibility & HCI

## Overview
Accessible games reach a wider audience and are increasingly required by platform holders (Xbox, PlayStation). This skill implements the core **WCAG 2.1** guidelines adapted for games: sufficient color contrast, scalable text, colorblind-friendly palettes, remappable controls, and audio cues for visually impaired players.

## When to Use
- Use before shipping on console (accessibility is a certification requirement on Xbox/PS5).
- Use when designing HUDs and menus for mass-market games.
- Use to implement a dedicated Accessibility Settings screen.
- ❌ This is NOT a one-time fix — accessibility must be designed in from the start.

## A11y Feature Matrix

| Feature | Impact | Implementation |
|---------|--------|---------------|
| **Text scaling** | Low vision | `IAccessibilitySettings.FontScale` → USS `font-size` |
| **Colorblind modes** | ~8% of males | Post-process Color Adjustment LUT |
| **High contrast** | Low vision | CSS-like USS theme swap |
| **Control remapping** | Motor impaired | New Input System `InputActionRebindingExtensions` |
| **Audio cues** | Visually impaired | `AudioSource.PlayOneShot` on UI focus |
| **Subtitle sizing** | Hard of hearing | Configurable subtitle font size |
| **Reduce motion** | Epilepsy / vestibular | Disable screen shake, flash effects |

## Core: Accessibility Settings

```csharp
// --- IAccessibilitySettings.cs ---
public interface IAccessibilitySettings
{
    float FontScale          { get; set; } // 0.75 – 2.0
    ColorblindMode Colorblind { get; set; }
    bool  HighContrast       { get; set; }
    bool  ReduceMotion       { get; set; }
    bool  AudioCuesEnabled   { get; set; }
    float SubtitleScale      { get; set; }
}

public enum ColorblindMode { None, Protanopia, Deuteranopia, Tritanopia }

// --- AccessibilitySettings.cs ---
using UnityEngine;

public class AccessibilitySettings : IAccessibilitySettings
{
    private const string KEY_FONT     = "a11y_font_scale";
    private const string KEY_COLORBLIND = "a11y_colorblind";

    public float FontScale
    {
        get => PlayerPrefs.GetFloat(KEY_FONT, 1f);
        set { PlayerPrefs.SetFloat(KEY_FONT, Mathf.Clamp(value, 0.75f, 2.0f)); ApplyFontScale(value); }
    }

    public ColorblindMode Colorblind
    {
        get => (ColorblindMode)PlayerPrefs.GetInt(KEY_COLORBLIND, 0);
        set { PlayerPrefs.SetInt(KEY_COLORBLIND, (int)value); ApplyColorblindMode(value); }
    }

    public bool ReduceMotion
    {
        get => PlayerPrefs.GetInt("a11y_reduce_motion", 0) == 1;
        set => PlayerPrefs.SetInt("a11y_reduce_motion", value ? 1 : 0);
    }

    public bool  HighContrast     { get; set; }
    public bool  AudioCuesEnabled { get; set; } = true;
    public float SubtitleScale    { get; set; } = 1f;

    private void ApplyFontScale(float scale)
    {
        // UI Toolkit: set custom property on root element
        var root = UnityEngine.UIElements.UIDocument.FindObjectOfType<UnityEngine.UIElements.UIDocument>();
        root?.rootVisualElement.style.fontSize = new UnityEngine.UIElements.StyleLength(16f * scale);
    }

    private void ApplyColorblindMode(ColorblindMode mode)
    {
        // Apply via post-processing Color Lookup or shader global
        Shader.SetGlobalInt("_ColorblindMode", (int)mode);
    }
}
```

## Colorblind Mode Shader

```hlsl
// Add to any post-process pass or full-screen blit shader:
int _ColorblindMode; // 0=None, 1=Protanopia, 2=Deuteranopia, 3=Tritanopia

float3 ApplyColorblind(float3 col)
{
    if (_ColorblindMode == 1) // Protanopia (red-blind)
        return float3(0.567*col.r + 0.433*col.g, 0.558*col.r + 0.442*col.g, 0.242*col.g + 0.758*col.b);
    if (_ColorblindMode == 2) // Deuteranopia (green-blind)
        return float3(0.625*col.r + 0.375*col.g, 0.700*col.r + 0.300*col.g, 0.300*col.g + 0.700*col.b);
    if (_ColorblindMode == 3) // Tritanopia (blue-blind)
        return float3(0.950*col.r + 0.050*col.g, 0.433*col.g + 0.567*col.b, 0.475*col.g + 0.525*col.b);
    return col;
}
```

## Control Remapping (New Input System)

```csharp
using UnityEngine.InputSystem;

public class ControlRemapper
{
    public void StartRebind(InputAction action, int bindingIndex, System.Action onComplete)
    {
        action.Disable();
        action.PerformInteractiveRebinding(bindingIndex)
              .WithCancelingThrough("<Keyboard>/escape")
              .OnComplete(op =>
              {
                  op.Dispose();
                  action.Enable();
                  onComplete?.Invoke();
                  // Save: PlayerPrefs.SetString(action.id.ToString(), action.SaveBindingOverridesAsJson())
              })
              .Start();
    }
}
```

## WCAG 2.1 Color Contrast Quick Reference

| Contrast Ratio | Usage |
|:--------------:|-------|
| **4.5:1** | Normal text (minimum) |
| **3:1** | Large text (≥18pt or bold ≥14pt) |
| **7:1** | Enhanced (AAA) — recommended for HUDs |

*Use the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) for any UI color combination.*

## Best Practices

- ✅ **Never convey information by color alone** — also use icons, patterns, or text labels.
- ✅ Provide a **dedicated Accessibility menu** in Settings, not buried in sub-menus.
- ✅ All interactive elements must be reachable via **keyboard/controller navigation**.
- ✅ Use the **Reduce Motion** flag to skip camera shake and flash VFX.
- ❌ **NEVER** use red/green as the sole indicator for success/failure (protanopia/deuteranopia).
- ❌ **NEVER** use text smaller than 12pt at 1080p for critical UI.



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void AccessibilityHci_Should{ExpectedBehavior}_When{Condition}()
{{
    // Arrange
    // TODO: Setup test fixtures
    
    // Act
    // TODO: Execute system under test
    
    // Assert
    Assert.Fail("Not implemented — write test first");
}}

// Test 2: should handle [edge case]
[Test]
public void AccessibilityHci_ShouldHandle{EdgeCase}()
{{
    // Arrange
    // TODO: Setup edge case scenario
    
    // Act
    // TODO: Execute
    
    // Assert
    Assert.Fail("Not implemented");
}}

// Test 3: should throw when [invalid input]
[Test]
public void AccessibilityHci_ShouldThrow_When{InvalidInput}()
{{
    // Arrange
    var invalidInput = default;
    
    // Act & Assert
    Assert.Throws<Exception>(() => {{ /* execute */ }});
}}
```

### Pasos para completar el TDD:

1. **Descomenta** los tests above
2. **Implementa** la funcionalidad mínima para que compile
3. **Ejecuta** los tests — deben fallar (RED)
4. **Implementa** la funcionalidad real
5. **Verifica** que los tests pasen (GREEN)
6. **Refactorea** manteniendo los tests verdes

---

**Nota**: Este skill fue marcado como `tdd_first: false` durante la auditoría v2.0.1. La sección TDD fue agregada automáticamente pero requiere customización manual para reflejar el comportamiento real del skill.


## Related Skills

- `@ui-toolkit-modern` — USS font-size and custom properties
- `@input-system-new` — Rebinding foundation
- `@mvvm-binding-system` — Bind `IAccessibilitySettings` to UI controls
