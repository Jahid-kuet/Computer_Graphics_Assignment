import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'''<w:tcMar {nsdecls("w")}>
        <w:top w:w="{top}" w:type="dxa"/>
        <w:bottom w:w="{bottom}" w:type="dxa"/>
        <w:left w:w="{left}" w:type="dxa"/>
        <w:right w:w="{right}" w:type="dxa"/>
    </w:tcMar>''')
    tcPr.append(tcMar)

def create_document():
    doc = Document()

    # Set standard A4 page margins (0.7 in = ~50.4 pt)
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)  # A4 width
        section.page_height = Inches(11.69) # A4 height
        section.top_margin = Inches(0.65)
        section.bottom_margin = Inches(0.65)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(30, 30, 30)

    COLOR_TITLE = RGBColor(15, 34, 64)       # Deep Navy
    COLOR_PRIMARY = RGBColor(27, 54, 93)     # Navy Blue
    COLOR_SECONDARY = RGBColor(180, 80, 20)  # Rust Orange / Dark Amber
    COLOR_MUTED = RGBColor(90, 100, 110)

    def add_title(text, subtitle=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(16)
        run.font.color.rgb = COLOR_TITLE

        if subtitle:
            p2 = doc.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p2.paragraph_format.space_before = Pt(0)
            p2.paragraph_format.space_after = Pt(10)
            run2 = p2.add_run(subtitle)
            run2.italic = True
            run2.font.name = 'Calibri'
            run2.font.size = Pt(10)
            run2.font.color.rgb = COLOR_MUTED

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.color.rgb = COLOR_PRIMARY

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_SECONDARY

    def add_body(text, bold_prefix=None, space_after=3):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.12
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Calibri'
            r_b.font.size = Pt(10)
            r_b.font.color.rgb = RGBColor(20, 20, 20)
        r_t = p.add_run(text)
        r_t.font.name = 'Calibri'
        r_t.font.size = Pt(10)
        return p

    def add_bullet(text, bold_prefix=None, space_after=2):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.1
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Calibri'
            r_b.font.size = Pt(9.5)
            r_b.font.color.rgb = RGBColor(20, 20, 20)
        r_t = p.add_run(text)
        r_t.font.name = 'Calibri'
        r_t.font.size = Pt(9.5)
        return p

    def add_callout(text, bold_title="Note:"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F2F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        r_title = p.add_run(bold_title + " ")
        r_title.bold = True
        r_title.font.name = 'Calibri'
        r_title.font.size = Pt(9.5)
        r_title.font.color.rgb = COLOR_PRIMARY
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(9.5)
        # Empty space after table
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(4)

    fig_dir = r"c:\Users\HP\OneDrive\Desktop\Graphics Nihal\Assignment\figures"

    # ==========================================
    # PAGE 1: Problem Statement & Algorithm Choice
    # ==========================================
    add_title("Forward (Light-Based) Ray Tracing for Multiple Spheres",
              "A Hand-Written Assignment Solution with Multiple Point Lights, Reflection, & Refraction")

    add_h1("1. Problem Statement")
    add_body(
        "Design and describe an efficient forward (light-based) ray-tracing algorithm that renders a multi-object scene "
        "containing multiple spheres with diverse optical properties (reflective, transparent, combined, and diffuse) "
        "illuminated by multiple point light sources (L1, L2, ..., Ln). Unlike the classical backward ray-tracing algorithm "
        "covered in class—where primary rays originate at the viewer/eye and shadow rays test light visibility—here rays originate "
        "at each light source, propagate forward into the scene, undergo recursive reflection and refraction at spherical interfaces, "
        "and are connected to the eye via camera-connection rays to produce the final shaded, visible image on the projection plane."
    )

    add_h1("2. Introduction & Comparative Algorithm Analysis")
    add_body(
        "Ray tracing is a comprehensive global illumination technique that solves hidden-surface removal, shadow generation, "
        "specular reflection, and Snell's law refraction within a unified geometric framework. In classical (backward) ray tracing, "
        "rays are fired from the camera into the scene through each pixel. Forward (light-based) ray tracing reverses this causal chain: "
        "energy is emitted directly from the light sources into the environment. To solve this problem efficiently, three candidate "
        "forward ray-tracing paradigms were evaluated:"
    )

    add_bullet(
        "Emits rays from each light source in uniformly distributed random directions over the full sphere of directions (4π steradians) "
        "and traces them until they strike surfaces or enter the camera. "
        "Critical Flaw: The probability P ≈ A_eye / (4π d²) of a randomly bounced ray hitting a pinhole camera aperture is practically zero. "
        "Almost all traced rays are wasted in empty space, causing catastrophic noise and unacceptable computational cost.",
        "Option A: Naive Random Forward Ray Tracing — "
    )

    add_bullet(
        "A two-pass technique where Pass 1 forward-traces photon rays from light sources and stores their energy, positions, and incident "
        "directions at intersection points inside a spatial k-d tree (the photon map). Pass 2 casts rays from the camera and performs "
        "k-nearest-neighbors (k-NN) spherical density estimation. "
        "Critical Flaw: While highly effective for complex caustics, it introduces heavy auxiliary data-structure overhead (k-d tree construction, "
        "balancing, and radius searching) and requires an extra backward gathering pass, exceeding the scope of direct forward tracing.",
        "Option B: Photon Mapping (Two-Pass Global Illumination) — "
    )

    add_bullet(
        "Constrains light emission to only the solid bounding cones subtended by the spheres in the scene (eliminating rays fired into empty space). "
        "When an emitted ray strikes a sphere, the intersection is solved in O(1) via the closed-form quadratic equation. Direct shading is evaluated, "
        "and a direct connection ray is cast from the hit point to the eye (inverting the classical shadow ray) to evaluate visibility and project energy. "
        "Simultaneously, specular reflection and refraction rays are spawned recursively to propagate illumination across other spheres.",
        "Option C: Targeted Forward Ray Tracing with Direct Eye Connection & Recursive Spawning (Chosen) — "
    )

    add_h2("Rationale for Selecting Option C:")
    add_body(
        "1. Maximum Efficiency: Solid angle cone bounding prevents wasted rays in void directions, achieving 100% ray-object engagement.\n"
        "2. Exact Slide Inversion: It represents the exact mathematical dual of the lecture slides—swapping eye-to-light shadow rays with "
        "surface-to-eye connection rays, while preserving identical O(1) quadratic intersection and Snell's law formulas.\n"
        "3. Zero Memory Overhead: Evaluates multi-bounce specular reflection and transparent refraction deterministically without requiring "
        "costly spatial indexing structures (k-d trees or photon maps)."
    )

    doc.add_page_break()

    # ==========================================
    # PAGE 2: 2D Diagrams & System Architecture
    # ==========================================
    add_h1("3. Forward Ray-Tracing System Architecture & 2D Diagrams")
    add_body(
        "To clearly visualize the forward ray-tracing pipeline across multiple spheres with distinct material properties, "
        "the diagrams below illustrate the reversed geometric scene setup and the corresponding recursive forward ray tree."
    )

    fig1_path = os.path.join(fig_dir, "fig1_forward_scene.png")
    if os.path.exists(fig1_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(fig1_path, width=Inches(5.6))

    add_body(
        "Figure 1: Forward ray-tracing scene with multiple point lights (L1, L2), multiple spheres (S1: transparent, S2: reflective, "
        "S3: reflective, S4: diffuse), and direct eye-connection rays. Notice that secondary reflected (R1) and refracted (T1) rays "
        "propagate light forward, while surface-to-eye connection rays replace classical shadow rays. Occlusion is tested along the connection line.",
        bold_prefix="Figure 1 Description: ", space_after=4
    )

    fig2_path = os.path.join(fig_dir, "fig2_forward_tree.png")
    if os.path.exists(fig2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(2)
        p_img2.paragraph_format.space_after = Pt(2)
        doc.add_picture(fig2_path, width=Inches(4.4))

    add_body(
        "Figure 2: Forward Ray Interaction Tree (Dual of Lecture Slide 18). Rays originate at light source Li (Root). At transparent sphere S1, "
        "the ray bifurcates into transmitted ray T1 (striking S3 then S4) and reflected ray R1 (striking S2). At every visible hit node, "
        "a direct connection ray splats radiance directly to the Eye / Image Plane.",
        bold_prefix="Figure 2 Description: ", space_after=4
    )

    add_callout(
        "When sketching these 2D figures by hand on your A4 page:\n"
        "• Draw Light L1 (top-left) and Light L2 (bottom-left) emitting yellow/gold rays toward transparent sphere S1.\n"
        "• Draw S1 refracting light (green ray T1) toward S3, and reflecting light (red ray R1) toward S2.\n"
        "• Draw Eye / Camera on the far right with a 1D/2D projection screen, and draw dashed purple connection lines from each hit point to Eye.\n"
        "• Draw the Forward Tree (Figure 2) branching downwards: Root Light -> S1 -> (Left: S3 -> S4, Right: S2), with dashed eye arrows at each node.",
        "Hand-Drawing Guide for 2D Figures:"
    )

    doc.add_page_break()

    # ==========================================
    # PAGE 3: Mathematical Formulations
    # ==========================================
    add_h1("4. Mathematical Formulations & Geometric Derivations")
    add_body(
        "The mathematical foundation directly implements the vector formulation taught in class (Slides 25–30, 45–46), "
        "extended to multi-sphere sorting, specular reflection, and Snell's refraction."
    )

    # Place Fig 3 & Fig 4 side by side or sequentially
    fig3_path = os.path.join(fig_dir, "fig3_raysphere_geom.png")
    fig4_path = os.path.join(fig_dir, "fig4_snell_reflection.png")

    if os.path.exists(fig3_path) and os.path.exists(fig4_path):
        table_geom = doc.add_table(rows=1, cols=2)
        table_geom.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell_l = table_geom.cell(0, 0)
        cell_r = table_geom.cell(0, 1)
        p_l = cell_l.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_l.paragraph_format.space_before = Pt(0)
        p_l.paragraph_format.space_after = Pt(0)
        cell_l.paragraphs[0].add_run().add_picture(fig3_path, width=Inches(3.2))

        p_r = cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(0)
        cell_r.paragraphs[0].add_run().add_picture(fig4_path, width=Inches(3.2))

        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(4)
        r_c = p_cap.add_run("Figure 3: Analytical Ray-Sphere Geometry (Slide 45)      |      Figure 4: Reflection & Snell's Refraction (Slides 25–30)")
        r_c.font.size = Pt(8.5)
        r_c.font.color.rgb = COLOR_MUTED

    add_h2("4.1 Parametric Ray & Implicit Sphere Equations")
    add_bullet("Parametric Ray:  u(t) = s + t·d,   with origin s, unit direction ||d|| = 1, and t > 0.")
    add_bullet("Implicit Sphere:  ||p - c||² = R²  <=>  (p - c) · (p - c) - R² = 0, with center c and radius R.")

    add_h2("4.2 Quadratic Intersection Derivation (Slide 45)")
    add_body(
        "Substitute ray u(t) into the sphere equation: ((s + t·d) - c) · ((s + t·d) - c) - R² = 0\n"
        "Expanding terms yields: (d · d)·t² + 2((s - c) · d)·t + ((s - c) · (s - c) - R²) = 0\n"
        "Standard Quadratic Form: A·t² + B·t + C = 0,   where:\n"
        "    • A = ||d||² = 1 (unit direction vector)\n"
        "    • B = 2 (s - c) · d\n"
        "    • C = ||s - c||² - R² = (s - c) · (s - c) - R²"
    )

    add_h2("4.3 Discriminant Analysis & Multi-Sphere Nearest-Hit Sorting")
    add_body(
        "The discriminant is:  Δ = B² - 4AC = B² - 4C\n"
        "    • Δ < 0: Ray misses the sphere entirely (no real roots).\n"
        "    • Δ = 0: Ray is tangent to the sphere at a single point t = -B / 2.\n"
        "    • Δ > 0: Ray intersects at two points: t0 = (-B - √Δ)/2  and  t1 = (-B + √Δ)/2.\n"
        "Multi-Sphere Nearest-Hit Rule: Iterate over all spheres k in {1, ..., M}. The true physical hit point is the smallest positive root:\n"
        "    t* = min_{k=1...M} { t in {t0,k, t1,k} | t > ε },   where ε ≈ 10⁻⁴ prevents self-intersection shadow acne."
    )

    add_h2("4.4 Hit Point, Surface Normal, and View Vector")
    add_bullet("Hit Point:  P = s + t*·d")
    add_bullet("Outward Unit Normal:  N = (P - c) / R.  (If ray hits from inside a transparent sphere, reverse: N = -N).")
    add_bullet("Unit View Vector (toward eye at E):  V = (E - P) / ||E - P||")

    add_h2("4.5 Specular Reflection & Snell's Law Refraction (Slides 25–30)")
    add_bullet("Ideal Specular Reflection Vector:  r = d - 2(d · N) N   (or for light incident vector L: R_spec = 2(N · L) N - L).")
    add_bullet(
        "Snell's Refraction Vector: Let relative index η = η1 / η2, and cos θ1 = -(d · N). From Snell's Law:\n"
        "    cos² θ2 = 1 - η² (1 - cos² θ1) = 1 - η² (1 - (d · N)²)\n"
        "    • If cos² θ2 < 0: Total Internal Reflection (TIR) occurs; no refraction, all energy reflects along r.\n"
        "    • If cos² θ2 ≥ 0: Transmitted Unit Direction:  t = η·d + (η (d · N) - √(cos² θ2)) N",
        "Refraction Vector (Slide 30): "
    )

    add_h2("4.6 Direct Eye-Connection Ray & Occlusion Test (Inverted Shadow Ray)")
    add_body(
        "To test visibility from P to Eye E, define the connection ray: r_eye(τ) = P + τ·V,   τ in (ε, ||E - P||).\n"
        "    1. Back-face culling: If N · V ≤ 0 (for opaque surfaces), point faces away from camera; connection is culled.\n"
        "    2. Occlusion test: Solve quadratic A·τ² + B·τ + C = 0 against all other spheres Sj (j ≠ hit). If any valid root τ "
        "lies in (ε, ||E - P||), P is occluded from the eye (in shadow). Otherwise, connect and splat to the image plane."
    )

    add_h2("4.7 Illumination Model & Recursive Radiance Accumulation")
    add_body(
        "Total Intensity at P:  I(P) = I_local + k_s · I(r) + k_t · I(t)\n"
        "Where local Phong illumination across n point lights is:  "
        "I_local = I_a·k_a + Σ_{i=1}^n I_{p,i} [ k_d (L_i · N) + k_s (R_i · V)^k ]"
    )

    doc.add_page_break()

    # ==========================================
    # PAGE 4: Pseudo-Algorithm & Findings
    # ==========================================
    add_h1("5. Concise Pseudo-Algorithm (Step-by-Step Text Form)")
    add_body(
        "Below is the complete, concise forward ray-tracing algorithm designed to be handwritten clearly on your final A4 page:"
    )

    steps = [
        ("Step 1: Scene & Cone Initialization — ",
         "Define M spheres {S1, ..., SM} with centers c_k, radii R_k, and material coefficients (k_a, k_d, k_s, k_t, η_k). "
         "For each point light source i = 1 to n, compute the bounding solid angle subtended by all spheres as viewed from light position s_i."),

        ("Step 2: Targeted Primary Emission — ",
         "For each light i, sample unit ray directions d restricted strictly within the solid angle bounding cones. Set primary ray origin s = pos(L_i) and depth = 0."),

        ("Step 3: Multi-Sphere Quadratic Intersection — ",
         "For the current ray (s, d), test intersection against every sphere k = 1 to M. Compute A = 1, B = 2(s - c_k)·d, and C = ||s - c_k||² - R_k². "
         "Evaluate discriminant Δ_k = B² - 4C."),

        ("Step 4: Discriminant & Nearest-Hit Selection — ",
         "If Δ_k < 0, discard sphere k. If Δ_k ≥ 0, calculate roots t0, t1. Find the global nearest valid hit: "
         "t* = min_k {t > ε}. If no sphere intersects with t > ε, the ray escapes into the background; terminate trace."),

        ("Step 5: Surface Differential Geometry — ",
         "Compute hit point P = s + t*·d, surface outward normal N = (P - c)/R (invert N if inside), and view vector toward eye V = (E - P) / ||E - P||."),

        ("Step 6: Direct Eye Connection & Occlusion Test (Inverted Shadow Ray) — ",
         "If N · V > 0 (or if surface is transparent): Cast connection ray r_eye(τ) = P + τ·V toward Eye E. "
         "Test quadratic intersection of r_eye against all other spheres S_j (j ≠ hit). "
         "If unoccluded for all τ in (ε, ||E - P||), project P onto the image plane through camera pinhole to pixel (x, y) and splat local intensity I_local."),

        ("Step 7: Specular Reflection Spawning — ",
         "If sphere has specular reflectivity (k_s > 0) and depth < MAX_DEPTH: Compute reflection direction r = d - 2(d · N) N. "
         "Spawn secondary ray with origin P + ε·r and direction r; recursively call trace from Step 3."),

        ("Step 8: Transparent Refraction Spawning (Snell's Law) — ",
         "If sphere is transparent (k_t > 0) and depth < MAX_DEPTH: Compute cos² θ2 = 1 - η²(1 - (d · N)²). "
         "If cos² θ2 < 0 (TIR), energy redirects along r. Otherwise, compute transmission direction t = η·d + (η(d·N) - √(cos² θ2))N. "
         "Spawn transmitted ray with origin P + ε·t and direction t; recursively call trace from Step 3."),

        ("Step 9: Radiance Accumulation & Splatting — ",
         "Accumulate blended radiance I(P) = I_local + k_s·I(r) + k_t·I(t) and weight into image buffer pixel (x, y) using anti-aliasing filter."),

        ("Step 10: Convergence & Completion — ",
         "Repeat Steps 2–9 for all sampled rays across all n lights. Normalize image buffer by total emitted ray count to produce the final rendered image.")
    ]

    for prefix, body in steps:
        add_bullet(body, prefix, space_after=2.5)

    add_h1("6. Key Findings and Analytical Comments (Point Form)")
    findings = [
        ("Targeted Emission Efficiency: ", "Restricting emitted light rays to the solid angle cones subtended by spheres converts a near-zero naive hit probability (P ≈ 0) into 100% ray-surface engagement, making forward ray tracing practical."),
        ("Exact Dual of Lecture Setup: ", "Forward ray tracing directly inverts the classical slide workflow: lights act as primary ray emitters, while eye connection rays replace shadow rays, demonstrating algorithmic duality."),
        ("O(1) Intersection with Early Rejection: ", "The closed-form quadratic equation resolves ray-sphere intersections in constant O(1) time per sphere. The discriminant check (Δ < 0) provides early rejection before computing square roots."),
        ("Multi-Object Shadowing: ", "Unlike a single-sphere scene (where self-shadowing is impossible on a convex hull), a multi-sphere scene requires testing the eye-connection ray against all other spheres to correctly render cast shadows and mutual occlusions."),
        ("Rigorous Handling of Snell's Law: ", "Transparent spheres accurately simulate light refraction and Total Internal Reflection (TIR) using the vector Snell formulation, naturally capturing caustics and internal reflections."),
        ("Direct Splatting vs. Photon Storage: ", "By connecting hit points directly to the eye and projecting to the image plane, this algorithm avoids the heavy memory overhead of k-d trees and photon maps while remaining completely feasible for manual analysis.")
    ]

    for prefix, text in findings:
        add_bullet(text, prefix, space_after=2.5)

    # Save document
    out_docx = r"c:\Users\HP\OneDrive\Desktop\Graphics Nihal\Assignment\Forward_Ray_Tracing_MultiSphere_Assignment.docx"
    doc.save(out_docx)
    print(f"Document successfully created at: {out_docx}")

if __name__ == "__main__":
    create_document()
