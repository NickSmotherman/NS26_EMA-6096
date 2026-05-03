// nih.typ -- NIH F31 Fellowship Page Setup
//
// Formatting requirements (NOT-OD-22-195, SF424 Application Guide):
//   - Font: Arial, Helvetica, Georgia, or Palatino Linotype, >= 11pt
//   - Margins: >= 0.5 inches all sides
//   - Paper: US Letter (8.5 x 11)
//   - Density: <= 15 chars/linear inch, <= 6 lines/vertical inch
//   - NO page numbers, headers, or footers

#let nih-page(
  font-family: ("Arial", "Helvetica", "Liberation Sans"),
  font-size: 11pt,
  margin: 0.5in,
  body,
) = {
  set document(author: "")
  set page(paper: "us-letter", margin: margin)
  set text(font: font-family, size: font-size, lang: "en", hyphenate: true)
  set par(leading: 0.5em, spacing: 0.55em, justify: true, first-line-indent: 0em)

  // H1: Section title -- centered bold
  show heading.where(level: 1): it => block(
    above: 0em, below: 0.3em, width: 100%,
    align(center, text(size: font-size, weight: "bold", it.body)),
  )
  // H2: Aim / major sub-section titles -- bold with subtle top rule
  show heading.where(level: 2): it => block(
    above: 0.55em, below: 0.15em,
    { line(length: 100%, stroke: 0.4pt + luma(180)); v(0.15em)
      text(size: font-size, weight: "bold", it.body) },
  )
  // H3: Sub-sections (e.g., "Preliminary Studies", "Timeline and Rigor")
  show heading.where(level: 3): it => block(
    above: 0.5em, below: 0.15em,
    text(size: font-size, weight: "bold", it.body),
  )

  body
}
