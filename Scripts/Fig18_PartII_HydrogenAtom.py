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
        ax.plot(transformed_v[:, 0], transformed_v[:, 1], color='#E0E0E0', lw=0.6, zorder=0)
        
        pts_h = np.column_stack((np.linspace(0, 100, line_res), np.full(line_res, val)))
        transformed_h = np.array([transform_point(p) for p in pts_h])
        ax.plot(transformed_h[:, 0], transformed_h[:, 1], color='#E0E0E0', lw=0.6, zorder=0)

    # =======================================================
    # ZONE 2: Electron Resonant Boundaries
    # =======================================================
    for r_offset in np.linspace(0, 1.5, 8):
        circle = patches.Circle(center, shell_radius + r_offset, 
                                facecolor='none', edgecolor='#00AACC', 
                                alpha=0.1, lw=2, zorder=1)
        ax.add_patch(circle)

    dashed_shell = patches.Circle(center, rm_radius, fill=False, 
                                  edgecolor='#777777', ls='--', alpha=0.5, lw=1.2, zorder=1)
    ax.add_patch(dashed_shell)
    
    rm_angle = np.radians(340)
    ax.text(50 + rm_radius * np.cos(rm_angle), 50 + rm_radius * np.sin(rm_angle), 
            r"$\mathrm{\mathbf{r_m}}$ (Lower Shell)", color='black', ha='center', va='center', 
            fontsize=9, bbox=mask_props, zorder=20)

    drop_x = 50
    ax.annotate("", xy=(drop_x, 50 - rm_radius), xytext=(drop_x, 50 - shell_radius),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.0), zorder=10)
    ax.text(drop_x + 1, 50 - (rm_radius + shell_radius)/2, r"$\mathrm{\Delta \ell}$ (The Drop)", 
            va='center', ha='left', family='serif', color='black', fontweight='normal', bbox=mask_props, zorder=30)

    # Dynamic Electron Wake
    wake_angle_span = 260 
    t_wake_start = 45 
    t_wake = np.linspace(t_wake_start - wake_angle_span, t_wake_start, 600)
    rad_t = np.radians(t_wake)
    
    wake_color = '#00AACC'
    for i in range(len(t_wake) - 1):
        alpha_val = (i / len(t_wake))**2.5 
        ax.plot([50 + shell_radius * np.cos(rad_t[i]), 50 + shell_radius * np.cos(rad_t[i+1])],
                [50 + shell_radius * np.sin(rad_t[i]), 50 + shell_radius * np.sin(rad_t[i+1])],
                color=wake_color, lw=4.0, alpha=alpha_val, zorder=2)

    # Electron Mass Core (Solid blue fill, no edge)
    core_x = 50 + shell_radius * np.cos(np.radians(t_wake_start))
    core_y = 50 + shell_radius * np.sin(np.radians(t_wake_start))
    ax.scatter([core_x], [core_y], facecolor='#00AACC', s=85, edgecolors='none', zorder=15)
    
    ax.annotate(r"$\mathrm{\mathbf{Electron\ Core}}\ (r_{amp})$", 
                xy=(core_x, core_y), xytext=(core_x + 5, core_y + 5),
                arrowprops=dict(arrowstyle="->", color="black", lw=0.8),
                color='black', family='serif', fontweight='bold', zorder=25,
                bbox=mask_props)

    # --- KINETIC EQUILIBRIUM VECTORS ---
    tangent_angle = np.radians(t_wake_start + 90)
    v_len = 12
    ax.annotate("", xy=(core_x + v_len * np.cos(tangent_angle), core_y + v_len * np.sin(tangent_angle)),
                xytext=(core_x, core_y),
                arrowprops=dict(arrowstyle="->", color="#0055AA", lw=1.5), zorder=16)
    ax.text(core_x + v_len * np.cos(tangent_angle), core_y + v_len * np.sin(tangent_angle) + 1, 
            r"$\mathbf{v_n}$", color='black', fontsize=12, fontweight='bold', ha='center',
            bbox=mask_props, zorder=25)

    f_len = 10
    ax.annotate("", xy=(core_x - f_len * np.cos(np.radians(t_wake_start)), core_y - f_len * np.sin(np.radians(t_wake_start))),
                xytext=(core_x, core_y),
                arrowprops=dict(arrowstyle="->", color="#CC0000", lw=1.5), zorder=16)
    ax.text(core_x - (f_len+2) * np.cos(np.radians(t_wake_start)), core_y - (f_len+2) * np.sin(np.radians(t_wake_start)), 
            r"$\mathbf{F_\chi}$", color='black', fontsize=12, fontweight='bold', ha='center',
            bbox=mask_props, zorder=25)

    # =======================================================
    # ZONE 1: Nucleus (The Torsional Anchor)
    # =======================================================
    nucleus_radius = 2.8
    ax.add_patch(patches.Circle(center, nucleus_radius, facecolor='#CC0000', zorder=10))
    
    # Nucleon Label
    ax.text(50, 43.0, r"$\mathrm{\mathbf{Hyper-Dense\ Nucleon\ Anchor}}$", 
            ha='center', va='top', color='black', fontsize=10, bbox=mask_props, zorder=20, family='serif')

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
            ax.plot(spiral_x[idx:idx+chunk+1], spiral_y[idx:idx+chunk+1], 
                    color='#CC0000', alpha=0.3, lw=lw_taper, zorder=5)

        ax.annotate("", xy=(spiral_x[-1], spiral_y[-1]), 
                    xytext=(spiral_x[-5], spiral_y[-5]),
                    arrowprops=dict(arrowstyle="->", color="#CC0000", lw=1.2, alpha=0.6), zorder=6)
        
        if i == 1:
            ax.text(spiral_x[-1] + 1.5, spiral_y[-1] + 1.5, r"$\chi(+1), +\hat{\mathbf{r}}$", 
                    color='black', fontsize=9, fontweight='bold', bbox=mask_props, zorder=21)
        elif i == 7:
            ax.text(spiral_x[-1] - 2.0, spiral_y[-1] + 2.0, r"$\chi(+1), +\hat{\mathbf{r}}$", 
                    color='black', fontsize=9, fontweight='bold', bbox=mask_props, zorder=21, ha='right')

        for r_frac in [0.4, 0.7]:
            idx_tick = int(len(t_spiral) * r_frac)
            tangent_vec = np.array([spiral_x[idx_tick+1]-spiral_x[idx_tick-1], 
                                    spiral_y[idx_tick+1]-spiral_y[idx_tick-1]])
            ang_deg = np.degrees(np.arctan2(tangent_vec[1], tangent_vec[0]))
            ax.text(spiral_x[idx_tick], spiral_y[idx_tick], r"$\ll$", 
                    color="#CC0000", fontsize=8, rotation=ang_deg, 
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
            ax.plot(spiral_x_in[idx:idx+chunk+1], spiral_y_in[idx:idx+chunk+1], 
                    color='#0055AA', alpha=0.2, lw=lw_taper, zorder=4)
        
        ax.annotate("", xy=(spiral_x_in[-1], spiral_y_in[-1]), 
                    xytext=(spiral_x_in[-5], spiral_y_in[-5]),
                    arrowprops=dict(arrowstyle="->", color="#0055AA", lw=1.0, alpha=0.4), zorder=5)

        if i == 1: # Upper Side
            ax.text(spiral_x_in[115], spiral_y_in[115], r"$\chi(-1), -\hat{\mathbf{r}}$", 
                    color='black', fontsize=9, fontweight='bold', bbox=mask_props, zorder=21)
        elif i == 6: # Lower Side
            ax.text(spiral_x_in[115], spiral_y_in[115], r"$\chi(-1), -\hat{\mathbf{r}}$", 
                    color='black', fontsize=9, fontweight='bold', bbox=mask_props, zorder=21)
        
        for r_frac in [0.3, 0.6]:
            idx_tick = int(len(t_in) * r_frac)
            tangent_vec = np.array([spiral_x_in[idx_tick-1]-spiral_x_in[idx_tick+1],
                                    spiral_y_in[idx_tick-1]-spiral_y_in[idx_tick+1]])
            ang_deg = np.degrees(np.arctan2(tangent_vec[1], tangent_vec[0]))
            ax.text(spiral_x_in[idx_tick], spiral_y_in[idx_tick], r"$\gg$", 
                    color="#0055AA", fontsize=7, rotation=ang_deg, 
                    ha='center', va='center', alpha=0.5, zorder=5)
            
            d = np.sqrt((spiral_x_in[idx_tick] - e_zoom_pos[0])**2 + (spiral_y_in[idx_tick] - e_zoom_pos[1])**2)
            if d < min_dist_e:
                min_dist_e = d
                e_zoom_coord = (spiral_x_in[idx_tick], spiral_y_in[idx_tick], ang_deg)

    # =======================================================
    # MAGNIFICATION CALLOUTS
    # =======================================================
    callout_rad = 5
    
    # 1. Nucleon Inward Pull (Top-Left)
    ax.add_patch(patches.Circle(p_zoom_pos, callout_rad, facecolor='white', edgecolor='#CC0000', lw=1.5, zorder=22, alpha=0.9))
    ax.text(p_zoom_pos[0], p_zoom_pos[1], r"$\ll$", color='#CC0000', fontsize=28, ha='center', va='center', rotation=p_zoom_coord[2], zorder=23)
    ax.text(p_zoom_pos[0], p_zoom_pos[1] - callout_rad - 2, r"$\mathrm{\mathbf{Nucleon's\ Inward\ Pull}}$", color='black', ha='center', fontweight='bold', zorder=23, bbox=mask_props)
    ax.annotate("", xy=p_zoom_pos, xytext=(p_zoom_coord[0], p_zoom_coord[1]), arrowprops=dict(arrowstyle="->", color="black", lw=0.6, alpha=0.5), zorder=21)

    # 2. Electron Outward Pull (Bottom-Left)
    ax.add_patch(patches.Circle(e_zoom_pos, callout_rad, facecolor='white', edgecolor='#0055AA', lw=1.5, zorder=22, alpha=0.9))
    ax.text(e_zoom_pos[0], e_zoom_pos[1], r"$\gg$", color='#0055AA', fontsize=28, ha='center', va='center', rotation=e_zoom_coord[2], zorder=23)
    ax.text(e_zoom_pos[0], e_zoom_pos[1] + callout_rad + 2, r"$\mathrm{\mathbf{Electron's\ Outward\ Pull}}$", color='black', ha='center', fontweight='bold', zorder=23, bbox=mask_props)
    ax.annotate("", xy=e_zoom_pos, xytext=(e_zoom_coord[0], e_zoom_coord[1]), arrowprops=dict(arrowstyle="->", color="black", lw=0.6, alpha=0.5), zorder=21)

    # =======================================================
    # ZONE 4: EXTERNAL NEUTRALITY
    # =======================================================
    neutrality_text = (r"$\mathrm{\mathbf{External\ Neutrality}}$" + "\n" +
                       r"$\mathrm{via\ Phase\ Superposition}$" + "\n\n" +
                       r"$\mathrm{(+1) + (-1) = 0}$" + "\n" + 
                       r"$\mathrm{(Undisturbed\ Lattice)}$")
    
    ax.text(82, 15, neutrality_text, ha='center', va='center', color='black', 
            fontsize=10, family='serif', fontweight='bold', bbox=mask_props)

    # =======================================================
    # ADDITIONAL LABELS
    # =======================================================
    ax.annotate(r"$\mathrm{\mathbf{Electron\ Resonant\ Boundary}}$" + "\n" + r"$\mathrm{(Continuous\ Chiral\ Wake)}$", 
                xy=(50, 50 + shell_radius), 
                xytext=(50, 96),
                arrowprops=dict(arrowstyle="->", color="black", lw=0.8),
                ha='center', va='top', color='black', fontsize=10, bbox=mask_props, zorder=20, family='serif')
    
    ax.text(35, 65, r"$\mathrm{Topological\ Shell\ Theorem}$" + "\n" + r"$\mathrm{Zero\ Net\ Electron\ Vector}$" + "\n" + r"$\mathrm{Proton\ Field\ Dominant}$", 
            ha='center', va='center', color='black', fontsize=9, bbox=mask_props, zorder=20, family='serif')

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