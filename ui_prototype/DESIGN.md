---
name: ScholarPulse Analytics
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#5a4138'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#8e7166'
  outline-variant: '#e2bfb2'
  surface-tint: '#a73a00'
  primary: '#a33900'
  on-primary: '#ffffff'
  primary-container: '#cc4900'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb599'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#006194'
  on-tertiary: '#ffffff'
  tertiary-container: '#007bb9'
  on-tertiary-container: '#fdfcff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbce'
  primary-fixed-dim: '#ffb599'
  on-primary-fixed: '#370e00'
  on-primary-fixed-variant: '#7f2b00'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#cce5ff'
  tertiary-fixed-dim: '#93ccff'
  on-tertiary-fixed: '#001d31'
  on-tertiary-fixed-variant: '#004b73'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-lg:
    fontFamily: Newsreader
    fontSize: 48px
    fontWeight: '600'
    lineHeight: 56px
  display-lg-mobile:
    fontFamily: Newsreader
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
  headline-lg:
    fontFamily: Newsreader
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Newsreader
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
  headline-md:
    fontFamily: Newsreader
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  headline-sm:
    fontFamily: Newsreader
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Hanken Grotesk
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system delivers an authoritative, high-clarity academic analytics environment tailored for institutional researchers, deans, academic advisors, and students tracking rigorous performance metrics. 

The aesthetic is grounded in **Modern Editorial Precision**: an intersection of clinical data presentation and warm, tactile academic stationery. It shuns sterile SaaS tropes in favor of an inviting, scholarly tone that encourages deep focus, longitudinal trend examination, and confident decision-making. 

Visual attributes emphasize crisp readability, structured data hierarchy, and intentional semantic cues. Whitespace is generous but disciplined, framing information cleanly against an alabaster canvas to mitigate visual fatigue across multi-hour analytical reviews.

## Colors

The palette establishes an unmistakable hierarchy built on high-contrast legibility and academic significance:

- **Canvas & Surface Architecture**: The primary canvas rests on a soft, warm alabaster tone (`#f8fafc` / `#f4f5f8`). Cards and structural modules lift from this background using pure white surfaces (`#ffffff`), delineated by whisper-thin structural borders (`#e2e8f0`).
- **Typography & High-Contrast Slate**: Core typography commands attention using deep slate tiers:
  - Deep Slate (`#0f172a`): Used for primary headers, quantitative metric readouts, and key values.
  - Charcoal Slate (`#1e293b`): Applied to subheaders, table row data, and active interface states.
  - Muted Slate (`#475569` to `#64748b`): Reserved for descriptive captions, auxiliary notes, and metadata labels.
- **Academic Orange (Primary - `#ea580c`)**: Serves as the primary focal point. It drives decisive calls to action, active navigation anchors, highlighted CGPA trend lines, and critical milestone flags.
- **Scholastic Emerald (Secondary - `#10b981`)**: Dedicated exclusively to positive trajectory indicators, honors classifications, upward velocity in grading trends, and pass/retention success marks.
- **Analytical Blue (Tertiary - `#0284c7`)**: Leveraged for benchmark comparisons, historical cohort comparisons, and neutral informational badges.

## Typography

The typographic hierarchy pairs the literary dignity of **Newsreader** for editorial headings and display metrics with the clinical clarity of **Hanken Grotesk** for interface controls and long-form analysis. 

Data labels, grade codes, percentile ranks, and tabular data leverage **JetBrains Mono** to guarantee vertical numeral alignment across comparative academic rosters and GPA breakdowns. All numerical data columns must employ tabular figures (`tnum`) to maintain structural balance.

## Layout & Spacing

The layout model enforces a 12-column fluid grid system pinned to a maximum container width of 1440px to ensure dense analytical modules do not stretch beyond ergonomic reading scanlines.

- **Breakpoints**:
  - **Desktop (1024px and up)**: 12-column grid, `margin`: 2rem, `gutter`: 1.5rem. Supports side-by-side analytical panels, multi-series trend line graphs, and deep data grids.
  - **Tablet (768px - 1023px)**: 8-column grid, `margin`: 1.5rem, `gutter`: 1.25rem. Secondary analytical rails collapse into drawer overlays or stacked tabs below primary metrics.
  - **Mobile (< 768px)**: 4-column grid, `margin-mobile`: 1rem, `gutter-mobile`: 1rem. Data cards collapse to full-width; complex multi-metric graphs shift to swipeable card carousels or simplified sparklines.

## Elevation & Depth

Visual hierarchy rejects heavy, murky dropshadows in favor of **Crisp Architectural Layering** and subtle ambient warmth:

- **Baseline Level (Canvas)**: Background tone (`#f8fafc`) sets the deepest optical depth.
- **Resting Containers (Cards & Tables)**: Pure white (`#ffffff`) background bounded by a 1px crisp outline in `#e2e8f0`. They cast a faint, diffused ambient shadow: `box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03), 0 1px 2px -1px rgba(15, 23, 42, 0.02)`.
- **Hover & Interactive Tiers**: Elevate with a micro-lift: `box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.05), 0 2px 4px -2px rgba(15, 23, 42, 0.03)`. Border tone sharpens to `#cbd5e1`.
- **Floating Modals & Flyout Filters**: Float with structured presence: `box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.07), 0 8px 10px -6px rgba(15, 23, 42, 0.04)`. Accompanied by a 1px border (`#e2e8f0`) to preserve structural edges against high-key backgrounds.

## Shapes

The design system incorporates a disciplined, low-radius architectural form factor (Level 1 - Soft). 

- Base UI components, input fields, and metric badges leverage a `0.25rem` (4px) corner radius.
- Cards, modal containers, and dashboard analytical widgets use `0.5rem` (8px).
- Navigation pills and micro-status tags adopt an intentional `0.75rem` (12px) maximum.

This restrained radius echoes classic academic certificates, index cards, and ledger grids, avoiding the overly playful feel of heavily rounded geometry.

## Components

### Buttons
- **Primary**: Deep orange fill (`#ea580c`), crisp white text (`#ffffff`), subtle inset highlight. Hover transitions to `#c2410c`.
- **Secondary**: Pure white fill (`#ffffff`), 1px border in `#e2e8f0`, deep slate text (`#0f172a`). Hover shifts border to `#cbd5e1` with a `#f8fafc` tint.
- **Tertiary / Ghost**: Transparent fill, muted slate text (`#475569`). Hover reveals `#f1f5f9` surface and slate text (`#0f172a`).

### Analytics Cards & Metric Modules
- Encased in `#ffffff` with a uniform 1px `#e2e8f0` border.
- Headers integrate editorial serif labeling (`Newsreader`, medium weight) alongside a `JetBrains Mono` timestamp or cohort tag.
- Core metric numbers (e.g., "3.92 CGPA") are displayed prominently in `#0f172a` using tabular figures.

### Status Chips & Badges
- **Academic Progress (Emerald)**: `#ecfdf5` background, `#047857` text, and a fine `#a7f3d0` border. Accompanied by an upward directional glyph.
- **Action Required / Academic Warning (Orange)**: `#fff7ed` background, `#c2410c` text, and `#fed7aa` border.
- **Cohort Metadata (Neutral)**: `#f1f5f9` background, `#334155` text, and `#e2e8f0` border.

### Data Tables & Rosters
- Alternating subtle row backgrounds (`#ffffff` and `#fcfdfd`) with a razor-thin border (`#f1f5f9`).
- Column headers formatted in `JetBrains Mono`, all-caps, 11px, tracked out by 0.05em, rendered in `#64748b`.
- Interactive rows elevate slightly with a `#f8fafc` hover fill.

### Input Fields & Select Controls
- Crisp white ground (`#ffffff`), 1px border (`#cbd5e1`), and `0.25rem` corner radius.
- Focus state reveals an orange outer ring: `box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.15)` with an `#ea580c` border stroke.

### Data Visualizations (CGPA Trendlines & Performance Curves)
- Primary metric line (CGPA) rendered in sharp deep orange (`#ea580c`) with a 2.5px stroke weight.
- Historical benchmark or institutional median mapped in dashed tertiary blue (`#0284c7`) or neutral slate (`#94a3b8`).
- Shaded area curves under positive trajectory lines use an emerald-to-transparent vertical gradient (`rgba(16, 185, 129, 0.12)` fading to `rgba(16, 185, 129, 0)`).