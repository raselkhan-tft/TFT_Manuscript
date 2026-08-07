import numpy as np # Selected for efficient array generation and coordinate math
import matplotlib.pyplot as plt # Selected for publication-grade 2D vector graphic control and native LaTeX rendering
import matplotlib.patheffects as pe # Selected for masking stroke effects to cleanly break the axis lines
import os # Selected for robust directory management and path-specific file saving

# ---------------------------------------------------------
# PRL STRICT FORMATTING PARAMETERS (Matched to Saturation Plot)
# ---------------------------------------------------------
plt.rcParams.update({
    'savefig.pad_inches': 0.1,
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'cm', 
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': False,
    'ytick.right': False,
    'axes.linewidth': 1.2,
    'font.size': 12
})

# ---------------------------------------------------------
# DATA GENERATION
# ---------------------------------------------------------
# X-axis: Normalized Density (rho_L / rho_QG)
rho_normalized_soft = np.linspace(0, 1.0, 500)
capacity_soft = 1.0 - rho_normalized_soft

# ---------------------------------------------------------
# FIGURE SETUP
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# 1. THE SUBSTRATE REGIME & SOFT FLOOR (Constrained to Y >= 0.0)
# Original Substrate Core (Solid black background starting EXACTLY at x=1.0)
ax.fill_between([1.0, 1.4], 0.0, 1.0, facecolor='black', zorder=1)

# Orthogonal grid lines constrained strictly to the substrate block
grid_x_sub = np.linspace(1.04, 1.4, 10)
grid_y_sub = np.linspace(0.0, 1.0, 21)
for gx in grid_x_sub:
    ax.plot([gx, gx], [0.0, 1.0], color='#444444', lw=1.0, linestyle='-', zorder=2)
for gy in grid_y_sub:
    ax.plot([1.0, 1.4], [gy, gy], color='#444444', lw=1.0, linestyle='-', zorder=2)

# Subtle background grid for the Soft Floor Region (x=0 to x=1.0)
grid_x_soft = np.linspace(0, 1.0, 11)
grid_y_soft = np.linspace(0, 1.0, 11)
for gx in grid_x_soft:
    ax.plot([gx, gx], [0, 1.0], color='#F2F2F2', linestyle=':', lw=0.8, zorder=0)
for gy in grid_y_soft:
    ax.plot([0, 1.0], [gy, gy], color='#F2F2F2', linestyle=':', lw=0.8, zorder=0)

# 2. THE PHASE TRANSITION BOUNDARY (Event Horizon - Constrained to Y >= 0.0)
ax.plot([1.0, 1.0], [0.0, 1.0], color='#8B0000', linestyle='--', linewidth=2.5, zorder=3, 
        label=r'Phase Transition ($\rho_{\mathrm{L}} / \rho_{\mathrm{QG}} = 1$)')

# Explicit Event Horizon Vertical Label
ax.text(0.97, 0.5, r"Event Horizon ($R_{\mathrm{QG}}$)", color='black', fontsize=12, fontweight='normal', 
        ha='right', va='center', rotation=90, bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=2), zorder=15)

# 3. PLOTTING THE CAPACITY CURVE
# Soft Floor Regime (Dark Blue) with rounded cap styling for smooth endpoints
ax.plot(rho_normalized_soft, capacity_soft, color='#003366', linewidth=2.25, zorder=4,
        solid_capstyle='round', label=r'Remaining State-I Response Capacity')

# 4. TERMINATION POINT
# The Electric Blue line descends from Max Capacity and terminates in a hard, definitive point exactly at X=1.0, Y=0
ax.plot(1.0, 0.0, marker='o', color='#8B0000', markersize=10, zorder=10, clip_on=False)

# 5. EQUATION PLACEMENT ALONG THE CURVE
eq_text = r'$|G^{(\tau)}|_{\mathrm{cap}} = \frac{\kappa G}{c_{\mathrm{E}}^4}(\tau_{\mathrm{QG}} - \tau_{\mathrm{L}})$'
ax.text(0.45, 0.58, eq_text, fontsize=12, rotation=-37, rotation_mode='anchor',
        color='black', ha='center', va='bottom', zorder=5)

# 6. AXES CONFIGURATION & BROKEN SCALE SPINE
ax.set_xlim(0, 1.4)
ax.set_ylim(-0.05, 1.05)

# Remove native spines and ALL native ticks for clean custom replacement
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

# Configure left spine bounds to perfectly cap the thick curvature line
ax.spines['left'].set_bounds(0, 1.02)
ax.spines['left'].set_color('black')
ax.spines['left'].set_linewidth(1.2)

# Draw custom broken bottom spine
ax.plot([0, 1.06], [0, 0], color='black', lw=1.2, clip_on=False, zorder=6)
ax.plot([1.14, 1.4], [0, 0], color='black', lw=1.2, clip_on=False, zorder=6)

# Slashes (//) across the baseline gap representing the broken scale
slash_pe = [pe.Stroke(linewidth=3.5, foreground='white'), pe.Normal()]
ax.plot([1.07, 1.10], [-0.03, 0.03], color='black', lw=1.5, clip_on=False, path_effects=slash_pe, zorder=10)
ax.plot([1.11, 1.14], [-0.03, 0.03], color='black', lw=1.5, clip_on=False, path_effects=slash_pe, zorder=10)

# =======================================================
# CUSTOM UNIFIED TICK MARKS (0.2 Intervals)
# =======================================================
# Calculated based on 10x6 figure ratio to ensure identical physical lengths for both axes
tick_len_x = 0.0135  # Length mapping for Y-direction
tick_len_y = 0.0105  # Length mapping for X-direction

# Custom X Ticks (Inward pointing)
for tx in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    ax.plot([tx, tx], [0.0, tick_len_x], color='black', lw=1.2, clip_on=False, zorder=10)
    if tx > 0: # Skip the origin label to leave room for the single shared zero
        ax.text(tx, -0.02, f'${tx}$', ha='center', va='top', fontsize=12)

# Custom Y Ticks (Inward pointing)
for ty in [0.2, 0.4, 0.6, 0.8, 1.0]:
    ax.plot([0.0, tick_len_y], [ty, ty], color='black', lw=1.2, clip_on=False, zorder=10)
    ax.text(-0.015, ty, f'${ty}$', ha='right', va='center', fontsize=12)

# Single Shared Origin Zero (Straight under Y-axis)
ax.text(0.0, -0.02, '$0$', ha='center', va='top', fontsize=12)

# Axis Titles
ax.set_xlabel(r'Normalized Local Converted-Capacity Density ($\rho_{\mathrm{L}} / \rho_{\mathrm{QG}}$)', fontsize=12, labelpad=12)
ax.set_ylabel(r'Normalized Remaining Response Capacity ($|G^{(\tau)}|_{\mathrm{cap}} / |G^{(\tau)}|_{\max}$)', fontsize=12, labelpad=25)

# 7. SUBSTRATE CORE LABEL
# Placed inside the black zone, perfectly equidistant from the event horizon (1.0) and right boundary (1.4)
core_center_x = 1.2
core_text = r"$\mathbf{State\ II\ Saturated\ Core}$" + "\n" + r"($\rho_{\mathrm{S}} \approx 10^{96}\ \mathrm{kg/m}^3$)"
ax.text(core_center_x, 0.5, core_text, color='white', fontsize=11, ha='center', va='center', rotation=0, zorder=15,
        bbox=dict(facecolor='black', edgecolor='none', alpha=0.85, pad=3))

# Legend Configuration
# Placed safely in the upper right of the soft floor
leg = ax.legend(loc='upper right', bbox_to_anchor=(0.68, 0.95), framealpha=0.9, edgecolor='lightgray', fontsize=11)
leg.set_zorder(6)

# Standard layout adjustment matching the reference styling
plt.tight_layout()

# -----------------------
# PDF Export Logic
# -----------------------
output_dir = "Figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
pdf_filename = os.path.join(output_dir, "FigX_PartII_Curvature.pdf")

try:
    plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
    print(f"High-fidelity vector PDF saved to: {pdf_filename}")
except PermissionError:
    print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

plt.show()