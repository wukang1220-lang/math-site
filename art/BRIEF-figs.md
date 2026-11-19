# Brief: 21 geometry diagrams for a junior-high math study page

You are drawing original explanatory diagrams for a junior-high mathematics study page
(Traditional Chinese, Taiwan, grades 7–9). Each diagram sits inside a lesson card next to the
key points and is read on phones (about 340 px wide) and desktops (up to about 640 px wide).
Draw everything yourself as clean schematic diagrams — do not trace or imitate any textbook
figure. **Mathematical accuracy matters most**: compute every coordinate (a small script is
fine, but do not save it inside `figs/`); right angles must be right angles, equal lengths
must be equal, midpoints must be midpoints, a tangent must touch the circle at one point,
the circumcenter / incenter / centroid must be at their true positions.

## Output

Write exactly one file per diagram into `figs/`: `figs/<id>.svg`. Write nothing else inside
`figs/`. The ids for your run are listed in the prompt; draw only those.

## Format (checked by `python check_svg.py figs`)

- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 H" role="img">` where H is
  between 140 and 280. No width/height on the root.
- First child: `<title>` with one plain sentence describing the diagram in Traditional Chinese.
- Allowed elements only: g path circle ellipse rect line polyline polygon text tspan title
  defs marker. No gradients, filters, style, script, image, href or comments.
- Colours: every fill/stroke is `none` or one of these CSS variables (they switch for dark mode):
  - `var(--fig-ink)` all text, outlines, points and arrows
  - `var(--fig-soft)` secondary text, dashed construction lines, tick marks
  - `var(--fig-line)` faint grid lines and panel borders
  - `var(--fig-paper)` panel / background fills that must contrast with ink text
  - `var(--ic)` the highlight colour for the one thing the diagram is about (a segment, an
    angle arc, an axis). Never put text on top of a `var(--ic)` fill.
  - `var(--fig-a)` a light blue tint fill, `var(--fig-b)` a light orange tint fill,
    `var(--fig-c)` a light green tint fill (for shading regions, squares, faces of solids)
- Text: `<text>` with `font-size` 11 to 14 (labels 12–13, panel titles 13–14) and
  `fill="var(--fig-ink)"` or `var(--fig-soft)`. Do not set font-family. Point names (A, B, C,
  O, P …) are plain capital letters at size 13. Text must stay inside the viewBox and must not
  overlap other text; budget about 1 em per Chinese character and 0.56 em per Latin
  letter/digit. Put labels in clear space, never on top of a line. No transform on `<text>`;
  groups may use `translate()` only.
- Math symbols: use the Unicode characters ∠ △ ⊥ ∥ ∼ ≅ ° ² √ π ½ ⅓ × − (minus sign) as written
  in the labels below. Write a segment name as plain letters (AB) — no overline needed.
- Marks: right angles = a small square (side 7–8); equal sides = matching tick marks; equal
  angles = matching small arcs (one arc, or two arcs for the second pair); points = filled
  circles r = 2.5.
- Arrows: a `<marker>` inside `<defs>` is fine; every id in a file must start with the file
  name (e.g. `m-perp-arr`).
- Under 9 KB per file; round numbers to at most 1 decimal.
- Use the exact label wording given below. Never add facts, numbers or names not listed.

## Visual style

Calm and readable: thin ink outlines (stroke-width 1.5), soft tint fills, generous white space,
at most one `var(--ic)` highlight per panel. Multi-panel diagrams: equal-width panels
separated by `var(--fig-line)`, each with a short title at the top (size 13). Phones show
these at about 340 px wide, so at most three panels side by side; use two rows if needed.

## The diagrams

### Run A

1. **m-perp** — title `垂直與點到直線的距離`. A horizontal line labelled `M` at its right end.
   A vertical line `L` crossing it at point `Q` (right-angle square at Q). Point `P` on `L`
   above Q; the segment PQ drawn in `var(--ic)` (stroke 3). Labels: `P`, `Q`, `L`, `M`.
   Text at the right side: `L ⊥ M`, `Q 是垂足`, `PQ 的長是 P 到 M 的距離`.
2. **m-bisector** — two panels. Left `中垂線`: horizontal segment AB, midpoint `M` with one
   tick mark on each half, a vertical line `L` through M with a right-angle square; label
   under it `AM = BM，L ⊥ AB`. Right `角平分線`: angle with vertex `O`, rays to `A` (about 10°
   above horizontal) and `B` (about 80°); ray `OC` exactly at the bisector (45°) drawn in
   `var(--ic)`; one small arc in each half; label `∠AOC = ∠COB`.
3. **m-symshapes** — title `常見圖形的對稱軸`. 2 rows × 3 columns of small shapes, each with
   all its symmetry axes as dashed `var(--ic)` lines, and a caption under the shape:
   `等腰三角形 1 條`, `箏形 1 條`, `菱形 2 條` (axes = the two diagonals),
   `長方形 2 條` (axes through midpoints of opposite sides, NOT the diagonals),
   `正方形 4 條`, `正五邊形 5 條`.
4. **m-views** — title `立體圖形與三視圖`. Left: an isometric drawing of 5 unit cubes:
   a 2 × 2 bottom layer plus one cube on top of the **back-left** bottom cube. Mark the
   viewing directions with small arrows labelled `前` (pointing at the front face) and `右`
   (pointing at the right face). Right: three small square-grid drawings with captions:
   `前視圖` = two columns, left column 2 squares tall, right column 1 square;
   `上視圖` = a 2 × 2 square; `右視圖` = two columns, left column 1 square, right column
   2 squares tall (viewed from the right, the front of the solid is on the left).
   Double-check the isometric drawing against these three views.
5. **m-pyth** — title `畢氏定理`. A right triangle with legs in ratio 3 : 4, placed so that
   each side has room for its square; right angle marked; side labels `a`, `b`, `c`
   (c is the hypotenuse). Draw a
   square outward on each side, filled `var(--fig-a)`, `var(--fig-b)`, `var(--fig-c)`, with
   the labels `a²`, `b²`, `c²` inside them (text on the light tint is fine). Caption:
   `直角三角形：a² + b² = c²`.
6. **m-extangle** — title `三角形的內角與外角`. Triangle ABC (A at the top, B bottom-left,
   C bottom-right); side BC extended past C to `D`. The exterior angle ∠ACD marked with an
   arc in `var(--ic)`; the interior angles at A and B marked with ordinary arcs. Captions:
   `∠A + ∠B + ∠ACB = 180°`, `外角 ∠ACD = ∠A + ∠B`.
7. **m-polygon** — title `多邊形的內角和`. A convex pentagon with the two diagonals from one
   vertex, splitting it into 3 triangles filled alternately with `var(--fig-a)` and
   `var(--fig-c)`. Captions: `五邊形分成 3 個三角形：3 × 180° = 540°`,
   `n 邊形內角和 = (n − 2) × 180°`, `任何凸多邊形的外角和 = 360°`.
8. **m-congruence** — title `三角形全等的判別`. Five small tiles (3 + 2 layout). Each tile has
   one triangle with the given parts marked (tick marks for sides, arcs for angles, square
   for the right angle) and a two-line caption: `SSS` / `三邊對應相等`; `SAS` /
   `兩邊及其夾角`; `ASA` / `兩角及其夾邊`; `AAS` / `兩角及一對應邊` (the side is NOT between
   the two angles); `RHS` / `直角、斜邊、一股`.
9. **m-parallel** — title `平行線的截角性質`. Two horizontal parallel lines `L₁` (top) and
   `L₂` (bottom) with small `∥` arrow marks, cut by one slanted transversal. Number the four
   angles at the top crossing `1` (above-right), `2` (above-left), `3` (below-left),
   `4` (below-right) and at the bottom crossing `5` (above-right), `6`, `7`, `8` in the same
   order. Highlight angle 5 in `var(--ic)`. Captions at the side or below:
   `同位角相等：∠1 = ∠5`, `內錯角相等：∠3 = ∠5`, `同側內角互補：∠4 + ∠5 = 180°`.
10. **m-quads** — title `四邊形家族`. A hierarchy with small shape icons inside boxes:
    `四邊形` at the top branching to `梯形`, `平行四邊形`, `箏形`; `平行四邊形` branches to
    `長方形` and `菱形`; both of these join into `正方形`. Under each of 平行四邊形, 長方形,
    菱形, 正方形 add one short soft-grey line: `兩組對邊平行`, `四個直角`, `四邊等長`,
    `四邊等長且四個直角`.
11. **m-construct** — title `尺規作圖：作線段的中垂線`. Segment AB. Two equal-radius arcs
    (radius a bit more than half of AB) centred at A and at B, drawn dashed in
    `var(--fig-soft)`, crossing above and below the segment at `P` and `Q`. Line PQ in
    `var(--ic)`. Step captions: `① 以 A 為圓心、大於 ½AB 為半徑畫弧`,
    `② 以 B 為圓心、同樣半徑畫弧，交於 P、Q`, `③ 連 PQ，即為 AB 的中垂線`.

### Run B

12. **m-midsegment** — two panels. Left `三角形兩邊中點連線`: triangle ABC, `D` midpoint of
    AB and `E` midpoint of AC (tick marks), segment DE in `var(--ic)`; caption
    `DE ∥ BC，DE = ½BC`. Right `梯形中線`: trapezoid with top base `上底` and bottom base
    `下底` (bottom twice as long or so), midline joining the midpoints of the legs in
    `var(--ic)`; caption `中線 = (上底 + 下底) ÷ 2`.
13. **m-similar** — title `相似三角形`. △ABC and a larger △DEF (all sides × 1.5, same
    orientation). Matching angle marks: one arc at A and D, two arcs at B and E, three arcs
    at C and F. Captions: `△ABC ∼ △DEF`, `對應角相等`,
    `對應邊成比例：AB : DE = BC : EF = CA : FD`, `面積比 = 邊長比的平方`.
14. **m-proportion** — title `平行線截比例線段`. Triangle ABC (A top). `D` on AB and `E` on
    AC with DE ∥ BC (DE in `var(--ic)`), AD : DB = 2 : 1 in the drawing. Captions:
    `DE ∥ BC`, `AD : DB = AE : EC`, `AD : AB = AE : AC = DE : BC`.
15. **m-specialtri** — two panels. Left `30°－60°－90°`: right triangle with angles marked
    30° and 60°, the side opposite 30° labelled `1`, opposite 60° labelled `√3`,
    hypotenuse `2`; caption `邊長比 1 : √3 : 2`. Right `45°－45°－90°`: isosceles right
    triangle, legs `1` and `1`, hypotenuse `√2`; caption `邊長比 1 : 1 : √2`.
    Proportions must be correct.
16. **m-circlepos** — title `點、直線與圓的位置關係`. Two rows of three small panels, each
    with a circle of the same radius `r` and centre `O`; `d` is the distance from O.
    Row 1 (a point P): `圓內：d < r`, `圓上：d = r`, `圓外：d > r`.
    Row 2 (a line, show the dashed perpendicular from O to the line): `不相交：d > r`,
    `相切：d = r` (mark the tangent point), `交於兩點：d < r`.
17. **m-inscribed** — two panels. Left `圓心角與圓周角`: circle O; points A and B on the
    lower part of the circle with arc AB in `var(--ic)`; central angle ∠AOB and an inscribed
    angle ∠APB with P on the upper (major) arc; caption lines `∠AOB = 弧 AB 的度數`,
    `∠APB = ½∠AOB`. Right `直徑所對的圓周角`: circle with diameter AB through O and a point
    P on the circle, right-angle square at P; caption `∠APB = 90°`.
18. **m-tangent** — two panels. Left `切線與半徑垂直`: circle O, tangent line L touching at
    `T`, radius OT with a right-angle square at T; caption `OT ⊥ L`. Right `圓外一點的兩條切線`:
    point P outside a circle O, two tangent segments PA and PB touching at A and B (true
    tangent points), radii OA and OB with right-angle squares, tick marks on PA and PB;
    caption `PA = PB`.
19. **m-centers** — title `三角形的三心`. Three panels with the same acute triangle ABC
    (not isosceles). `外心 O`: the three perpendicular bisectors dashed, the circumscribed
    circle through A, B, C, point O; caption `OA = OB = OC`. `內心 I`: the three angle
    bisectors dashed, the inscribed circle tangent to all three sides, point I; caption
    `I 到三邊等距`. `重心 G`: the three medians (D, E, F midpoints), point G; caption
    `AG : GD = 2 : 1`. Compute O, I, G, both circles and the tangent points exactly.
20. **m-solids** — title `柱體與錐體`. Four small oblique drawings (hidden edges dashed):
    `三角柱`, `圓柱`, `四角錐`, `圓錐`. On the 三角柱 label `底面` and `側面`; on the 圓柱 label
    `高`; on the 四角錐 label `頂點`; on the 圓錐 label `底面` and `高`. Captions under the row:
    `直角柱體積 = 底面積 × 高`, `柱體、錐體的表面積：看展開圖`.
21. **m-nets** — two panels. Left `正方體的展開圖`: a cross-shaped net of 6 equal squares
    (a column of 4 with one square on each side of the second square). Right
    `圓柱的展開圖`: a rectangle with one circle touching its top edge and one touching its
    bottom edge; label the rectangle's long side `2πr` and short side `h`, the circle
    radius `r`; caption `側面積 = 2πr × h`.
