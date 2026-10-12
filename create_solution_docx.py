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

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
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

    # Set standard A4 page margins (top/bottom 0.55 in, left/right 0.65 in)
    for section in doc.sections:
        section.page_width = Inches(8.27)   # A4 width
        section.page_height = Inches(11.69) # A4 height
        section.top_margin = Inches(0.55)
        section.bottom_margin = Inches(0.55)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(25, 25, 25)

    COLOR_TITLE = RGBColor(12, 30, 60)       # Deep Navy
    COLOR_PRIMARY = RGBColor(22, 50, 92)     # Navy Blue
    COLOR_SECONDARY = RGBColor(175, 75, 15)  # Rust Orange / Dark Amber
    COLOR_MUTED = RGBColor(85, 95, 105)

    def add_title(text, subtitle=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(15.5)
        run.font.color.rgb = COLOR_TITLE

        if subtitle:
            p2 = doc.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p2.paragraph_format.space_before = Pt(0)
            p2.paragraph_format.space_after = Pt(8)
            run2 = p2.add_run(subtitle)
            run2.italic = True
            run2.font.name = 'Calibri'
            run2.font.size = Pt(9.5)
            run2.font.color.rgb = COLOR_MUTED

    def add_h1(text, space_before=6, space_after=2.5):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(11.5)
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h2(text, space_before=4, space_after=1.5):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_body(text, bold_prefix=None, space_after=2.5, line_spacing=1.10):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
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

    def add_bullet(text, bold_prefix=None, space_after=2, line_spacing=1.08):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Calibri'
            r_b.font.size = Pt(9)
            r_b.font.color.rgb = RGBColor(20, 20, 20)
        r_t = p.add_run(text)
        r_t.font.name = 'Calibri'
        r_t.font.size = Pt(9)
        return p

    def add_callout(text, bold_title="Note:", space_after=3):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F2F5F9")
        set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.08
        r_title = p.add_run(bold_title + " ")
        r_title.bold = True
        r_title.font.name = 'Calibri'
        r_title.font.size = Pt(8.5)
        r_title.font.color.rgb = COLOR_PRIMARY
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(8.5)
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(space_after)

    fig_dir = r"c:\Users\HP\OneDrive\Desktop\Graphics Nihal\Assignment\figures"

    # ==============================================================================
    # PAGE 1: Problem Statement & Comparative Algorithm Analysis
    # ==============================================================================
    add_title("Forward (Light-Based) Ray Tracing for Multiple Spheres",
              "A Hand-Written Assignment Solution with Multiple Point Lights, Full RGB Color Computation, Reflection, & Refraction")

    add_h1("1. Problem Statement")
    add_body(
        "Design and describe an efficient forward (light-based) ray-tracing algorithm that renders a multi-object 3D scene "
        "containing multiple spheres with diverse optical and chromatic properties (RGB color materials: diffuse, specular, "
        "transparent filter tint, and reflective) illuminated by multiple point light sources (L1, L2, ..., Ln) each emitting "
        "spectral/RGB illumination. Unlike classical backward ray tracing covered in class—where primary rays originate at the "
        "camera eye and shadow rays test light visibility—here primary rays originate at each light source carrying color energy, "
        "propagate forward into the scene, undergo recursive reflection and refraction with spectral color filtering, and are "
        "connected to the eye via camera-connection rays to compute and composite the final full-color RGB image on the projection plane."
    )

    add_h1("2. Introduction & Comparative Algorithm Analysis")
    add_body(
        "Ray tracing is a comprehensive global illumination paradigm that integrates hidden-surface removal, shadow generation, "
        "specular reflection, Snell's law refraction, and color shading into a single framework. In backward ray tracing, rays are "
        "cast from the eye through each pixel. Forward ray tracing reverses this physical causality: energy is emitted directly "
        "from the light sources into the environment. To solve this problem efficiently, three candidate forward paradigms were evaluated:"
    )

    add_bullet(
        "Emits rays from each light source in uniformly distributed random directions across 4π steradians. Rays bounce around the scene "
        "and are recorded only if they randomly hit the camera aperture. "
        "Critical Flaw: The probability P ≈ A_eye / (4π d²) of a randomly bounced ray hitting a pinhole camera aperture is practically zero. "
        "Almost all traced rays are wasted in empty space, causing catastrophic noise and unacceptable computational cost.",
        "Option A: Naive Random Forward Ray Tracing — "
    )

    add_bullet(
        "A two-pass technique where Pass 1 forward-traces photon rays from light sources and stores their RGB energy, positions, and incident "
        "directions inside a spatial k-d tree (the photon map). Pass 2 casts rays from the camera and performs k-nearest-neighbors (k-NN) "
        "density estimation. "
        "Critical Flaw: While highly effective for complex caustics, it introduces heavy auxiliary data-structure overhead (k-d tree construction, "
        "balancing, and radius searching) and requires an extra backward gathering pass, exceeding the scope of direct forward tracing.",
        "Option B: Photon Mapping (Two-Pass Global Illumination) — "
    )

    add_bullet(
        "Constrains light emission strictly to the solid bounding cones subtended by all spheres in the scene (100% ray-object engagement). "
        "When an emitted ray strikes a sphere, the intersection is solved in O(1) via the closed-form quadratic equation. Local Phong RGB color "
        "shading is evaluated, and a direct connection ray is cast from the hit point to the eye (inverting the classical shadow ray) to evaluate "
        "visibility and splat RGB radiance into the image buffer. "
        "Simultaneously, specular reflection and refraction rays are spawned recursively to propagate illumination across subsequent spheres.",
        "Option C: Targeted Forward Ray Tracing with Direct Eye Connection & Recursive Spawning (Chosen) — "
    )

    add_h2("Rationale for Selecting Option C:")
    add_body(
        "1. Maximum Sampling Efficiency: Solid angle cone bounding prevents wasted rays in void directions, achieving 100% ray-object engagement.\n"
        "2. Exact Mathematical Dual of Class Slides: Swaps eye-to-light shadow rays with surface-to-eye connection rays, preserving identical "
        "O(1) quadratic intersection, Snell's law formulas, and Phong shading.\n"
        "3. Full RGB Spectral Fidelity: Directly tracks color propagation channel-by-channel across reflections and refractions without channel crosstalk.\n"
        "4. Zero Memory Overhead: Evaluates multi-bounce specular reflection and transparent refraction deterministically without requiring spatial k-d trees."
    )

    doc.add_page_break()

    # ==============================================================================
    # PAGE 2: 2D Diagrams & System Architecture
    # ==============================================================================
    add_h1("3. Forward Ray-Tracing System Architecture & 2D Diagrams")
    add_body(
        "To clearly visualize the forward ray-tracing pipeline across multiple spheres with distinct material and chromatic properties, "
        "the diagrams below illustrate the reversed geometric scene setup and the corresponding recursive forward ray tree."
    )

    fig1_path = os.path.join(fig_dir, "fig1_forward_scene.png")
    if os.path.exists(fig1_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(0)
        doc.add_picture(fig1_path, width=Inches(4.1))

    add_body(
        "Figure 1: Forward ray-tracing scene with multiple point lights (L1, L2), multiple spheres (S1: transparent, S2: reflective, "
        "S3: reflective, S4: diffuse), and direct eye-connection rays. Notice that secondary reflected (R1) and refracted (T1) rays "
        "propagate light forward, while surface-to-eye connection rays replace classical shadow rays. Occlusion is tested along the connection line.",
        bold_prefix="Figure 1 Description: ", space_after=2
    )

    fig2_path = os.path.join(fig_dir, "fig2_forward_tree.png")
    if os.path.exists(fig2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(0)
        p_img2.paragraph_format.space_after = Pt(0)
        doc.add_picture(fig2_path, width=Inches(3.3))

    add_body(
        "Figure 2: Forward Ray Interaction Tree (Dual of Lecture Slide 18). Rays originate at light source Li (Root). At transparent sphere S1, "
        "the ray bifurcates into transmitted ray T1 (striking S3 then S4) and reflected ray R1 (striking S2). At every visible hit node, "
        "a direct connection ray splats radiance directly to the Eye / Image Plane.",
        bold_prefix="Figure 2 Description: ", space_after=2
    )

    add_callout(
        "When sketching these 2D figures by hand on your A4 page:\n"
        "• Draw Light L1 (top-center) and Light L2 (top-right) emitting yellow/gold rays toward transparent sphere S1.\n"
        "• Color S1 light blue (Transparent), S2 slate grey (Reflective), S3 amber (Reflective), and S4 red (Diffuse/Opaque).\n"
        "• Draw S1 refracting light (cyan ray T1) toward S2, and reflecting light (amber ray R1) toward S3.\n"
        "• Draw Eye / Camera on the far right with a 1D/2D projection screen, and draw dashed purple connection lines from each hit point to Eye.\n"
        "• Draw the Forward Tree (Figure 2) branching downwards: Root Light -> S1 -> (Left: S3 -> S4, Right: S2), with dashed eye arrows at each node.",
        "Hand-Drawing Guide for 2D Figures:",
        space_after=0
    )

    doc.add_page_break()

    # ==============================================================================
    # PAGE 3: Mathematical Formulations & Geometric Derivations
    # ==============================================================================
    add_h1("4. Mathematical Formulations & Geometric Derivations")
    add_body(
        "The mathematical foundation directly implements the vector formulation taught in class (Slides 25–30, 45–46), "
        "extended to multi-sphere sorting, specular reflection, and Snell's refraction."
    )

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
        cell_l.paragraphs[0].add_run().add_picture(fig3_path, width=Inches(3.1))

        p_r = cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(0)
        cell_r.paragraphs[0].add_run().add_picture(fig4_path, width=Inches(3.1))

        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(2.5)
        r_c = p_cap.add_run("Figure 3: Analytical Ray-Sphere Geometry (Slide 45)      |      Figure 4: Reflection & Snell's Refraction (Slides 25–30)")
        r_c.font.size = Pt(8)
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

    doc.add_page_break()

    # ==============================================================================
    # PAGE 4: Full Multi-Channel RGB Color Illumination & Energy Transport
    # ==============================================================================
    add_h1("4.7 Full Multi-Channel RGB Color Illumination Model")
    add_body(
        "In physical rendering and standard ray tracing (Slides 20–25), illumination is evaluated across three independent "
        "color channels: Red, Green, and Blue (λ ∈ {R, G, B}). All radiant intensities and material reflectance properties are "
        "formulated as 3-component color vectors in the normalized RGB space [0, 1]³:"
    )

    add_h2("4.7.1 Tri-stimulus RGB Color Vectors & Material Definitions")
    add_bullet("Light Source Emission Color:  I_{p,i} = [I_{p,i}^R, I_{p,i}^G, I_{p,i}^B]^T  for each point light i = 1 to n.")
    add_bullet("Scene Ambient Illumination:   I_a = [I_a^R, I_a^G, I_a^B]^T  (uniform background environmental lighting).")
    add_bullet("Sphere Material Color Coefficients (Sphere k):")
    add_body(
        "    • Ambient Reflectance:    k_a = [k_a^R, k_a^G, k_a^B]^T  (response to ambient lighting)\n"
        "    • Diffuse Body Color:     k_d = [k_d^R, k_d^G, k_d^B]^T  (Lambertian intrinsic color, e.g. red sphere = [0.85, 0.1, 0.1])\n"
        "    • Specular Highlight:     k_s = [k_s^R, k_s^G, k_s^B]^T  (achromatic [k_s, k_s, k_s] for plastics; tinted for metals)\n"
        "    • Specular Exponent:      m (shininess power, controlling highlight tightness, typically m ∈ [10, 150])\n"
        "    • Mirror Reflection Tint: k_r = [k_r^R, k_r^G, k_r^B]^T  (specular reflection attenuation per bounce)\n"
        "    • Transmission Tint:      k_t = [k_t^R, k_t^G, k_t^B]^T  (transparency filter color; e.g. cyan glass = [0.1, 0.9, 0.95])",
        space_after=2
    )

    add_h2("4.7.2 Vector Phong Color Illumination Equation (Slide 22 Dual)")
    add_body(
        "At surface hit point P with outward normal N and view direction V, the local reflected RGB color vector is computed using "
        "the component-wise (Hadamard / Schur) product ⊙ across all visible light sources:\n"
        "    C_local(P) = I_a ⊙ k_a + Σ_{i=1}^n S_i · I_{p,i} ⊙ [ k_d · max(0, N · L_i) + k_s · max(0, R_i · V)^m ]\n"
        "where S_i ∈ {0, 1} is the binary visibility factor (tested via occlusion against intervening spheres), and:\n"
        "    L_i = (pos(L_i) - P) / ||pos(L_i) - P||,     R_i = 2(N · L_i)N - L_i.\n"
        "Scalar Form per Color Channel (λ ∈ {R, G, B}):\n"
        "    C_{local,λ}(P) = I_{a,λ} · k_{a,λ} + Σ_{i=1}^n S_i · I_{p,i,λ} [ k_{d,λ}(N · L_i) + k_{s,λ}(R_i · V)^m ]"
    )

    add_h2("4.8 Recursive Color Accumulation & Forward Splatting (Whitted Dual)")
    add_body(
        "Total Recursive RGB Color at Hit Point P (Slide 23 Dual):\n"
        "    C_total(P) = C_local(P) + k_r ⊙ C_refl + k_t ⊙ C_trans\n"
        "    Per Channel: C_{total,λ}(P) = C_{local,λ}(P) + k_{r,λ}·C_{refl,λ} + k_{t,λ}·C_{trans,λ},   ∀ λ ∈ {R, G, B}\n"
        "    • Total Internal Reflection (TIR): If cos² θ2 < 0, all transmitted energy reflects: C_total = C_local + (k_r + k_t) ⊙ C_refl.\n"
        "Forward Ray Energy Transport & Splatting Pipeline:\n"
        "    1. Emitted Ray Color Flux: Primary ray emitted from light L_i carries initial spectral flux Φ_ray = I_{p,i} · Δω_i.\n"
        "    2. Bounce Filtering: Reflected ray carries Φ_refl = Φ_ray ⊙ k_r; Transmitted ray carries Φ_trans = Φ_ray ⊙ k_t.\n"
        "    3. Beer-Lambert Absorption: For transparent spheres, light traveling path length d inside the medium is attenuated by "
        "absorption coefficient vector α: k_t(d) = exp(-α · d), naturally modeling colored glass saturation.\n"
        "    4. Eye Splatting: At visible point P, energy scattered toward Eye E is: C_splat = Φ_ray ⊙ [k_d(N·(-d)) + k_s(r·V)^m].\n"
        "    5. Subpixel Bilinear Accumulation: Point P projects to subpixel (p_x, p_y); C_splat is accumulated into ColorBuffer[W][H][3] "
        "and normalized by continuous WeightBuffer[W][H].\n"
        "    6. Final Compositing & Gamma Correction: C_pixel = I_a ⊙ k_a + ColorBuffer / WeightBuffer; C_final = clamp(C_pixel^(1/2.2), 0, 1)."
    )

    add_h2("4.9 Optical Dispersion & Chromatic Aberration (Cauchy's Equation)")
    add_body(
        "A major physical advantage of forward ray tracing is the natural simulation of chromatic dispersion (prism rainbow caustics). "
        "The refractive index of dielectric glass varies with wavelength λ according to Cauchy's empirical formula:\n"
        "    η(λ) = A + B / λ²     ==>     η_Red < η_Green < η_Blue   (since λ_R ≈ 700 nm > λ_G ≈ 546 nm > λ_B ≈ 436 nm)\n"
        "When a white light ray (Φ = [1, 1, 1]) strikes a transparent sphere, it automatically bifurcates into three separate spectral rays "
        "with refraction angles θ_{2,R} > θ_{2,G} > θ_{2,B}, rendering realistic physical rainbow caustics without extra post-processing."
    )

    doc.add_page_break()

    # ==============================================================================
    # PAGE 5: Pseudo-Algorithm & Findings
    # ==============================================================================
    add_h1("5. Concise Pseudo-Algorithm with Full RGB Color (Step-by-Step Text Form)")
    add_body(
        "Below is the complete, concise forward ray-tracing algorithm incorporating full RGB color computation, "
        "designed to be handwritten clearly on your final A4 submission page:"
    )

    steps = [
        ("Step 1: Scene & Color Property Initialization — ",
         "Define M spheres {S1, ..., SM} with centers c_k, radii R_k, and RGB material coefficients: ambient k_a, diffuse k_d, specular k_s, "
         "mirror reflection k_r, transmission filter k_t, shininess m, and refractive indices η_k (or η(λ)). "
         "Define n point lights with positions pos(L_i) and RGB emission colors I_{p,i}. Set ambient color I_a and background C_bg. "
         "Allocate RGB image color buffer ColorBuffer[W][H][3] and WeightBuffer[W][H]. For each light i, compute bounding solid angle cones."),

        ("Step 2: Targeted Primary Emission with Spectral Energy — ",
         "For each light i, sample unit ray directions d restricted strictly within the solid angle bounding cones. Set primary ray origin s = pos(L_i), "
         "initial ray RGB color flux Φ_ray = I_{p,i} · Δω_i, and recursion depth = 0."),

        ("Step 3: Multi-Sphere Quadratic Intersection — ",
         "For current ray (s, d), test intersection against every sphere k = 1 to M. Compute A = ||d||² = 1, B = 2(s - c_k)·d, and "
         "C = ||s - c_k||² - R_k². Evaluate discriminant Δ_k = B² - 4C."),

        ("Step 4: Discriminant & Nearest-Hit Selection — ",
         "If Δ_k < 0, discard sphere k. If Δ_k ≥ 0, compute roots t0, t1. Find global nearest valid hit: t* = min_k {t > ε}. "
         "If no sphere intersects with t > ε, ray escapes into background; terminate trace."),

        ("Step 5: Surface Differential Geometry — ",
         "Compute 3D hit point P = s + t*·d, surface outward unit normal N = (P - c)/R (reverse N = -N if ray hits from inside a transparent sphere), "
         "and unit view vector toward eye V = (E - P) / ||E - P||."),

        ("Step 6: Direct Eye Connection & RGB Color Splatting (Inverted Shadow Ray) — ",
         "If N · V > 0 (or if surface is transparent): Cast connection ray r_eye(τ) = P + τ·V toward Eye E. "
         "Test quadratic intersection of r_eye against all other spheres Sj (j ≠ hit). "
         "If unoccluded for all τ in (ε, ||E - P||), compute scattered RGB color C_splat = Φ_ray ⊙ [k_d max(0, N·(-d)) + k_s max(0, r·V)^m]. "
         "Project P through camera pinhole to pixel (x, y) and splat C_splat into ColorBuffer with bilinear weighting."),

        ("Step 7: Specular Reflection Ray Spawning — ",
         "If sphere is reflective (||k_r|| > 0) and depth < MAX_DEPTH: Compute reflection direction r = d - 2(d · N) N. "
         "Filter ray color flux: Φ_refl = Φ_ray ⊙ k_r. Spawn secondary ray with origin P + ε·r, direction r, and flux Φ_refl; recurse to Step 3."),

        ("Step 8: Transparent Refraction Ray Spawning (Snell's Law & Dispersion) — ",
         "If sphere is transparent (||k_t|| > 0) and depth < MAX_DEPTH: Compute cos² θ2 = 1 - η²(1 - (d · N)²). "
         "If cos² θ2 < 0 (TIR), redirect all energy along r with flux Φ_ray ⊙ (k_r + k_t). "
         "Otherwise, compute transmission direction t = η·d + (η(d·N) - √(cos² θ2))N and filter color flux Φ_trans = Φ_ray ⊙ k_t. "
         "(Optionally split into λ ∈ {R, G, B} for chromatic dispersion). Spawn transmitted ray from P + ε·t along t; recurse to Step 3."),

        ("Step 9: Radiance Blending & Multi-Light Composition — ",
         "Synthesize total color across the ray tree: C(P) = C_local + k_r ⊙ C_refl + k_t ⊙ C_trans. "
         "Direct photon connections and secondary scattered radiance deposit energy additively into the image accumulation buffer."),

        ("Step 10: Buffer Normalization, Ambient Addition & Gamma Correction — ",
         "Repeat Steps 2–9 for all sampled rays across all n lights. For every pixel (x, y), compute final linear color: "
         "C_linear = I_a ⊙ k_a + ColorBuffer(x, y) / max(ε, WeightBuffer(x, y)). "
         "Apply display gamma correction: C_final(x, y) = clamp((C_linear)^(1/2.2), 0, 1), producing the final rendered RGB image.")
    ]

    for prefix, body in steps:
        add_bullet(body, prefix, space_after=2.0)

    add_h1("6. Key Findings and Analytical Comments (Point Form)")
    findings = [
        ("Targeted Emission Efficiency: ", "Restricting emitted light rays to the solid angle cones subtended by spheres converts a near-zero naive hit probability (P ≈ 0) into 100% ray-surface engagement, making forward ray tracing practical."),
        ("Exact Dual of Lecture Setup: ", "Forward ray tracing directly inverts the classical slide workflow: lights act as primary ray emitters, while eye connection rays replace shadow rays, demonstrating algorithmic duality."),
        ("Multi-Channel RGB Spectral Fidelity: ", "Operating component-wise with Hadamard products (⊙) across R, G, and B channels faithfully models physical wavelength filtering through colored transparent glass and metallic specular reflections without non-physical channel crosstalk."),
        ("O(1) Intersection with Early Rejection: ", "The closed-form quadratic equation resolves ray-sphere intersections in constant O(1) time per sphere. The discriminant check (Δ < 0) provides early rejection before computing square roots."),
        ("Multi-Object Shadowing: ", "Unlike a single-sphere scene (where self-shadowing is impossible on a convex hull), a multi-sphere scene requires testing the eye-connection ray against all other spheres to correctly render cast shadows and mutual occlusions."),
        ("Natural Chromatic Dispersion & Caustics: ", "Because rays originate at the light, forward ray tracing naturally handles wavelength-dependent refraction η(λ) via Cauchy's dispersion equation, splitting white light rays into rainbow caustics with zero extra gathering overhead.")
    ]

    for prefix, text in findings:
        add_bullet(text, prefix, space_after=2.0)

    # Save document
    out_docx = r"c:\Users\HP\OneDrive\Desktop\Graphics Nihal\Assignment\Forward_Ray_Tracing_MultiSphere_Assignment.docx"
    doc.save(out_docx)
    print(f"Document successfully created at: {out_docx}")

if __name__ == "__main__":
    create_document()
