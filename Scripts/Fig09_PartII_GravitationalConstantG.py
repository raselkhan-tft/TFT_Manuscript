import numpy as np # Used for spacing, array generation, and dynamic opacity gradients
import matplotlib.pyplot as plt # Chosen for robust 2D schematic drawing and native LaTeX rendering
import matplotlib.patches as patches # Chosen for precise primitive shapes (Ellipse, Polygon, Arc)
import os # Chosen for robust directory management

def create_publication_schematic():
    # Enforce clear, publication-ready font settings (Black and White Theme)
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'mathtext.fontset': 'cm', # Ensures math symbols render cleanly 
        'font.size': 12
    })
    
    # Initialize diagram canvas
    fig, ax = plt.subplots(figsize=(12, 12), dpi=150)
    ax.set_facecolor('white')
    
    # Absolute coordinate system mapping
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # =======================================================
    # 1. SUBSTRATE GRID (Bottom)
    # =======================================================
    # Starting at 12.5 ensures vertical lines at 47.5 and 52.5
    # This centers the SQUARE at x=50 instead of a line.
    grid_start_x = 12.5
    grid_end_x = 87.5
    box_w = 5.0
    
    # Highlight the central A_S block as a SINGLE cubic unit (top row)
    ax.add_patch(patches.Rectangle((47.5, 15), 5, 5, facecolor='#F2F2F2', edgecolor='black', lw=1.2, zorder=1))
    
    # Vertical grid lines with fading opacity away from center
    v_lines = np.arange(grid_start_x, grid_end_x + box_w, box_w)
    for x in v_lines:
        dist = abs(x - 50)
        alpha_val = max(0.05, 1.0 - (dist / 35.0))
        ax.plot([x, x], [10, 20], color='black', lw=1.0, alpha=alpha_val, zorder=2)
        
    # Horizontal grid lines with gradient fading
    x_segs = np.linspace(grid_start_x, grid_end_x, 150)
    for i in range(len(x_segs)-1):
        x_m = (x_segs[i] + x_segs[i+1]) / 2.0
        alpha_v = max(0.05, 1.0 - abs(x_m - 50) / 35.0)
        for y in [10, 15, 20]:
            ax.plot([x_segs[i], x_segs[i+1]], [y, y], color='black', lw=1.0, alpha=alpha_v, zorder=2)
            
    # Substrate Labels
    ax.text(50, 17.5, r"$\mathbf{A_{\mathrm{S}}}$", ha='center', va='center', fontsize=14, zorder=4)
    ax.text(50, 3, r"$\mathbf{Latent\ Substrate}$", ha='center', va='center', fontsize=20, zorder=4)
    ax.annotate("", xy=(50, 9.5), xytext=(50, 4.5), 
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color="black", mutation_scale=15), zorder=4)
    
    # Formal Scale Indicator (Dimension Line)
    # Moved to the third square from the right, safely below the grid geometry
    # Grid limits: 87.5 (Right). Square 1: 82.5-87.5 | Square 2: 77.5-82.5 | Square 3: 72.5-77.5
    sq3_left = 72.5
    sq3_right = 77.5
    sq3_center = 75.0
    y_arrow = 8.0
    
    ax.plot([sq3_left, sq3_left], [y_arrow - 0.5, y_arrow + 0.5], color='black', lw=1.0, zorder=4)
    ax.plot([sq3_right, sq3_right], [y_arrow - 0.5, y_arrow + 0.5], color='black', lw=1.0, zorder=4)
    ax.annotate("", xy=(sq3_left, y_arrow), xytext=(sq3_right, y_arrow),
                arrowprops=dict(arrowstyle="<|-|>", lw=1.0, color='black', mutation_scale=10), zorder=4)
    ax.text(sq3_center, y_arrow - 0.8, r"$\ell_{\mathrm{S}} \approx 10^{-35}\ \mathrm{m}$", 
            ha='center', va='top', fontsize=12, color='black', zorder=4)

    # =======================================================
    # 2. PROJECTION FUNNEL (Middle)
    # =======================================================
    ellipse_y = 75
    ellipse_w = 40
    ellipse_h = 12
    
    # Funnel top corners at the Nucleon
    funnel_left_x = 50 - (ellipse_w / 2)
    funnel_right_x = 50 + (ellipse_w / 2)
    
    # Volumetric Shading for the projection tunnel
    funnel_pts = [[47.5, 20], [52.5, 20], [funnel_right_x, ellipse_y], [funnel_left_x, ellipse_y]]
    funnel = patches.Polygon(funnel_pts, facecolor='#F8F8F8', alpha=0.6, edgecolor='none', zorder=1)
    ax.add_patch(funnel)
    
    # Funnel boundary lines (DOTTED starting from two sides/corners of the AS square)
    ax.plot([47.5, funnel_left_x], [20, ellipse_y], color='black', lw=1.8, linestyle=':', zorder=2)
    ax.plot([52.5, funnel_right_x], [20, ellipse_y], color='black', lw=1.8, linestyle=':', zorder=2)
    
    # Central kinematic flow vector & Label
    # Shifted downward to increase nucleon gap by 30%
    ce_label = r"$\text{Kinematic Energy Budget}$" + "\n" + r"$(c_{\mathrm{E}}^2)$"
    ax.text(50, 55.7, ce_label, fontsize=14, fontweight='bold', color="black", ha='center', va='center', zorder=4)
    
    # Bottom segment of broken vector (perfectly symmetric around label)
    ax.plot([50, 50], [43.7, 50.7], color="black", lw=2.5, zorder=3)
    # Top segment of broken vector with stealth arrowhead
    ax.annotate("", xy=(50, 67.7), xytext=(50, 60.7), 
                arrowprops=dict(arrowstyle="-|>", lw=2.5, color="black", mutation_scale=15), zorder=3)

    # Emergence of Gravity Equation
    # Shifted upward to reduce gap to leader tail by 50%
    g_eq = r"$G = \dfrac{c_{\mathrm{E}}^2 A_{\mathrm{S}}}{J_{\mathrm{N}}}$"
    ax.text(50, 34.7, g_eq, ha='center', va='bottom', fontsize=22, color='black', zorder=10)

    # =======================================================
    # 3. Inertial MASS (NUCLEON TORSION) ELLIPSE (Top)
    # =======================================================
    # Toroidal Projection (Filled Annulus)
    # Facecolor uses RGBA (0.545, 0.0, 0.0, 0.15) for a light, semi-transparent maroon
    ax.add_patch(patches.Ellipse((50, ellipse_y), ellipse_w, ellipse_h, 
                                 facecolor=(0.545, 0.0, 0.0, 0.15), edgecolor='#8B0000', lw=1.8, zorder=3))
    
    # Central white hole (Singular Core)
    hole_w = ellipse_w * 0.25
    hole_h = ellipse_h * 0.25
    ax.add_patch(patches.Ellipse((50, ellipse_y), hole_w, hole_h, 
                                 facecolor='white', edgecolor='#8B0000', lw=1.2, zorder=4))
    
    # Torsional Shear Vector (Curved stealth arrow sweeping along outer perimeter)
    ax.annotate("", xy=(65, 81.5), xytext=(35, 81.5),
                arrowprops=dict(arrowstyle="-|>", color="#8B0000", lw=2.0, connectionstyle="arc3,rad=-0.3", mutation_scale=15), zorder=6)
    
    # Updated Nucleon Title
    ax.text(50, 87, r"$\mathbf{Nucleon\ (Structural\ Mass\ Moment)}$", ha='center', va='bottom', fontsize=18)
    
    # Radius dimension line (Internal stealth arrow)
    ax.annotate("", xy=(50 + ellipse_w/2, ellipse_y), xytext=(50, ellipse_y), 
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color='black', mutation_scale=12), zorder=6)
    ax.text(50 + ellipse_w/4, ellipse_y + 1, r"$r_{\mathrm{N}}$", fontsize=16, ha='center', va='bottom', zorder=6)
    
    # rho N placed inside the circle (Legible over semi-transparent fill)
    ax.text(42, ellipse_y - 2.5, r"$\rho_{\mathrm{N}}$", color="black", fontsize=16, fontweight='bold', zorder=6)

    # Torsion Equation
    jn_eq = r"$J_{\mathrm{N}} = \rho_{\mathrm{N}} r_{\mathrm{N}}^4$"
    ax.text(66.6, 81.5, jn_eq, ha='left', va='center', fontsize=22, color='black', zorder=10)

    # =======================================================
    # FINAL RENDER & EXPORT
    # =======================================================
    plt.tight_layout()
    
    # -----------------------
    # PDF Export Logic
    # -----------------------
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig09_PartII_GravitationalConstantG.pdf")
    
    try:
        # Saving as high-fidelity vector PDF for publication
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()

if __name__ == "__main__":
    create_publication_schematic()