import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

fig_dir = r'c:\Users\HP\OneDrive\Desktop\Graphics Nihal\Assignment\figures'
os.makedirs(fig_dir, exist_ok=True)

plt.rcParams['font.family'] = 'DejaVu Sans'

# ==============================================================================
# FIGURE 1: Multi-Sphere Forward Ray Tracing Scene (Slide 17/18 Reversed)
# ==============================================================================
fig, ax = plt.subplots(figsize=(11, 8.2), dpi=300)
ax.set_facecolor('#ffffff')

# Spheres
# S1: Transparent sphere at (5.2, 4.2), R=1.35
c_s1 = (5.2, 4.2)
r_s1 = 1.35
circle_s1 = plt.Circle(c_s1, r_s1, color='#e0f2fe', ec='#0284c7', lw=2.5, zorder=2)
ax.add_patch(circle_s1)
ax.text(5.2, 3.2, r'$S_1$ [Transparent]', color='#0369a1', weight='bold', ha='center', fontsize=11, zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#0284c7', lw=1, alpha=0.9))

# S2: Reflective sphere at (9.4, 3.2), R=1.15
c_s2 = (9.4, 3.2)
r_s2 = 1.15
circle_s2 = plt.Circle(c_s2, r_s2, color='#f1f5f9', ec='#475569', lw=2.5, zorder=2)
ax.add_patch(circle_s2)
ax.text(9.4, 2.2, r'$S_2$ [Reflective]', color='#334155', weight='bold', ha='center', fontsize=11, zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#475569', lw=1, alpha=0.9))

# S3: Reflective sphere at (3.5, 8.0), R=1.05
c_s3 = (3.5, 8.0)
r_s3 = 1.05
circle_s3 = plt.Circle(c_s3, r_s3, color='#fef3c7', ec='#d97706', lw=2.5, zorder=2)
ax.add_patch(circle_s3)
ax.text(3.5, 8.7, r'$S_3$ [Reflective]', color='#b45309', weight='bold', ha='center', fontsize=11, zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#d97706', lw=1, alpha=0.9))

# S4: Opaque / Diffuse sphere at (8.5, 8.5), R=0.95
c_s4 = (8.5, 8.5)
r_s4 = 0.95
circle_s4 = plt.Circle(c_s4, r_s4, color='#fee2e2', ec='#dc2626', lw=2.5, zorder=2)
ax.add_patch(circle_s4)
ax.text(8.5, 9.2, r'$S_4$ [Diffuse / Opaque]', color='#b91c1c', weight='bold', ha='center', fontsize=11, zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#dc2626', lw=1, alpha=0.9))

# Lights
l1 = (1.0, 9.5)
l2 = (10.2, 10.5)

def draw_light(pos, label):
    ax.scatter(pos[0], pos[1], s=350, color='#f59e0b', edgecolors='#b45309', lw=2.5, zorder=6)
    for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
        dx = 0.45 * np.cos(angle)
        dy = 0.45 * np.sin(angle)
        ax.plot([pos[0] + 0.2*np.cos(angle), pos[0] + dx], 
                [pos[1] + 0.2*np.sin(angle), pos[1] + dy], color='#f59e0b', lw=2.2, zorder=5)
    ax.text(pos[0], pos[1] + 0.65, label, fontsize=12, weight='bold', color='#b45309', ha='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#fffbeb', edgecolor='#f59e0b', lw=1))

draw_light(l1, r'Light $L_1$')
draw_light(l2, r'Light $L_2$')

# Eye / Camera & Screen
eye = (0.8, 1.2)
ax.scatter(eye[0], eye[1], s=250, color='#0f172a', zorder=6)
ax.text(eye[0], eye[1] - 0.6, 'Projection Reference\nPoint (Eye / Camera)', fontsize=10.5, weight='bold', color='#0f172a', ha='center')

# Image Plane (Screen)
screen_x = [1.8, 2.7]
screen_y = [2.9, 1.1]
ax.plot(screen_x, screen_y, color='#475569', lw=4, zorder=4)
ax.text(2.6, 2.3, 'Image Plane\n(Screen)', fontsize=9.5, color='#334155', weight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#94a3b8', lw=1))

# Ray Paths:
# 1. Primary Light ray from L1 to S1 (hit P1)
p1 = (4.1, 5.0) # hit on S1
ax.annotate('', xy=p1, xytext=l1, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.5, mutation_scale=16), zorder=5)
ax.text(1.9, 7.6, r'Primary Ray ($\mathbf{s}_1 + t\mathbf{d}_1$)', color='#ea580c', weight='bold', fontsize=10, rotation=-52,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

# Secondary Ray A: Reflected ray R1 from P1 to S3 (hit P3)
p3 = (3.6, 7.0) # hit on S3
ax.annotate('', xy=p3, xytext=p1, arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=2.2, mutation_scale=15), zorder=5)
ax.text(4.4, 6.0, r'Reflected Ray $R_1$', color='#d97706', weight='bold', fontsize=9.5, rotation=-75,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

# Secondary Ray A2: From P3 on S3 to S4 (hit P4)
p4 = (7.6, 8.5) # hit on S4
ax.annotate('', xy=p4, xytext=p3, arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=2.0, mutation_scale=14), zorder=5)
ax.text(5.3, 8.0, r'Reflected Ray $R_3$', color='#d97706', weight='bold', fontsize=9.5, rotation=18,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

# Secondary Ray B: Refracted/Transmitted ray T1 inside S1, exits at p1_exit towards S2 (hit P2)
p1_exit = (6.2, 3.6)
p2 = (8.3, 3.4)
ax.plot([p1[0], p1_exit[0]], [p1[1], p1_exit[1]], color='#0284c7', lw=2.2, ls='--', zorder=4)
ax.text(4.9, 4.3, r'Refraction $T_1$', color='#0284c7', weight='bold', fontsize=9.5,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))
ax.annotate('', xy=p2, xytext=p1_exit, arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=2.2, mutation_scale=15), zorder=5)
ax.text(6.8, 3.8, r'Transmitted Ray $T_1$', color='#0284c7', weight='bold', fontsize=9.5, rotation=-6,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

# At S2, reflected ray R2 bounces away
p_r2 = (10.3, 4.6)
ax.annotate('', xy=p_r2, xytext=p2, arrowprops=dict(arrowstyle="-|>", color='#475569', lw=1.8, mutation_scale=12), zorder=5)
ax.text(9.6, 4.3, r'$R_2$', color='#475569', weight='bold', fontsize=9)

# 2. Primary Light ray from L2 to S1 (hit P1_b)
p1_b = (6.2, 5.1)
ax.annotate('', xy=p1_b, xytext=l2, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.0, mutation_scale=15), zorder=5)
ax.text(8.2, 7.3, r'Primary Ray from $L_2$', color='#ea580c', weight='bold', fontsize=9.5, rotation=52,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

# Hit Points
for pt, lbl in [(p1, r'$P_1$'), (p2, r'$P_2$'), (p3, r'$P_3$'), (p4, r'$P_4$')]:
    ax.scatter(pt[0], pt[1], s=65, color='#ffffff', edgecolors='#0f172a', lw=2, zorder=7)
    ax.text(pt[0]+0.15, pt[1]+0.15, lbl, fontsize=11, weight='bold', color='#0f172a', zorder=8)

# Direct Connection Rays (Replacing Backward Primary/Shadow Rays!)
# From P1 to Eye (Direct Visibility)
ax.annotate('', xy=eye, xytext=p1, arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=2.2, ls='-', mutation_scale=15), zorder=4)
ax.text(1.7, 3.6, 'Eye Connection Ray\n(Direct Visibility)', color='#2563eb', weight='bold', fontsize=9.5, rotation=48,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

# From P2 to Eye (Tested for Occlusion by S1)
ax.annotate('', xy=eye, xytext=p2, arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=1.8, ls=':', mutation_scale=13), zorder=4)
ax.text(4.4, 1.8, 'Eye Connection Ray (Occlusion-Checked)', color='#2563eb', weight='bold', fontsize=9, rotation=17,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

# From P3 to Eye
ax.annotate('', xy=eye, xytext=p3, arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=1.8, ls=':', mutation_scale=13), zorder=4)

ax.set_xlim(-0.2, 11.2)
ax.set_ylim(-0.2, 11.8)
ax.set_aspect('equal')
ax.axis('off')

plt.title("Figure 1: Forward (Light-Based) Ray Tracing Scene for Multiple Spheres\n" +
          r"(Reversal of Slide 17/18: Light $\rightarrow$ Surface Hits $\rightarrow$ Reflection/Transmission $\rightarrow$ Direct Eye Connection)",
          fontsize=12, weight='bold', pad=15)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig1_forward_scene.png'), dpi=300, bbox_inches='tight')
plt.close()

# ==============================================================================
# FIGURE 2: Forward Ray-Tracing Tree (Light Tree)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 7.2), dpi=300)
ax.set_facecolor('#ffffff')

# Root: Light Source L
ax.scatter(5.0, 5.8, s=650, color='#f59e0b', edgecolors='#b45309', lw=2.5, zorder=5)
ax.text(5.0, 5.8, 'Light\n' + r'$L_i$', color='#ffffff', weight='bold', ha='center', va='center', fontsize=11.5, zorder=6)

# Child 1: Hit S1
ax.annotate('', xy=(5.0, 4.4), xytext=(5.0, 5.3), arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.5, mutation_scale=16))
ax.text(5.2, 4.85, 'Primary Ray', color='#ea580c', weight='bold', fontsize=10)

ax.scatter(5.0, 3.9, s=950, color='#e0f2fe', edgecolors='#0284c7', lw=2.5, zorder=5)
ax.text(5.0, 3.9, r'$S_1$' + '\n(Hit ' + r'$P_1$)', color='#0369a1', weight='bold', ha='center', va='center', fontsize=11, zorder=6)

# Splat to Eye from S1
ax.annotate('', xy=(1.5, 3.9), xytext=(4.1, 3.9), arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=2.2, ls='--', mutation_scale=15))
ax.text(2.6, 4.1, r'Eye Splat (to Pixel)', color='#2563eb', weight='bold', fontsize=9.5)

# Branches from S1:
# Left: Reflection R1 to S3
ax.annotate('', xy=(2.8, 2.4), xytext=(4.3, 3.5), arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=2.2, mutation_scale=15))
ax.text(3.1, 3.1, r'Reflection $R_1$', color='#d97706', weight='bold', fontsize=10)

ax.scatter(2.8, 2.0, s=900, color='#fef3c7', edgecolors='#d97706', lw=2.5, zorder=5)
ax.text(2.8, 2.0, r'$S_3$' + '\n(Hit ' + r'$P_3$)', color='#b45309', weight='bold', ha='center', va='center', fontsize=10.5, zorder=6)

# Eye Splat from S3
ax.annotate('', xy=(0.6, 2.0), xytext=(1.9, 2.0), arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=2.0, ls='--', mutation_scale=14))
ax.text(0.9, 2.2, r'Eye Splat', color='#2563eb', weight='bold', fontsize=9)

# From S3 to S4: Reflection R3
ax.annotate('', xy=(2.8, 0.9), xytext=(2.8, 1.4), arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=2.0, mutation_scale=14))
ax.text(3.0, 1.15, r'Reflection $R_3$', color='#d97706', weight='bold', fontsize=9.5)

ax.scatter(2.8, 0.5, s=850, color='#fee2e2', edgecolors='#dc2626', lw=2.5, zorder=5)
ax.text(2.8, 0.5, r'$S_4$' + '\n(Hit ' + r'$P_4$)', color='#b91c1c', weight='bold', ha='center', va='center', fontsize=10, zorder=6)

# Right: Transmission T1 from S1 to S2
ax.annotate('', xy=(7.2, 2.4), xytext=(5.7, 3.5), arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=2.2, mutation_scale=15))
ax.text(6.5, 3.1, r'Transmission $T_1$', color='#0284c7', weight='bold', fontsize=10)

ax.scatter(7.2, 2.0, s=900, color='#f1f5f9', edgecolors='#475569', lw=2.5, zorder=5)
ax.text(7.2, 2.0, r'$S_2$' + '\n(Hit ' + r'$P_2$)', color='#334155', weight='bold', ha='center', va='center', fontsize=10.5, zorder=6)

# Eye Splat from S2
ax.annotate('', xy=(9.4, 2.0), xytext=(8.1, 2.0), arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=2.0, ls='--', mutation_scale=14))
ax.text(8.2, 2.2, r'Eye Splat', color='#2563eb', weight='bold', fontsize=9)

# From S2: Reflection R2
ax.annotate('', xy=(7.2, 0.9), xytext=(7.2, 1.4), arrowprops=dict(arrowstyle="-|>", color='#475569', lw=2.0, mutation_scale=14))
ax.text(7.4, 1.15, r'Reflection $R_2$', color='#475569', weight='bold', fontsize=9.5)
ax.text(7.2, 0.5, '[Escapes Scene]', color='#64748b', style='italic', ha='center', fontsize=9.5)

ax.set_xlim(0, 10.5)
ax.set_ylim(-0.1, 6.8)
ax.axis('off')

plt.title("Figure 2: Forward Ray-Tracing Tree (Light Tree)\n" +
          r"(Inverted from Slide 18: Light Source at Root $\rightarrow$ Branching via Reflection & Transmission $\rightarrow$ Eye Splat at Nodes)",
          fontsize=12, weight='bold', pad=15)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig2_forward_tree.png'), dpi=300, bbox_inches='tight')
plt.close()

# ==============================================================================
# FIGURE 3: Ray-Sphere Analytical Intersection Geometry (Slide 45-46 Notation)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
ax.set_facecolor('#ffffff')

# Coordinate axes (like Slide 45!)
orig_axes = (1.0, 1.0)
ax.annotate('', xy=(1.0, 4.5), xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.8))
ax.text(0.85, 4.6, 'y', color='#475569', weight='bold', fontsize=12)
ax.annotate('', xy=(5.5, 1.0), xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.8))
ax.text(5.6, 0.95, 'x', color='#475569', weight='bold', fontsize=12)
ax.annotate('', xy=(0.2, 0.2), xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.8))
ax.text(0.1, 0.05, 'z', color='#475569', weight='bold', fontsize=12)

# Sphere center c and circle
c = (7.0, 3.8)
R = 2.0
circle = plt.Circle(c, R, color='#fef2f2', ec='#ef4444', lw=2.5, zorder=2)
ax.add_patch(circle)
ax.scatter(c[0], c[1], s=80, color='#991b1b', zorder=5)
ax.text(c[0] + 0.25, c[1] - 0.25, r'Center $\mathbf{c} = (x_c, y_c, z_c)$', fontsize=11, weight='bold', color='#991b1b',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#ef4444', lw=1))

# Ray origin s
s = (2.2, 2.5)
ax.scatter(s[0], s[1], s=85, color='#ea580c', zorder=5)
ax.text(s[0] - 0.2, s[1] + 0.35, r'Origin $\mathbf{s}$ (Light)', fontsize=11, weight='bold', color='#ea580c')

# Vector s from world origin (1.0, 1.0)
ax.annotate('', xy=s, xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=1.8, ls=':'), zorder=3)
ax.text(1.3, 1.9, r'$\mathbf{s}$', color='#ea580c', weight='bold', fontsize=11)

# Vector c from world origin
ax.annotate('', xy=c, xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#991b1b', lw=1.8, ls=':'), zorder=3)
ax.text(3.8, 2.2, r'$\mathbf{c}$', color='#991b1b', weight='bold', fontsize=11)

# Ray line calculation
# d direction
d = np.array([0.92, 0.39])
d = d / np.linalg.norm(d)
s_vec = np.array(s)
c_vec = np.array(c)
diff = s_vec - c_vec
B = 2 * np.dot(diff, d)
C_val = np.dot(diff, diff) - R**2
disc = B**2 - 4 * C_val
t0 = (-B - np.sqrt(disc)) / 2
t1 = (-B + np.sqrt(disc)) / 2

p_hit0 = s_vec + t0 * d
p_hit1 = s_vec + t1 * d

# Draw ray line
ray_end = s_vec + (t1 + 1.2) * d
ax.plot([s[0], ray_end[0]], [s[1], ray_end[1]], color='#1e293b', lw=2.2, zorder=3)
ax.annotate('', xy=ray_end, xytext=s_vec + (t1+0.5)*d, arrowprops=dict(arrowstyle="-|>", color='#1e293b', lw=2.2, mutation_scale=14), zorder=3)

# Ray direction vector d (arrow)
d_start = s_vec + 0.5 * d
ax.annotate('', xy=d_start + 0.9*d, xytext=d_start, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.8, mutation_scale=15), zorder=5)
ax.text(d_start[0] - 0.1, d_start[1] + 0.35, r'Direction $\mathbf{d}$ ($|\mathbf{d}|=1$)', fontsize=10.5, weight='bold', color='#ea580c')

# Hit point P
ax.scatter(p_hit0[0], p_hit0[1], s=95, color='#ffffff', edgecolors='#0284c7', lw=2.5, zorder=6)
ax.text(p_hit0[0] - 0.8, p_hit0[1] + 0.35, r'Hit Point $\mathbf{P} = \mathbf{s} + t_0\mathbf{d}$', fontsize=11, weight='bold', color='#0284c7',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#0284c7', lw=1))

# Vector p from world origin to P
ax.annotate('', xy=p_hit0, xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=1.8, ls=':'), zorder=3)
ax.text(2.6, 2.9, r'$\mathbf{p}$', color='#0284c7', weight='bold', fontsize=11)

# Far root t1
ax.scatter(p_hit1[0], p_hit1[1], s=65, color='#ffffff', edgecolors='#64748b', lw=2, zorder=6)
ax.text(p_hit1[0] + 0.2, p_hit1[1] + 0.2, r'$t_1$ (Far Root)', fontsize=9.5, color='#64748b')

# Outward Normal N at P
normal = (p_hit0 - c_vec) / R
n_end = p_hit0 + 1.4 * normal
ax.annotate('', xy=n_end, xytext=p_hit0, arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=2.5, mutation_scale=16), zorder=6)
ax.text(n_end[0] - 1.2, n_end[1] + 0.35, r'Normal $\mathbf{N} = \frac{\mathbf{P} - \mathbf{c}}{R}$', fontsize=11, weight='bold', color='#0284c7',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#0284c7', lw=1))

# Radius R line from c to hit point P
ax.plot([c[0], p_hit0[0]], [c[1], p_hit0[1]], color='#94a3b8', lw=2.0, ls='--', zorder=4)
mid_r = (c_vec + p_hit0) / 2
ax.text(mid_r[0] + 0.1, mid_r[1] - 0.28, r'Radius $R$', fontsize=10.5, color='#475569', weight='bold')

# Parameter t text
ax.text(3.3, 3.4, r'Valid root: $t = t_0 = \min(t_0, t_1) > 0$', fontsize=10.5, weight='bold', color='#1e293b', rotation=23,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f8fafc', edgecolor='#cbd5e1', lw=1))

ax.set_xlim(-0.1, 10.2)
ax.set_ylim(-0.1, 6.2)
ax.set_aspect('equal')
ax.axis('off')

plt.title("Figure 3: Ray-Sphere Analytical Intersection Geometry (Slide 45-46 Notation)\n" +
          r"Ray $\mathbf{u}(t) = \mathbf{s} + t\mathbf{d}$ intersects sphere $|\mathbf{p} - \mathbf{c}|^2 = R^2 \rightarrow At^2 + Bt + C = 0$",
          fontsize=11.5, weight='bold', pad=15)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig3_raysphere_geom.png'), dpi=300, bbox_inches='tight')
plt.close()

print("Figures 1, 2, 3 re-generated with perfect margins and callout boxes.")
