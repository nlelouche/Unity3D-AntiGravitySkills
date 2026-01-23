---
name: localization-specialist
description: "Integration of Unity Localization package for multi-language support, covering Tables, Smart Strings, and CSV workflows."
version: 1.0.0
tags: ["localization", "i18n", "translation", "language", "csv"]
argument-hint: "key='MainMenu_Play' OR language='es-ES' table='UI_Text'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# Localization Specialist

## Overview
Management of multi-language support using Unity's Localization package. Covers String Tables, Asset Tables, Smart Strings for dynamic values, and CSV import/export workflows.

## When to Use
- Use for translating UI text
- Use for regional asset swapping (flags, voiceover)
- Use for dynamic text (player names, numbers)
- Use when preparing for global release
- Use for managing enormous text databases

## Key Concepts

| Concept | Description |
|---------|-------------|
| **String Table** | Key-Value pairs for text (Key -> "Hello") |
| **Asset Table** | Key-Value pairs for assets (Key -> Texture/Audio) |
| **Locale** | Represents a language/region (en-US, ja-JP) |
| **Smart String** | Text with logic: "You have {count} coin{count:plural(s)}" |
| **Key** | Unique identifier string (e.g., `HUD_Health_Label`) |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  LOCALIZATION ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  LOCALIZATION SETTINGS                                      │
│  ┌──────────────────────┐                                   │
│  │ Locales: [EN, ES, JP]│                                   │
│  │ Default: EN          │                                   │
│  └──────────┬───────────┘                                   │
│             │                                               │
│             ▼                                               │
│  STRING TABLES COLLECTION                                   │
│  ┌──────────┬───────────┬───────────┐                       │
│  │ EN Table │ ES Table  │ JP Table  │                       │
│  ├──────────┼───────────┼───────────┤                       │
│  │ "Play"   │ "Jugar"   │ "Play"    │                       │
│  └──────────┴───────────┴───────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Use descriptive Keys (`Screen_Widget_Description`)
- ✅ Separate Tables by context (`UI`, `Dialogues`, `Items`)
- ✅ Use Smart Strings for pluralization and gender
- ✅ Use CSV for external translation workflow
- ✅ Load Locales asynchronously
- ❌ **NEVER** hardcode text in C# strings
- ❌ **NEVER** use auto-generated Keys (hard to maintain)
- ❌ **NEVER** mix assets and strings in the same table

## Few-Shot Examples

### Example 1: Localizing Logic (C#)
**User**: "Get localized string in code."

**Agent**:
```csharp
using UnityEngine.Localization;
using UnityEngine.Localization.Settings;

public class LocalizationHelper : MonoBehaviour
{
    [SerializeField] private LocalizedString _welcomeMessage; 

    public async void UpdateText()
    {
        // Approach 1: Async handle (Recommended)
        string text = await _welcomeMessage.GetLocalizedStringAsync().Task;
        Debug.Log(text);

        // Approach 2: Direct Table Key
        var op = LocalizationSettings.StringDatabase.GetLocalizedStringAsync("UI_Table", "HUD_Welcome");
        if (op.IsDone) 
            Debug.Log(op.Result);
    }
}
```

### Example 2: Smart String (Pluralization)
**User**: "Text should say '1 coin' or '5 coins'."

**Agent**:
```
Key: `HUD_Coins_Found`
Values:
- EN: "Found {count} coin{count:plural(s)}!"
- ES: "¡Encontraste {count} moneda{count:plural(s)}!"

C# Usage:
_localizedString.Arguments = new object[] { coinCount };
_localizedString.RefreshString();
```

### Example 3: Changing Language
**User**: "Switch language to Spanish."

**Agent**:
```csharp
using UnityEngine.Localization.Settings;

public void SetLanguage(string localeCode) // "es"
{
    var locale = LocalizationSettings.AvailableLocales.GetLocale(localeCode);
    if (locale != null)
    {
        LocalizationSettings.SelectedLocale = locale;
    }
}
```

## Related Skills
- `@ui-toolkit-modern` - Binding localized strings
- `@addressables-asset-management` - Localization uses Addressables
- `@data-driven-design` - Structure keys effectively
