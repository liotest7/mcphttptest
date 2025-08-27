# Ninjamock Editor – Agent Context Guide

Generated: 2025-08-10

This document summarizes the editor’s element model, common properties, behaviors, events, and design system hooks to help an AI agent reason about changes and generate valid tool calls. Use this as RAG context.

## Overview

- Elements are represented as JSON objects that follow the project contract; each element typically includes `id`, `type`, `properties` and (optionally) `children` or `parentId`.
- Treat elements as data records (JSON shapes). This document describes the canonical JSON contract agents should emit or modify; it does not require knowledge of internal code structure.

## Element types (catalogue)

The runtime recognizes a set of element `type` strings used in serialized payloads. Agents should use these `type` values when creating or modifying elements. Each type has specific capabilities and use cases in the design system.
The available types are listed below:

**button** - Interactive button element for user actions
- Primary use: Call-to-action buttons, form submissions, navigation triggers
- Supports: hover/active states, text content, styling
- Best for: Primary actions, secondary actions, icon buttons

**checkbox** - Boolean input control with checkmark indicator
- Primary use: Multi-selection options, toggle settings, form inputs
- Supports: Checked/unchecked states, labels, validation
- Best for: Multiple choice selections, feature toggles, consent forms

**radio** - Single-selection input control within a group
- Primary use: Exclusive choice selection from multiple options
- Supports: Selected state, grouping with other radios, labels
- Best for: Single choice from predefined options, settings selection

**dropdown** - Expandable list selection component
- Primary use: Space-efficient selection from many options
- Supports: Option lists, search filtering, custom styling
- Best for: Country selection, category filters, compact option lists

**select** - Native select dropdown element
- Primary use: Standard form selection with native OS styling
- Supports: Option groups, multiple selection, validation
- Best for: Standard form inputs, accessibility-first designs

**slider** - Range input control with draggable handle
- Primary use: Numeric value selection within a range
- Supports: Min/max values, step increments, value display
- Best for: Volume controls, price ranges, quantity selection

**toggle** - Switch-style boolean control
- Primary use: On/off settings, feature enables/disables
- Supports: Animation, custom styling, accessibility labels
- Best for: Settings panels, feature flags, binary choices

**input-text** - Text input field for user data entry
- Primary use: Text data collection, search boxes, form fields
- Supports: Placeholder text, validation, different input types
- Best for: Names, emails, search queries, form data

**progress-bar** - Visual indicator of task completion
- Primary use: Loading states, task progress, completion status
- Supports: Percentage values, indeterminate states, styling
- Best for: File uploads, form completion, loading indicators

### Media and Content Elements

**image** - Raster image display element
- Primary use: Photos, illustrations, icons, visual content
- Supports: Multiple formats (JPG, PNG, SVG), responsive sizing, alt text
- Best for: Hero images, product photos, user avatars, decorative graphics

**video** - Video playback element
- Primary use: Video content display with controls
- Supports: Multiple formats, autoplay, controls, poster images
- Best for: Product demos, tutorials, background videos, media content

**icon-svg** - Scalable vector icon element
- Primary use: Small decorative or functional icons
- Supports: Vector scaling, color theming, accessibility labels
- Best for: Navigation icons, status indicators, action buttons

**text** - Rich text content element
- Primary use: Headings, paragraphs, labels, content display
- Supports: Typography styling, rich formatting, text alignment
- Best for: Headlines, body text, captions, labels

### Layout and Structure

**device** - Mobile/Desktop Container Framework (Page)
- Primary Use: Device Mockups and Responsive Design Previews
- Supports: Screen Dimensions and Orientation
- Ideal for: All types of layout and app development to maintain a defined work area for other elements.

**container** - Basic grouping element for absolute positioning
- Primary use: Grouping related elements with manual positioning
- Supports: Absolute positioning, z-index stacking, basic styling
- Best for: Custom layouts, overlays, precise positioning needs

**container-layout** - Advanced responsive container with flex/grid capabilities (Beta)
- Primary use: Responsive layouts with automatic child positioning
- Supports: Flexbox, CSS Grid, gap spacing, alignment controls
- Best for: Responsive designs, component layouts, adaptive interfaces

**stack-layout** - Vertical or horizontal stack container
- Primary use: Simple linear arrangements of elements
- Supports: Direction control, spacing, alignment
- Best for: Navigation menus, button groups, content lists

**group** - Logical grouping element without layout constraints
- Primary use: Organizing elements for selection and manipulation
- Supports: Selection as unit, transformation as group
- Best for: Design organization, batch operations, component grouping

**workspace** - Top-level design canvas container
- Primary use: Root container for entire design compositions
- Supports: Multiple artboards, zoom levels, canvas management
- Best for: Design file organization, artboard management

### Navigation and Layout Components

**navbar** - Horizontal navigation bar component
- Primary use: Primary site navigation and branding
- Supports: Logo placement, navigation links, action buttons
- Best for: Website headers, app navigation, primary menus

**sidebar-web** - Vertical sidebar navigation component
- Primary use: Secondary navigation, filtering, content organization
- Supports: Collapsible sections, nested navigation, responsive behavior
- Best for: Admin interfaces, content management, secondary navigation

### Geometric and Drawing Elements

**shape-rectangle** - Rectangular shape element
- Primary use: Backgrounds, containers, decorative shapes
- Supports: Fill colors, borders, corner radius, effects
- Best for: Cards, panels, background elements, geometric designs

**ellipse** - Circular or oval shape element
- Primary use: Circular buttons, avatars, decorative elements
- Supports: Fill colors, borders, proportional sizing
- Best for: Profile pictures, decorative circles, rounded elements

**line** - Straight line element
- Primary use: Dividers, connectors, decorative elements
- Supports: Stroke styling, endpoints, thickness
- Best for: Section dividers, decorative lines, simple connections

**path** - Custom vector path element
- Primary use: Complex shapes, custom illustrations, icons
- Supports: SVG path data, bezier curves, complex shapes
- Best for: Custom graphics, complex icons, artistic elements

**shape-polygon** - Generic shape element
- Primary use: Basic geometric forms and custom shapes
- Supports: Various shape types, styling, transformations
- Best for: Geometric designs, placeholder shapes, basic forms

**shape-star** - Generic shape element
- Primary use: Basic geometric forms and custom shapes
- Supports: Various shape types, styling, transformations
- Best for: Geometric designs, placeholder shapes, basic forms


### Specialized Interface Elements

**radio-icon** - Visual icon component for radio button styling
- Primary use: Custom radio button appearance
- Supports: Custom styling, states, accessibility
- Best for: Styled radio buttons, custom form controls

**checkbox-label** - Text label component for checkbox controls
- Primary use: Descriptive text for checkbox options
- Supports: Text styling, click-to-toggle, accessibility
- Best for: Form labels, option descriptions, interactive text

### Usage Guidelines for AI Agents

**Structure Strategy:**
- Start with `device` containers for mobile/desktop mockups and when you try to build a page
- Use geometric elements (`shape-rectangle`, `ellipse`) for backgrounds and shapes

**Layout Strategy:**
- Use `container` for precise, absolute positioning needs
- Use `container-layout` for responsive, flexible designs (Beta)
- Use `stack-layout` for simple linear arrangements
- Use `group` for logical organization without layout constraints

**Content Strategy:**
- Use `text` for all textual content with proper typography
- Use `image` for raster graphics and photos
- Use `icon-svg` for scalable icons and simple graphics
- Use `video` for multimedia content

**Interaction Strategy:**
- Use `button` for primary user actions
- Use `input-text` for text data collection
- Use `checkbox`/`radio` for selections
- Use `slider` for range inputs
- Use `dropdown`/`select` for option selection

**Best Practices:**
- Use semantic element types that match the intended user interaction
- Prefer layout containers over absolute positioning for maintainable designs

## Templates vs direct elements

- Direct element: Use the element `type` directly in JSON.
- Template-based element: Use the concrete runtime `type` (e.g., "button", "image") plus `meta.templateRef` carrying the template id/version. Only send differences in an `overrides` object.

### TemplateId → Template Metadata Mapping

Use this list to identify the available `templateId` values and their associated metadata. When using a template, always include `meta.templateRef` in the payload. The `type` field is no longer required, as it will be derived from the template JSON during runtime.

- **image** → Template for images. Add `meta.templateRef` with `id: "image"`.
- **video** → Template for videos. Add `meta.templateRef` with `id: "video"`.
- **icon-svg** → Template for SVG icons. Add `meta.templateRef` with `id: "icon-svg"`.
- **text** → Template for text elements. Add `meta.templateRef` with `id: "text"`.
- **button-basic** → Template for basic buttons. Add `meta.templateRef` with `id: "button-basic"`.
- **toggle-ios** → Template for iOS toggles. Add `meta.templateRef` with `id: "toggle-ios"`.
- **tabbar-ios** → Template for iOS tab bars. Add `meta.templateRef` with `id: "tabbar-ios"`.
- **stepper-ios** → Template for iOS steppers. Add `meta.templateRef` with `id: "stepper-ios"`.
- **status-bar-ios** → Template for iOS status bars. Add `meta.templateRef` with `id: "status-bar-ios"`.
- **slider-ios** → Template for iOS sliders. Add `meta.templateRef` with `id: "slider-ios"`.
- **sidebar-ios** → Template for iOS sidebars. Add `meta.templateRef` with `id: "sidebar-ios"`.
- **segmented-control-ios** → Template for iOS segmented controls. Add `meta.templateRef` with `id: "segmented-control-ios"`.
- **progress-indicator-ios** → Template for iOS progress indicators. Add `meta.templateRef` with `id: "progress-indicator-ios"`.
- **progress-bar-ios** → Template for iOS progress bars. Add `meta.templateRef` with `id: "progress-bar-ios"`.
- **date-time-picker-ios** → Template for iOS date-time pickers. Add `meta.templateRef` with `id: "date-time-picker-ios"`.
- **page-control-ios** → Template for iOS page controls. Add `meta.templateRef` with `id: "page-control-ios"`.
- **notification-ios** → Template for iOS notifications. Add `meta.templateRef` with `id: "notification-ios"`.
- **navbar-ios** → Template for iOS navigation bars. Add `meta.templateRef` with `id: "navbar-ios"`.
- **menu-ios** → Template for iOS menus. Add `meta.templateRef` with `id: "menu-ios"`.
- **input-ios** → Template for iOS input fields. Add `meta.templateRef` with `id: "input-ios"`.
- **alert-ios** → Template for iOS alerts. Add `meta.templateRef` with `id: "alert-ios"`.
- **action-sheet-ios** → Template for iOS action sheets. Add `meta.templateRef` with `id: "action-sheet-ios"`.
- **ios-button** → Template for iOS buttons. Add `meta.templateRef` with `id: "ios-button"`.
- **text-field-android** → Template for Android text fields. Add `meta.templateRef` with `id: "text-field-android"`.
- **tab-bar-android** → Template for Android tab bars. Add `meta.templateRef` with `id: "tab-bar-android"`.
- **toggle-android** → Template for Android toggles. Add `meta.templateRef` with `id: "toggle-android"`.
- **slider-android** → Template for Android sliders. Add `meta.templateRef` with `id: "slider-android"`.
- **side-sheet-android** → Template for Android side sheets. Add `meta.templateRef` with `id: "side-sheet-android"`.
- **bottom-sheet-android** → Template for Android bottom sheets. Add `meta.templateRef` with `id: "bottom-sheet-android"`.
- **search-bar-android** → Template for Android search bars. Add `meta.templateRef` with `id: "search-bar-android"`.
- **radio-android** → Template for Android radio buttons. Add `meta.templateRef` with `id: "radio-android"`.
- **menu-android** → Template for Android menus. Add `meta.templateRef` with `id: "menu-android"`.
- **list-android** → Template for Android lists. Add `meta.templateRef` with `id: "list-android"`.
- **segmented-buttons-android** → Template for Android segmented buttons. Add `meta.templateRef` with `id: "segmented-buttons-android"`.
- **icon-button-android** → Template for Android icon buttons. Add `meta.templateRef` with `id: "icon-button-android"`.
- **fab-extended-android** → Template for Android extended FABs. Add `meta.templateRef` with `id: "fab-extended-android"`.
- **fab-android** → Template for Android FABs. Add `meta.templateRef` with `id: "fab-android"`.
- **dialog-android** → Template for Android dialogs. Add `meta.templateRef` with `id: "dialog-android"`.
- **chip-android** → Template for Android chips. Add `meta.templateRef` with `id: "chip-android"`.
- **checkbox-android** → Template for Android checkboxes. Add `meta.templateRef` with `id: "checkbox-android"`.
- **android-button** → Template for Android buttons. Add `meta.templateRef` with `id: "android-button"`.
- **web-button** → Template for web buttons. Add `meta.templateRef` with `id: "web-button"`.
- **sidebar-web** → Template for web sidebars. Add `meta.templateRef` with `id: "sidebar-web"`.
- **card-web** → Template for web cards. Add `meta.templateRef` with `id: "card-web"`.
- **list-group-web** → Template for web list groups. Add `meta.templateRef` with `id: "list-group-web"`.
- **tab-group-web** → Template for web tab groups. Add `meta.templateRef` with `id: "tab-group-web"`.
- **pagination-web** → Template for web pagination. Add `meta.templateRef` with `id: "pagination-web"`.
- **notification-web** → Template for web notifications. Add `meta.templateRef` with `id: "notification-web"`.
- **progress-web** → Template for web progress bars. Add `meta.templateRef` with `id: "progress-web"`.
- **input-web** → Template for web input fields. Add `meta.templateRef` with `id: "input-web"`.
- **toggle-web** → Template for web toggles. Add `meta.templateRef` with `id: "toggle-web"`.
- **checkbox-web** → Template for web checkboxes. Add `meta.templateRef` with `id: "checkbox-web"`.
- **radio-web** → Template for web radio buttons. Add `meta.templateRef` with `id: "radio-web"`.
- **select-web** → Template for web select dropdowns. Add `meta.templateRef` with `id: "select-web"`.

Examples:

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
### Notes
- Always include `meta.templateRef` when using a template. The `type` field is not required, as it will be derived from the template JSON.
- Ensure that the `templateId` exists in the backend or project configuration before referencing it.

## Base Element Properties

### Identity & Metadata Properties

**name** - `string` (default: `""`)
- Human-readable label for element identification and organization
- Used in layer panels, search, and development workflows
- Can be changed by users for better project organization

**id** - `string` (default: auto-generated UUID)
- Unique identifier for the element, automatically generated
- Required and immutable after creation
- Used for internal references and relationships

**type** - `string` (required)
- Element type that determines behavior and capabilities
- Must be from allowed types: device, button, image, text, rectangle, ellipse, line, container, etc.
- Cannot be changed after element creation

**bindingKey** - `string|null` (default: `null`)
- Optional unique key for data binding relationships
- Used to connect elements in templates and dynamic content
- Enables property synchronization between elements

**templateId** - `string|null` (default: `null`)
- Reference to template this element is based on
- Used for template instances and component systems
- Enables template-based element creation and updates

**referenceElementId** - `string|null` (default: `null`)
- Reference to another element for relationships
- Used for linking, grouping, and interactive behaviors
- Enables element-to-element connections

### Layout & Positioning Properties

**position** - `select` (default: `"absolute"`)
- CSS position type controlling layout behavior
- Options: `absolute`, `relative`, `static`
- Affects how left/top coordinates are interpreted

**left** - `number|null` (default: `null`)
- X-coordinate position relative to parent container
- Measured in pixels with decimal precision (2 places)
- Only applies when position is `absolute` or `relative`

**top** - `number|null` (default: `null`)
- Y-coordinate position relative to parent container
- Measured in pixels with decimal precision (2 places)
- Only applies when position is `absolute` or `relative`

**width** - `number|null` (default: `null`)
- Element width in pixels
- Must be non-negative with decimal precision (2 places)
- Interacts with widthBehavior and lockAspectRatio

**height** - `number|null` (default: `null`)
- Element height in pixels
- Must be non-negative with decimal precision (2 places)
- Interacts with heightBehavior and lockAspectRatio

**widthBehavior** - `select` (default: `"fixed"`)
- Controls how element width responds to content and container
- **fixed**: Uses explicit width value
- **hug**: Width adjusts to fit content (disables width property)
- **fill**: Expands to fill available container width

**heightBehavior** - `select` (default: `"fixed"`)
- Controls how element height responds to content and container
- **fixed**: Uses explicit height value
- **hug**: Height adjusts to fit content (disables height property)
- **fill**: Expands to fill available container height

**zIndex** - `number` (default: `0`)
- Stacking order - higher values appear on top
- Used for layering elements and managing visual hierarchy
- Can be negative for elements that should appear behind others

**lockAspectRatio** - `boolean` (default: `false`)
- Maintains width/height ratio when resizing
- When true, changing width automatically adjusts height and vice versa
- Only applies when both dimensions use fixed behavior

### Transform & Rotation Properties

**scale** - `number` (default: `1`)
- Scale factor for element size transformation
- Range: 0.1 to 10.0
- Applied as CSS transform, affects visual appearance only

**rotation** - `number` (default: `0`)
- Rotation angle in degrees
- Range: -360 to 360, automatically normalized to 0-360
- Applied as CSS transform around element center

### Appearance & Styling Properties

**fill** - `color|null` (default: `null`)
- Background color, gradient, or pattern
- Supports solid colors, linear gradients and radial gradients
- Can be null for transparent background

**stroke** - `color|null` (default: `null`)
- Border/outline color
- Supports same color types as fill
- Works with strokeWidth to create visible borders

**strokeWidth** - `number` (default: `0`)
- Border thickness in pixels
- Can be uniform or per-side (top, right, bottom, left)
- Zero value means no visible border

**strokeStyle** - `select` (default: `"solid"`)
- Border line style
- Options: `solid`, `dashed`, `dotted`
- Only visible when strokeWidth > 0

**strokePosition** - `select` (default: `"inside"`)
- Border position relative to element bounds
- **inside**: Border drawn inside element bounds
- **center**: Border centered on element edge
- **outside**: Border drawn outside element bounds

**borderRadius** - `number|object` (default: `0`)
- Corner radius for rounded corners
- Can be uniform number or object with per-corner values
- Measured in pixels, creates rounded rectangle effect

**opacity** - `number` (default: `100`)
- Element transparency level
- Range: 0-100 (percentage)
- 100 = fully opaque, 0 = fully transparent

**visible** - `boolean` (default: `true`)
- Element visibility state
- Controls CSS display property
- Hidden elements don't participate in layout or interactions

### Spacing Properties

**padding** - `number|object` (default: `0`)
- Internal spacing inside element bounds
- Can be uniform number or object with per-side values (top, right, bottom, left)
- Affects content positioning within element
- Only has effect when the element is a container in 'flex' mode

**margin** - `number|object` (default: `0`, hidden)
- External spacing around element
- Can be uniform number or object with per-side values
- Currently hidden in UI but available for advanced layouts
- Only has effect when the element is a child of container in 'flex' mode

### Constraint Properties

**minWidth** - `number|null` (default: `null`, hidden)
- Minimum width constraint for responsive sizing
- Prevents element from becoming smaller than specified width
- Works with flexible width behaviors

**minHeight** - `number|null` (default: `null`, hidden)
- Minimum height constraint for responsive sizing
- Prevents element from becoming smaller than specified height
- Works with flexible height behaviors

**maxWidth** - `number|null` (default: `null`, hidden)
- Maximum width constraint for responsive sizing
- Prevents element from becoming larger than specified width
- Works with flexible width behaviors

**maxHeight** - `number|null` (default: `null`, hidden)
- Maximum height constraint for responsive sizing
- Prevents element from becoming larger than specified height
- Works with flexible height behaviors

### Effects Properties

**boxShadow** - `object|null` (default: `null`)
- Drop shadow effect with blur, offset, and color
- Properties: offsetX, offsetY, blur, spread, color
- Creates depth and visual separation

**innerShadow** - `object|null` (default: `null`)
- Inner shadow effect for inset depth
- Same properties as boxShadow but applied inside element bounds
- Creates recessed or pressed appearance

**dropShadow** - `object|null` (default: `null`)
- Filter-based drop shadow effect
- Alternative to boxShadow for certain visual effects
- Properties: offsetX, offsetY, blur, color

**layerBlur** - `number|null` (default: `null`)
- Gaussian blur applied to entire element
- Measured in pixels
- Creates focus/unfocus effects

**bgBlur** - `number|null` (default: `null`)
- Background blur effect (backdrop-filter)
- Measured in pixels
- Creates frosted glass effects over background content

### State & Behavior Properties

**state** - `select|null` (default: `null`)
- Current interactive state for stateful elements
- Options: `default`, `hover`, `active`, `disabled`, `focused`
- Used with state-based styling and interactions

**states** - `object|null` (default: `null`, internal)
- Configuration object for available states
- Defines properties that change based on current state
- Internal property managed by state system

### Base Property Value Examples

```json
// Solid color fill
"fill": {
  "type": "solid",
  "color": "#3b82f6",
  "alpha": 1
}

// Linear gradient fill
"fill": {
  "type": "linear-gradient",
  "angle": 45,
  "stops": [
    { "color": "#3b82f6", "offset": 0 },
    { "color": "#8b5cf6", "offset": 1 }
  ]
}

// Box shadow
"boxShadow": {
  "offsetX": 0,
  "offsetY": 4,
  "blur": 6,
  "spread": -1,
  "color": "rgba(0, 0, 0, 0.1)"
}
// Inner Shadow
"innerShadow": {
  "offsetX": 2,
  "offsetY": 2,
  "blur": 4,
  "spread": -1,
  "color": "rgba(0, 0, 0, 0.1)"
}
// Drop Shadow
"dropShadow": {
  "offsetX": 0,
  "offsetY": 2,
  "blur": 3,
  "color": "rgba(0, 0, 0, 0.1)"
}
// Padding object
"padding": {
  "top": 12,
  "right": 16,
  "bottom": 12,
  "left": 16
}
//Margin object
"margin":{
   "top": 16,
  "right": 0,
  "bottom": 0,
  "left": 0
}

// Border radius object
"borderRadius": {
  "topLeft": 8,
  "topRight": 8,
  "bottomRight": 0,
  "bottomLeft": 0
}
```

## Container Element Properties

Container elements extend base element properties with specialized layout, flexbox, and child management capabilities. There are two main container types: `container` (basic) and `container-layout` (advanced with responsive layout features - Beta).

### Layout System Properties

**layout** - `select` (default: `"absolute"`)
- Sets the primary axis direction for layout
- **flex-horizontal**: Children arranged left-to-right (flex-direction: row)
- **flex-vertical**: Children arranged top-to-bottom (flex-direction: column)
- **flex-grid**: Children arranged in a grid pattern with wrapping
- **absolute**: Children positioned absolutely (no layout constraints)
- Determines how children are positioned and sized within the container
- Controls which gap and alignment properties are visible and active

### Flexbox Layout Properties

**flexDirection** - `select` (default: `"row"`,internal only modified by "layout" -> 'flex-[mode]')
- CSS flex-direction property
- **row**: Horizontal main axis, left-to-right
- **column**: Vertical main axis, top-to-bottom
- **row-reverse**: Horizontal main axis, right-to-left
- **column-reverse**: Vertical main axis, bottom-to-top
- Automatically set based on layout property 

**flexWrap** - `select` (default: `"nowrap"`,internal only modified by "layout" -> 'flex-grid' or 'flex-[direction]')
- CSS flex-wrap property controlling line wrapping
- **nowrap**: Items stay on single line, may overflow
- **wrap**: Items wrap to new lines as needed
- **wrap-reverse**: Items wrap to new lines in reverse order
- Automatically set to "wrap" when layout is "flex-grid"

**justifyContent** - `select` (default: `"start"`,internal only modified by "layoutAlign")
- CSS justify-content property for main axis alignment
- **start**: Items aligned to start of container
- **end**: Items aligned to end of container
- **center**: Items centered in container
- **space-between**: Items evenly distributed, first/last at edges
- Automatically updated based on layoutAlign and spacing settings

**alignItems** - `select` (default: `"start"`,internal only modified by "layoutAlign")
- CSS align-items property for cross axis alignment
- **start**: Items aligned to start of cross axis
- **end**: Items aligned to end of cross axis
- **center**: Items centered on cross axis
- **stretch**: Items stretched to fill cross axis
- **baseline**: Items aligned to text baseline
- Automatically updated based on layoutAlign settings

**alignContent** - `select` (default: `"start"`, internal only modified by "layoutAlign")
- CSS align-content property for multi-line flex containers
- **flex-start**: Lines aligned to start of container
- **flex-end**: Lines aligned to end of container
- **center**: Lines centered in container
- **space-between**: Lines evenly distributed
- **space-around**: Lines with equal space around
- **stretch**: Lines stretched to fill container
- Automatically updated based on layoutAlign settings

### Spacing & Gap Properties

**gap** - `number` (default: `0`)
- General gap between all children in pixels
- Used when spacing is uniform in both directions
- Can be disabled when justifyContent uses space distribution
- Applies to both row and column gaps in basic containers

**gapX** - `number|auto` (default: `0`, layout flex only)
- Horizontal gap between children in pixels
- **number**: Fixed pixel value for column gap
- **auto**: Automatic spacing using space-between distribution
- Visible only in horizontal and grid directions
- Controls CSS column-gap property

**gapY** - `number|auto` (default: `0`, clayout flex only)
- Vertical gap between children in pixels
- **number**: Fixed pixel value for row gap
- **auto**: Automatic spacing using space-between distribution
- Visible only in vertical and grid directions
- Controls CSS row-gap property

### Advanced Layout Properties (container width layout diferent to 'absolute')

**layoutAlign** - `layoutAlign` (default: `"top-left"`)
- Combined alignment control for both axes
- Format: `{vertical}-{horizontal}`
- **Vertical options**: top, middle, bottom
- **Horizontal options**: left, center, right
- Examples: "top-left", "middle-center", "bottom-right"
- Automatically updates justifyContent and alignItems properties

**spacingType** - `select` (default: `"fixed"`, layout flex only)
- Controls how spacing between children is calculated
- **fixed**: Uses explicit gap values (gapX, gapY)
- **auto**: Uses automatic space distribution (space-between)
- When set to "auto", gap properties are disabled
- Affects layoutAlign behavior and justifyContent settings

### Selection & Color Management

**selectionColors** - `array` (default: `null`, For internal use, it is modified in runtime)
- Automatically generated collection of color properties from container and children
- Used for batch color editing and design system consistency
- Updates automatically when child colors change
- Provides unified color management interface for complex hierarchies

### Property Value Examples

```json
// Horizontal flexbox container
{
  "layout": "flex-horizontal",
  "layoutAlign": "middle-center",
  "gapX": 16,
  "spacingType": "fixed"
}

// Vertical stack with auto spacing
{
  "layout": "flex-vertical",
  "layoutAlign": "top-left",
  "gapY": "auto",
  "spacingType": "auto"
}

// Grid layout container
{
  "layout": "flex-grid",
  "layoutAlign": "top-left",
  "gapX": 12,
  "gapY": 12,
  "flexWrap": "wrap"
}

// absolute component container
{
  "layout": "absolute"
}
```
### Hierarchy (serialization notes)
- parentId: string — persisted in flat exports to attach during deserialization.
- children: string[] — array of child ids in flat exports. Payloads may omit full child objects when they are present elsewhere in the same `elements` payload.

## Text Element Properties

Text elements extend base element properties with specialized typography, formatting, and text behavior capabilities. They are optimized for displaying and editing textual content with comprehensive styling options.

### Content Properties

**text** - `string` (default: `""`)
- The actual text content to display
- Can include line breaks and special characters
- Primary content property that drives element sizing

### Typography Properties

**fontFamily** - `select` (default: `"Roboto"`)
- Font family for text display
- Available options from font family options list
- Common values: "Roboto", "Arial", "Helvetica", "Times New Roman", "Georgia"
- Affects text rendering and character metrics

**fontSize** - `number` (default: `14`)
- Font size in pixels
- Range: 1-1000 pixels with validation
- Affects text size and automatic height calculations
- Triggers automatic line height recalculation when set to auto

**fontWeight** - `select` (default: `"400"`)
- Font weight/boldness level
- Standard values: "100", "200", "300", "400" (normal), "500", "600", "700" (bold), "800", "900"
- Affects text thickness and visual prominence
- Works in conjunction with isBold property

**fontVariant** - `fontVariation` (default: `FontVariationSource.default()`,this is )
- Advanced font variation settings
- Controls font style variations and OpenType features
- Automatically syncs with isItalic property when changed
- Used for advanced typography control
- This is used by Google variant fonts dynamically loaded into the project, no modification is needed for now.

**lineHeight** - `number|auto` (default: `"auto"`)
- Line spacing between text lines
- **auto**: Calculated as fontSize × 1.222 ratio
- **number**: Fixed line height in pixels
- Affects text block height and readability

**letterSpacing** - `number` (default: `0`)
- Additional space between characters in pixels
- Positive values: increased spacing
- Negative values: tighter spacing
- Affects text width and readability

### Text Styling Properties

**color** - `color` (default: `{ type: 'solid', color: #000000, alpha: 1 }`)
- Text color using full color system
- Supports solid colors with alpha transparency
- Primary visual property for text appearance
- Used in CSS color generation

**isItalic** - `boolean` (default: `false`)
- Applies italic styling to text
- Alternative to fontStyle property
- Syncs automatically with fontVariant changes
- Toggle button control in UI

**isBold** - `boolean` (default: `false`)
- Applies bold styling to text
- Works in addition to fontWeight property
- Quick toggle for bold appearance
- Toggle button control in UI

**textDecoration** - `select` (default: `"none"`)
- Text decoration styling
- Options: "none", "underline","line-through"
- Adds visual emphasis and semantic meaning
- Can be combined with other styling

**textTransform** - `select` (default: `"none"`)
- Text case transformation
- **none**: No transformation
- **uppercase**: ALL CAPS
- **lowercase**: all lowercase
- **capitalize**: First Letter Capitalized
- Applied during rendering, doesn't modify source text

**textBaseline** - `select` (default: `"none"`)
- Vertical text alignment baseline
- Options: "none", "super", "sub"
- Affects vertical positioning within text line
- Used for advanced typography control

### Alignment Properties

**textAlign** - `select` (default: `"left"`)
- Horizontal text alignment within element bounds
- **left**: Left-aligned text
- **center**: Center-aligned text
- **right**: Right-aligned text
- Affects text layout within container

**verticalAlign** - `select` (default: `"start"`)
- Vertical alignment of text within element bounds
- **start**: Top alignment
- **center**: Middle alignment
- **end**: Bottom alignment
- Controls text positioning in vertical space

### Sizing and Layout Properties

**autoSizeType** - `select` (default: `"auto-width"`)
- Controls automatic sizing behavior
- **auto-width**: Width and height adjust to content (hug both)
- **auto-height**: Fixed width, height adjusts to content
- **fixed**: Both width and height are fixed
- Automatically updates widthBehavior and heightBehavior

**widthBehavior** - `select` (default: `"hug"`, controlled by autoSizeType)
- How text element width responds to content
- Managed automatically by autoSizeType property
- Disabled for direct editing in text elements
- **hug**: Width fits content exactly

**heightBehavior** - `select` (default: `"hug"`, controlled by autoSizeType)
- How text element height responds to content
- Managed automatically by autoSizeType property
- Disabled for direct editing in text elements
- **hug**: Height fits content exactly

### List Properties

**listStyle** - `select` (default: `"none"`)
- List formatting when text contains list items
- Options: "none", "orderer", "unorderer"
- Used for structured text content
- Affects text presentation and indentation

### Removed/Hidden Properties

The following base element properties are deleted or hidden for text elements:

**Deleted Properties:**
- `stroke` - Text uses color instead of stroke
- `borderStyle` - Text typically doesn't have borders
- `borderRadius` - Not applicable to text
- `fill` - Text uses color property instead
- `padding` - Text manages spacing differently

**Modified Properties:**
- `widthBehavior` and `heightBehavior` are controlled by autoSizeType
- Size properties work with text measurement system

### Property Value Examples

```json
// Basic text configuration
{
  "text": "Hello World",
  "fontSize": 16,
  "fontFamily": "Roboto",
  "color": { "type": "solid", "color": "#333333", "alpha": 1 }
}

// Advanced typography
{
  "text": "Stylized Text",
  "fontSize": 24,
  "fontFamily": "Georgia",
  "fontWeight": "700",
  "isItalic": true,
  "textDecoration": "underline",
  "letterSpacing": 1.5,
  "lineHeight": 32
}

// Transformed text
{
  "text": "transform this text",
  "textTransform": "uppercase",
  "textAlign": "center",
  "fontSize": 18,
  "fontWeight": "600"
}
```

## Image Element Properties

Image elements extend base element properties with specialized image handling, aspect ratio management, and source type capabilities. They are optimized for displaying various types of visual content including raster images, SVG icons, and icon fonts.

### Image Source Properties

**src** - `ImageProp` (default: `null`)
- Primary image source property supporting multiple source types
- Controls visibility of other properties based on source type
- Triggers automatic size detection for URL-based images
- Core property that determines rendering behavior

**Image Source Types:**

**url** - Web URLs and file paths
```json
{
  "type": "url",
  "value": "https://example.com/image.jpg"
}
```
### Size and Aspect Ratio Properties
**lockAspectRatio** - boolean (default: true)

- Maintains width/height proportions during resizing
- Automatically enabled when loading images with intrinsic dimensions
- Prevents distortion of image content
- Critical for maintaining visual integrity

**widthBehavior** - select (default: "fixed", disabled)

- Fixed to prevent automatic width adjustments
- Ensures precise control over image dimensions
- Works with lockAspectRatio for proportional scaling
- Disabled to maintain image sizing consistency

**heightBehavior** - select (default: "fixed", disabled)

- Fixed to prevent automatic height adjustments
- Ensures precise control over image dimensions
- Works with lockAspectRatio for proportional scaling
- Disabled to maintain image sizing consistency

## Device Element Properties

Device elements represent a special container that simulates a device frame within the editor. They act as locked root-level containers that encapsulate child elements, providing structured dimensions, design grids, and controlled navigation behavior.

### Dimension Properties

**deviceWidth** – number (default: null, required)

- Defines the device frame width in pixels.

- Drives layout calculations and container bounds.

- Falls back to the element’s current width if null.

**deviceHeight** – number (default: null, required)

- Defines the device frame height in pixels.

- Controls the total vertical bounds.

- Falls back to the element’s current height if null.

### Layout Properties

**layoutGrid** – layoutGrid (default: null, for use in editor does not apply or interfere with the final design)

- Controls the design grid configuration inside the device.

- Accepts grid, column, or row layouts.

### Grid Layout Example
```json
{
  "type": "grid",
  "size": 8,
  "color": "#e0e0e0"
}
```

- Uniform grid lines across the device frame.

- **size**: spacing in pixels between lines.

- **color**: grid line color.
### Column Layout Example
```json
{
  "type": "column",
  "count": 12,
  "gutter": 16,
  "margin": 24,
  "width": "auto",
  "alignment": "center",
  "color": "#cccccc"
}
```

- Divides the frame into vertical columns.

- **count**: number of columns.

- **gutter**: spacing between columns in pixels.

- **margin**: left and right margins.

- **width**: column width (number or "auto").

- **alignment**: "start", "center", or "end".

- **color**: guide color.

### Row Layout Example
```json
{
  "type": "row",
  "count": 8,
  "gutter": 12,
  "margin": 20,
  "height": "auto",
  "alignment": "start",
  "color": "#dddddd"
}
```

- Divides the frame into horizontal rows.

- Properties equivalent to column layout, but applied vertically.

### Property Value Examples
```json
// Basic device (mobile frame)
{
  "name":"Android Compact",
  "deviceWidth": 375,
  "deviceHeight": 812,
  "width":375,
  "height":912,
  "left":0,
  "top":0,
  "fill":{
    "type":"solid",
    "color":"#ffffff",
    "alpha":1
  }
}
// Basic device (mobile frame) with grid layout
{
  "name":"Android Compact",
  "deviceWidth": 375,
  "deviceHeight": 812,
  "width":375,
  "height":912,
  "left":0,
  "top":0,
  "layoutGrid": {
    "type": "grid",
    "size": 8,
    "color": "#e0e0e0"
  }
}

// Device with 12-column layout
{
  "name":"Desktop",
  "deviceWidth": 1440,
  "deviceHeight": 900,
  "width":1440,
  "height":900,
  "left":0,
  "top":0,
  "layoutGrid": {
    "type": "column",
    "count": 12,
    "gutter": 24,
    "margin": 32,
    "width": "auto",
    "alignment": "center",
    "color": "#cccccc"
  }
}

```

## Video Element Properties

Video elements extend base element properties with specialized video playback, thumbnail management, and source handling capabilities. They support both direct video files and YouTube embeds with adaptive controls and presentation options.

### Video Source Properties

**videoSource** - `VideoProp` (default: `""`)
- Primary video source property supporting multiple source types
- Controls availability of thumbnail and transform properties
- Automatically detects YouTube URLs for embed handling
- Core property that determines rendering behavior and controls

**Video Source Types:**

**Direct Video URLs**
```json
{
  "type": "url",
  "value": "https://example.com/video.mp4"
}
```

**Youtube Videos**
```json
{
  "type": "url", 
  "value": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```
### Source Control Properties
**sourceType** - select (default: "url")

- Controls video source input method
- url: Direct URL input for video sources
- file: Local file selection (if supported)
- Changes videoSource property label dynamically
- Determines input interface for video source

### Presentation Properties

**thumbnail** - image (default: "")

Poster image displayed before video plays
Used as fallback when video is loading
Disabled automatically for YouTube videos
Standard image property supporting various formats
Enhances user experience and loading states

**transformType** - select (default: "cover")

Controls how video content fits within element bounds
Based on CSS object-fit property
Disabled automatically for YouTube videos
Affects video aspect ratio and cropping behavior

**Transform Type Options**:

cover: Video scaled to cover entire element (may crop)
contain: Video scaled to fit within element (may letterbox)
crop: 
tile:

### Property value example
```json
// Standard MP4 video with custom thumbnail
{
  "videoSource": {
    "type": "url",
    "value": "https://example.com/demo.mp4"
  },
  "thumbnail": "https://example.com/poster.jpg",
  "transformType": "cover",
  "sourceType": "url"
}

// YouTube video (auto-detected)
{
  "videoSource": {
    "type": "url", 
    "value": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  "sourceType": "url"
  // thumbnail and transformType automatically disabled
}

// Video with contain scaling
{
  "videoSource": {
    "type": "url",
    "value": "/local/video.webm"
  },
  "thumbnail": "/local/poster.png",
  "transformType": "contain",
  "sourceType": "file"
}

// Video with no poster (loading state)
{
  "videoSource": {
    "type": "url",
    "value": "https://cdn.example.com/video.mp4"
  },
  "thumbnail": "",
  "transformType": "cover"
}
```