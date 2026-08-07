# ListView

## 1. Purpose and characteristic

Use `ListView` to display and interact with a vertical collection of data items. It supports data binding, virtualization, selection, invocation, and item templates.

### WINUI-LISTVIEW-PURPOSE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** choosing a list without defining selection or invocation behavior

Define whether the list is display-only, single-select, multi-select, or item-invoking. Configure `SelectionMode` and interaction behavior to match that purpose.

**Sources:** `MS-WIN-CONTROLS-LISTVIEW`

## 2. Anatomy

A list contains the `ListView` viewport, generated `ListViewItem` containers, item content from a data template, selection and focus states, and optional headers or empty-state content outside the list.

### WINUI-LISTVIEW-ANATOMY-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** data items and containers being treated as the same object

Bind business data through `ItemsSource` and use `ItemTemplate` for presentation. Do not depend on visual child traversal to read or update data state.

**Sources:** `MS-WIN-CONTROLS-LISTVIEW`

### WINUI-LISTVIEW-XBIND-001

**Level:** MUST
**Evidence:** derived
**Prevents:** compiled `x:Bind` item templates failing generated XAML code because the chosen item model is not compatible with the target binding/compiler projection

When a `DataTemplate` uses typed `{x:Bind}`, compile the exact item model with the target WinUI/.NET environment. In the verified LazyDesign v0.1 environment, use ordinary public get/set properties for values exposed by the typed item template unless another model shape has been independently compiled. Do not assume that a positional record with init-only properties is safe merely because the binding reads those values.

**Derived reasoning:** `{x:Bind}` is converted to generated code at XAML compile time and typed data templates declare the item type with `x:DataType`. The pinned WinUI environment is therefore sensitive to the projected shape of that model. The get/set-class recommendation is a verified compatibility pattern for this environment, not a universal ban on records or immutable models.

**Sources:** `MS-WIN-XBIND`

## 3. Content rules

### WINUI-LISTVIEW-CONTENT-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** items being ignored because both population mechanisms are used

Populate the list using either direct `Items` or `ItemsSource`, not both.

**Sources:** `MS-WIN-CONTROLS-LISTVIEW`

### WINUI-LISTVIEW-CONTENT-002

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** dense items with no visual hierarchy

Give each item a clear primary label and only the secondary information required for scanning or deciding. Keep repeated item structure consistent.

**Derived reasoning:** ListView guidance defines repeated item content while Windows content guidance establishes primary and secondary hierarchy; limiting each row to decision-relevant information is an inference from those structures.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `MS-WIN-CONTROLS-LISTVIEW`

### WINUI-LISTVIEW-CONTENT-003

**Level:** MUST  
**Evidence:** derived  
**Prevents:** nested buttons conflicting with item invocation or selection

When an item contains interactive children, define whether the row itself remains invokable and verify pointer and keyboard behavior for both the row and nested controls.

**Derived reasoning:** ListView and keyboard guidance define row selection, invocation, and focus behavior; requiring an explicit interaction decision for nested controls is a conservative inference to avoid conflicting input semantics.

**Sources:** `MS-WIN-CONTROLS-LISTVIEW`, `MS-WIN-KEYBOARD-INTERACTIONS`

## 4. Sizing and layout

### WINUI-LISTVIEW-SIZE-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** variable content clipping or uncontrolled row growth

Define wrapping, trimming, and maximum content for primary and secondary text. Test long Korean and English strings at constrained widths and text scaling.

**Derived reasoning:** ListView supports templated text content and accessible-text guidance requires localized scaled text to remain readable; defining wrapping or trimming and testing long strings is the combined operational inference.

**Sources:** `MS-WIN-CONTROLS-LISTVIEW`, `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-LISTVIEW-LAYOUT-001

**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** large collections losing virtualization through unnecessary outer scrolling

Let the list own its scrolling viewport for large collections. Avoid placing it in an unconstrained parent scroller unless the resulting measurement and virtualization behavior are verified.

**Sources:** `MS-WIN-CONTROLS-LISTVIEW`

## 5. States and interaction

### WINUI-LISTVIEW-STATE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** selected, focused, and invoked states being conflated

Treat selection and invocation as separate concepts. Configure and handle each explicitly.

**Sources:** `MS-WIN-CONTROLS-LISTVIEW`

### WINUI-LISTVIEW-STATE-002

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** custom item visuals removing native state feedback

Preserve native pointer-over, pressed, selected, focused, and disabled states when customizing item content.

**Sources:** `MS-WIN-CONTROLS-LISTVIEW`, `MS-WIN-XAML-THEME-RESOURCES`

### WINUI-LISTVIEW-KEYBOARD-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** pointer-only navigation and selection

Verify keyboard entry, directional navigation, selection, invocation, and focus movement into and out of nested interactive controls.

**Sources:** `MS-WIN-KEYBOARD-INTERACTIONS`

## 6. Theme, accessibility, and localization

### WINUI-LISTVIEW-A11Y-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** list items announced without meaningful identity or selection state

Ensure each item exposes a meaningful accessible name and relevant state. Do not use color alone to communicate selection, status, or errors.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-CONTROLS-LISTVIEW`

### WINUI-LISTVIEW-THEME-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** selected or focused items disappearing across themes

Use theme resources for item foregrounds, backgrounds, separators, and state visuals. Verify Light, Dark, and contrast themes after customization.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-CONTRAST-THEMES`

## 7. Common failures

- Mixing `Items` and `ItemsSource`.
- Leaving `SelectionMode` at a default that does not match product behavior.
- Treating selection as activation.
- Dense item templates without a primary information hierarchy.
- Nested buttons that steal or duplicate row invocation.
- Fixed row heights that clip localized or scaled text.
- Removing native selected and focus states with a custom template.
- Wrapping a large list in another unconstrained scroll viewer.
- Assuming an unverified init-only or positional-record model is compatible with typed `x:Bind` code generation.

## 8. Minimal native XAML

```xml
<ListView ItemsSource="{x:Bind Devices}"
          SelectionMode="Single">
    <ListView.ItemTemplate>
        <DataTemplate x:DataType="local:DeviceViewModel">
            <StackPanel Padding="12,8">
                <TextBlock Text="{x:Bind Name}" />
                <TextBlock Text="{x:Bind Status}" />
            </StackPanel>
        </DataTemplate>
    </ListView.ItemTemplate>
</ListView>
```

Use a model shape that has been compiled with the target typed template. This get/set class pattern is verified in the pinned v0.1 environment:

```csharp
using System.Collections.ObjectModel;

public ObservableCollection<DeviceViewModel> Devices { get; } =
    new()
    {
        new DeviceViewModel { Name = "Conference room display", Status = "Connected" },
        new DeviceViewModel { Name = "회의실 디스플레이", Status = "연결됨" },
    };

public sealed class DeviceViewModel
{
    public string Name { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
}
```

## 9. Verification checklist

- [ ] Display, selection, and invocation behavior are explicitly defined.
- [ ] Only one population mechanism is used.
- [ ] Item templates present a consistent information hierarchy.
- [ ] The exact typed `x:Bind` item model compiled in the target WinUI/.NET environment.
- [ ] Long Korean and English text and text scaling were checked.
- [ ] Large-list scrolling and virtualization behavior were considered.
- [ ] Pointer, selected, focused, pressed, and disabled states remain visible.
- [ ] Keyboard navigation, selection, invocation, and nested controls work.
- [ ] Accessible item names and relevant states are exposed.
- [ ] Light, Dark, and contrast themes were checked after customization.

## 10. Sources

- `MS-WIN-CONTROLS-LISTVIEW`
- `MS-WIN-XBIND`
- `MS-WIN-DESIGN-CONTENT`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-KEYBOARD-INTERACTIONS`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-CONTRAST-THEMES`
- `WINUI-GALLERY-V2-9-3`

Windows Design Kit evidence remains inactive because component-level inspection has not been completed.