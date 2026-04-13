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
    ax.text(50, 17.5, r"$\mathbf{A_S}$", ha='center', va='center', fontsize=14, zorder=4)
    ax.text(50, 5, r"$\mathbf{Latent\ Substrate}$", ha='center', va='center', fontsize=20, zorder=4)
    
    # Length scale annotation
    ax.annotate(r"$\ell_S \approx 10^{-35}\ \mathrm{m}$", xy=(grid_end_x - 5, 15), xytext=(85, 15),
                arrowprops=dict(arrowstyle="->", lw=1.5, color='black'), va='center', fontsize=16)

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
    ax.plot([47.5, funnel_left_x], [20, ellipse_y], color='black', lw=1.5, linestyle=':', zorder=2)
    ax.plot([52.5, funnel_right_x], [20, ellipse_y], color='black', lw=1.5, linestyle=':', zorder=2)
    
    # Central kinematic flow vector (Shifted up to make room for G equation below)
    ax.annotate("", xy=(50, 55), xytext=(50, 32), 
                arrowprops=dict(arrowstyle="->", lw=2.5, color="black"), zorder=3)
        
    # Label for cE^2 positioned centrally on the vector
    ce_label = r"$\text{Kinematic Energy Budget}$" + "\n" + r"$(c_E^2)$"
    ax.text(50, 43.5, ce_label, fontsize=14, fontweight='bold', color="black", ha='center', va='center', zorder=4,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=3))

    # Emergence of Gravity Equation (Centered directly on top of Substrate)
    g_eq = r"$G = \dfrac{c_E^2 A_S}{J_N}$"
    ax.text(50, 22.0, g_eq, ha='center', va='bottom', fontsize=22, color='black',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=3), zorder=10)

    # =======================================================
    # 3. Inertial MASS (NUCLEON TORSION) ELLIPSE (Top)
    # =======================================================
    # Simple hollow ellipse (No shading)
    ax.add_patch(patches.Ellipse((50, ellipse_y), ellipse_w, ellipse_h, 
                                 facecolor='white', edgecolor='black', lw=2.5, zorder=3))
    
    # Center dot
    ax.plot(50, ellipse_y, 'ko', markersize=5, zorder=5)
    
    # Torsional Shear Vector (Curved arrow sweeping along outer perimeter)
    ax.annotate("", xy=(65, 81.5), xytext=(35, 81.5),
                arrowprops=dict(arrowstyle="->", color="black", lw=2.0, connectionstyle="arc3,rad=-0.3"), zorder=6)
    
    # Updated Nucleon Title
    ax.text(50, 87, r"$\mathbf{Inertial\ Mass\ (Nucleon\ Torsion)}$", ha='center', va='bottom', fontsize=18)
    
    # Radius dimension line (Internal)
    ax.annotate("", xy=(50 + ellipse_w/2, ellipse_y), xytext=(50, ellipse_y), 
                arrowprops=dict(arrowstyle="->", lw=1.5, color='black'), zorder=5)
    ax.text(50 + ellipse_w/4, ellipse_y + 1, r"$r_N$", fontsize=16, ha='center', va='bottom')
    
    # rho N placed inside the circle
    ax.text(42, ellipse_y - 2.5, r"$\rho_N$", color="black", fontsize=16, fontweight='bold', zorder=6)

    # Torsion Equation (Moved slightly left to reduce gap to arrow tip by 20%)
    jn_eq = r"$J_N = \rho_N r_N^4$"
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
        
    pdf_filename = os.path.join(output_dir, "Fig08_PartII_GravitationalConstantG.pdf")
    
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