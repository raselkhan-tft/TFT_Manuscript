import numpy as np # Used for efficient parametric generation of the orbital sweep
import matplotlib.pyplot as plt # Chosen for publication-grade 2D schematic layout and native LaTeX rendering
import matplotlib.patches as patches # Chosen for precise structural primitives (Circles, Bounding Boxes)
import os # Chosen for robust directory management and path-specific file saving

def create_quantum_of_action_schematic():
    # Enforce clear, publication-ready font settings
    plt.rcParams.update({
        'savefig.pad_inches': 0.05,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'mathtext.fontset': 'cm', # Ensures math symbols render cleanly in standard Computer Modern italics
        'font.size': 12
    })
    
    # Established color palette for visual logic integration
    light_gray_fill = '#F5F5F5'  # Original Solid Scaffold fill
    active_cyan_edge = '#00CCFF' # Boundary of the Interstitial field (Electric Blue)
    navy_blue_kinematics = '#000080' # Established color for transverse/chiral kinetics
    
    # Initialize diagram canvas (Perfect square for balanced rotational geometry)
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    ax.set_facecolor('white')
    
    # Absolute coordinate system mapping
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # =======================================================
    # 1. THE SOFT FLOOR NODE (Center)
    # =======================================================
    center_x, center_y = 50, 55
    R_node = 20
    
    # Render the localized node (Original gray fill with Cyan active perimeter)
    node = patches.Circle((center_x, center_y), R_node, 
                          facecolor=light_gray_fill, 
                          edgecolor=active_cyan_edge, lw=3.0, zorder=2)
    ax.add_patch(node)
    
    # Center anchor dot
    ax.plot(center_x, center_y, 'ko', markersize=5, zorder=3)
    
    # Internal Density Label (Strictly upright descriptive subscript)
    ax.text(center_x - 3, center_y + 3, r"$\rho_{\mathrm{D}}$", fontsize=18, ha='center', va='center', color='black', zorder=3)
    
    # Internal Radius Vector
    ax.annotate("", xy=(center_x + R_node, center_y), xytext=(center_x, center_y),
                arrowprops=dict(arrowstyle="->", lw=1.5, color='black'), zorder=3)
    ax.text(center_x + R_node/2, center_y + 1.5, r"$r_{\mathrm{D}}$", fontsize=16, ha='center', va='bottom', color='black', zorder=3)

    # =======================================================
    # 2. ORBITAL KINEMATICS (The Speed Limit Sweep)
    # =======================================================
    R_orbit = 28
    
    # Parametric sweep from bottom-left (225 deg), over the top, to bottom-right (-45 deg)
    t = np.linspace(np.radians(225), np.radians(-45), 200)
    arc_x = center_x + R_orbit * np.cos(t)
    arc_y = center_y + R_orbit * np.sin(t)
    
    # Draw the orbital path (Updated to Black)
    ax.plot(arc_x, arc_y, color='black', lw=4.0, zorder=1)
    
    # Attach arrowhead at the terminal point of the sweep (Black)
    dx = arc_x[-1] - arc_x[-2]
    dy = arc_y[-1] - arc_y[-2]
    ax.arrow(arc_x[-2], arc_y[-2], dx, dy, shape='full', lw=0, length_includes_head=True, 
             head_width=3.5, head_length=4.5, color='black', zorder=1)
             
    # Orbital Label (Proper math italics for c_E with upright subscript)
    ax.text(center_x, center_y + R_orbit + 2, r"$\mathbf{Kinematic\ Speed\ Limit}$ ($c_{\mathrm{E}}$)", 
            ha='center', va='bottom', fontsize=14, color='black', zorder=4)

    # =======================================================
    # 3. THE INVARIANT (Terminal Point of Rotation)
    # =======================================================
    inv_x = arc_x[-1] + 1.0 
    inv_y = arc_y[-1] - 0.6
    
    jd_eq = r"$J_{\mathrm{D}} = \rho_{\mathrm{D}} r_{\mathrm{D}}^4$"
    ax.text(inv_x, inv_y, jd_eq, ha='center', va='top', fontsize=18, color='black', zorder=5)

    # Secondary action label placed strictly below the equation
    ax.text(inv_x, inv_y - 4.0, "(Soft Floor Torsion)", ha='center', va='top', fontsize=12, color='black', zorder=5)

    # =======================================================
    # 4. THE MASTER EQUATION (Bottom Center)
    # =======================================================
    h_eq = r"$h = 2\pi \cdot J_{\mathrm{D}} \cdot c_{\mathrm{E}}$"
    
    ax.text(50, 15, h_eq, ha='center', va='center', fontsize=26, color='black', zorder=10)

    # =======================================================
    # 5. EXPORT LOGIC
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig04_PartI_QuantumAction.pdf")
    
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
    create_quantum_of_action_schematic()