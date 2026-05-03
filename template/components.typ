// components.typ -- Semantic building blocks for NIH F31 grants

#import "@preview/wrap-it:0.1.1": wrap-content

// Disable figure numbering globally (NIH grants use manual bold labels)
#show figure.caption: set text(size: 9pt)

// --- Inline helpers ---
#let term(body) = [_*#body*_]
#let goal(body) = [*Long-term goal:* #body]
#let objective(body) = [*Objective:* #body]
#let rationale(body) = [*Rationale:* #body]
#let sub-label(label, body) = [_*#label:*_ #body]

// --- Central Hypothesis callout ---
#let central-hypothesis(body) = block(
  width: 100%,
  inset: (x: 0.6em, y: 0.3em),
  stroke: (left: 2pt + rgb("#2b579a")),
  fill: rgb("#f0f4fa"),
  [*Central Hypothesis:* #body],
)

// --- Aim block (structured) ---
#let aim(
  number, title,
  hypothesis: none, approach: none, outcomes: none, pitfalls: none,
  body,
) = {
  [== Aim #number: #title]
  body
  if hypothesis != none {
    block(width: 100%, inset: (x: 0.5em, y: 0.2em),
      stroke: (left: 1.5pt + rgb("#5b9bd5")),
      [*Hypothesis #number:* #hypothesis])
  }
  if approach != none { sub-label([Experimental Approach], approach) }
  if outcomes != none { sub-label([Expected Outcomes], outcomes) }
  if pitfalls != none { sub-label([Potential Pitfalls & Alternative Strategies], pitfalls) }
}

// --- Impact / Training ---
#let impact(body) = { [== Impact]; body }
#let training-relevance(body) = block(
  width: 100%, inset: (x: 0.5em, y: 0.2em),
  stroke: (left: 1.5pt + rgb("#70ad47")),
  [*Training Relevance:* #body],
)

// ═══════════════════════════════════════════════════
// FIGURES
// ═══════════════════════════════════════════════════

// --- Full-width figure (multi-panel data, schematics) ---
#let nih-figure(path, caption) = figure(
  image(path),
  caption: caption,
  numbering: none,
)

// --- Wrapped figure with text flowing beside it ---
// width: explicit width of the figure column (e.g., 2.8in)
// side: left or right (where the FIGURE goes)
#let nih-figure-wrap(path, caption, body, width: 3in, side: right) = {
  let fig = box(width: width, {
    image(path, width: 100%)
    v(0.1em)
    text(size: 8.5pt, caption)
  })
  wrap-content(
    align: side,
    column-gutter: 0.5em,
    fig,
    body,
  )
}

// --- Figure placeholder (for figures not yet created) ---
#let figure-placeholder(caption, width: 100%, height: 2.0in) = block(
  width: width, height: height, inset: 0.5em,
  stroke: 0.5pt + luma(180), radius: 2pt,
  align(center + horizon, text(fill: luma(120), size: 9pt, [_[#caption]_])),
)

// ═══════════════════════════════════════════════════

// --- Compact bibliography ---
#let nih-references(bib-path) = {
  v(0.5em)
  set text(size: 9pt)
  set par(leading: 0.3em, spacing: 0.35em)
  bibliography(bib-path, title: "References", style: "american-medical-association")
}

#let gap(size: 0.3em) = v(size)
