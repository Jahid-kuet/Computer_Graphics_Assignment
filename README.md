# Forward (Light-Based) Ray Tracing for Multiple Spheres

An assignment solution and implementation framework exploring **Forward (Light-Based) Ray Tracing** with multiple point lights, full RGB color shading, ray–sphere intersection geometry, recursive specular reflection, and Snell's Law refraction.

---

## 1. Overview & Problem Statement

Classical ray tracing (Whitted-style) covered in standard computer graphics curricula traces primary rays backward from the camera/eye through pixel samples on the view plane into the scene, subsequently casting shadow rays to light sources.

In this assignment, the causality is inverted:
* Primary rays originate at each **point light source** ($L_1, L_2, \dots, L_n$).
* Light rays propagate forward into a 3D scene populated with spheres of varied material properties (diffuse, specular, reflective, and refractive/dielectric).
* Upon surface intersection, local Phong illumination is evaluated, recursive reflection and refraction rays are spawned, and **camera-connection rays** link hit points back to the eye to accumulate RGB radiance onto the image plane.

---

## 2. Comparative Algorithm Analysis

Three forward-tracing paradigms were evaluated to address the low efficiency of naive light emission:

| Approach | Description | Primary Limitation / Decision |
| :--- | :--- | :--- |
| **Option A: Naive Random Forward Tracing** | Emits rays uniformly in all $4\pi$ steradians from each light. | **Rejected**: Probability of randomly hitting a pinhole camera aperture is near zero; causes extreme sample waste and noise. |
| **Option B: Photon Mapping (Two-Pass)** | Emits photon rays into a spatial data structure (k-d tree), followed by backward camera gather. | **Rejected**: Heavy auxiliary data structure and density estimation overhead for an analytic multi-sphere scene. |
| **Option C: Targeted Forward Tracing with Direct Eye Connection** | Constrains emission to solid angles subtended by scene spheres, solves closed-form intersections, shades locally, spawns recursive rays, and casts direct connection rays to the eye. | **Selected**: Highly efficient, achieves 100% ray-object engagement, leverages exact analytic intersections, and cleanly mirrors classical backward ray tracing. |

---

## 3. Mathematical Formulation

### 3.1 Ray Formulation & Ray–Sphere Intersection
A forward ray with origin $\mathbf{s}$ and unit direction $\mathbf{d}$ ($|\mathbf{d}| = 1$) is defined as:
$$\mathbf{u}(t) = \mathbf{s} + t\mathbf{d}, \quad t > 0$$

For a sphere centered at $\mathbf{c}$ with radius $R$, substituting the ray equation yields the quadratic equation $At^2 + Bt + C = 0$:
* $A = |\mathbf{d}|^2 = 1$
* $B = 2(\mathbf{s} - \mathbf{c}) \cdot \mathbf{d}$
* $C = |\mathbf{s} - \mathbf{c}|^2 - R^2$

The discriminant $\Delta = B^2 - 4C$ determines intersection:
* $\Delta < 0$: Ray misses the sphere.
* $\Delta = 0$: Ray is tangent to the sphere.
* $\Delta > 0$: Two intersections at $t = \frac{-B \pm \sqrt{\Delta}}{2}$. The valid hit is the smallest positive root $t = \min(t_0, t_1) > 0$.

Hit point and surface normal:
$$\mathbf{P} = \mathbf{s} + t\mathbf{d}, \qquad \mathbf{N} = \frac{\mathbf{P} - \mathbf{c}}{R}$$

### 3.2 Eye Connection & Visibility
* The connection vector to the camera eye $\mathbf{E}$ is $\mathbf{V} = \frac{\mathbf{E} - \mathbf{P}}{\|\mathbf{E} - \mathbf{P}\|}$.
* **Back-face culling**: If $\mathbf{N} \cdot \mathbf{V} \le 0$, the surface faces away from the camera and is discarded.
* **Occlusion testing**: A visibility ray is cast along $\mathbf{V}$ towards $\mathbf{E}$; if intersected by any intervening opaque sphere, the contribution is shadowed.

### 3.3 Phong Illumination Model
At visible hit point $\mathbf{P}$:
$$\mathbf{I} = \mathbf{I}_a \mathbf{k}_a + \sum_{i=1}^{n} \mathbf{I}_{p,i} \left[ \mathbf{k}_d (\mathbf{L}_i \cdot \mathbf{N}) + \mathbf{k}_s (\mathbf{R}_i \cdot \mathbf{V})^k \right]$$
where $\mathbf{L}_i$ is the light direction vector and $\mathbf{R}_i = 2(\mathbf{N} \cdot \mathbf{L}_i)\mathbf{N} - \mathbf{L}_i$ is the mirror reflection direction.

### 3.4 Recursive Reflection & Refraction
* **Specular Reflection**:
  $$\mathbf{d}_{\text{refl}} = \mathbf{d} - 2(\mathbf{d} \cdot \mathbf{N})\mathbf{N}$$
* **Snell's Law Refraction**:
  $$\cos\theta_1 = -\mathbf{N} \cdot \mathbf{d}, \quad \eta = \frac{\eta_1}{\eta_2}$$
  $$\mathbf{d}_{\text{refr}} = \eta \mathbf{d} + \left(\eta \cos\theta_1 - \sqrt{1 - \eta^2(1 - \cos^2\theta_1)}\right) \mathbf{N}$$
  *(Subject to Total Internal Reflection check when $1 - \eta^2(1 - \cos^2\theta_1) < 0$)*.

---

## 4. Repository Structure

```text
Assignment/
├── Copy of L10 Ray-tracingv2.pptx.pdf       # Lecture 10 reference slide notes
├── Forward_Ray_Tracing_Assignment_Solution.docx  # Formatted assignment document
├── Forward_Ray_Tracing_MultiSphere_Assignment.docx # Multi-sphere assignment docx
├── create_solution_docx.py                 # Script generating styled Word document
├── make_all_figures.py                     # Generates all diagrams (Figures 1-4)
├── make_fig1.py                            # Standalone figure 1 generator
├── make_perfect_figures.py                 # High-resolution figure refinement script
├── render_clean_fig1.py                    # Clean rendering script for Figure 1
├── render_clean_fig2_3.py                  # Clean rendering script for Figures 2 & 3
├── inspect_runs.py                         # Inspection tool for Word document XML runs
├── trial02_dump.txt                        # Working notes and raw algorithm dump
├── figures/                                # Exported publication-ready diagrams
│   ├── fig1_forward_scene.png              # Multi-sphere forward tracing scene
│   ├── fig2_forward_tree.png               # Forward ray-tracing recursion tree
│   ├── fig3_raysphere_geom.png             # Ray-sphere geometric vectors
│   └── fig4_snell_reflection.png           # Reflection and Snell's law refraction
└── extracted_img/                          # Extracted presentation reference assets
```

---

## 5. Setup & Usage

### Prerequisites
* Python 3.8+
* `matplotlib`, `numpy`, `python-docx`

Install dependencies:
```bash
pip install matplotlib numpy python-docx
```

### Generating Figures
To regenerate the high-resolution vector diagrams in `figures/`:
```bash
python make_all_figures.py
```
Or run the refined scripts:
```bash
python render_clean_fig1.py
python render_clean_fig2_3.py
```

### Generating the Assignment Report Document
To compile and assemble the final styled Word report:
```bash
python create_solution_docx.py
```
The output file will be written to `Forward_Ray_Tracing_MultiSphere_Assignment.docx`.
