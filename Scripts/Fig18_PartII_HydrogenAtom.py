import numpy as np # Selected for non-linear coordinate transformations and vector math
import matplotlib.pyplot as plt # Selected for publication-grade 2D diagrammatic composition
import matplotlib.patches as patches # Selected for rendering structural shells, anchors, and callouts
import os # Selected for robust directory management and path-specific file saving

def create_tft_atom_blueprint_final():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 10
    })
    
    # Initialize diagram canvas
    fig, ax = plt.subplots(figsize=(14, 12), dpi=150)
    ax.set_facecolor('white')
    
    # Setup coordinate system [0, 100]
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    center = np.array([50, 50])
    shell_radius = 36
    rm_radius = 24 # The lower kinetic shell radius
    
    # Fixed positions for magnification levels
    p_zoom_pos = (15, 80)
    e_zoom_pos = (15, 15)
    
    # High-visibility mask properties for all text labels
    mask_props = dict(facecolor='white', edgecolor='none', alpha=0.9, boxstyle='round,pad=0.5')

    # =======================================================
    # BACKGROUND: Warped Soft Floor FCC Lattice
    # =======================================================
    num_lines = 41
    grid_range = np.linspace(0, 100, num_lines)
    
    def transform_point(p):
        r_vec = p - center
        r = np.linalg.norm(r_vec)
        if r > shell_radius or r < 0.1:
            return p
        strength = 0.4 * (1 - r/shell_radius)
        angle = strength * np.log(r / shell_radius)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        rot = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
        return center + rot.dot(r_vec)

    line_res = 200
    for val in grid_range:
        pts_v = np.column_stack((np.full(line_res, val), np.linspace(0, 100, line_res)))
        transformed_v = np.array([transform_point(p) for p in pts_v])
        # Grid line opacity dropped to 10% (alpha=0.1) for a faint, clean background
        ax.plot(transformed_v[:, 0], transformed_v[:, 1], color='#E0E0E0', lw=0.6, alpha=0.1, zorder=0)
        
        pts_h = np.column_stack((np.linspace(0, 100, line_res), np.full(line_res, val)))
        transformed_h = np.array([transform_point(p) for p in pts_h])
        # Grid line opacity dropped to 10% (alpha=0.1)
        ax.plot(transformed_h[:, 0], transformed_h[:, 1], color='#E0E0E0', lw=0.6, alpha=0.1, zorder=0)

    # =======================================================
    # ZONE 2: Electron Resonant Boundaries
    # =======================================================
    for r_offset in np.linspace(0, 1.5, 8):
        # Boundary rings standardized to Deep Navy Blue
        circle = patches.Circle(center, shell_radius + r_offset, 
                                facecolor='none', edgecolor='#000080', 
                                alpha=0.1, lw=2, zorder=1)
        ax.add_patch(circle)

    dashed_shell = patches.Circle(center, rm_radius, fill=False, 
                                  edgecolor='#777777', ls='--', alpha=0.5, lw=1.2, zorder=1)
    ax.add_patch(dashed_shell)
    
    rm_angle = np.radians(340)
    ax.text(50 + rm_radius * np.cos(rm_angle), 50 + rm_radius * np.sin(rm_angle), 
            r"$r_m$ (Lower Shell)", color='black', ha='center', va='center', 
            fontsize=9, bbox=mask_props, zorder=20)

    drop_x = 50
    ax.annotate("", xy=(drop_x, 50 - rm_radius), xytext=(drop_x, 50 - shell_radius),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.0), zorder=10)
    ax.text(drop_x + 1, 50 - (rm_radius + shell_radius)/2, r"$\Delta r$ (The Drop)", 
            va='center', ha='left', family='serif', color='black', fontweight='normal', bbox=mask_props, zorder=30)

    # -------------------------------------------------------
    # Electron Core and Tail Dynamics
    # -------------------------------------------------------
    t_wake_start = 45 
    core_x = 50 + shell_radius * np.cos(np.radians(t_wake_start))
    core_y = 50 + shell_radius * np.sin(np.radians(t_wake_start))
    
    e_radius = 0.8 # Exactly halved from original 1.6
    R_main = e_radius * 0.65
    
    # Dynamic Electron Wake (Offset so it touches the ring but does not penetrate it)
    wake_angle_span = 260 
    line_cap_buffer = 0.12 # Accounting for the geometric bleed of the lw=4.0 stroke cap
    angular_offset_deg = np.degrees((R_main + line_cap_buffer) / shell_radius)
    t_wake_end = t_wake_start - angular_offset_deg
    t_wake = np.linspace(t_wake_end - wake_angle_span, t_wake_end, 600)
    rad_t = np.radians(t_wake)
    
    # Wake color standardized to Deep Navy Blue
    wake_color = '#000080'
    for i in range(len(t_wake) - 1):
        alpha_val = (i / len(t_wake))**2.5 
        ax.plot([50 + shell_radius * np.cos(rad_t[i]), 50 + shell_radius * np.cos(rad_t[i+1])],
                [50 + shell_radius * np.sin(rad_t[i]), 50 + shell_radius * np.sin(rad_t[i+1])],
                color=wake_color, lw=4.0, alpha=alpha_val, zorder=2)

    # Electron Mass Core (Single Maroon Hollow Ring)
    t_ring = np.linspace(0, 2 * np.pi, 200)
    ring_x = core_x + R_main * np.cos(t_ring)
    ring_y = core_y + R_main * np.sin(t_ring)
    
    ax.plot(ring_x, ring_y, color='#8B0000', lw=2.5, zorder=15)
    
    # r_amp Leader (Originates exactly from the outer edge of the ring)
    ramp_angle = np.arctan2(5, 5) # 45 degrees towards the text box
    ramp_edge_x = core_x + R_main * np.cos(ramp_angle)
    ramp_edge_y = core_y + R_main * np.sin(ramp_angle)
    
    ax.annotate(r"Electron Core ($r_{\mathrm{amp}}$)", 
                xy=(ramp_edge_x, ramp_edge_y), xytext=(core_x + 5, core_y + 5),
                arrowprops=dict(arrowstyle="->", color="black", lw=0.8),
                color='black', family='serif', fontweight='bold', zorder=25,
                bbox=mask_props)

    # --- KINETIC EQUILIBRIUM VECTORS (Originating exactly at the perimeter) ---
    tangent_angle = np.radians(t_wake_start + 90)
    v_len = 12
    v_start_x = core_x + R_main * np.cos(tangent_angle)
    v_start_y = core_y + R_main * np.sin(tangent_angle)
    
    ax.annotate("", xy=(core_x + v_len * np.cos(tangent_angle), core_y + v_len * np.sin(tangent_angle)),
                xytext=(v_start_x, v_start_y),
                arrowprops=dict(arrowstyle="->", color="#000080", lw=1.5), zorder=16)
    ax.text(core_x + v_len * np.cos(tangent_angle), core_y + v_len * np.sin(tangent_angle) + 1, 
            r"$v_n$", color='black', fontsize=12, fontweight='bold', ha='center',
            bbox=mask_props, zorder=25)

    f_len = 10
    rad_start = np.radians(t_wake_start)
    f_start_x = core_x - R_main * np.cos(rad_start)
    f_start_y = core_y - R_main * np.sin(rad_start)
    
    ax.annotate("", xy=(core_x - f_len * np.cos(rad_start), core_y - f_len * np.sin(rad_start)),
                xytext=(f_start_x, f_start_y),
                arrowprops=dict(arrowstyle="->", color="#8B0000", lw=1.5), zorder=16)
    ax.text(core_x - (f_len+2) * np.cos(rad_start), core_y - (f_len+2) * np.sin(rad_start), 
            r"$\mathbf{F}_\chi$", color='black', fontsize=12, fontweight='bold', ha='center',
            bbox=mask_props, zorder=25)

    # =======================================================
    # ZONE 1: Nucleus (The Torsional Anchor)
    # =======================================================
    nucleus_radius = 2.8
    
    # Generate the Compact Rosette Core (Dense Nucleon Lattice)
    def draw_dense_lobe(ax, cx, cy, angle, inner_radius=0.4, outer_reach=2.8):
        t = np.linspace(0, 2 * np.pi, 200)
        A = (outer_reach - inner_radius) / 2.0
        B = A * 0.8  
        x_center_offset = inner_radius + A
        x_base = x_center_offset + A * np.cos(t)
        y_base = B * np.sin(t) * (1.0 - 0.4 * np.cos(t))
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        x_rot = cx + (x_base * cos_a - y_base * sin_a)
        y_rot = cy + (x_base * sin_a + y_base * cos_a)
        
        # Solid Body Fill (Opaque pale maroon)
        ax.fill(x_rot, y_rot, color='#FFDDDD', alpha=0.95, zorder=10)
        # Outer Ribbon (Muted Maroon)
        ax.plot(x_rot, y_rot, color='#8B0000', lw=1.0, zorder=11)

    # Line density reduced by 25% (60 -> 45) to preserve woven visibility at scale
    num_nodes = 45
    for i in range(num_nodes):
        angle = i * (2 * np.pi / num_nodes)
        draw_dense_lobe(ax, center[0], center[1], angle, inner_radius=0.3, outer_reach=nucleus_radius)
    
    # Nucleon Label
    ax.annotate("Hyper-Dense Nucleon Anchor", 
                xy=(50, 50 - nucleus_radius), xytext=(50, 43.0),
                arrowprops=dict(arrowstyle="->", color="#8B0000", lw=1.5, alpha=0.8),
                ha='center', va='top', color='black', fontsize=10, fontweight='bold', bbox=mask_props, zorder=20, family='serif')

    # Proton Chiral Field (Outward Propagation, Inward Pull)
    p_angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
    p_zoom_coord = None
    min_dist_p = float('inf')

    for i, angle_start in enumerate(p_angles):
        t_spiral = np.linspace(nucleus_radius, shell_radius, 200)
        twist_factor = 0.5
        spiral_x = center[0] + t_spiral * np.cos(angle_start + twist_factor * np.log(t_spiral))
        spiral_y = center[1] + t_spiral * np.sin(angle_start + twist_factor * np.log(t_spiral))
        
        segs = 10
        chunk = len(t_spiral) // segs
        for s in range(segs):
            idx = s * chunk
            lw_taper = 3.0 * (1 - (s/segs)) + 0.5
            # Color standardized to Muted Maroon
            ax.plot(spiral_x[idx:idx+chunk+1], spiral_y[idx:idx+chunk+1], 
                    color='#8B0000', alpha=0.3, lw=lw_taper, zorder=5)

        ax.annotate("", xy=(spiral_x[-1], spiral_y[-1]), 
                    xytext=(spiral_x[-5], spiral_y[-5]),
                    arrowprops=dict(arrowstyle="->", color="#8B0000", lw=1.2, alpha=0.6), zorder=6)
        
        if i == 1:
            ax.text(spiral_x[-1] + 1.5, spiral_y[-1] + 1.5, r"$\chi(+1), +\hat{r}$", 
                    color='black', fontsize=9, fontweight='bold', bbox=mask_props, zorder=21)
        elif i == 7:
            ax.text(spiral_x[-1] - 2.0, spiral_y[-1] + 2.0, r"$\chi(+1), +\hat{r}$", 
                    color='black', fontsize=9, fontweight='bold', bbox=mask_props, zorder=21, ha='right')

        for r_frac in [0.4, 0.7]:
            idx_tick = int(len(t_spiral) * r_frac)
            tangent_vec = np.array([spiral_x[idx_tick+1]-spiral_x[idx_tick-1], 
                                    spiral_y[idx_tick+1]-spiral_y[idx_tick-1]])
            ang_deg = np.degrees(np.arctan2(tangent_vec[1], tangent_vec[0]))
            ax.text(spiral_x[idx_tick], spiral_y[idx_tick], r"$\ll$", 
                    color="#8B0000", fontsize=8, rotation=ang_deg, 
                    ha='center', va='center', alpha=0.6, zorder=7)
            
            d = np.sqrt((spiral_x[idx_tick] - p_zoom_pos[0])**2 + (spiral_y[idx_tick] - p_zoom_pos[1])**2)
            if d < min_dist_p:
                min_dist_p = d
                p_zoom_coord = (spiral_x[idx_tick], spiral_y[idx_tick], ang_deg)

    # =======================================================
    # ZONE 3: Internal Electron Field
    # =======================================================
    e_angles = np.linspace(np.pi/12, 2*np.pi + np.pi/12, 8, endpoint=False)
    e_zoom_coord = None
    min_dist_e = float('inf')

    for i, angle_start in enumerate(e_angles):
        t_in = np.linspace(shell_radius, nucleus_radius + 6, 150)
        twist_in = -0.4 
        spiral_x_in = center[0] + t_in * np.cos(angle_start + twist_in * np.log(t_in))
        spiral_y_in = center[1] + t_in * np.sin(angle_start + twist_in * np.log(t_in))
        
        segs = 8
        chunk = len(t_in) // segs
        for s in range(segs):
            idx = s * chunk
            lw_taper = 2.5 * (1 - (s/segs)) + 0.4
            # Color standardized to Deep Navy Blue
            ax.plot(spiral_x_in[idx:idx+chunk+1], spiral_y_in[idx:idx+chunk+1], 
                    color='#000080', alpha=0.2, lw=lw_taper, zorder=4)
        
        ax.annotate("", xy=(spiral_x_in[-1], spiral_y_in[-1]), 
                    xytext=(spiral_x_in[-5], spiral_y_in[-5]),
                    arrowprops=dict(arrowstyle="->", color="#000080", lw=1.0, alpha=0.4), zorder=5)

        if i == 1: # Upper Side
            ax.text(spiral_x_in[115], spiral_y_in[115], r"$\chi(-1), -\hat{r}$", 
                    color='black', fontsize=9, fontweight='bold', bbox=mask_props, zorder=21)
        elif i == 6: # Lower Side
            ax.text(spiral_x_in[115], spiral_y_in[115], r"$\chi(-1), -\hat{r}$", 
                    color='black', fontsize=9, fontweight='bold', bbox=mask_props, zorder=21)
        
        for r_frac in [0.3, 0.6]:
            idx_tick = int(len(t_in) * r_frac)
            tangent_vec = np.array([spiral_x_in[idx_tick-1]-spiral_x_in[idx_tick+1],
                                    spiral_y_in[idx_tick-1]-spiral_y_in[idx_tick+1]])
            ang_deg = np.degrees(np.arctan2(tangent_vec[1], tangent_vec[0]))
            ax.text(spiral_x_in[idx_tick], spiral_y_in[idx_tick], r"$\gg$", 
                    color="#000080", fontsize=7, rotation=ang_deg, 
                    ha='center', va='center', alpha=0.5, zorder=5)
            
            d = np.sqrt((spiral_x_in[idx_tick] - e_zoom_pos[0])**2 + (spiral_y_in[idx_tick] - e_zoom_pos[1])**2)
            if d < min_dist_e:
                min_dist_e = d
                e_zoom_coord = (spiral_x_in[idx_tick], spiral_y_in[idx_tick], ang_deg)

    # =======================================================
    # MAGNIFICATION CALLOUTS
    # =======================================================
    # 1. Nucleon Inward Pull (Top-Left)
    ax.text(p_zoom_pos[0], p_zoom_pos[1], "Nucleon's Inward Pull", 
            color='black', ha='center', va='center', fontweight='bold', zorder=23, bbox=mask_props)
    
    # Gap offset reduced from 3 to 1.5
    ax.annotate("", xy=(p_zoom_coord[0], p_zoom_coord[1]), xytext=(p_zoom_pos[0], p_zoom_pos[1] - 1.5), 
                arrowprops=dict(arrowstyle="->", color="#8B0000", lw=1.5, alpha=0.8), zorder=21)

    # 2. Electron Outward Pull (Bottom-Left)
    ax.text(e_zoom_pos[0], e_zoom_pos[1], "Electron's Outward Pull", 
            color='black', ha='center', va='center', fontweight='bold', zorder=23, bbox=mask_props)
            
    # Gap offset reduced from 3 to 1.5
    ax.annotate("", xy=(e_zoom_coord[0], e_zoom_coord[1]), xytext=(e_zoom_pos[0], e_zoom_pos[1] + 1.5), 
                arrowprops=dict(arrowstyle="->", color="#000080", lw=1.5, alpha=0.8), zorder=21)

    # =======================================================
    # ZONE 4: EXTERNAL NEUTRALITY
    # =======================================================
    neutrality_text = "External Neutrality\n" + r"$\Sigma\chi = 0$"
    ax.text(82, 15, neutrality_text, ha='center', va='center', color='black', 
            fontsize=10, family='serif', fontweight='bold', bbox=mask_props)

    # =======================================================
    # ADDITIONAL LABELS
    # =======================================================
    ax.annotate("Electron Resonant Boundary\n(Continuous Chiral Wake)", 
                xy=(50, 50 + shell_radius), 
                xytext=(50, 96),
                arrowprops=dict(arrowstyle="->", color="black", lw=0.8),
                ha='center', va='top', color='black', fontsize=10, fontweight='bold', bbox=mask_props, zorder=20, family='serif')

    # Internal Shell Theorem Neutrality
    ax.text(50, 80, r"$\sum \mathbf{F}_{\chi(-1)} = 0$", 
            ha='center', va='center', color='black', fontsize=11, fontweight='bold', bbox=mask_props, zorder=20)

    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig18_PartII_HydrogenAtom.pdf")
    
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
    create_tft_atom_blueprint_final()