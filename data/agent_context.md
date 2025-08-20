# Ninjamock Editor – Agent Context Guide

Generated: 2025-08-10

This document summarizes the editor’s element model, common properties, behaviors, events, and design system hooks to help an AI agent reason about changes and generate valid tool calls. Use this as RAG context.

## Overview

- Elements are represented as JSON objects that follow the project contract; each element typically includes `id`, `type`, `properties` and (optionally) `children` or `parentId`.
- Treat elements as data records (JSON shapes). This document describes the canonical JSON contract agents should emit or modify; it does not require knowledge of internal code structure.
- Properties are defined and managed via a `Properties` system, supporting constraints, validators, options, subscriptions (reactive reactions), and internal/hidden flags.
- The runtime keeps internal reactive state for selection, hover, dragging, etc. Agents do not need to reference framework-specific APIs.

## Element types

This document references the set of runtime element types agents can create or modify. The full list below is a concise catalogue of the types the agent may use in payloads; prefer the `type` string in examples.

- button, image, text, rectangle, ellipse, line, lineConnector, path, group, container, container-layout, device, workspace, selection, shape, radio, checkbox, input-text, slider, progress-bar, navbar, sidebar-web, table, carousel-web, video, icon-svg
# Ninjamock Editor – Agent Design Context (for RAG)

Scope: This document contains only the information needed for an agent that creates, modifies, deletes, and suggests UI elements. It excludes framework internals and general project architecture.

Use this document as retrieval context for tool-call generation and validation.

## Core concepts

- Element types: the runtime supports a set of element types (see "Element types" below). Each type has a serialized `type`, `properties`, and optional `children`.
- Serialized element: JSON form stored/applied in the project, with `type`, `properties`, and `children`.
- Template elements (templateId): Predefined components that instantiate one element or a composition of multiple elements with preset properties/states. They’re referenced via `templateId`.
- Container element: A general-purpose element used to group/compose other elements.
- Bindings: Dynamic property links between elements/properties (data-driven or interactive), defined as bindings rather than static values.
- Layout: Supports both absolute positioning and responsive (flex-like) layouts. Agents should prefer responsive containers for designs targeting multiple screen sizes, and may still use absolute positioning for pixel-precise placements.

### Container strategy (single adaptable container)

- The editor supports a `container-layout` (or `container`) element that can switch its layout behavior via a `layout` or `display` property. Valid values include `absolute`, `flex`, and `grid` (if supported). This lets the agent create a single container type and toggle its layout mode later to convert the subtree to a responsive layout without replacing the container node.

-- Recommendation: prefer using the same `container-layout` type when grouping content so the agent or user can switch between `absolute` and `flex` later. This reduces friction when adapting a design for responsive breakpoints.
-- States & tokens: Style states and design tokens to enable themeable, stateful designs aligned with HTML/CSS exports.

## Centralized properties reference

This section centralizes the canonical property reference used across element types. Use these canonical entries as the single source of truth for property names, types, allowed values and serialization notes. Per-type subsections later list which of these properties are commonly used by each type and any defaults or aliases.

### Identity & meta
- name: string — default: "" — human readable label for the element; serialized in `properties.name`.
- bindingKey: string | null — unique binding identifier for data bindings (nullable).
- templateId / meta.templateRef: string | object — references the toolbox template or template metadata; when present prefer `overrides`/`propsMode: "diff"` semantics.
- referenceElementId: string | null — references another element for relative layout or binding.

### Placement & sizing
- position: 'absolute' | 'relative' | 'static' — default: 'absolute'.
- left, top, right, bottom: number | null — decimal(2). When omitted, the runtime may compute layout from parent/flow.
- width, height: number | null — decimal(2).
- widthBehavior, heightBehavior: 'fixed' | 'hug' — default: 'fixed' unless a type overrides to 'hug' (content-driven).
- lockAspectRatio: boolean — if true, maintain aspect ratio when resizing.
- scale: number — default: 1.
- rotation: number (degrees) — default: 0; allowed range typically [-360..360].
- zIndex: number — stacking order.

### Visibility & effects
- visible: boolean — default: true.
- opacity: number (0..100) — default: 100.
- clip: boolean — internal: whether children are clipped to this element.

### Style
- fill, stroke: color token or color object — may accept token references.
- strokeStyle: select — border style options (type-defined choices).
- borderRadius: number | object — per-corner radius or shorthand.
- strokeWidth: number — border thickness.
- strokePosition: select — inside | center | outside (type-defined).
- padding: Box — object with top/right/bottom/left.
- boxShadow, innerShadow, dropShadow: object — shadow descriptors.
- layerBlur, bgBlur: number — blur amounts.

### Constraints and layout hints
- minWidth, minHeight, maxWidth, maxHeight: number — layout constraints.
- widthBehaviorHint / heightBehaviorHint: hint fields (optional) used by some types.

### Layout-specific helpers
- layout / display: 'absolute' | 'flex' | 'grid' — high-level layout mode for containers; the runtime may map aliases.
- direction / flexDirection: 'horizontal'|'vertical'|'row'|'column' — aliases exist; runtime maps to concrete flex axis.
- justifyContent, alignItems: select — start|center|end|space-between|space-around (type-defined set).
- gap, gapX, gapY: number — spacing between children (gap shorthand with optional axis overrides).
- spacingType: 'fixed' | 'auto' — how children size against gap rules.
- layoutAlign: preset string — convenience presets (see `layoutAlign` list below) that set both `justifyContent` and `alignItems`.

### Bindings & dynamic values
- bindings: array/object — structured bindings between element properties; serialized as a `bindings` section when present.
- tokens: Record<string, any> — token pointer map used to resolve theme values via `getValueFromToken`.

### Hierarchy & state (serialization notes)
- parentId: string — persisted in flat exports to attach during deserialization.
- children: string[] — array of child ids in flat exports. Payloads may omit full child objects when they are present elsewhere in the same `elements` payload.

### layoutAlign presets (quick-reference)
- `top-left`, `top-center`, `top-right`
- `middle-left`, `middle-center`, `middle-right`
- `bottom-left`, `bottom-center`, `bottom-right`

## Toolbox templates (catalog)

| Template ID | Runtime type | Category | Title |
|---|---|---:|---|
| text | text | basic | Text |
| tabbar-ios | container-layout | ios | Tabbar |
| menu-ios | container-layout | ios | Menu |
| status-bar-ios | container-layout | ios | Status Bar |
| pagination-web | container-layout | web | Pagination |
| notification-web | container-layout | web | Notification |
| toggle-web | toggle-web | web | Toggle |
| image | image | basic | Image |
| video | video | basic | Video |
| stepper-ios | container-layout | ios | Stepper |
| slider-ios | container-layout | ios | Slider |
| segmented-control-ios | container-layout | ios | Segmented Control |
| text-field-android | container-layout | android | Text Field |
| sidebar-ios | container-layout | ios | Sidebar |
| progress-indicator-ios | container-layout | ios | Progress Indicator |
| date-time-picker-ios | container-layout | ios | Date Time Picker |
| alert-ios | container-layout | ios | Alert |
| list-group-web | container-layout | web | List Group |
| progress-bar-ios | container-layout | ios | Progress Bar Wrapper |
| page-control-ios | container-layout | ios | Page Control |
| navbar-ios | container-layout | ios | Navigation Bar |
| search-bar-android | container-layout | android | Search Bar |
| input-ios | input-ios | ios | Input iOS |
| action-sheet-ios | container-layout | ios | Action Sheet |
| ios-button | button-ios | ios | iOS Button |
| tab-bar-android | container-layout | android | Tab Bar |
| menu-android | container-layout | android | Menu |
| slider-android | slider-android | android | Slider |
| bottom-sheet-android | container-layout | android | Bottom Sheet |
| toggle-android | toggle-android | android | Toggle |
| side-sheet-android | container-layout | android | Side Sheet |
| segmented-buttons-android | container-layout | android | Segmented Buttons |
| progress-web | progress-bar | web | Progress Bar |
| radio-android | radio-android | android | Radio |
| list-android | container-layout | android | List |
| icon-button-android | icon-button-android | android | Icon Button |
| fab-android | fab-android | android | Fab |
| chip-android | chip-android | android | Chip |
| fab-extended-android | extended-fab-android | android | Fab Extended |
| dialog-android | container-layout | android | Container Layout |
| checkbox-android | container-layout | android | Checkbox |
| sidebar-web | sidebar-web | web | Sidebar |
| android-button | buttonAndroid | android | Android Button |
| web-button | buttonWeb | web | Web Button |
| tab-group-web | container-layout | web | Tabs |
| radio-web | radio-web | web | Radio |
| toggle-ios | toggle | ios | Toggle |
| notification-ios | container-layout | ios | Container Layout |
| input-web | container-layout | web | Input |
| button-basic | button | basic | Button |
| select-web | select-web | web | Select |
| icon

## Element types (catalogue)

The runtime recognizes a set of element `type` strings used in serialized payloads. Agents should use these `type` values when creating or modifying elements. Integrations may expose additional types or aliases; consult integration docs if unsure.

Common runtime types (examples):

- button
- image
- text
- rectangle
- ellipse
- line
- lineConnector
- path
- video
- checkbox
- radio
- dropdown
- select
- slider
- progress-bar
- sidebar-web
- navbar
- group
- container
- container-layout
- stack-layout
- table
- table-row
- table-cell
- table-section
- device
- workspace
- selection
- shape
- radio-icon
- checkbox-label
- input-text
- toggle
- carousel-web
- icon-svg

Note: Exact `type` strings or aliases may vary between backend integrations. When necessary, prefer the canonical type strings provided by your integration documentation.

## Templates vs direct elements

- Direct element: Use the element `type` directly in JSON.
- Template-based element: Use the concrete runtime `type` (e.g., "button", "image") plus `meta.templateRef` carrying the template id/version. Only send differences in an `overrides` object.

Template instantiation rules (children-as-root vs composite)

- Key flags/shape on a template definition:
  - persistentFields.isComposite: boolean indicating a multi-element composition with internal wiring/bindings.
  - useChildAsRoot (aka isChildrenAsRoot): when true, the template’s child node(s) should be inlined directly (no wrapper element type is used).
  - children: may be a single object (single child) or an array (multiple children). Treat a single object as one-child.

- Decision tree the agent must follow when creating from a templateId:
  1) If isComposite is true OR the template represents a composition (multiple children/bindings), serialize the root element using its concrete runtime `type` and include `meta.templateRef`.
  2) If the template is a single concrete element (e.g., image, text) or useChildAsRoot is true, inline the child with its runtime `type` and still include `meta.templateRef`.
  3) If useChildAsRoot is true and there are multiple children, insert all top-level children. If a single parent is required, wrap them in a container/group.

Examples

- Direct element
```json
{
  "type": "image",
  "properties": {
    "name": "Logo",
    "src": { "type": "url", "value": "https://..." }
  }
}
```

// Template-based element (diff style)
```json
{
  "type": "button",
  "meta": { "origin": "template", "templateRef": { "id": "button-basic", "version": 1, "kind": "primitive" } },
  "overrides": {
    "name": "PrimaryCTA",
    "left": 186,
    "top": 548,
    "width": 73,
    "height": 45,
    "zIndex": 3
  }
}
```

- Inlined from a single-element template (children-as-root)
```json
{
  "type": "image",
  "properties": {
    "name": "Image",
    "templateId": "image",
    "left": 122,
    "top": 112,
    "width": 128,
    "height": 128,
    "zIndex": 1,
    "src": {
      "type": "url",
      "value": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80"
    }
  },
  "children": []
}
```

### TemplateId → renderer type mapping and instantiation mode

Use this list to pick the runtime element `type`. If originating from a template, always add `meta.templateRef`.

- image → type: "image" (inline)
- video → type: "video" (inline)
- icon-svg → type: "icon-svg" (inline)
- text → type: "text" (inline)
- button-basic → type: "button" + meta.templateRef.id="button-basic"
- toggle-ios → wrapper (no direct type)
- tabbar-ios → wrapper
- stepper-ios → wrapper
- status-bar-ios → wrapper
- slider-ios → wrapper
- sidebar-ios → wrapper
- segmented-control-ios → wrapper
- progress-indicator-ios → wrapper
- progress-bar-ios → wrapper (map to "progress-bar" only if your adapter resolves to that type)
- date-time-picker-ios → wrapper
- page-control-ios → wrapper
- notification-ios → wrapper
- navbar-ios → type: "navbar" (inline)
- menu-ios → wrapper
- input-ios → type: "input-ios" (inline)
- alert-ios → wrapper
- action-sheet-ios → wrapper
- ios-button → type: "button-ios" (inline)
- text-field-android → wrapper
- tab-bar-android → wrapper
- toggle-android → type: "toggle-android" (inline)
- slider-android → type: "slider-android" (inline)
- side-sheet-android → wrapper
- bottom-sheet-android → wrapper
- search-bar-android → wrapper
- radio-android → type: "radio-android" (inline)
- menu-android → wrapper
- list-android → wrapper
- segmented-buttons-android → wrapper
- icon-button-android → type: "icon-button-android" (inline)
- fab-extended-android → type: "extended-fab-android" (inline)
- fab-android → type: "fab-android" (inline)
- dialog-android → wrapper
- chip-android → type: "chip-android" (inline)
- checkbox-android → type: "checkbox" (inline)
- android-button → type: "buttonAndroid" (inline)
- web-button → type: "buttonWeb" (inline)
- sidebar-web → type: "sidebar-web" (inline)
- card-web → wrapper
- list-group-web → wrapper
- tab-group-web → wrapper
- pagination-web → wrapper
- notification-web → wrapper
- progress-web → type: "progress-bar" (inline)
- input-web → wrapper
- toggle-web → type: "toggle-web" (inline)
- checkbox-web → type: "checkbox-web" (inline)
- radio-web → type: "radio-web" (inline)
- select-web → type: "select-web" (inline)

Aliases used by the renderer
- extended-fab-android is the renderer type for templateId "fab-extended-android"
- buttonAndroid is the renderer type for templateId "android-button"
- buttonWeb is the renderer type for templateId "web-button"

## Serialized element schema (baseline)

```json
{
  "id": "uuid",
  "type": "<element-type>",
  "properties": { "<key>": <value>, ... },
  "children": [ { /* same schema */ } ]
}
```

Keys in `properties` map to the `CommonProperties` enum and any element-specific properties (adapters can add their own).

### Common properties (always available)

Identity & meta
- name: string
- bindingKey: string | null
- templateId: string | null
- referenceElementId: string | null

Placement & sizing
- position: string (default: "absolute")
- left, top, right, bottom: number | null (Decimal(2))
- width, height: number | null (Decimal(2))
- widthBehavior, heightBehavior: 'fixed' | 'hug'
- lockAspectRatio: boolean
- scale: number
- rotation: number (°)
- zIndex: number

Visibility & effects
- visible: boolean
- opacity: number (0..100)
- clip: boolean (internal)

Style
- fill, stroke: color
- strokeStyle: select (border style options)
- borderRadius: number | object
- strokeWidth: number
- strokePosition: select
- margin: number (hidden)
- padding: Box
- boxShadow, innerShadow, dropShadow: objects
- layerBlur, bgBlur: number

Constraints (hidden defaults)
- minWidth, minHeight, maxWidth, maxHeight

Hierarchy & state
- parent: object (internal)
- state: select
- states: array (internal, used by PropertyStates)

## Centralized properties reference

This section centralizes the canonical property reference used across element adapters. Use these canonical entries as the single source of truth for property names, types, allowed values and serialization notes. Per-type subsections below list which of these properties are commonly used by the adapter and any adapter-specific defaults or aliases.

### Identity & meta
- name: string — default: "" — human readable label for the element; serialized in `properties.name`.
- bindingKey: string | null — unique binding identifier for data bindings (nullable).
- templateId / meta.templateRef: string | object — references the toolbox template or template metadata; when present prefer `overrides`/`propsMode: "diff"` semantics.
- referenceElementId: string | null — references another element for relative layout or binding.

### Placement & sizing
- position: 'absolute' | 'relative' | 'static' — default: 'absolute'.
- left, top, right, bottom: number | null — decimal(2). When omitted, the runtime may compute layout from parent/flow.
- width, height: number | null — decimal(2).
- widthBehavior, heightBehavior: 'fixed' | 'hug' — default: 'fixed' unless adapter overrides to 'hug' (content-driven).
- lockAspectRatio: boolean — if true, maintain aspect ratio when resizing.
- scale: number — default: 1.
- rotation: number (degrees) — default: 0; allowed range typically [-360..360].
- zIndex: number — stacking order.

### Visibility & effects
- visible: boolean — default: true.
- opacity: number (0..100) — default: 100.
- clip: boolean — internal: whether children are clipped to this element.

### Style
- fill, stroke: color token or color object — may accept token references.
- strokeStyle: select — border style options (adapter-defined choices).
- borderRadius: number | object — per-corner radius or shorthand.
- strokeWidth: number — border thickness.
- strokePosition: select — inside | center | outside (adapter-defined).
- padding: Box — object with top/right/bottom/left.
- boxShadow, innerShadow, dropShadow: object — shadow descriptors.
- layerBlur, bgBlur: number — blur amounts.

### Constraints and layout hints
- minWidth, minHeight, maxWidth, maxHeight: number — layout constraints.
- widthBehaviorHint / heightBehaviorHint: adapter hint fields (optional) used by some adapters.

### Layout-specific helpers
- layout / display: 'absolute' | 'flex' | 'grid' — high-level layout mode for containers; adapter may map aliases.
- direction / flexDirection: 'horizontal'|'vertical'|'row'|'column' — aliases exist; runtime maps to concrete flex axis.
- justifyContent, alignItems: select — start|center|end|space-between|space-around (adapter-defined set).
- gap, gapX, gapY: number — spacing between children (gap shorthand with optional axis overrides).
- spacingType: 'fixed' | 'auto' — how children size against gap rules.
- layoutAlign: preset string — convenience presets (see `layoutAlign` list below) that set both `justifyContent` and `alignItems`.

### Bindings & dynamic values
- bindings: array/object — structured bindings between element properties; serialized as adapter-specific `bindings` section when present.
- tokens: Record<string, any> — token pointer map used to resolve theme values via `getValueFromToken`.

### Hierarchy & state (serialization notes)
- parentId: string — persisted in flat exports to attach during deserialization.
- children: string[] — array of child ids in flat exports. Adapters may omit full child objects when they are present in the same `elements` payload.

### layoutAlign presets (quick-reference)
- `top-left`, `top-center`, `top-right`
- `middle-left`, `middle-center`, `middle-right`
- `bottom-left`, `bottom-center`, `bottom-right`

## Property value examples (contracts)
Below are canonical JSON shapes for commonly used complex properties. Include these shapes when producing payloads so the importer and adapters can validate and apply them correctly.

- fill (solid example)

```json
{
  "type": "solid",
  "alpha": 1,
  "color": "#ffffff"
}
```

- fill (gradient example)

```json
{
  "type": "linear-gradient",
  "angle": 90,
  "stops": [
    { "color": "#ff7a18", "offset": 0 },
    { "color": "#af002d", "offset": 1 }
  ]
}
```

- padding (box)

```json
{
  "top": 8,
  "right": 12,
  "bottom": 8,
  "left": 12
}
```

- boxShadow

```json
{
  "offsetX": 0,
  "offsetY": 2,
  "blur": 8,
  "spread": 0,
  "color": "rgba(0,0,0,0.12)",
  "inset": false
}
```

- safeArea

```json
{ "top": 44, "bottom": 34, "left": 0, "right": 0 }
```

- layoutDefaults (device subtree defaults)

```json
{ "display": "flex", "flexDirection": "column", "gap": 16 }
```

- image `src` property (url or data object)

```json
{ "type": "url", "value": "https://example.com/image.jpg" }
```

- tokens (theme pointer)

```json
{ "color": "theme.primary", "spacing": "theme.size.2" }
```

- bindings (simple example linking text to another element's property)

```json
{
  "source": { "elementId": "title-1", "property": "text" },
  "target": { "property": "text" },
  "transform": null
}
```

- Generic `children`/`parentId` usage in flat payloads

```json
{ "id": "child-1", "type": "text", "properties": { "text": "Hello" }, "parentId": "container-1", "children": [] }
```

Include these examples for agents when producing payloads; adapt values to the specific adapter if the adapter documents different or additional fields.

## Type-specific property notes (summary)
This subsection lists commonly used properties and adapter-specific defaults for a few high-priority runtime types. Use these as examples; adapters may expose additional, adapter-only properties.

### container-layout
- Canonical props used: `layout`, `direction`, `flexDirection`, `justifyContent`, `alignItems`, `gap`, `gapX`, `gapY`, `spacingType`, `widthBehavior`, `heightBehavior`, `layoutAlign`, `flexWrap`.
- Defaults (adapter): `layout: "flex"`, `flexWrap: "nowrap"`, `widthBehavior: "hug"`, `heightBehavior: "hug"`.
- Notes: `direction` is a high-level alias for `flexDirection`. `layoutAlign` is a convenience preset that maps to `justifyContent`/`alignItems`.

### device
- Canonical props used: `name`, `width`, `height`, `orientation`, `safeArea`, `layoutDefaults`.
- `layoutDefaults` example: `{ "display": "flex", "flexDirection": "column" }` — used to apply defaults to children created within the device.
- Notes: Treat `device` as a normal element in flat payloads; `device` may be a workspace root element.

### workspace
- Canonical props used: `name`, `rootElements` (array of ids), metadata fields (owner, createdAt etc. depending on backend).
- Notes: Workspaces are stored in the `workspaces` array in flat exports and their `rootElements` reference element ids.

### image
- Canonical props used: `src`, `width`, `height`, `fit` (contain|cover|fill), `alt`.

### text
- Canonical props used: `text`, `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `color`, `textAlign`.

### button
- Canonical props used: inherits `text` properties plus `onClick` binding, `states` for hover/active, and `padding`.

### group / container
- Canonical props used: inherits general layout props; often used with `position: absolute` and explicit left/top/width/height in absolute mode.

---


Add per-template or per-type detailed examples below or inline near the template catalog when needed; the runtime maps these canonical names to adapter internals at import time.

## Detailed property contracts by type
Below are concrete JSON shapes for properties that are adapter-specific or commonly differ per type. Use these as reference contracts when creating payloads for the backend.

### container-layout (expanded)
- `flexWrap` (wrap behavior)

```json
"flexWrap": "nowrap" // "nowrap" | "wrap" | "wrap-reverse"
```

- `justifyContent` / `alignItems` (explicit)

```json
"justifyContent": "start" // start|center|end|space-between|space-around
"alignItems": "center"    // start|center|end|stretch
```

### device (expanded)
- `orientation` (string)

```json
"orientation": "portrait" // "portrait" | "landscape"
```

- `safeArea` (object — all numbers)

```json
"safeArea": { "top": 44, "bottom": 34, "left": 0, "right": 0 }
```

- `layoutDefaults` (object applied to newly created children)

```json
"layoutDefaults": { "display": "flex", "flexDirection": "column", "gap": 16 }
```

### workspace
- `rootElements` (array of ids)

```json
{"id": "workspace-1", "name": "Mobile Screens", "rootElements": ["device-1"]}
```

### image
- `src` (url/data)

```json
"src": { "type": "url", "value": "https://example.com/img.png" }
// or
"src": { "type": "data", "mime": "image/png", "value": "iVBORw0KG..." }
```

### text
- `text` and rich-text hint

```json
"text": "Hello world"
// optional rich text
"textRich": { "ops": [ { "insert": "Hello" }, { "attributes": { "bold": true }, "insert": " world" } ] }
```

### button
- `states` (map of stateName → property overrides)

```json
"states": {
  "hover": { "properties": { "fill": { "type": "solid", "color": "#f1f5f9" } } },
  "active": { "properties": { "scale": 0.98 } }
}
```

- `onClick` (binding or action reference)

```json
"onClick": { "type": "navigate", "target": "screen-2" }
// or binding to an action id
"onClick": { "actionId": "action-123" }
```

### rectangle / ellipse / shape (vector)
- `borderRadius` (number or per-corner)

```json
// uniform
"borderRadius": 8
// per-corner
"borderRadius": { "topLeft": 8, "topRight": 8, "bottomRight": 4, "bottomLeft": 4 }
```

- `stroke` and `strokePosition`

```json
"stroke": { "type": "solid", "color": "#111827", "alpha": 1 }
"strokeWidth": 2
"strokePosition": "center" // inside | center | outside
```

### polygon / shape-polygon
- `points` (array of {x,y})

```json
"points": [ { "x": 0, "y": 0 }, { "x": 100, "y": 0 }, { "x": 50, "y": 86 } ]
```

### path
- `pathData` (array of path commands or SVG path string)

```json
// array form
"pathData": [ { "cmd": "M", "args": [0,0] }, { "cmd": "L", "args": [100,0] }, { "cmd": "C", "args": [120,0,120,50,100,50] } ]
// svg string form
"path": "M0 0 L100 0 C120 0 120 50 100 50"
```

### line
- `x1,y1,x2,y2` or endpoints

```json
"x1": 0, "y1": 0, "x2": 120, "y2": 0
```

### lineConnector
- `from` / `to` references and anchor hints

```json
"from": { "elementId": "btn-1", "anchor": "bottom" },
"to":   { "elementId": "input-1", "anchor": "top" },
"routing": "manhattan" // or "direct"
```

### group / container (absolute mode specifics)
- absolute-positioned children often set `left`, `top`, `width`, `height` explicitly; include `position: "absolute"`.

```json
{ "type": "group", "properties": { "position": "absolute" }, "children": ["e1","e2"] }
```

### bindings (expanded)
- full shape when multiple transforms/params are present

```json
{
  "id": "binding-1",
  "source": { "elementId": "input-1", "property": "value" },
  "target": { "elementId": "label-1", "property": "text" },
  "transform": { "type": "template", "template": "Value: {{value}}" }
}
```

---

### Behaviors and rules

- Hug vs fixed: 'hug' disables width/height (size follows content). 'fixed' enables explicit size.
- Aspect ratio: when `lockAspectRatio` is true, setting one dimension adjusts the other (unless the other behavior is 'fill').
- Invalidation: property changes trigger `invalidate(...)` and propagate up/down the hierarchy for recalculation.

## Bindings (dynamic properties)

- Bindings link a source element/property to a target element/property.
- Use bindings for user-created components or dynamic UI behavior instead of fixed values.
- Bindings are applied via adapter-level APIs (PropertyBinding). When serializing, include a `bindings` section if applicable.

## Layout model

- Current default: absolute positioning using `position`, `left`, `top`, etc.
- Goal: responsive design using a flex-like model (analogous to CSS flexbox) for groups/containers.
- Agents should:
  - For absolute layouts, set explicit coordinates/sizes or use 'hug' for content-driven sizes.
  - For future flex layouts, prefer container elements and properties that align children (e.g., justify/align/gap) when available in templates/adapters.

## States & design tokens

- `states` define alternate property sets per element state (e.g., hover, active), applied via `PropertyStates`.
- Tokens (`tokens: Record<string, any>`) allow themeable values; `getValueFromToken('group.key')` resolves along the parent chain.
- For HTML/CSS export, prefer tokenized colors, spacing, and typography when available.

## Tool-call recipes (expected JSON commands)

Create or add elements
```json
{
  "tool": "add_to_workspace",
  "args": {
    "elements": [
      {
        "type": "button",
        "meta": { "origin": "template", "templateRef": { "id": "button-basic", "version": 1, "kind": "primitive" } },
        "overrides": { "name": "PrimaryCTA" }
      }
    ]
  }
}
```

Add child to a parent
```json
{
  "tool": "add_to_parent",
  "args": {
    "parentId": "uuid",
    "child": {
      "type": "image",
      "properties": {
        "name": "Logo",
        "src": { "type": "url", "value": "https://..." }
      }
    }
  }
}
```

Modify existing elements
```json
{
  "tool": "modify_element",
  "args": {
    "elements": [
      {
        "id": "uuid",
        "properties": {
          "widthBehavior": "fixed",
          "width": 320,
          "height": 80,
          "fill": { "type": "solid", "alpha": 1, "color": "#1d4ed8" }
        }
      }
    ]
  }
}
```

Deletion
- Provide the element `id` and indicate deletion via a high-level tool or a specific delete command if available in the backend API.

## Best practices for the agent

- Prefer templates (with meta.templateRef) for standard UI patterns; they may instantiate multi-element compositions with correct defaults and states.
- When using direct element types, set only compatible properties (respect disabled/hidden ones under current behaviors).
- Use 'hug' when layout should be content-driven; otherwise use 'fixed' with explicit dimensions.
- Respect constraints (decimals for size/position, opacity 0..100, rotation within [-360..360]).
- For grouping/composition, use `container` or appropriate layout elements (e.g., stack layouts) as parents.
- Bindings should be used where dynamic or synchronized behavior between elements is needed.

---

This document intentionally omits framework internals and general project architecture to keep RAG focused on design elements and their JSON schemas.

## Runtime mapping: templates → runtime types

- When the agent references a toolbox template, prefer setting `meta.templateRef` on the element JSON. The runtime will use `meta.templateRef.id` to find the template and apply the template's defaults and children. Example:

- template usage (primitive):

```json
{
  "type": "button",
  "meta": { "origin": "template", "templateRef": { "id": "button-basic", "version": 1, "kind": "primitive" } },
  "overrides": { "name": "PrimaryCTA" }
}
```

- template usage (composite): the root element should carry the `meta.templateRef` and the runtime will create the contained subtree. Avoid manually including full child objects unless you intend to override or extend the template.

### Common templateId → runtime type guidance

- button-* → runtime type: `button` (primitive)
- input-* → runtime type: `text-input` (primitive)
- list-* → runtime type: `list` (composite: generates children)
- card-* → runtime type: `card` (composite)
- frame/device templates → runtime type: `device-frame` or `device-root` (runtime-only frame wrappers)

If a template is not available, the agent may provide direct `type` and `properties`; the runtime will treat it as a plain element.
## Other runtime types
- container
- container-layout
- device
- workspace
- path
- line
- ellipse
- group
- lineConnector
- shape-rectangle
- shape-polygon
- shape-star

All of the types listed above (and the additional types provided by toolbox templates) can be created by users or agents via the flat project contract. When creating `workspace` or `device` nodes, follow the backend contract (for example, required properties such as workspace metadata or device screen dimensions). The deserializer will validate references and emit warnings for missing or orphaned children.

## Special nodes and device elements

- `workspace` — top-level container recorded in the `workspaces` array; agents should reference `workspace.id` when they want to add a root-level element to a workspace via `parentId`.

- `device` — a first-class element that agents or users can create. A `device` element carries properties (screen size, safe-area, orientation, display/layout defaults) and its `type` and `properties` determine how its subtree is rendered. Treat `device` as a normal element in the flat payloads: it may be created, moved, or deleted by agents.

- `device-frame`, `device-root` — optional wrapper nodes used by the app for device preview or export flows. Agents do not need to create these wrappers unless specifically instructed by the backend contract.

- `group`, `container`, `stack` — layout containers; agents may create container elements (for example `container-layout` or `container`) to group children and to apply layout properties.

Agents are allowed to create `device` and `container-layout` elements. When creating containers, prefer the `container-layout` type which can switch its internal layout mode via a `layout` or `display` property (see "Container strategy" above).

### Examples: creating a `device` element

- Minimal device element (single element):

```json
{
  "id": "device-1",
  "type": "device",
  "properties": {
    "name": "iPhone 16 Preview",
    "width": 393,
    "height": 852,
    "orientation": "portrait",
    "safeArea": { "top": 44, "bottom": 34, "left": 0, "right": 0 },
    "layoutDefaults": { "display": "flex", "flexDirection": "column" }
  },
  "children": []
}
```

- Device with a container child (device as workspace content root):

```json
{
  "id": "device-2",
  "type": "device",
  "properties": {
    "name": "Android Medium",
    "width": 700,
    "height": 840,
    "orientation": "portrait",
    "layoutDefaults": { "display": "absolute" }
  },
  "children": ["container-1"]
}
```

### Example: creating a `workspace` plus a `device` in a bulk payload

- The client typically sends a flat payload with a `parentId` (workspace id or other parent) and an `elements` array. To create a workspace and device together the backend contract may accept workspaces in the `workspaces` array and elements in `elements`.

Example (bulk create where the workspace already exists and we add a device as a root element):

```json
{
  "parentId": "workspace-123",
  "elements": [
    {
      "id": "device-3",
      "type": "device",
      "properties": {
        "name": "MacBook Air Preview",
        "width": 1280,
        "height": 832,
        "orientation": "landscape",
        "layoutDefaults": { "display": "flex", "flexDirection": "column" }
      },
      "parentId": "workspace-123",
      "children": []
    }
  ]
}
```

- If the payload must create a new workspace object itself, include the workspace in the project `workspaces` array and reference its `id` from element `parentId`.

```json
{
  "workspaces": [
    { "id": "workspace-456", "name": "Mobile Screen", "rootElements": ["device-4"] }
  ],
  "elements": {
    "device-4": {
      "id": "device-4",
      "type": "device",
      "properties": { "name": "iPhone SE", "width": 320, "height": 568 },
      "parentId": "workspace-456",
      "children": []
    }
  }
}
```

Notes:
- Required fields depend on backend contract; at minimum provide `id`, `type`, `properties` (width/height or templateRef) and `parentId` when attaching to a workspace or parent element.
- Use `layoutDefaults` or `properties.display` to set whether a device subtree uses `flex` or `absolute` by default.

### Example: `container-layout` with flex properties

- The `container-layout` adapter defaults to `layout: "flex"` and has properties for direction/spacing/alignment. Example showing a horizontal flex row with centered children and a gap:

```json
{
  "id": "container-1",
  "type": "container-layout",
  "properties": {
    "name": "Header Row",
    "layout": "flex",
    "direction": "horizontal",        // high-level direction option (horizontal|vertical|grid)
    "flexDirection": "row",          // explicit flex axis (row|column)
    "justifyContent": "center",      // start|center|end|space-between|space-around
    "alignItems": "center",          // start|center|end|stretch
    "gap": 16,                         // uniform gap
    "gapX": 16,                        // optional X gap
    "gapY": 8,                         // optional Y gap
    "spacingType": "fixed",          // fixed | auto
    "widthBehavior": "hug",
    "heightBehavior": "hug"
  },
  "children": ["logo-1", "nav-1", "actions-1"]
}
```

- Child examples (simple text and image elements):

```json
{
  "id": "logo-1",
  "type": "image",
  "properties": { "name": "Logo", "width": 120, "height": 32 },
  "parentId": "container-1"
}
{
  "id": "nav-1",
  "type": "text",
  "properties": { "name": "Navigation", "text": "Home · Products · About" },
  "parentId": "container-1"
}
{
  "id": "actions-1",
  "type": "container-layout",
  "properties": { "layout": "flex", "direction": "horizontal", "gap": 8 },
  "parentId": "container-1",
  "children": ["btn-1","btn-2"]
}
```

- Notes on property names:
  - Some adapters expose both `direction` (stack helper) and `flexDirection` (explicit CSS axis). Use whichever your integration expects; the runtime maps these to internal layout behavior.
  - `gap` is a shorthand; `gapX`/`gapY` allow asymmetric spacing.
  - `layoutAlign` is a quick-alignment helper that sets both `justifyContent` and `alignItems` together. Available values:

    - `top-left` (Top Left)
    - `top-center` (Top Center)
    - `top-right` (Top Right)
    - `middle-left` (Middle Left)
    - `middle-center` (Middle Center)
    - `middle-right` (Middle Right)
    - `bottom-left` (Bottom Left)
    - `bottom-center` (Bottom Center)
    - `bottom-right` (Bottom Right)

    Using `layoutAlign` avoids configuring `alignItems` and `justifyContent` separately when you want a common alignment preset. Example:

```json
{
  "properties": { "layout": "flex", "layoutAlign": "middle-center" }
}
```

## Flat bulk payloads (preferred for composite creates)

- The client and backend exchange a flat project contract. When creating multi-node compositions (templates or deep groups), agents should prepare a flat subtree array and send it to the backend as a bulk payload.

Example bulk create payload the client will send to the backend:

```json
{
  "parentId": "workspace-or-parent-uuid",
  "elements": [
    { "id": "root-uuid", "type": "card", "meta": { "origin": "template", "templateRef": { "id": "card-basic" } }, "properties": { "name": "Card A" }, "children": ["child-1","child-2"] },
    { "id": "child-1", "type": "image", "properties": { "src": "https://..." }, "parentId": "root-uuid", "children": [] },
    { "id": "child-2", "type": "text", "properties": { "text": "Hello" }, "parentId": "root-uuid" }
  ]
}
```

- Note: elements can be provided as an array or as a map keyed by `id`. The deserializer will first create adapters in dependency order and then attach parent-child relationships using `parentId` and `children` arrays.

## Agent rules & best practices (summary)

- Prefer templates for standard UI patterns. Use `meta.templateRef` to reference the toolbox template; let the runtime apply template children and defaults.
- For composite creates, produce a flat elements array and send it as `{ parentId, elements: [...] }` so the backend can apply the whole subtree atomically.
- When producing plain elements (not templates), include `parentId` for where the root belongs and `children` as id arrays (children objects are optional if they are also present in `elements`).
- Keep element properties minimal: only override what must change from the template/runtime defaults. Use `propsMode: "diff"` when applicable if you have the template context.
- Validate that every child id referenced exists in the `elements` array or in the server-side store. If a referenced id is missing, the importer will emit a warning and treat the child as orphaned.
- When creating `workspace` or `device` nodes, ensure required fields are present (workspace metadata, device size/orientation, etc.) and respect the backend API contract; otherwise the importer may emit validation warnings.

## Examples: agent workflows

- Create a template-based card inside a workspace:
  - Agent returns a single root element with `meta.templateRef` set to the card template; or the agent returns a bulk subtree with root+children and the client will send `{ parentId: workspaceId, elements: [...] }`.

- Add a single child to an existing parent:

```json
{
  "parentId": "existing-parent-uuid",
  "elements": [
    { "id": "new-img-uuid", "type": "image", "properties": { "src": "https://..." }, "parentId": "existing-parent-uuid", "children": [] }
  ]
}
```
