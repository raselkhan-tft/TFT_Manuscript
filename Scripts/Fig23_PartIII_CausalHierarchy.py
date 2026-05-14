import matplotlib.pyplot as plt # Selected for publication-grade 2D schematic layout and native LaTeX rendering
import matplotlib.patches as patches # Selected for precise structural primitives (Polygons, Rectangles)
import numpy as np # Selected for efficient spatial array generation and affine transformations
from matplotlib.patches import Polygon
import os # Selected for robust directory management and path-specific file saving

def draw_light_cone(ax, center_x, center_y, scale=1.0, width_scale=1.0, angle_deg=0, 
                    facecolor='blue', alpha=1.0, arrow_color='black', arrow_alpha=1.0):
    """
    Draws a relativistic light cone (hourglass shape) rotated by angle_deg.
    width_scale: 1.0 = Speed c (45 deg), <1.0 = Speed < c (Narrow), 0 = Speed 0 (Line)
    """
    w = 0.4 * scale * width_scale
    h = 0.8 * scale
    
    # Rotation Matrix
    theta = np.radians(angle_deg)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    
    # Top Triangle
    verts_top = np.array([[-w, h], [w, h], [0, 0]])
    verts_top_trans = np.dot(verts_top, R.T)
    verts_top_trans[:, 0] += center_x
    verts_top_trans[:, 1] += center_y
    poly_top = Polygon(verts_top_trans, closed=True, facecolor=facecolor, edgecolor='none', alpha=alpha, zorder=3)
    ax.add_patch(poly_top)
    
    # Bottom Triangle
    verts_bot = np.array([[-w, -h], [w, -h], [0, 0]])
    verts_bot_trans = np.dot(verts_bot, R.T)
    verts_bot_trans[:, 0] += center_x
    verts_bot_trans[:, 1] += center_y
    poly_bot = Polygon(verts_bot_trans, closed=True, facecolor=facecolor, edgecolor='none', alpha=alpha, zorder=3)
    ax.add_patch(poly_bot)
    
    # Add a "Future" vector arrow 
    # Perfectly aligned with the exact center axis of the rotated cone
    arrow_len = h * 0.8
    arrow_end = np.dot(np.array([0, arrow_len]), R.T)
    ax.arrow(center_x, center_y, arrow_end[0], arrow_end[1], 
             head_width=0.08*scale, head_length=0.12*scale, fc=arrow_color, ec=arrow_color, 
             alpha=arrow_alpha, length_includes_head=True, zorder=5)

def create_causal_hierarchy_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    # --- Main Plotting ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), dpi=150)
    fig.patch.set_facecolor('white')

    # Base setup for both axes
    for ax in (ax1, ax2):
        ax.set_facecolor('white')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 12) 
        ax.set_xticks([])
        ax.set_yticks([])
        # Enforce 1:1 aspect ratio to guarantee perfectly symmetrical rotations visually
        ax.set_aspect('equal', adjustable='box')
        
        # Spatial baseline (Replaced simple line with directed coordinate vector)
        ax.arrow(0, 1.0, 9.6, 0, head_width=0.2, head_length=0.3, fc='black', ec='black', alpha=0.4, zorder=0)
        ax.text(9.8, 0.6, r'Space ($r$)', color='black', fontsize=11, ha='right', va='top', alpha=0.7)
        
        for spine in ax.spines.values():
            spine.set_visible(False)

    # =========================================================================
    # LEFT PANEL: (a) Type I Causal Failure
    # =========================================================================
    ax1.text(0.5, 11.2, r"$\mathbf{(a)\ Type\ I\ Causal\ Failure}$", color='black', fontsize=14, ha='left', va='bottom', zorder=10)

    # 1. The State II Saturated Core (Pure Black)
    # Cropped vertically starting strictly at y=1.0 to remain flush with the spatial baseline
    rect = patches.Rectangle((0, 1.0), 2.0, 9.8, facecolor='black', alpha=1.0, zorder=1)
    ax1.add_patch(rect)

    # Core Labels
    core_text = r"State II Saturated Core" + "\n" + r"($\boldsymbol{\alpha_{\mathrm{G}} = 1}$)"
    ax1.text(1, 6.0, core_text, color='white', rotation=90, ha='center', va='center', fontweight='bold', fontsize=12, zorder=10)
    
    ax1.plot(1, 2.5, marker='s', markersize=8, color='white', zorder=10)
    time_text = r"Time Frozen" + "\n" + r"($\boldsymbol{t = 0}$)"
    ax1.text(1, 2.0, time_text, color='white', ha='center', va='top', fontsize=10, fontweight='bold', zorder=10)

    # 2. Event Horizon Line (R_QG)
    # Cropped strictly at y=1.0 to remain flush with the spatial baseline
    # Updated to Maroon color
    ax1.plot([2.0, 2.0], [1.0, 10.8], color='#8B0000', linestyle='--', linewidth=2, zorder=5)
    
    # Increased gap to 2.35 to geometrically balance the visual clearance from the solid black core
    # Label color restored to black
    ax1.text(2.35, 8.5, r'$\mathbf{Black\ Hole\ Horizon}$ ($R_{\mathrm{QG}}$)', color='black', rotation=90, ha='center', va='center', fontsize=12, zorder=10)

    # 3. Tipping and Squeezing Light Cones (Right to Left - 5 Cones)
    positions_A = [8.5, 6.8, 5.1, 3.8, 3.024] 
    angles_A    = [0,   22.5, 45,  67.5, 90]   # Progressive counter-clockwise tipping
    widths_A    = [1.0, 0.8,  0.5, 0.2,  0.0]  # Progressive symmetrical squeezing
    # Baseline cone match: All structural cones maintain 100% opacity to denote mechanical failure, not energy fading
    poly_alphas = [1.0, 1.0,  1.0, 1.0,  0.0]  

    for x, ang, w, p_alpha in zip(positions_A, angles_A, widths_A, poly_alphas):
        draw_light_cone(ax1, x, 5, scale=1.6, width_scale=w, angle_deg=ang, 
                        facecolor='#4682B4', alpha=p_alpha, arrow_color='black', arrow_alpha=1.0)

    # Effective Inertia Equation (Upper)
    ax1.text(5.5, 7.6, r"$\mu_{\mathrm{eff}} = \frac{\mu_{\mathrm{D}}}{(1 - \alpha_{\mathrm{G}})^4}$", 
             fontsize=16, color='black', ha='center', va='center', zorder=10)

    # Kinematic Speed Equation & Condition (Lower)
    # Pure mathematical implication removes English text strings to eliminate CM Roman/Italic font weight mismatch
    # Replaced '\implies' with '\Rightarrow' to prevent compilation errors in Matplotlib's native mathtext parser
    cp_text = r"$c_{\mathrm{P}} = c_{\mathrm{E}} \sqrt{\mu_{\mathrm{D}} / \mu_{\mathrm{eff}}}$" + "\n" + r"$(\alpha_{\mathrm{G}} \rightarrow 1 \Rightarrow \mu_{\mathrm{eff}} \rightarrow \infty \Rightarrow c_{\mathrm{P}} = 0)$"
    ax1.text(5.5, 2.67, cp_text, fontsize=14, fontweight='normal', color='black', ha='center', va='center', 
             bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=1.5), zorder=10)
             
    ax1.annotate("", xy=(2.0, 4.65), xytext=(4.1, 2.95),
                 arrowprops=dict(arrowstyle="->", color="black", lw=1.5, connectionstyle="arc3,rad=-0.15"), zorder=9)

    # =========================================================================
    # RIGHT PANEL: (b) Type II Causal Saturation
    # =========================================================================
    ax2.text(0.5, 11.2, r"$\mathbf{(b)\ Type\ II\ Causal\ Saturation}$", color='black', fontsize=14, ha='left', va='bottom', zorder=10)

    # Time Arrow
    ax2.arrow(0.5, 1.0, 0, 7.5, head_width=0.2, head_length=0.3, fc='black', ec='black', alpha=0.4, zorder=1)
    ax2.text(0.8, 8.5, r'Time ($t$)', color='black', fontsize=11, rotation=90, alpha=0.7)

    # 1. Viscous Cosmic Horizon Line (R_U)
    ax2.plot([9.0, 9.0], [1.0, 10.8], color='gray', linestyle='--', linewidth=2, zorder=5)
    ax2.text(8.75, 8.5, r'$\mathbf{Viscous\ Cosmic\ Horizon}$ ($R_{\mathrm{U}}$)', color='black', rotation=90, ha='center', va='center', fontsize=12, zorder=10)

    # 2. Fading Light Cones (Left to Right - 4 Cones)
    positions_B = [2.0, 4.3, 6.6, 8.8]
    alphas_B    = [1.0, 0.6, 0.3, 0.05] # Fading into the vacuum (100%, 60%, 30%, 5%)

    for x, alp in zip(positions_B, alphas_B):
        # Arrow opacity (arrow_alpha) locked to 1.0 and color to 'black' to maintain time vector contrast
        draw_light_cone(ax2, x, 5, scale=1.6, width_scale=1.0, angle_deg=0, 
                        facecolor='#4682B4', alpha=alp, arrow_color='black', arrow_alpha=1.0)

    # Energy Decay Equation (Upper)
    ax2.text(5.5, 7.6, r"$E_{\mathrm{obs}} = E_{\mathrm{emit}} e^{-\Gamma_{\mathrm{D}} x / c_{\mathrm{E}}}$", 
             fontsize=16, color='black', ha='center', va='center', zorder=10)

    # Universal Potential Equation (Lower)
    ax2.text(5.5, 2.4, r"$\phi_{\mathrm{G,U}} = \int_{0}^{R_{\mathrm{U}}} \frac{G \cdot dm}{r} = c_{\mathrm{E}}^2$", 
             fontsize=16, color='black', ha='center', va='center', zorder=10)

    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig23_PartIII_CausalHierarchy.pdf")
    
    try:
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()

if __name__ == "__main__":
    create_causal_hierarchy_visual()