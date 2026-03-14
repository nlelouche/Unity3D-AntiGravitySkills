---
name: monetization-iap
description: "Setup for In-App Purchases (IAP) using Unity Purchasing. Handles product catalogs, receipt validation, and store initialization."
version: 2.0.0
tags: ["iap", "monetization", "store", "billing", "revenue"]
argument-hint: "action='buy' product='coins_100' OR type='consumable'"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "N/A - async or editor-only"
  max_update_cost: "N/A"
tdd_first: false
---

# Monetization & IAP

## Overview
Standardized In-App Purchasing (IAP) implemenation using Unity Purchasing package. Supports Consumable (Coins), Non-Consumable (Remove Ads), and Subscription products.

## When to Use
- Use for mobile games (Google Play, App Store)
- Use for selling premium currency
- Use for unlocking features (No Ads)
- Use for DLC content
- Use for verifying purchase receipts

## Product Types

| Type | Description | Example |
|------|-------------|---------|
| **Consumable** | Can be bought repeatedly | 100 Gems, Health Potion |
| **Non-Consumable** | Bought once, permanent | Remove Ads, Level Pack |
| **Subscription** | Recurring billing | VIP Pass (Monthly) |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       IAP FLOW                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  UI BUTTON              IAP MANAGER (Unity)                 │
│  ┌──────────────┐      ┌─────────────────────────┐          │
│  │ OnClick()    │─────▶│ InitiatePurchase(ID)    │          │
│  └──────────────┘      └────────────┬────────────┘          │
│                                     │                       │
│                                     ▼                       │
│                        ┌─────────────────────────┐          │
│                        │ APP STORE / PLAY STORE  │          │
│                        │ (Process Payment)       │          │
│                        └────────────┬────────────┘          │
│                                     │                       │
│                                     ▼                       │
│  GAME LOGIC            ┌─────────────────────────┐          │
│  ┌──────────────┐      │ ProcessPurchase (Cb)    │          │
│  │ Grant Reward │◀─────│ Validate Receipt        │          │
│  └──────────────┘      └─────────────────────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices
- ✅ Initialize early (App Start)
- ✅ Use a catalog (ScriptableObject) for Product IDs
- ✅ Validate receipts server-side if possible (avoid hacking)
- ✅ Handle "Restore Purchases" (Required for iOS)
- ✅ Test with Fake Store in Editor
- ❌ **NEVER** hardcode Product IDs in UI buttons
- ❌ **NEVER** grant rewards before transaction succeeds
- ❌ **NEVER** block UI during purchase (show a spinner)

## Few-Shot Examples

### Example 1: IAP Manager Init
**User**: "Setup IAP with coin packs."

**Agent**:
```csharp
public void InitializePurchasing()
{
    var builder = ConfigurationBuilder.Instance(StandardPurchasingModule.Instance());
    
    // Add Products
    builder.AddProduct("com.game.coins_100", ProductType.Consumable);
    builder.AddProduct("com.game.remove_ads", ProductType.NonConsumable);
    
    UnityPurchasing.Initialize(this, builder);
}
```

### Example 2: Process Purchase
**User**: "Handle successful purchase."

**Agent**:
```csharp
public PurchaseProcessingResult ProcessPurchase(PurchaseEventArgs args)
{
    var product = args.purchasedProduct;
    
    if (product.definition.id == "com.game.coins_100")
    {
        CurrencyManager.AddCoins(100);
    }
    else if (product.definition.id == "com.game.remove_ads")
    {
        AdsManager.DisableAds();
    }
    
    return PurchaseProcessingResult.Complete;
}
```

### Example 3: Restore Transactions
**User**: "Add restore button for iOS."

**Agent**:
```csharp
public void RestorePurchases()
{
    if (Application.platform == RuntimePlatform.IPhonePlayer || 
        Application.platform == RuntimePlatform.OSXPlayer)
    {
        var apple = _extensionProvider.GetExtension<IAppleExtensions>();
        apple.RestoreTransactions(result => {
            Debug.Log($"Restore result: {result}");
        });
    }
}
```

## Related Skills
- `@backend-integration` - Receipt validation
- `@analytics-heatmaps` - Track revenue events
- `@ui-toolkit-modern` - Store UI
