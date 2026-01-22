# Plotting Rules (stataX)

This document defines **strict rules** for visualization artifacts in stataX.

These are not suggestions — they are guarantees.

---

## 1. Artifact Contract

Every plot artifact must:

- Declare **explicit inputs**
- Fail loudly on ambiguity
- Produce deterministic output
- Never infer scale or semantics

---

## 2. Survey Semantics

### Likert & Diverging Likert

- `scale:` is **mandatory**
- `neutral:` must be present **and included in scale**
- Order matters (left → right)
- No auto-centering
- No auto-labeling

**Invalid:**
```yaml
scale: [Low, High]
neutral: Medium
```
**Valid**
```yaml
scale: [Low, Medium, High]
neutral: Medium
```

---

## 3. Multiselect Questions

### Multiselect artifacts assume:

- Multiple responses per row
- Delimiter-aware parsing
- Explicit normalization (percent | count)

### Artifacts:

- multiselect_profile
- heatmap (categorical × categorical)

---

## 4. Styling Rules

- Styling is per artifact
- Global plot styles are not inferred
- Palette names are symbolic (not hardcoded colors)

### Supported palettes:

- `muted`
- `bright`
- `greys`
- `viridis`
- `red_blue`

---

## 5. Output Guarantees

- PNG only (v1.3.x)
- DPI explicitly set
- No GUI backends (CI-only)
- No interactive plots

---

## 6. Failure Philosophy

### stataX will fail if:

- A scale is incomplete
- A center value is missing
- Data encoding is ambiguous
- A plot lacks semantic meaning

This is intentional.

---

## 7. Design Non-goals

- Automatic plot selection
- Implicit survey inference
- Auto-encoding detection
- Silent category merging
