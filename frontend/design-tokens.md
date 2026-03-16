# OdooAI — Design Tokens
## Brand Designer (42) + UX Designer (27)
## Date : 2026-03-21

---

## Colors

| Token | Value | Usage |
|-------|-------|-------|
| primary | #1B2A4A | Headers, buttons, links, brand |
| accent | #F0C674 | Badges, highlights, CTAs |
| success | #22C55E | Connected indicator, positive feedback |
| warning | #F59E0B | Alerts, caution |
| error | #EF4444 | Errors, negative feedback |
| gray-50 | #F9FAFB | Chat background |
| gray-100 | #F3F4F6 | Borders, separators |
| gray-400 | #9CA3AF | Secondary text, placeholders |
| gray-700 | #374151 | Body text |
| gray-800 | #1F2937 | Headings |
| gray-900 | #111827 | Input text |
| white | #FFFFFF | Cards, bubbles |

## Typography

| Token | Value | Usage |
|-------|-------|-------|
| font-body | Inter, system-ui, sans-serif | All body text |
| font-mono | JetBrains Mono, monospace | Code blocks |
| text-xs | 0.75rem (12px) | Metadata, badges |
| text-sm | 0.875rem (14px) | Body, messages |
| text-base | 1rem (16px) | Headings in messages |
| text-lg | 1.125rem (18px) | Page headings |
| text-xl | 1.25rem (20px) | Header title |
| font-medium | 500 | Emphasis |
| font-semibold | 600 | Headings, strong |
| font-bold | 700 | Hero titles |

## Spacing

| Token | Value | Usage |
|-------|-------|-------|
| space-1 | 4px | Tight gaps |
| space-2 | 8px | Inline spacing |
| space-3 | 12px | Component padding |
| space-4 | 16px | Card padding, section gaps |
| space-5 | 20px | Message padding |
| space-6 | 24px | Section spacing |
| space-8 | 32px | Large sections |

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| radius-sm | 6px | Badges, small buttons |
| radius-md | 12px | Cards, inputs |
| radius-lg | 16px | Messages, modals |
| radius-xl | 24px | Large cards |
| radius-full | 9999px | Pills, avatars |

## Shadows

| Token | Value | Usage |
|-------|-------|-------|
| shadow-sm | 0 1px 2px rgba(0,0,0,0.05) | Subtle lift |
| shadow-md | 0 4px 6px rgba(0,0,0,0.07) | Cards, header |
| shadow-lg | 0 10px 15px rgba(0,0,0,0.1) | Modals, dropdowns |

## Components

| Component | Background | Border | Radius | Shadow |
|-----------|-----------|--------|--------|--------|
| User bubble | primary | none | radius-lg | shadow-sm |
| AI bubble | white | gray-100 | radius-lg | shadow-sm |
| Header | primary | none | none | shadow-md |
| Input | white | gray-200 | radius-md | none |
| Button primary | primary | none | radius-md | none |
| Badge domain | accent/20 | none | radius-full | none |
| Tool card | blue-50 | primary (left) | radius-md | none |
| Modal | white | none | radius-xl | shadow-lg |

## Tailwind Config Reference

```js
// tailwind.config.js
colors: {
  primary: '#1B2A4A',
  accent: '#F0C674',
  success: '#22C55E',
}
```
