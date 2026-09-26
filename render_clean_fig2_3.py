import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

fig_dir = r'c:\Users\HP\OneDrive\Desktop\Graphics Nihal\Assignment\figures'
os.makedirs(fig_dir, exist_ok=True)

plt.rcParams['font.family'] = 'DejaVu Sans'

# ==============================================================================
# FIGURE 2: Forward Ray-Tracing Tree (Light Tree)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=300)
ax.set_facecolor('#ffffff')

# Root: Light Source L
ax.scatter(5.2, 5.4, s=700, color='#f59e0b', edgecolors='#b45309', lw=2.5, zorder=5)
ax.text(5.2, 5.4, 'Light\n' + r'$L_i$', color='#ffffff', weight='bold', ha='center', va='center', fontsize=11.5, zorder=6)

# Child 1: Hit S1
ax.annotate('', xy=(5.2, 4.2), xytext=(5.2, 4.95), arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.5, mutation_scale=16))
ax.text(5.4, 4.6, 'Primary Ray', color='#ea580c', weight='bold', fontsize=10)

ax.scatter(5.2, 3.7, s=1000, color='#e0f2fe', edgecolors='#0284c7', lw=2.5, zorder=5)
ax.text(5.2, 3.7, r'$S_1$' + '\n(Hit ' + r'$P_1$)', color='#0369a1', weight='bold', ha='center', va='center', fontsize=11, zorder=6)

# Splat to Eye from S1
ax.annotate('', xy=(1.5, 3.7), xytext=(4.1, 3.7), arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=2.2, ls='--', mutation_scale=15))
ax.text(2.6, 3.9, r'Eye Splat (to Pixel)', color='#2563eb', weight='bold', fontsize=9.5)

# Branches from S1:
# Left: Reflection R1 to S3
ax.annotate('', xy=(2.8, 2.3), xytext=(4.4, 3.3), arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=2.2, mutation_scale=15))
ax.text(3.1, 2.95, r'Reflection $R_1$', color='#d97706', weight='bold', fontsize=10)

ax.scatter(2.8, 1.8, s=950, color='#fef3c7', edgecolors='#d97706', lw=2.5, zorder=5)
ax.text(2.8, 1.8, r'$S_3$' + '\n(Hit ' + r'$P_3$)', color='#b45309', weight='bold', ha='center', va='center', fontsize=10.5, zorder=6)

# Eye Splat from S3
ax.annotate('', xy=(0.5, 1.8), xytext=(1.8, 1.8), arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=2.0, ls='--', mutation_scale=14))
ax.text(0.8, 2.0, r'Eye Splat', color='#2563eb', weight='bold', fontsize=9)

# From S3 to S4: Reflection R3
ax.annotate('', xy=(2.8, 0.95), xytext=(2.8, 1.3), arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=2.0, mutation_scale=14))
ax.text(3.0, 1.15, r'Reflection $R_3$', color='#d97706', weight='bold', fontsize=9.5)

ax.scatter(2.8, 0.5, s=900, color='#fee2e2', edgecolors='#dc2626', lw=2.5, zorder=5)
ax.text(2.8, 0.5, r'$S_4$' + '\n(Hit ' + r'$P_4$)', color='#b91c1c', weight='bold', ha='center', va='center', fontsize=10, zorder=6)

# Right: Transmission T1 from S1 to S2
ax.annotate('', xy=(7.4, 2.3), xytext=(5.9, 3.3), arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=2.2, mutation_scale=15))
ax.text(6.7, 2.95, r'Transmission $T_1$', color='#0284c7', weight='bold', fontsize=10)

ax.scatter(7.4, 1.8, s=950, color='#f1f5f9', edgecolors='#475569', lw=2.5, zorder=5)
ax.text(7.4, 1.8, r'$S_2$' + '\n(Hit ' + r'$P_2$)', color='#334155', weight='bold', ha='center', va='center', fontsize=10.5, zorder=6)

# Eye Splat from S2
ax.annotate('', xy=(9.6, 1.8), xytext=(8.3, 1.8), arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=2.0, ls='--', mutation_scale=14))
ax.text(8.5, 2.0, r'Eye Splat', color='#2563eb', weight='bold', fontsize=9)

# From S2: Reflection R2
ax.annotate('', xy=(7.4, 0.95), xytext=(7.4, 1.3), arrowprops=dict(arrowstyle="-|>", color='#475569', lw=2.0, mutation_scale=14))
ax.text(7.6, 1.15, r'Reflection $R_2$', color='#475569', weight='bold', fontsize=9.5)
ax.text(7.4, 0.5, '[Escapes Scene]', color='#64748b', style='italic', ha='center', fontsize=9.5)

ax.set_xlim(0, 10.8)
ax.set_ylim(-0.1, 6.2)
ax.axis('off')

plt.title("Figure 2: Forward Ray-Tracing Tree (Light Tree)\n" +
          r"(Inverted from Slide 18: Light Source at Root $\rightarrow$ Branching via Reflection & Transmission $\rightarrow$ Eye Splat at Nodes)",
          fontsize=12, weight='bold', pad=15)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig2_forward_tree.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Figure 2 re-rendered cleanly.")

# ==============================================================================
# FIGURE 3: Ray-Sphere Analytical Intersection Geometry (Exact Slide 45 Notation)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.5, 7.2), dpi=300)
ax.set_facecolor('#ffffff')

# Coordinate axes (Slide 45)
orig_axes = (1.0, 1.0)
ax.annotate('', xy=(1.0, 5.5), xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.8))
ax.text(0.85, 5.6, 'y', color='#475569', weight='bold', fontsize=12)
ax.annotate('', xy=(6.0, 1.0), xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.8))
ax.text(6.1, 0.95, 'x', color='#475569', weight='bold', fontsize=12)
ax.annotate('', xy=(0.2, 0.2), xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.8))
ax.text(0.1, 0.05, 'z', color='#475569', weight='bold', fontsize=12)

# Sphere center c and circle (Sphere placed at lower-right relative to hit point!)
c = (7.5, 3.2)
R = 2.2
circle = plt.Circle(c, R, color='#fef2f2', ec='#ef4444', lw=2.5, zorder=2)
ax.add_patch(circle)
ax.scatter(c[0], c[1], s=90, color='#991b1b', zorder=5)
ax.text(c[0] + 0.3, c[1] - 0.3, r'Center $\mathbf{c} = (x_c, y_c, z_c)$', fontsize=11, weight='bold', color='#991b1b',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#ef4444', lw=1))

# Ray origin s (Light)
s = (2.0, 3.0)
ax.scatter(s[0], s[1], s=90, color='#ea580c', zorder=5)
ax.text(s[0] - 0.2, s[1] - 0.45, r'Origin $\mathbf{s}$ (Light)', fontsize=11, weight='bold', color='#ea580c')

# Vector s from world origin
ax.annotate('', xy=s, xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=1.8, ls=':'), zorder=3)
ax.text(1.3, 2.2, r'$\mathbf{s}$', color='#ea580c', weight='bold', fontsize=11)

# Vector c from world origin
ax.annotate('', xy=c, xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#991b1b', lw=1.8, ls=':'), zorder=3)
ax.text(4.2, 1.8, r'$\mathbf{c}$', color='#991b1b', weight='bold', fontsize=11)

# Ray direction d (aimed at top of sphere)
d = np.array([0.94, 0.34])
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
d_start = s_vec + 0.6 * d
ax.annotate('', xy=d_start + 0.9*d, xytext=d_start, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.8, mutation_scale=15), zorder=5)
ax.text(d_start[0] + 0.1, d_start[1] + 0.35, r'Direction $\mathbf{d}$ ($|\mathbf{d}|=1$)', fontsize=10.5, weight='bold', color='#ea580c')

# Hit point P
ax.scatter(p_hit0[0], p_hit0[1], s=100, color='#ffffff', edgecolors='#0284c7', lw=2.5, zorder=6)
ax.text(p_hit0[0] + 0.15, p_hit0[1] + 0.45, r'Hit Point $\mathbf{P} = \mathbf{s} + t_0\mathbf{d}$', fontsize=11, weight='bold', color='#0284c7',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#0284c7', lw=1))

# Vector p from world origin to P
ax.annotate('', xy=p_hit0, xytext=orig_axes, arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=1.8, ls=':'), zorder=3)
ax.text(3.1, 2.5, r'$\mathbf{p}$', color='#0284c7', weight='bold', fontsize=11)

# Far root t1
ax.scatter(p_hit1[0], p_hit1[1], s=70, color='#ffffff', edgecolors='#64748b', lw=2, zorder=6)
ax.text(p_hit1[0] + 0.25, p_hit1[1] + 0.15, r'$t_1$ (Far Root)', fontsize=9.5, color='#64748b')

# Outward Normal N at P: N = (P - c) / R (Points UP and LEFT!)
normal = (p_hit0 - c_vec) / R
n_end = p_hit0 + 1.6 * normal
ax.annotate('', xy=n_end, xytext=p_hit0, arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=2.8, mutation_scale=16), zorder=6)
ax.text(n_end[0] - 1.5, n_end[1] + 0.3, r'Normal $\mathbf{N} = \frac{\mathbf{P} - \mathbf{c}}{R}$', fontsize=11.5, weight='bold', color='#0284c7',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#0284c7', lw=1))

# Radius R line from c to hit point P
ax.plot([c[0], p_hit0[0]], [c[1], p_hit0[1]], color='#94a3b8', lw=2.0, ls='--', zorder=4)
mid_r = (c_vec + p_hit0) / 2
ax.text(mid_r[0] + 0.2, mid_r[1] - 0.2, r'Radius $R$', fontsize=11, color='#475569', weight='bold')

# Distance t label along ray segment
ax.text(3.2, 3.0, r'Valid root: $t = t_0 = \min(t_0, t_1) > 0$', fontsize=10.5, weight='bold', color='#1e293b', rotation=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f8fafc', edgecolor='#cbd5e1', lw=1))

ax.set_xlim(-0.1, 10.8)
ax.set_ylim(-0.1, 6.8)
ax.set_aspect('equal')
ax.axis('off')

plt.title("Figure 3: Ray-Sphere Analytical Intersection Geometry (Slide 45-46 Notation)\n" +
          r"Ray $\mathbf{u}(t) = \mathbf{s} + t\mathbf{d}$ intersects sphere $|\mathbf{p} - \mathbf{c}|^2 = R^2 \rightarrow At^2 + Bt + C = 0$",
          fontsize=11.5, weight='bold', pad=15)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig3_raysphere_geom.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Figure 3 re-rendered cleanly matching Slide 45.")
