import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs(r'c:\Users\HP\OneDrive\Desktop\Graphics Nihal\Assignment\figures', exist_ok=True)
fig_dir = r'c:\Users\HP\OneDrive\Desktop\Graphics Nihal\Assignment\figures'

# Set high DPI and aesthetic styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# ==========================================
# FIGURE 1: Multi-Sphere Forward Ray Tracing Scene
# ==========================================
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
ax.set_facecolor('#ffffff')

# Draw Spheres
# S1: Transparent sphere at (5, 4.5), R=1.2
circle_s1 = plt.Circle((5.0, 4.5), 1.2, color='#e0f2fe', ec='#0284c7', lw=2, zorder=2)
ax.add_patch(circle_s1)
ax.text(5.0, 4.5, r'$S_1$ (Transparent)', color='#0369a1', weight='bold', ha='center', va='center', fontsize=11, zorder=4)

# S2: Reflective sphere at (8.5, 3.2), R=1.0
circle_s2 = plt.Circle((8.5, 3.2), 1.0, color='#f1f5f9', ec='#475569', lw=2, zorder=2)
ax.add_patch(circle_s2)
ax.text(8.5, 3.2, r'$S_2$ (Reflective)', color='#334155', weight='bold', ha='center', va='center', fontsize=11, zorder=4)

# S3: Reflective/Opaque sphere at (5.2, 7.8), R=0.9
circle_s3 = plt.Circle((5.2, 7.8), 0.9, color='#fef3c7', ec='#d97706', lw=2, zorder=2)
ax.add_patch(circle_s3)
ax.text(5.2, 7.8, r'$S_3$ (Reflective)', color='#b45309', weight='bold', ha='center', va='center', fontsize=11, zorder=4)

# S4: Diffuse sphere at (8.2, 8.2), R=0.8
circle_s4 = plt.Circle((8.2, 8.2), 0.8, color='#fee2e2', ec='#dc2626', lw=2, zorder=2)
ax.add_patch(circle_s4)
ax.text(8.2, 8.2, r'$S_4$ (Diffuse)', color='#b91c1c', weight='bold', ha='center', va='center', fontsize=11, zorder=4)

# Light Sources
l1 = (2.2, 8.5)
l2 = (9.5, 9.8)

def draw_light(pos, label):
    ax.scatter(pos[0], pos[1], s=250, color='#f59e0b', edgecolors='#b45309', lw=2, zorder=5)
    for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
        dx = 0.35 * np.cos(angle)
        dy = 0.35 * np.sin(angle)
        ax.plot([pos[0] + 0.18*np.cos(angle), pos[0] + dx], 
                [pos[1] + 0.18*np.sin(angle), pos[1] + dy], color='#f59e0b', lw=1.8, zorder=4)
    ax.text(pos[0], pos[1] + 0.45, label, fontsize=12, weight='bold', color='#b45309', ha='center')

draw_light(l1, r'Light $L_1$')
draw_light(l2, r'Light $L_2$')

# Eye / Camera & Screen
eye = (1.0, 1.2)
ax.scatter(eye[0], eye[1], s=180, color='#0f172a', zorder=5)
ax.text(eye[0] - 0.2, eye[1] - 0.4, 'Projection Reference\nPoint (Eye / Camera)', fontsize=10, weight='bold', color='#0f172a', ha='center')

# Screen / Projection Plane
screen_x = [2.0, 2.8]
screen_y = [2.8, 1.0]
ax.plot(screen_x, screen_y, color='#64748b', lw=3.5, zorder=3)
ax.text(2.6, 2.3, 'Image Plane\n(Screen)', fontsize=9, color='#475569', weight='bold')

# Forward Ray Paths
# 1. Primary Light ray from L1 to S1 hit point P1
p1 = (4.0, 5.2) # Hit on S1
ax.annotate('', xy=p1, xytext=l1, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.2, mutation_scale=15), zorder=4)
ax.text(2.8, 7.1, 'Primary Light Ray', color='#ea580c', weight='bold', fontsize=9.5, rotation=-45)

# Secondary rays at P1:
# A. Reflected ray R1 towards S3
p3 = (4.6, 7.2) # Hit on S3
ax.annotate('', xy=p3, xytext=p1, arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=2, mutation_scale=14), zorder=4)
ax.text(4.0, 6.2, r'Reflected Ray $R_1$', color='#d97706', weight='bold', fontsize=9, rotation=70)

# From S3, reflected ray R3 to S4
p4 = (7.5, 8.4)
ax.annotate('', xy=p4, xytext=p3, arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=1.8, mutation_scale=12), zorder=4)
ax.text(5.8, 8.1, r'Reflected Ray $R_3$', color='#d97706', weight='bold', fontsize=8.5)

# B. Transmitted/Refracted ray T1 through S1 to S2
# Ray enters at p1, refracts to p1_exit, then to p2 on S2
p1_exit = (5.9, 4.0)
p2 = (7.6, 3.6)
ax.plot([p1[0], p1_exit[0]], [p1[1], p1_exit[1]], color='#0284c7', lw=2, ls='--', zorder=4)
ax.annotate('', xy=p2, xytext=p1_exit, arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=2, mutation_scale=14), zorder=4)
ax.text(5.0, 4.0, r'Refracted Ray $T_1$', color='#0284c7', weight='bold', fontsize=9)

# At S2, ray reflects as R2
p_r2_end = (9.2, 4.8)
ax.annotate('', xy=p_r2_end, xytext=p2, arrowprops=dict(arrowstyle="-|>", color='#475569', lw=1.8, mutation_scale=12), zorder=4)
ax.text(8.6, 4.4, r'$R_2$', color='#475569', weight='bold', fontsize=8.5)

# 2. Primary Light ray from L2 to S1 hit point P1_b
p1_b = (5.7, 5.5)
ax.annotate('', xy=p1_b, xytext=l2, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=1.8, mutation_scale=14), zorder=4)

# Hit points markers
for pt, lbl in [(p1, r'$P_1$'), (p2, r'$P_2$'), (p3, r'$P_3$')]:
    ax.scatter(pt[0], pt[1], s=40, color='#ffffff', edgecolors='#0f172a', lw=1.5, zorder=6)
    ax.text(pt[0]-0.25, pt[1]+0.15, lbl, fontsize=10, weight='bold', color='#0f172a')

# Direct Connection Rays (to Eye) with Occlusion Testing!
# Connection from P1 to Eye
ax.annotate('', xy=eye, xytext=p1, arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=2, ls='-', mutation_scale=14), zorder=3)
ax.text(2.3, 3.7, 'Connection Ray (to Eye)', color='#2563eb', weight='bold', fontsize=9.5, rotation=48)

# Connection from P2 to Eye (Tested for occlusion!)
ax.annotate('', xy=eye, xytext=p2, arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=1.5, ls=':', mutation_scale=12), zorder=3)
ax.text(4.8, 2.1, 'Connection Ray (Direct Visibility Checked)', color='#2563eb', fontsize=8.5, rotation=20)

# Connection from P3 to Eye
ax.annotate('', xy=eye, xytext=p3, arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=1.5, ls=':', mutation_scale=12), zorder=3)

# Legend / Note box
ax.set_xlim(0, 11)
ax.set_ylim(0, 10.5)
ax.set_aspect('equal')
ax.axis('off')

# Title
plt.title("Figure 1: Forward (Light-Based) Ray Tracing for Multiple Spheres (Slide-Reversed Setup)\n" +
          r"Rays propagate: Light $\rightarrow$ Surface Hits $\rightarrow$ Reflected/Transmitted Rays $\rightarrow$ Direct Eye Connection",
          fontsize=12, weight='bold', pad=15)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig1_forward_scene.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Figure 1 saved successfully.")
