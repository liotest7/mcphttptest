# Ninjamock Editor – Agent Context Guide

Generated: 2025-08-10

This document summarizes the editor’s element model, common properties, behaviors, events, and design system hooks to help an AI agent reason about changes and generate valid tool calls. Use this as RAG context.

## Overview

- Elements are modeled via “adapters” under `src/infrastructure/adapters`.
- The base class is `ElementAdapter`, and specific elements extend it from `src/infrastructure/adapters/elements/*ElementAdapter.ts`.
- Properties are defined and managed via a `Properties` system, supporting constraints, validators, options, subscriptions (reactive reactions), and internal/hidden flags.
- Angular signals are used internally for state like selection, hover, dragging, etc.

## Element taxonomy (adapters)

Located in `src/infrastructure/adapters/elements/`:

- ButtonElementAdapter
- CarouselWebElementAdapter
- CheckboxElementAdapter
- CheckboxLabelElementAdapter
- ContainerElementAdapter
- DeviceElementAdapter
- DropdownElementAdapter
- EllipseElementAdapter
- ErrorElementAdapter
- GroupElementAdapter
- ImageElementAdapter
- InputTextElementAdapter
- LineConnectorElementAdapter
- LineElementAdapter
- NavBarELementAdapter
- PathElementAdapter
- ProgressBarElementAdapter
- RadioElementAdapter
- RadioIconElementAdapter
- RectangleElementAdapter
- SelectElementAdapter
- SelectionElementAdapter
# Ninjamock Editor – Agent Design Context (for RAG)

Scope: This document contains only the information needed for an agent that creates, modifies, deletes, and suggests UI elements. It excludes Angular classes/services and general project architecture.

Use this document as retrieval context for tool-call generation and validation.

## Core concepts

- Element adapters: Code representations of element types, located in `src/infrastructure/adapters/elements/*ElementAdapter.ts`. Each adapter defines a serialized element type and its specific properties/behaviors on top of the base `ElementAdapter`.
- Serialized element: JSON form stored/applied in the project, with `type`, `properties`, and `children`.
- Template elements (templateId): Predefined components that instantiate one element or a composition of multiple elements with preset properties/states. They’re referenced via `templateId`.
- Container element: A general-purpose element used to group/compose other elements.
- Bindings: Dynamic property links between elements/properties (data-driven or interactive), defined as bindings rather than static values.
- Layout: Currently primarily absolute positioning; transitioning to responsive (flex-like) layouts for future export to HTML/CSS.
- States & tokens: Style states and design tokens to enable themeable, stateful designs aligned with HTML/CSS exports.

## Element types (adapters catalogue)

Adapters reside under `src/infrastructure/adapters/elements/`. The serialized `type` typically corresponds to the adapter name without the `ElementAdapter` suffix, lowercased (unless overridden in code via `this.type`). Examples:

- ButtonElementAdapter → type: "button"
- ImageElementAdapter → type: "image"
- TextElementAdapter → type: "text"
- RectangleElementAdapter → type: "rectangle"
- EllipseElementAdapter → type: "ellipse"
- LineElementAdapter → type: "line"
- LineConnectorElementAdapter → type: "line-connector" (or similar)
- SvgElementAdapter → type: "svg"
- PathElementAdapter → type: "path"
- VideoElementAdapter → type: "video"
- CheckboxElementAdapter → type: "checkbox"
- RadioElementAdapter → type: "radio"
- DropdownElementAdapter → type: "dropdown"
- SelectElementAdapter → type: "select"
- SliderElementAdapter → type: "slider"
- ProgressBarElementAdapter → type: "progress-bar"
- SidebarWebElementAdapter → type: "sidebar-web"
- NavBarELementAdapter → type: "navbar"
- GroupElementAdapter → type: "group"
- ContainerElementAdapter → type: "container"
- StackLayoutElementAdapter → type: "stack-layout"
- TableElementAdapter → type: "table"
- TableRowAdapter → type: "table-row"
- TableCellAdapter → type: "table-cell"
- TableSectionAdapter → type: "table-section"
- DeviceElementAdapter → type: "device"
- SelectionElementAdapter → type: "selection"
- ShapeElementAdapter → type: "shape"
- RadioIconElementAdapter → type: "radio-icon"
- CheckboxLabelElementAdapter → type: "checkbox-label"
- InputTextElementAdapter → type: "input-text"
- ToogleElementAdapter → type: "toggle" (nomenclature may vary)
- CarouselWebElementAdapter → type: "carousel-web"

Note: The exact `type` can be customized per adapter. When in doubt, prefer the adapter-defined `this.type` in code.

## Templates vs direct elements

- Direct element: Use the element `type` directly in JSON.
- Template element: Use `type: "templated-element"` with a `templateId` (e.g., "button", "image", etc.). Templates can instantiate single or multiple nested elements with preset properties and states.

Template instantiation rules (children-as-root vs composite)

- Key flags/shape on a template definition:
  - persistentFields.isComposite: boolean indicating a multi-element composition with internal wiring/bindings.
  - useChildAsRoot (aka isChildrenAsRoot): when true, the template’s child node(s) should be inlined as the actual element(s) in the project, not wrapped by a `templated-element`.
  - children: may be a single object (single child) or an array (multiple children). Treat a single object as one-child.

- Decision tree the agent must follow when creating from a templateId:
  1) If isComposite is true OR the template represents a composition (multiple children/bindings), serialize as a wrapper:
     - type: "templated-element"
     - properties.templateId: the template id
     - Do not inline the internal children.
  2) If the template is a single concrete element (e.g., image, text) or useChildAsRoot is true, inline the child:
     - type: child.type (e.g., "image")
     - properties.templateId: keep the source template id
     - Merge defaults from the template and user-specified overrides; children usually [].
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

- Template element
```json
{
  "type": "templated-element",
  "properties": {
    "templateId": "button-basic",
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

Use this list to pick the serialized element type and whether to inline or wrap as a templated-element. If no direct renderer type exists in `generic-element.component.html`, default to wrapper so the engine can realize internal composition.

- image → type: "image" (inline)
- video → type: "video" (inline)
- icon-svg → type: "icon-svg" (inline)
- text → type: "text" (inline)
- button-basic → wrapper (composite) → type: "templated-element" with properties.templateId="button-basic"
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
        "type": "templated-element",
        "properties": {
          "templateId": "button-basic",
          "name": "PrimaryCTA"
        }
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

- Prefer templates (`templated-element`) for standard UI patterns; they may instantiate multi-element compositions with correct defaults and states.
- When using direct element types, set only compatible properties (respect disabled/hidden ones under current behaviors).
- Use 'hug' when layout should be content-driven; otherwise use 'fixed' with explicit dimensions.
- Respect constraints (decimals for size/position, opacity 0..100, rotation within [-360..360]).
- For grouping/composition, use `container` or appropriate layout elements (e.g., stack layouts) as parents.
- Bindings should be used where dynamic or synchronized behavior between elements is needed.

---

This document intentionally omits Angular classes, services, and general project architecture to keep RAG focused on design elements and their JSON schemas.
