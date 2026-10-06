// Place exactly once INSIDE each page, including title and blank pages.
// #import "present-meta.typ": present-meta
// #page[#present-meta() ...]
// #page(fill: rgb("#111418"))[
//   #present-meta(kind: "animation", background: "dark",
//     video: "/media/example.mp4", loop: true)
//   ... poster image ...
// ]
// Video/poster paths name files already staged in public/ (same-origin).
// An omitted poster uses the SVG rendering of this page.
#let present-meta(kind: "static", background: "light", video: none,
  poster: none, loop: true, title: none) = {
  assert(kind in ("static", "animation"), message: "Invalid presenter kind")
  assert(background in ("light", "dark"), message: "Invalid presenter background")
  assert(kind != "animation" or video != none,
    message: "Animation pages require a same-origin video")
  [#metadata((kind: kind, background: background, video: video,
    poster: poster, loop: loop, title: title)) <present-page>]
}
