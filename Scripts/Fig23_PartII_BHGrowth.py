import numpy as np # Selected for efficient trigonometric mapping and radial array generation
import matplotlib.pyplot as plt # Selected for precise 2D vector graphic control and native LaTeX text rendering
import matplotlib.patches as patches # Selected for rendering distinct structural zones (Circles, Arrows, Polygons)
import os # Selected for robust directory management and path-specific file saving

def create_black_hole_rupture_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    # Setup Figure (Full Bleed, High-Contrast Architectural Styling)
    fig, ax = plt.subplots(figsize=(14, 14), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # -------------------------------------------------------
    # PARAMETERS & SCALING (Logarithmic/Symbolic Representation)
    # -------------------------------------------------------
    R_core = 3.0   # 10^26 m (Saturated Core)
    R_res = 8.0    # 10^35 m (Cosmic Reservoir)
    limit = 10.0   # Infinite Canvas Boundary
    block_size = 0.4 # Background cubic grid scaling
    
    # Calculate the 2/3 distance mark between Core and Reservoir
    r_two_thirds = R_core + (2.0 / 3.0) * (R_res - R_core)
    
    # -------------------------------------------------------
    # LAYER 1: THE INFINITE CANVAS (State 0 / Latent Substrate)
    # -------------------------------------------------------
    # A faint, infinite 2D square grid bleeding completely off the edges.
    # The generation bounds are extended well past the visible limits (+/- 15) 
    # to guarantee the top horizontal lines perfectly close the grid even after aspect-ratio scaling.
    grid_ticks = np.arange(-15.0, 15.0, block_size)
    for t in grid_ticks:
        ax.axhline(t, color='#E8E8E8', lw=0.35, alpha=0.6, zorder=0)
        ax.axvline(t, color='#E8E8E8', lw=0.35, alpha=0.6, zorder=0)

    # State 0 Anchor Label (Standard capitalization, anchored to bottom-left corner)
    ax.text(-limit + 0.3, -limit + 0.3, "State 0 Substrate\n(Omnipresent)", 
            color='#777777', fontsize=12, fontweight='bold', ha='left', va='bottom', zorder=10)

    # -------------------------------------------------------
    # LAYER 4: THE SATURATED CORE (State II / SC Geometry)
    # -------------------------------------------------------
    # Solid dark-grey circle
    core_color = '#2F3640'
    core_circle = patches.Circle((0, 0), R_core, facecolor=core_color, edgecolor='none', zorder=2)
    ax.add_patch(core_circle)
    
    # Internal SC Grid (Darker, tighter orthogonal lines perfectly clipped to the core boundary)
    sc_ticks = np.arange(-R_core, R_core, 0.3)
    for t in sc_ticks:
        h_line, = ax.plot([-R_core, R_core], [t, t], color='#111111', lw=1.2, zorder=3)
        v_line, = ax.plot([t, t], [-R_core, R_core], color='#111111', lw=1.2, zorder=3)
        h_line.set_clip_path(core_circle)
        v_line.set_clip_path(core_circle)

    # Saturated Core Finite Mechanical Limits (Stacked in dead center)
    core_text = (r"State II Saturated Core" + "\n" + 
                 r"$\rho_S \approx 10^{96} \text{ kg/m}^3$" + "\n" + 
                 r"$\tau_S \approx 10^{112} \text{ N/m}^2$")
    ax.text(0, 0, core_text, color='white', fontsize=11, fontweight='bold', ha='center', va='center', zorder=10)

    # -------------------------------------------------------
    # LAYER 5: THE ACTION (Contiguous Layer & Diluted Void Fill)
    # -------------------------------------------------------
    # Reduced density to 32 elements to massively increase the size of the nodes and voids
    num_elements = 32
    angles = np.linspace(0, 2 * np.pi, num_elements, endpoint=False)
    angle_step = 2 * np.pi / num_elements
    
    # Exact trigonometric derivation ensures the FCC nodes physically touch the Core AND adjacent spheres
    fcc_radius = R_core * np.sin(angle_step / 2) / (1 - np.sin(angle_step / 2))
    R1 = R_core + fcc_radius

    # Matter color updated to red for high visibility
    matter_color = '#CC0000' 

    for idx, angle in enumerate(angles):
        dx = np.cos(angle)
        dy = np.sin(angle)

        # 1. PRIMARY ADVANCING FCC NODE (Active Vacuum Layer)
        # alpha=1.0 ensures absolute occlusion, preventing underlying polygons from bleeding through
        ax.add_patch(patches.Circle((R1 * dx, R1 * dy), fcc_radius, 
                                    facecolor='#00E0FF', edgecolor='#0055AA', lw=0.8, alpha=1.0, zorder=6))

        # 2. ALTERNATING MATTER NUCLEATION (50% Void Fill)
        # Drawn directly from the origin to ensure a 100% solid color fill with no gaps.
        # The Core and FCC nodes sit on top of this polygon, punching out the perfect curved negative space.
        if idx % 2 == 0:
            next_angle = angles[(idx + 1) % num_elements]
            v1 = (0, 0)
            v2 = (R1 * np.cos(angle), R1 * np.sin(angle))
            v3 = (R1 * np.cos(next_angle), R1 * np.sin(next_angle))

            void_poly = patches.Polygon([v1, v2, v3], closed=True, facecolor=matter_color, edgecolor='none', zorder=1.5)
            ax.add_patch(void_poly)

        # 3. AMBIENT CONFINEMENT PRESSURE (Inward-Pointing Arrows)
        # Drawn every 4th element to prevent visual crowding of the scaled-down nodes
        if idx % 4 == 0:
            arrow_start_r = R1 + fcc_radius + 0.8
            arrow_len = 0.8  
            
            # Added length_includes_head=True so the arrow tip lands exactly on the FCC node outer boundary
            ax.arrow(arrow_start_r * dx, arrow_start_r * dy, 
                     -arrow_len * dx, -arrow_len * dy, 
                     head_width=0.3, head_length=0.4, fc='#2F3640', ec='#222222', 
                     lw=1.5, zorder=5, length_includes_head=True)

    # -------------------------------------------------------
    # BOUNDARY TRIGGERS (Phase Transition Conditions)
    # -------------------------------------------------------
    # Keep the text label starting positions anchored to the original gap angle
    gap_angle_orig = np.pi / num_elements  
    
    r_start = R_core + 2.5
    start_x = r_start * np.cos(gap_angle_orig)
    start_y = r_start * np.sin(gap_angle_orig)
    
    # Decoupled targeting: Shift arrow tip 1 void UP (counter-clockwise) into the adjacent empty blank space
    gap_angle_target = gap_angle_orig + angle_step
    target_x = R_core * np.cos(gap_angle_target)
    target_y = R_core * np.sin(gap_angle_target)
    
    # Draw indicator line with a gentle arc to visually bypass the intermediate FCC node
    ax.annotate("", xy=(target_x, target_y), xytext=(start_x, start_y),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5, connectionstyle="arc3,rad=0.2"), zorder=11)

    eq_text = (r"$R_{QG} \approx 10^{26}\ \mathrm{m}$" + "\n" + 
               r"$g \approx a_D$" + "\n" + 
               r"$\Delta P \approx 0$")
               
    ax.text(start_x + 0.2, start_y + 0.3, eq_text,
            color='black', fontsize=11, fontweight='bold', ha='left', va='top', zorder=11)

    # -------------------------------------------------------
    # LAYER 2 & 3: COSMIC RESERVOIR & DEPLETED ZONE LABELS
    # -------------------------------------------------------
    # The Reservoir Boundary
    res_circle = patches.Circle((0, 0), R_res, fill=False, edgecolor='#888888', linestyle='--', lw=2.5, zorder=1)
    ax.add_patch(res_circle)
    
    ax.text(0, R_res + 0.2, r"Cosmic Reservoir Limit ($\approx 10^{35}$ m)", 
            color='#333333', fontsize=12, fontweight='bold', ha='center', va='bottom', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=3), zorder=10)
            
    ax.text(0, r_two_thirds, "Exposed State 0 Substrate\n(Harvested Zone)", 
            color='#333333', fontsize=11, fontweight='bold', ha='center', va='center', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=3), zorder=10)

    # -------------------------------------------------------
    # TARGETED ANNOTATIONS
    # -------------------------------------------------------
    # State I Active Vacuum Annotation
    idx_vac_orig = int(num_elements * 3 / 8) # Approx 135 degrees
    angle_vac_orig = angles[idx_vac_orig]
    
    # Original text box anchor coordinate
    orig_x_vac = R1 * np.cos(angle_vac_orig)
    orig_y_vac = R1 * np.sin(angle_vac_orig)
    lbl_x_vac = orig_x_vac - 3.5
    lbl_y_vac = orig_y_vac + 1.2
    
    # Decoupled targeting: Shift arrow tip 2 nodes DOWN (clockwise)
    idx_vac_target = (idx_vac_orig - 2) % num_elements
    angle_vac_target = angles[idx_vac_target]
    target_x_vac = R1 * np.cos(angle_vac_target)
    target_y_vac = R1 * np.sin(angle_vac_target)
    
    ax.annotate(r"State I Active Vacuum" + "\n" + r"FCC Node ($r_D \approx 10^{-26}\ \mathrm{m}$)",
                xy=(target_x_vac, target_y_vac), 
                xytext=(lbl_x_vac, lbl_y_vac),
                arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2, connectionstyle="arc3,rad=-0.15"),
                color='#222222', fontsize=11, fontweight='bold', ha='right', va='center',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=3), zorder=12)

    # Diluted Phase Segregated Matter Annotation
    idx_mat = int(num_elements * 7 / 8) # Approx 315 degrees
    if idx_mat % 2 != 0: idx_mat += 1 # Ensure it targets a void filled with matter
    
    angle_mat = angles[idx_mat]
    next_angle_mat = angles[(idx_mat + 1) % num_elements]
    mid_angle_mat = angle_mat + angle_step / 2
    
    target_fill_x = (R1 * np.cos(angle_mat) + R1 * np.cos(next_angle_mat) + R_core * np.cos(mid_angle_mat)) / 3
    target_fill_y = (R1 * np.sin(angle_mat) + R1 * np.sin(next_angle_mat) + R_core * np.sin(mid_angle_mat)) / 3

    # Modified ha='center' for precision alignment, adjusted x-shift to +4.0
    ax.annotate(r"Phase Segregated Matter" + "\n" + r"($M \propto R_{QG}$)",
                xy=(target_fill_x, target_fill_y),
                xytext=(target_fill_x + 4.0, target_fill_y - 1.2),
                arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2, connectionstyle="arc3,rad=-0.15"),
                color='#222222', fontsize=10, fontweight='bold', ha='center', va='center', 
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3), zorder=12)

    # -------------------------------------------------------
    # STYLING & FORMATTING
    # -------------------------------------------------------
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    ax.set_aspect('equal')
    
    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig23_PartII_BHGrowth.pdf")
    
    try:
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()

if __name__ == "__main__":
    create_black_hole_rupture_visual()