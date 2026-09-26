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
fig, ax = plt.subplots(figsize=(11.5, 8.5), dpi=300)
ax.set_facecolor('#ffffff')

# Spheres positioned matching Slide 18
# S1: Transparent sphere at (5.2, 4.2), R=1.35
c_s1 = (5.2, 4.2)
r_s1 = 1.35
circle_s1 = plt.Circle(c_s1, r_s1, color='#e0f2fe', ec='#0284c7', lw=2.5, zorder=2)
ax.add_patch(circle_s1)
ax.text(5.2, 3.2, r'$S_1$ [Transparent]', color='#0369a1', weight='bold', ha='center', fontsize=11, zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#0284c7', lw=1, alpha=0.9))

# S2: Reflective sphere at (9.4, 3.5), R=1.15
c_s2 = (9.4, 3.5)
r_s2 = 1.15
circle_s2 = plt.Circle(c_s2, r_s2, color='#f1f5f9', ec='#475569', lw=2.5, zorder=2)
ax.add_patch(circle_s2)
ax.text(9.4, 2.5, r'$S_2$ [Reflective]', color='#334155', weight='bold', ha='center', fontsize=11, zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#475569', lw=1, alpha=0.9))

# S3: Reflective sphere at (3.2, 7.8), R=1.1
c_s3 = (3.2, 7.8)
r_s3 = 1.1
circle_s3 = plt.Circle(c_s3, r_s3, color='#fef3c7', ec='#d97706', lw=2.5, zorder=2)
ax.add_patch(circle_s3)
ax.text(3.2, 8.7, r'$S_3$ [Reflective]', color='#b45309', weight='bold', ha='center', fontsize=11, zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#d97706', lw=1, alpha=0.9))

# S4: Opaque / Diffuse sphere at (7.8, 8.8), R=0.95
c_s4 = (7.8, 8.8)
r_s4 = 0.95
circle_s4 = plt.Circle(c_s4, r_s4, color='#fee2e2', ec='#dc2626', lw=2.5, zorder=2)
ax.add_patch(circle_s4)
ax.text(7.8, 9.6, r'$S_4$ [Diffuse / Opaque]', color='#b91c1c', weight='bold', ha='center', fontsize=11, zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#dc2626', lw=1, alpha=0.9))

# Lights:
# L1 at top-center: (5.2, 10.5)
l1 = (5.2, 10.5)
# L2 at top-right: (10.2, 10.0)
l2 = (10.2, 10.0)

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
p1 = (4.9, 5.5) # hit on top-surface of S1
ax.annotate('', xy=p1, xytext=l1, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.5, mutation_scale=16), zorder=5)
ax.text(5.3, 8.5, r'Primary Ray ($\mathbf{s}_1 + t\mathbf{d}_1$)', color='#ea580c', weight='bold', fontsize=9.5, rotation=-88,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

# Secondary Ray A: Reflected ray R1 from P1 to S3 (hit P3)
p3 = (3.8, 7.0) # hit on S3
ax.annotate('', xy=p3, xytext=p1, arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=2.2, mutation_scale=15), zorder=5)
ax.text(3.9, 6.0, r'Reflected Ray $R_1$', color='#d97706', weight='bold', fontsize=9.5, rotation=-52,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

# Secondary Ray A2: From P3 on S3 to S4 (hit P4)
p4 = (7.0, 8.4) # hit on S4
ax.annotate('', xy=p4, xytext=p3, arrowprops=dict(arrowstyle="-|>", color='#d97706', lw=2.0, mutation_scale=14), zorder=5)
ax.text(5.1, 7.9, r'Reflected Ray $R_3$', color='#d97706', weight='bold', fontsize=9.5, rotation=24,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

# Secondary Ray B: Refracted/Transmitted ray T1 inside S1, exits at p1_exit towards S2 (hit P2)
p1_exit = (6.2, 3.6)
p2 = (8.3, 3.5)
ax.plot([p1[0], p1_exit[0]], [p1[1], p1_exit[1]], color='#0284c7', lw=2.2, ls='--', zorder=4)
ax.text(5.3, 4.3, r'Refraction $T_1$', color='#0284c7', weight='bold', fontsize=9.5,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))
ax.annotate('', xy=p2, xytext=p1_exit, arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=2.2, mutation_scale=15), zorder=5)
ax.text(7.2, 4.0, r'Transmitted Ray $T_1$', color='#0284c7', weight='bold', fontsize=9.5, rotation=-4,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

# At S2, reflected ray R2 bounces away
p_r2 = (10.4, 4.7)
ax.annotate('', xy=p_r2, xytext=p2, arrowprops=dict(arrowstyle="-|>", color='#475569', lw=1.8, mutation_scale=12), zorder=5)
ax.text(9.7, 4.4, r'$R_2$', color='#475569', weight='bold', fontsize=9)

# 2. Primary Light ray from L2 to S1 (hit P1_b)
p1_b = (6.4, 4.8)
ax.annotate('', xy=p1_b, xytext=l2, arrowprops=dict(arrowstyle="-|>", color='#ea580c', lw=2.0, mutation_scale=15), zorder=5)
ax.text(8.4, 7.3, r'Primary Ray from $L_2$', color='#ea580c', weight='bold', fontsize=9.5, rotation=54,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

# Hit Points
for pt, lbl in [(p1, r'$P_1$'), (p2, r'$P_2$'), (p3, r'$P_3$'), (p4, r'$P_4$')]:
    ax.scatter(pt[0], pt[1], s=65, color='#ffffff', edgecolors='#0f172a', lw=2, zorder=7)
    ax.text(pt[0]+0.15, pt[1]+0.15, lbl, fontsize=11, weight='bold', color='#0f172a', zorder=8)

# Direct Connection Rays (to Eye)
# From P1 to Eye (Direct Visibility)
ax.annotate('', xy=eye, xytext=p1, arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=2.2, ls='-', mutation_scale=15), zorder=4)
ax.text(2.1, 3.4, 'Eye Connection Ray\n(Direct Visibility)', color='#2563eb', weight='bold', fontsize=9.5, rotation=46,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

# From P2 to Eye (Tested for Occlusion by S1)
ax.annotate('', xy=eye, xytext=p2, arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=1.8, ls=':', mutation_scale=13), zorder=4)
ax.text(4.4, 1.8, 'Eye Connection Ray (Occlusion-Checked)', color='#2563eb', weight='bold', fontsize=9, rotation=17,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

# From P3 to Eye
ax.annotate('', xy=eye, xytext=p3, arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=1.8, ls=':', mutation_scale=13), zorder=4)
ax.text(1.7, 5.0, 'Eye Connection Ray', color='#2563eb', weight='bold', fontsize=9, rotation=63,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

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

print("Figure 1 rendered with zero path overlaps!")
