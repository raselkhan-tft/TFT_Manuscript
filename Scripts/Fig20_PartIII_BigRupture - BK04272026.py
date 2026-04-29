import numpy as np # Selected for efficient trigonometric mapping and radial array generation
import matplotlib.pyplot as plt # Selected for precise 2D vector graphic control and native LaTeX text rendering
import matplotlib.patches as patches # Selected for rendering distinct structural zones (Circles, Arrows)
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
    core_circle = patches.Circle((0, 0), R_core, facecolor='#2F3640', edgecolor='none', zorder=2)
    ax.add_patch(core_circle)
    
    # Internal SC Grid (Darker, tighter orthogonal lines perfectly clipped to the core boundary)
    sc_ticks = np.arange(-R_core, R_core, 0.3)
    for t in sc_ticks:
        # Using set_clip_path ensures mathematical smoothness at the circular boundary
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
    # BOUNDARY TRIGGERS (Phase Transition Conditions)
    # -------------------------------------------------------
    # The expanding ruptures occur at 45 degree intervals (0, 45, 90).
    # To pass perfectly through the 50% gap, the angle must be exactly 22.5 degrees (pi/8).
    gap_angle = np.pi / 8  
    
    # Arrow exactly targets the core boundary along the radial line
    target_x = R_core * np.cos(gap_angle)
    target_y = R_core * np.sin(gap_angle)
    
    # Arrow starts midway between core and reservoir
    r_start = 5.5
    start_x = r_start * np.cos(gap_angle)
    start_y = r_start * np.sin(gap_angle)
    
    # Draw indicator line (Passes perfectly symmetrically through the gap)
    ax.annotate("", xy=(target_x, target_y), xytext=(start_x, start_y),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5), zorder=11)

    # Mathematical Triggers (Position held strictly constant)
    eq_text = (r"$R_{QC} \approx 10^{26}\ \mathrm{m}$" + "\n" + 
               r"$g \approx a_D$" + "\n" + 
               r"$\Delta P \approx 0$")
               
    # By using va='bottom', the y-coordinate represents the baseline of the bottom line (\Delta P).
    ax.text(start_x + 0.1, start_y - 0.05, eq_text,
            color='black', fontsize=11, fontweight='bold', ha='left', va='bottom', zorder=11)
            
    # Title Text (Decoupled: Pushed 2.25 blocks left and 1/3 block up from its original base position)
    title_x = start_x - 0.5 - (2.25 * block_size)
    title_y = start_y + 0.8 + (block_size / 3.0)
    ax.text(title_x, title_y, "Phase Transition Triggers", 
            color='black', fontsize=11, fontweight='bold', ha='left', va='bottom', zorder=11)

    # -------------------------------------------------------
    # LAYER 2 & 3: COSMIC RESERVOIR & DEPLETED ZONE LABELS
    # -------------------------------------------------------
    # The Reservoir Boundary
    res_circle = patches.Circle((0, 0), R_res, fill=False, edgecolor='#888888', linestyle='--', lw=2.5, zorder=1)
    ax.add_patch(res_circle)
    
    # Reservoir Label (Darkened text with white bounding box for PRL-style readability)
    ax.text(0, R_res + 0.2, r"Cosmic Reservoir Limit ($\approx 10^{35}$ m)", 
            color='#333333', fontsize=12, fontweight='bold', ha='center', va='bottom', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=3), zorder=10)
            
    # Depleted Zone Label (Exposed State 0)
    ax.text(0, r_two_thirds, "Exposed State 0 Substrate\n(Harvested Zone)", 
            color='#333333', fontsize=11, fontweight='bold', ha='center', va='center', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=3), zorder=10)

    # Catastrophic Decompression Label (Switched from aggressive red to austere dark slate)
    ax.text(0, -r_two_thirds, "Catastrophic Decompression\n(Restoring the State I FCC Vacuum)", 
            color='#222222', fontsize=11, fontweight='bold', ha='center', va='center', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=3), zorder=10)

    # -------------------------------------------------------
    # LAYER 5: THE ACTION (Catastrophic Decompression)
    # -------------------------------------------------------
    # Radial vectors representing the rupture and outward expansion
    num_ruptures = 8
    angles = np.linspace(0, 2 * np.pi, num_ruptures, endpoint=False)

    for idx, angle in enumerate(angles):
        dx = np.cos(angle)
        dy = np.sin(angle)
        
        # Draw "Shattering" Cracks on the Core Boundary (Explicitly dashed and top-layered for high visibility)
        ax.plot([R_core * 0.85 * dx, R_core * 1.15 * dx], 
                [R_core * 0.85 * dy, R_core * 1.15 * dy], 
                color='white', linestyle='--', lw=3.5, zorder=6)

        # Heavy Outward-Pointing Arrows (The Burst) - Changed to austere dark gray/black
        arrow_start_r = R_core * 0.9
        arrow_len = 0.95  
        ax.arrow(arrow_start_r * dx, arrow_start_r * dy, 
                 arrow_len * dx, arrow_len * dy, 
                 head_width=0.4, head_length=0.5, fc='#2F3640', ec='#222222', lw=3, zorder=5)

        # Restoring the State I FCC Vacuum (Cyan blue geometry being dragged outward)
        fcc_r = arrow_start_r + arrow_len + 0.6
        fcc_radius = 0.5
        
        # Primary advancing FCC node
        ax.add_patch(patches.Circle((fcc_r * dx, fcc_r * dy), fcc_radius, 
                                    facecolor='#00E0FF', edgecolor='#0055AA', lw=1.5, alpha=0.9, zorder=6))
        # Adjacent supporting nodes to simulate a lattice front
        perp_dx, perp_dy = np.cos(angle + np.pi/2), np.sin(angle + np.pi/2)
        ax.add_patch(patches.Circle((fcc_r * dx + 0.9 * perp_dx, fcc_r * dy + 0.9 * perp_dy), fcc_radius, 
                                    facecolor='#00E0FF', edgecolor='#0055AA', lw=1.5, alpha=0.9, zorder=6))
        ax.add_patch(patches.Circle((fcc_r * dx - 0.9 * perp_dx, fcc_r * dy - 0.9 * perp_dy), fcc_radius, 
                                    facecolor='#00E0FF', edgecolor='#0055AA', lw=1.5, alpha=0.9, zorder=6))
        
        # --- NEW: State I Active Vacuum Annotation (Upper-Left Quadrant) ---
        if np.isclose(angle, 3 * np.pi / 4): # 135 degrees
            lbl_r = fcc_r + 2.0
            # Target the outer edge of the sphere to prevent the arrow from intruding
            target_r = fcc_r + fcc_radius + 0.05
            
            ax.annotate("State I Active Vacuum (FCC)",
                        xy=(target_r * dx, target_r * dy), 
                        xytext=(lbl_r * dx, lbl_r * dy),
                        arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2, connectionstyle="arc3,rad=-0.15"),
                        color='#222222', fontsize=11, fontweight='bold', ha='right', va='bottom',
                        bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=3), zorder=12)

        # --- SEEDING MATTER FORMATION (Topological Phase Defects) ---
        # Draw tiny geometric knots attached to alternating spheres to represent vorticity
        if idx % 2 == 0:
            t_knot = np.linspace(0, 2 * np.pi, 150)
            knot_scale = 0.18
            
            # Parametric Lissajous knot (locked vorticity loop)
            kx = knot_scale * np.sin(3 * t_knot + np.pi/4)
            ky = knot_scale * np.sin(2 * t_knot)
            
            # Rotate knot to naturally trail or bridge the expansion front
            kx_rot = kx * np.cos(angle) - ky * np.sin(angle)
            ky_rot = kx * np.sin(angle) + ky * np.cos(angle)
            
            # Attach exactly to the outer leading edge of the primary sphere
            knot_cx = fcc_r * dx + 0.45 * dx
            knot_cy = fcc_r * dy + 0.45 * dy
            
            # Draw the twisted defect line
            ax.plot(knot_cx + kx_rot, knot_cy + ky_rot, color='#222222', lw=1.2, alpha=0.85, zorder=8)
            
            # Annotate exactly ONE knot to formally introduce the concept (Right-side horizontal knot)
            if np.isclose(angle, 0):
                # Applied white bbox masking to ensure text cuts clearly through the dotted reservoir line
                ax.annotate("Topological Phase Defects\n(Locked Vorticity / Matter)",
                            xy=(knot_cx + knot_scale, knot_cy),
                            xytext=(knot_cx + 2.0, knot_cy - 0.6),
                            arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2, connectionstyle="arc3,rad=-0.15"),
                            color='#222222', fontsize=10, fontweight='bold', ha='left', va='center', 
                            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3), zorder=12)

    # -------------------------------------------------------
    # STYLING & FORMATTING
    # -------------------------------------------------------
    # Strip axes to enforce the "Infinite Canvas" look
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Absolute framing and layout calculation
    ax.set_aspect('equal')
    
    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig20_PartIII_BigRupture.pdf")
    
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
    create_black_hole_rupture_visual()