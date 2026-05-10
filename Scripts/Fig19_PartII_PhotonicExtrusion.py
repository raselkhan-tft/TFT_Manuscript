import numpy as np # Selected for non-linear coordinate transformations and vector math
import matplotlib.pyplot as plt # Selected for publication-grade 2D diagrammatic composition
import matplotlib.patches as patches # Selected for rendering structural shells, funnels, and boxes
import matplotlib.transforms as transforms # Selected for precise cross-axis geometric alignment
import os # Selected for robust local directory management and path-specific file saving

def create_photonic_extrusion_blueprint():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })
    
    # Initialize a two-panel side-by-side figure with expanded gap (wspace = 0.18)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8.5), dpi=150, gridspec_kw={'wspace': 0.18})
    fig.patch.set_facecolor('white')

    # Masking properties for legibility
    mask_props = dict(facecolor='white', edgecolor='none', alpha=0.9, boxstyle='round,pad=0.4')
    
    # =======================================================
    # PANEL A: THE MACROSCOPIC COLLAPSE (Atomic Scale)
    # =======================================================
    ax1.set_aspect('equal')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    
    # Consolidated Panel Label
    # Use a blended transform to lock the Y-coordinate to ax2's height while keeping X anchored to ax1
    trans_a = transforms.blended_transform_factory(ax1.transAxes, ax2.transAxes)
    ax1.text(0.0, 1.02, r"$\mathbf{(a)\ Macroscopic\ Atomic\ Drop}$", transform=trans_a, fontsize=15, color='black', ha='left', va='bottom')
    
    center = np.array([50, 50])
    rn = 38 # Outer boundary (previous state)
    rm = 26 # Inner boundary (collapsed state)
    n_rad = 3.5 # Nucleus radius
    
    # 1. The Boundaries
    # Outer boundary (previous state - dotted and empty)
    circle_n = patches.Circle(center, rn, fill=False, edgecolor='#000080', ls=':', lw=1.5, alpha=0.5, zorder=1)
    ax1.add_patch(circle_n)
    
    # Inner boundary (collapsed state) - Gradient Shell synced with Hydrogen Model
    for r_offset in np.linspace(0, 1.5, 8):
        circle_m_grad = patches.Circle(center, rm + r_offset, fill=False, edgecolor='#000080', alpha=0.1, lw=2, zorder=1)
        ax1.add_patch(circle_m_grad)

    # Label rn and rm vertically at the bottom (6 o'clock) with strict italics
    ax1.text(center[0], center[1] - rn - 1.5, r"$r_n$", ha='center', va='top', fontsize=12, fontweight='bold', bbox=mask_props, zorder=35)
    ax1.text(center[0], center[1] - rm - 1.5, r"$r_m$", ha='center', va='top', fontsize=12, fontweight='bold', bbox=mask_props, zorder=35)
    
    # 2. INTERNAL FIELD (Core to rm)
    for angle_start in np.linspace(0, 2*np.pi, 12, endpoint=False):
        r_inner = np.linspace(n_rad, rm, 120)
        twist = 0.5
        ax1.plot(center[0] + r_inner*np.cos(angle_start + twist*np.log(r_inner)), 
                 center[1] + r_inner*np.sin(angle_start + twist*np.log(r_inner)), 
                 color='#8B0000', alpha=0.6, lw=1.2, zorder=1)
    
    for angle_start in np.linspace(np.pi/12, 2*np.pi + np.pi/12, 8, endpoint=False):
        r_in = np.linspace(rm, n_rad + 2, 100)
        twist_in = -0.4 
        ax1.plot(center[0] + r_in*np.cos(angle_start + twist_in*np.log(r_in)), 
                 center[1] + r_in*np.sin(angle_start + twist_in*np.log(r_in)), 
                 color='#000080', alpha=0.25, lw=1.0, zorder=1)

    # 3. NEUTRALIZATION GAP (rm to rn)
    # Replaced jitter with smooth, dense dashed curves
    for angle in np.linspace(0, 2*np.pi, 24, endpoint=False):
        r_gap = np.linspace(rm, rn, 50)
        
        twist_red = 0.5
        ax1.plot(center[0] + r_gap*np.cos(angle + twist_red*np.log(r_gap)), 
                 center[1] + r_gap*np.sin(angle + twist_red*np.log(r_gap)), 
                 color='#8B0000', alpha=0.35, lw=1.2, ls='--', zorder=1)
        
        twist_blue = -0.5
        ax1.plot(center[0] + r_gap*np.cos(angle + twist_blue*np.log(r_gap)), 
                 center[1] + r_gap*np.sin(angle + twist_blue*np.log(r_gap)), 
                 color='#000080', alpha=0.35, lw=1.2, ls='--', zorder=1)

    # 4. The Drop Vector and Electron States (3 O'CLOCK SIDE)
    ax1.annotate("", xy=(center[0]+rm, center[1]), xytext=(center[0]+rn, center[1]), arrowprops=dict(arrowstyle="->", color="black", lw=2.5), zorder=10)
    ax1.text(center[0]+(rn+rm)/2, center[1]+3.5, r"$\Delta r = r_n - r_m$", ha='center', va='bottom', fontweight='bold', bbox=mask_props, zorder=25)

    e_radius = 0.88 * (rm / 36.0) # Scaled up by 10%
    R_main = e_radius * 0.65
    
    # -------------------------------------------------------
    # START STATE (Inactive / Previous Orbit at rn)
    # -------------------------------------------------------
    # Dotted hollow ring to match the new electron geometry
    t_ring = np.linspace(0, 2 * np.pi, 200)
    ring_start_x = (center[0] + rn) + R_main * np.cos(t_ring)
    ring_start_y = center[1] + R_main * np.sin(t_ring)
    ax1.plot(ring_start_x, ring_start_y, color='#8B0000', lw=0.9, ls=':', alpha=0.5, zorder=16)

    # -------------------------------------------------------
    # END STATE (Active / Current Orbit at rm)
    # -------------------------------------------------------
    t_wake_start = 0  # 3 o'clock position (0 degrees)
    core_x = center[0] + rm * np.cos(np.radians(t_wake_start))
    core_y = center[1] + rm * np.sin(np.radians(t_wake_start))
    
    # Dynamic Electron Wake (Offset so it touches the ring but does not penetrate it)
    wake_angle_span = 260 
    line_cap_buffer = 0.12 # Accounting for the geometric bleed of the thick stroke cap
    angular_offset_deg = np.degrees((R_main + line_cap_buffer) / rm)
    t_wake_end = t_wake_start - angular_offset_deg
    t_wake = np.linspace(t_wake_end - wake_angle_span, t_wake_end, 600)
    rad_t = np.radians(t_wake)
    
    # Wake color standardized to Deep Navy Blue
    wake_color = '#000080'
    for i in range(len(t_wake) - 1):
        alpha_val = (i / len(t_wake))**2.5 
        ax1.plot([center[0] + rm * np.cos(rad_t[i]), center[0] + rm * np.cos(rad_t[i+1])],
                 [center[1] + rm * np.sin(rad_t[i]), center[1] + rm * np.sin(rad_t[i+1])],
                 color=wake_color, lw=2.17, alpha=alpha_val, zorder=28)

    # Electron Mass Core (Single Maroon Hollow Ring)
    ring_end_x = core_x + R_main * np.cos(t_ring)
    ring_end_y = core_y + R_main * np.sin(t_ring)
    
    # Reduced line width by 25% to increase internal hollow space
    ax1.plot(ring_end_x, ring_end_y, color='#8B0000', lw=0.94, zorder=32)

    # 5. Nucleus (Compact Rosette Core)
    def draw_dense_lobe(ax_obj, cx, cy, angle, inner_radius=0.4, outer_reach=3.5):
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
        ax_obj.fill(x_rot, y_rot, color='#FFDDDD', alpha=0.95, zorder=5)
        # Outer Ribbon (Muted Maroon)
        ax_obj.plot(x_rot, y_rot, color='#8B0000', lw=1.0, zorder=6)

    # Line density reduced to 31 to preserve woven visibility at this smaller scale
    num_nodes = 31
    for i in range(num_nodes):
        angle = i * (2 * np.pi / num_nodes)
        draw_dense_lobe(ax1, center[0], center[1], angle, inner_radius=0.3, outer_reach=n_rad)
    
    # 6. Component Level Labels
    ax1.text(center[0], center[1] - n_rad - 2.5, "Nucleon", ha='center', va='top', fontsize=10, fontweight='normal', bbox=mask_props, zorder=40)
    
    # Resurrected Original Electron Label
    elec_angle = np.radians(330)
    elec_label_r = 52
    elec_xytext = center + elec_label_r * np.array([np.cos(elec_angle), np.sin(elec_angle)])
    ax1.annotate("Electron", xy=(core_x, core_y), xytext=elec_xytext,
                 arrowprops=dict(arrowstyle="->", color="black", lw=0.8),
                 fontsize=10, fontweight='normal', ha='left', va='top', bbox=mask_props, zorder=40)

    # 7. Pinch Point
    ext_pt = np.array([center[0] + rn, center[1]])
    zoom_w = 16
    rect_zoom = patches.Rectangle((ext_pt[0]-zoom_w*0.8, ext_pt[1]-zoom_w/2), zoom_w, zoom_w, fill=False, edgecolor='black', ls='--', lw=1.5, zorder=20)
    ax1.add_patch(rect_zoom)

    # =======================================================
    # PANEL B: THE MICROCAVITATION CHANNEL (Zoom)
    # =======================================================
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    
    # Consolidated Panel Label (Closed compound word to avoid math-mode kerning issues)
    ax2.text(0.0, 1.02, r"$\mathbf{(b)\ Microcavitation\ Channel}$", transform=ax2.transAxes, fontsize=15, color='black', ha='left', va='bottom')
    
    wall_x_end = 35
    funnel_y_center = 50
    gap_h = 10
    
    # 1. THE RIGID LATTICE WALL (Smooth Implicit Continuum Background)
    ax2.add_patch(patches.Rectangle((0, 0), wall_x_end, 90, facecolor='#EAEAEA', alpha=1.0, zorder=1))

    # 2. THE CHANNEL VOID (White "Hole" carving through the lattice)
    funnel_pts = np.array([[0, 80], [wall_x_end, 55], [wall_x_end, 45], [0, 20]])
    ax2.add_patch(patches.Polygon(funnel_pts, facecolor='white', alpha=1.0, zorder=3))
    
    ax2.plot([0, wall_x_end], [80, 55], color='black', lw=1.5, zorder=4)
    ax2.plot([0, wall_x_end], [20, 45], color='black', lw=1.5, zorder=4)
    
    # 3. ANNOTATIONS & LABELS
    # Bipolar Squeeze / Turbulent Flow
    for i, y_start in enumerate(np.linspace(15, 85, 14)):
        color = '#000080' if i % 2 == 0 else '#8B0000'
        rad = 0.3 if i % 2 == 0 else -0.3
        ax2.annotate("", xy=(wall_x_end-1, 50 + (y_start-50)*0.1), xytext=(2, y_start),
                     arrowprops=dict(arrowstyle="->", color=color, lw=1.8, alpha=0.6, connectionstyle=f"arc3,rad={rad}"), zorder=5)
    
    # Energy Integral Label
    ax2.text(8, 50, r"$E_\gamma = \int \delta\tau \, dV$", color='black', fontsize=12, fontweight='bold', ha='center', bbox=mask_props, zorder=10)

    # FCC Lattice (cE^2) Level - Centered in middle of gray lattice (50% of wall width)
    ax2.text(wall_x_end / 2, 12, r"$\mathbf{FCC\ Lattice}\ (c_{\mathrm{E}}^2)$", ha='center', va='top', fontsize=10, fontweight='bold', color='black', zorder=20)

    # Neutralization Funnel Identifier - Placed at bottom white area with thin arrow
    ax2.annotate("Neutralization Funnel", xy=(22, 44), xytext=(65, 20),
                 arrowprops=dict(arrowstyle="->", color="black", lw=0.8),
                 fontsize=10, fontweight='normal', ha='center', va='top', zorder=20)

    # 4. EXTRUSION ELEMENTS
    # Slit Width Indicator (using upright \mathrm for descriptive subscript)
    ax2.annotate('', xy=(wall_x_end, 55), xytext=(wall_x_end, 45), arrowprops=dict(arrowstyle='<->', color='black', lw=0.75), zorder=25)
    ax2.text(wall_x_end + 1.5, 50, r"$A_{\mathrm{chan}}$", va='center', ha='left', fontweight='bold', fontsize=12, zorder=25)

    # THE EXTRUDED PHOTON (3D Double Helix Perception)
    photon_x = np.linspace(wall_x_end, 95, 400)
    helix_amp = 7
    helix_freq = 0.28
    
    # Base Lines (Drawn behind masks)
    # Red (+1 Twist)
    ax2.plot(photon_x, funnel_y_center + helix_amp * np.sin(helix_freq * (photon_x - wall_x_end)), color='#8B0000', lw=2.8, zorder=10, alpha=0.9)
    # Blue (-1 Twist)
    ax2.plot(photon_x, funnel_y_center - helix_amp * np.sin(helix_freq * (photon_x - wall_x_end)), color='#000080', lw=2.8, zorder=10, alpha=0.9, ls=(0, (5, 1)))
    
    # Visual 3D "Over/Under" Cues at the intersection points on the central axis
    # Crossing points occur at multiples of pi/frequency
    crossing_pts = wall_x_end + np.arange(6) * (np.pi / helix_freq)
    
    for i, cx in enumerate(crossing_pts):
        if cx > 95: continue
        
        # Determine the "front" string based on alternating helix projection
        # Even i: Red is Over. Odd i: Blue is Over.
        is_red_over = (i % 2 == 0)
        over_color = '#8B0000' if is_red_over else '#000080'
        over_ls = 'solid' if is_red_over else (0, (5, 1))
        
        # 1. Draw a small white occlusion circle at the crossing point to break the "under" line
        ax2.scatter([cx], [funnel_y_center], color='white', s=60, zorder=11, edgecolors='none')
        
        # 2. Redraw a small segment of the "front" line to maintain continuity
        seg_x = np.linspace(cx - 1.2, cx + 1.2, 10)
        if is_red_over:
            seg_y = funnel_y_center + helix_amp * np.sin(helix_freq * (seg_x - wall_x_end))
        else:
            seg_y = funnel_y_center - helix_amp * np.sin(helix_freq * (seg_x - wall_x_end))
            
        ax2.plot(seg_x, seg_y, color=over_color, lw=2.8, ls=over_ls, zorder=12, alpha=0.9)

    # Propagation identification
    # Arrow remains perfectly anchored to the central axis (y=50)
    ax2.annotate("", xy=(100, 50), xytext=(88, 50), arrowprops=dict(arrowstyle="-|>", color="black", lw=2.5), zorder=15)
    
    # Label Y-coordinate explicitly decoupled. Wave peak is at 50 + 7 = 57. 
    # Gap reduced by 20% (from 1.0 to 0.8), placing the baseline precisely at 57.8.
    photon_label_y = 57.8
    ax2.text(94, photon_label_y, r"$\mathrm{Extruded\ Photon}\ (c_{\mathrm{P}} \approx c_{\mathrm{E}})$", fontweight='bold', fontsize=12, ha='center', va='bottom')
    
    # Bracketless math on top of the lattice column (using upright \mathrm for descriptive subscripts)
    ax2.text(17.5, 96, r"$E_\gamma \approx \tau_{\mathrm{bulk}} \cdot A_{\mathrm{chan}} \cdot \Delta r$", ha='center', va='top', fontsize=11, fontweight='bold', color='black')

    # =======================================================
    # LEADER LINES
    # =======================================================
    con = patches.ConnectionPatch(xyA=(ext_pt[0], ext_pt[1]), xyB=(0, 50), 
                                  coordsA="data", coordsB="data", 
                                  axesA=ax1, axesB=ax2, color="gray", lw=1.2, ls=':', alpha=0.5)
    ax2.add_artist(con)

    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout(rect=[0, 0.03, 1, 0.98])
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig19_PartII_PhotonicExtrusion.pdf")
    
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
    create_photonic_extrusion_blueprint()