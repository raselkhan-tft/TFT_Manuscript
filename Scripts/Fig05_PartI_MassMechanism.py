import numpy as np # Selected for efficient, vectorized array math and coordinate geometry
import matplotlib.pyplot as plt # Selected for precise 2D vector graphic control and native LaTeX text rendering
from matplotlib.patches import Circle, FancyArrowPatch
import os # Selected for robust directory management

# ============================================================
# Figure: Mass-Amplitude Hierarchy (PRL Academic Standard)
# Comparative mechanical schematic of two FCC lattice nodes:
#   (a) Structural Limit Regime (Top Quark)
#   (b) High-Resolution Linear Regime (Electron)
# ============================================================

# -----------------------
# Global style parameters
# -----------------------
plt.rcParams.update({
    "figure.dpi": 160,
    "savefig.dpi": 300,
    "font.size": 11,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "mathtext.fontset": "cm",   # Computer Modern for italicized math variables
    "axes.linewidth": 0.8,
})

# -----------------------
# Physical scale settings
# -----------------------
rD = 1.81e-27 # m 
amp_top = 1.31 * rD 
amp_electron = 7.0e-33 # m

# -----------------------
# Colors
# -----------------------
NODE_FACE = "#F5F5F5"          # Light gray (Solid sphere face)
NODE_EDGE = "#00CCFF"          # Electric Blue (Matching FCC flagship geometry)
FLUID_FILL = "#b2bfc9"         # Swept volume ring
WIRE = "#c9c9c9"               # Light grey dashed lattice
SHELL = "black"
TEXT = "black"

# -----------------------
# FCC wireframe geometry
# -----------------------
cube_pts = {
    "A": np.array([0.0, 0.0]), "B": np.array([1.8, 0.0]),
    "C": np.array([2.55, 0.72]), "D": np.array([0.75, 0.72]),
    "E": np.array([0.0, 1.85]), "F": np.array([1.8, 1.85]),
    "G": np.array([2.55, 2.57]), "H": np.array([0.75, 2.57]),
}

cube_edges = [
    ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
    ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"),
    ("A", "E"), ("B", "F"), ("C", "G"), ("D", "H"),
]

fcc_extra = [
    ("A", "F"), ("B", "E"), ("D", "G"), ("C", "H"),
    ("A", "C"), ("B", "D"), ("E", "G"), ("F", "H"),
]

def draw_fcc_wireframe(ax, origin=(0, 0), scale=1.0):
    pts = {k: origin + scale * v for k, v in cube_pts.items()}
    for p, q in cube_edges:
        ax.plot([pts[p][0], pts[q][0]], [pts[p][1], pts[q][1]], ls=(0, (3, 3)), lw=1.0, color=WIRE, zorder=1)
    for p, q in fcc_extra:
        ax.plot([pts[p][0], pts[q][0]], [pts[p][1], pts[q][1]], ls=(0, (2, 3)), lw=0.8, color=WIRE, alpha=0.85, zorder=1)
    return pts

def oscillation_arrow(ax, start, end, lw=1.2, ms=8):
    arr = FancyArrowPatch(posA=start, posB=end, arrowstyle='<|-|>', mutation_scale=ms, lw=lw, color='black', shrinkA=0, shrinkB=0, zorder=5)
    ax.add_patch(arr)

# -----------------------
# Figure / axes
# -----------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 6))
# Adjusted top margin to 0.85 to provide ample clearance for the extended labels
fig.subplots_adjust(top=0.85, bottom=0.08, left=0.05, right=0.95, wspace=0.2)

# ============================================================
# PANEL (a) — "SHOUT" (Top Quark)
# ============================================================
ax = axes[0]
ax.set_aspect('equal')
ax.axis('off')

draw_fcc_wireframe(ax, origin=np.array([0.2, 0.15]), scale=1.25)
center_left = np.array([1.65, 1.55])
node_r = 0.68
r_amp_val = node_r * 0.31
outer_r, inner_r = node_r + r_amp_val, node_r - r_amp_val

# Swept Volume
ax.add_patch(Circle(center_left, outer_r, facecolor=FLUID_FILL, edgecolor='none', zorder=2.5))
# Core Node (Reduced lw from 2.5 to 1.2 for thinner cyan ring)
ax.add_patch(Circle(center_left, node_r, facecolor=NODE_FACE, edgecolor=NODE_EDGE, lw=1.2, zorder=3))
# Boundaries
ax.add_patch(Circle(center_left, outer_r, fill=False, edgecolor=SHELL, lw=1.0, ls=':', zorder=4))
ax.add_patch(Circle(center_left, inner_r, fill=False, edgecolor=SHELL, lw=1.0, ls=':', zorder=4))

# Oscillation Arrows
angles = np.deg2rad([90, 210, 330])
for th in angles:
    start = center_left + inner_r * np.array([np.cos(th), np.sin(th)])
    end   = center_left + outer_r * np.array([np.cos(th), np.sin(th)])
    oscillation_arrow(ax, start, end, lw=1.2, ms=8)

# Academic Label (a) - Decoupled using transAxes to strictly pin it above the rendering geometry
ax.text(0.0, 1.02, r"$\mathbf{(a)\ The\ Top\ Quark\ (Vibrational\ Limit\ Regime)}$", 
        transform=ax.transAxes, fontsize=14, fontweight='bold', ha='left', va='bottom', color='black')

# Geometric Labels (Clean Tier 2)
# Adjusted V_eff target radius to terminates the arrow tip inside the shadow zone (swept volume ring)
v_eff_target_r = node_r + (0.5 * r_amp_val)
ax.annotate(r"$V_{\mathrm{eff}}$ (Swept Volume)", 
            xy=(center_left[0] + v_eff_target_r * np.cos(np.deg2rad(135)), 
                center_left[1] + v_eff_target_r * np.sin(np.deg2rad(135))), 
            xytext=(center_left[0] - 1.3, center_left[1] + 1.3),
            arrowprops=dict(arrowstyle="->", lw=0.9, color='black'),
            fontsize=11, ha='center', va='bottom', zorder=10)

ax.annotate("Vibration", 
            xy=(center_left[0], center_left[1] + outer_r), 
            xytext=(center_left[0] + 1.0, center_left[1] + 1.1),
            arrowprops=dict(arrowstyle="->", lw=0.9, color='black'),
            fontsize=11, ha='center', va='bottom', zorder=10)

# Radial Amplitude
start_ramp = center_left + node_r * np.array([1, 0])
end_ramp   = center_left + outer_r * np.array([1, 0])
ramp_arrow = FancyArrowPatch(posA=start_ramp, posB=end_ramp, arrowstyle='<|-|>', mutation_scale=8, lw=1.2, color='black', shrinkA=0, shrinkB=0, zorder=6)
ax.add_patch(ramp_arrow)
ax.text(end_ramp[0] + 0.08, end_ramp[1], r'$r_{\mathrm{amp}}$', fontsize=12, va='center', ha='left', fontweight='bold')

ax.set_xlim(-0.1, 3.8); ax.set_ylim(-0.5, 3.8)

# ============================================================
# PANEL (b) — "WHISPER" (Electron)
# ============================================================
ax = axes[1]
ax.set_aspect('equal')
ax.axis('off')

draw_fcc_wireframe(ax, origin=np.array([0.2, 0.15]), scale=1.25)
center_right = np.array([1.65, 1.55])
tiny_amp = 0.04
outer_r_tiny, inner_r_tiny = node_r + tiny_amp, node_r - tiny_amp

ax.add_patch(Circle(center_right, outer_r_tiny, facecolor=FLUID_FILL, edgecolor='none', zorder=2.5))
# Core Node (Reduced lw from 2.5 to 1.2 for thinner cyan ring)
ax.add_patch(Circle(center_right, node_r, facecolor=NODE_FACE, edgecolor=NODE_EDGE, lw=1.2, zorder=3))
ax.add_patch(Circle(center_right, outer_r_tiny, fill=False, edgecolor=SHELL, lw=1.0, ls=':', zorder=4))
ax.add_patch(Circle(center_right, inner_r_tiny, fill=False, edgecolor=SHELL, lw=1.0, ls=':', zorder=4))

# Academic Label (b) - Decoupled using transAxes to strictly pin it above the rendering geometry
ax.text(0.0, 1.02, r"$\mathbf{(b)\ The\ Electron\ (High-Resolution\ Linear\ Regime)}$", 
        transform=ax.transAxes, fontsize=14, fontweight='bold', ha='left', va='bottom', color='black')

# Internal Signal Visuals
ax.plot([center_right[0] - node_r, center_right[0] + node_r], [center_right[1], center_right[1]], color='black', lw=1.2, ls='--', zorder=5)

# Subscripts strictly formatted for upright Roman standards
ax.text(center_right[0], center_right[1] - 0.12, r"$2r_{\mathrm{D}}$", fontsize=12, fontweight='bold', ha='center', va='top')
ax.text(center_right[0], center_right[1] + 0.12, r"$f_{\mathrm{m}} = c_{\mathrm{E}} / 2r_{\mathrm{D}}$", fontsize=11, fontweight='bold', ha='center', va='bottom')

# Tier 2 Labels
ax.annotate("Internal Wave Signal", 
            xy=(center_right[0] - 0.3, center_right[1] + 0.25), 
            xytext=(center_right[0] - 0.9, center_right[1] + 1.2),
            arrowprops=dict(arrowstyle="->", lw=0.9, color='black', connectionstyle="arc3,rad=0.2"),
            fontsize=11, ha='left', va='bottom', zorder=10)

ax.annotate("Low Amplitude Pulsating", 
            xy=(center_right[0], center_right[1] - outer_r_tiny), 
            xytext=(center_right[0], 0.1),
            arrowprops=dict(arrowstyle="->", lw=0.9, color='black'),
            fontsize=11, ha='center', va='top', zorder=10)

ax.set_xlim(-0.1, 3.8); ax.set_ylim(-0.5, 3.8)

# -----------------------
# PDF Export Logic
# -----------------------
output_dir = "Figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
pdf_filename = os.path.join(output_dir, "Fig05_PartI_Massmechanism.pdf")

try:
    plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
    print(f"High-fidelity vector PDF saved to: {pdf_filename}")
except PermissionError:
    print(f"Permission denied: Please close {pdf_filename} before re-running.")
except Exception as e:
    print(f"Export error: {e}")

plt.show()