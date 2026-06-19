import numpy as np # Selected for efficient spatial masking, percolation MST algorithms, and geometric broadcasting
import matplotlib.pyplot as plt # Selected for precise 2D vector graphic control and publication layout
import matplotlib.patches as patches # Selected for rendering distinct structural zones (Circles, Boundaries, BAO rings)
from matplotlib.collections import PatchCollection # Selected for highly optimized bulk rendering of 10,000+ FCC nodes
import os # Selected for robust directory management and path-specific file saving

def create_deflation_rupture_baseline():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    # Setup Figure (Two-Panel Bipartite Architecture with minimized gap)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9), dpi=150, gridspec_kw={'wspace': 0.05})
    fig.patch.set_facecolor('white')

    # -------------------------------------------------------
    # VISUAL SCALING PARAMETERS
    # -------------------------------------------------------
    R_orig = 10.0   # Geometric Cosmic Horizon (Original / Expanded)
    R_rup = 8.5     # Deflated Rupture Radius (Percolation Limit)
    
    # CRITICAL FIX: Expanded canvas boundary to provide ample margin for annotations
    limit = 15.0    
    
    text_bbox = dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3)

    # =======================================================
    # GLOBAL GEOMETRY GENERATION (Shared across both panels)
    # =======================================================
    # SPANNING CLUSTER ALGORITHM
    np.random.seed(48) 
    
    # Strictly enforcing the 5.26% Percolation Limit Volume/Area (\beta_oct)
    target_area = 0.0526 * np.pi * R_rup**2
    
    core_centers, base_radii = [], []

    # Backbone
    num_trunk = 45
    trunk_y = np.linspace(R_rup * 0.98, -R_rup * 0.98, num_trunk)
    W = np.cumsum(np.random.normal(0, 1, num_trunk))
    B = W - np.linspace(0, 1, num_trunk) * W[-1]
    trunk_x = B * (R_rup * 0.6 / (np.max(np.abs(B)) + 1e-6))
    
    for i in range(num_trunk):
        core_centers.append((trunk_x[i], trunk_y[i]))
        if np.random.rand() > 0.85 and abs(trunk_y[i]) < R_rup * 0.8:
            base_radii.append(np.random.uniform(1.8, 2.8)) 
        else:
            base_radii.append(np.random.uniform(0.3, 1.0)) 

    # Branches
    num_branches = 70
    curr_idx = num_trunk
    for _ in range(num_branches):
        root_idx = np.random.randint(0, curr_idx)
        br_x, br_y = core_centers[root_idx]
        br_len = np.random.randint(3, 9)
        prev_idx = root_idx
        
        angle = np.random.uniform(-np.pi/2, np.pi/2) if br_x > 0 else np.random.uniform(np.pi/2, 3*np.pi/2)

        for step in range(br_len):
            step_size = np.random.uniform(0.8, 2.0)
            br_x += np.cos(angle) * step_size
            br_y += np.sin(angle) * step_size

            if np.hypot(br_x, br_y) > R_rup * 0.95: break

            core_centers.append((br_x, br_y))
            if np.random.rand() > 0.90: base_radii.append(np.random.uniform(1.2, 2.3))
            else: base_radii.append(np.random.uniform(0.2, 0.8))
                
            prev_idx = curr_idx
            curr_idx += 1
            angle += np.random.normal(0, 1.0) 

    # Scale ALL radii mathematically to perfectly match the requirement
    current_area = np.sum(np.pi * np.array(base_radii)**2)
    scale_factor = np.sqrt(target_area / current_area)
    all_radii = np.array(base_radii) * scale_factor
    pts = np.array(core_centers)

    # -------------------------------------------------------
    # CLUSTER SWAP LOGIC
    # -------------------------------------------------------
    mask_a = (pts[:, 0] > 1.0) & (pts[:, 1] < -1.0) & (pts[:, 1] > -7.0)
    mask_b = (pts[:, 0] > -4.0) & (pts[:, 0] < 1.0) & (pts[:, 1] > -2.0) & (pts[:, 1] < 4.0)

    indices_a = np.where(mask_a)[0]
    indices_b = np.where(mask_b)[0]

    if len(indices_a) > 0 and len(indices_b) > 0:
        centroid_a = np.mean(pts[indices_a], axis=0)
        centroid_b = np.mean(pts[indices_b], axis=0)
        
        vec_a_to_b = centroid_b - centroid_a
        vec_b_to_a = centroid_a - centroid_b
        
        pts[indices_a] += vec_a_to_b
        pts[indices_b] += vec_b_to_a
        
        radii_check = np.hypot(pts[:, 0], pts[:, 1])
        escaped = radii_check > (R_rup * 0.95)
        if np.any(escaped):
            pts[escaped, 0] *= (R_rup * 0.95) / radii_check[escaped]
            pts[escaped, 1] *= (R_rup * 0.95) / radii_check[escaped]

    # -------------------------------------------------------
    # MINIMUM SPANNING TREE (MST) REWIRING
    # -------------------------------------------------------
    connected = [0]
    unconnected = list(range(1, len(pts)))
    edges = []

    while unconnected:
        conn_pts = pts[connected]
        unconn_pts = pts[unconnected]
        
        dx = conn_pts[:, 0, None] - unconn_pts[:, 0, None].T
        dy = conn_pts[:, 1, None] - unconn_pts[:, 1, None].T
        dists = dx**2 + dy**2
        
        min_idx = np.unravel_index(np.argmin(dists), dists.shape)
        u = connected[min_idx[0]]
        v_idx = min_idx[1]
        v = unconnected[v_idx]
        
        edges.append((u, v))
        connected.append(v)
        unconnected.pop(v_idx)

    # -------------------------------------------------------
    # RENDER PANELS
    # -------------------------------------------------------
    panels = [
        (ax1, r"$\mathbf{(a)\ At\ Rupture}$", True),
        (ax2, r"$\mathbf{(b)\ Post\ Rupture}$", False)
    ]

    for ax, panel_title, is_left in panels:
        ax.set_facecolor('white')
        
        # LAYER 1: THE INFINITE CANVAS
        block_size = 0.6 
        grid_ticks = np.arange(-20.0, 20.0, block_size)
        for t in grid_ticks:
            ax.axhline(t, color='#E8E8E8', lw=0.5, alpha=0.8, zorder=0)
            ax.axvline(t, color='#E8E8E8', lw=0.5, alpha=0.8, zorder=0)

        # State 0 Anchor Label (Updated to Invariant Continuum with internal center alignment)
        ax.text(-limit + 0.5, -limit + 0.5, "State 0 Substrate\n(Invariant Continuum)", 
                color='#777777', fontsize=12, fontweight='bold', ha='left', va='bottom', multialignment='center', zorder=10,
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=2))

        # =======================================================
        # LEFT PANEL: PRE-RUPTURE GEOMETRY
        # =======================================================
        if is_left:
            orig_horizon = patches.Circle((0, 0), R_orig, fill=False, edgecolor='#888888', linestyle='--', lw=2.0, zorder=1)
            ax.add_patch(orig_horizon)
            
            solid_base = patches.Circle((0, 0), R_rup, facecolor='#0055AA', edgecolor='none', alpha=1.0, zorder=2)
            ax.add_patch(solid_base)
            
            rup_horizon = patches.Circle((0, 0), R_rup, fill=False, edgecolor='#002266', linestyle='-', lw=2.5, zorder=2.1)
            ax.add_patch(rup_horizon)

            ax.annotate("Geometric Cosmic Horizon\n(Pre-Deflation)", xy=(0, R_orig), xytext=(0, R_orig + 1.5),
                        arrowprops=dict(arrowstyle="->", color="#888888", lw=1.2),
                        color='#555555', fontsize=10, ha='center', va='bottom', bbox=text_bbox, zorder=10)

            rup_text = r"$\mathbf{Deflated\ Rupture\ Radius}$" + "\n" + r"($R_{\mathrm{rup}} \approx 10^{34}\ \mathrm{m}$)"
            ax.annotate(rup_text, xy=(0, -R_rup), xytext=(0, -R_rup - 1.5),
                        arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
                        color='black', fontsize=11, ha='center', va='top', bbox=text_bbox, zorder=10)

            # Fault Lines Rendering
            for u, v in edges:
                x1, y1 = pts[u]
                x2, y2 = pts[v]
                dist = np.hypot(x2 - x1, y2 - y1)
                num_pts = max(int(dist * 3), 4)
                
                t = np.linspace(0, 1, num_pts)
                x_line = x1 + t * (x2 - x1)
                y_line = y1 + t * (y2 - y1)
                
                nx, ny = -(y2 - y1)/dist, (x2 - x1)/dist
                noise = np.random.uniform(-0.35, 0.35, num_pts)
                noise[0] = noise[-1] = 0 
                x_frac = x_line + nx * noise
                y_frac = y_line + ny * noise
                
                ax.plot(x_frac, y_frac, color='#00FFFF', lw=2.0, alpha=0.9, zorder=4.0)
                ax.plot(x_frac, y_frac, color='#FFFFFF', lw=1.0, zorder=4.5)

            # Granular Bulk FCC
            fcc_radius = 0.08 
            spacing = fcc_radius * 1.732 
            xs = np.arange(-R_rup, R_rup, spacing)
            ys = np.arange(-R_rup, R_rup, spacing * np.sqrt(3)/2)
            X_grid, Y_grid = np.meshgrid(xs, ys)
            X_grid[1::2] += spacing / 2
            X_flat, Y_flat = X_grid.flatten(), Y_grid.flatten()
            
            mask_circle = (X_flat**2 + Y_flat**2) < (R_rup - fcc_radius * 1.5)**2
            X_flat, Y_flat = X_flat[mask_circle], Y_flat[mask_circle]
            
            DX = X_flat[:, None] - pts[:, 0][None, :]
            DY = Y_flat[:, None] - pts[:, 1][None, :]
            DIST_SQ = DX**2 + DY**2
            
            MIN_DIST_SQ = (all_radii[None, :] + fcc_radius * 1.5)**2
            valid_mask = np.all(DIST_SQ >= MIN_DIST_SQ, axis=1)
            
            X_valid, Y_valid = X_flat[valid_mask], Y_flat[valid_mask]
            
            bulk_fcc = [patches.Circle((x, y), fcc_radius) for x, y in zip(X_valid, Y_valid)]
            bulk_col = PatchCollection(bulk_fcc, facecolor='#00E0FF', edgecolor='#0055AA', lw=0.3, alpha=0.9, zorder=3)
            ax.add_collection(bulk_col)

            # Highly Packed Surface Boundaries
            boundary_fcc = []
            for px, py, r in zip(pts[:, 0], pts[:, 1], all_radii):
                circ = 2 * np.pi * (r + fcc_radius * 0.8)
                n_b = max(int(circ / (fcc_radius * 2.0)), 6)
                for theta in np.linspace(0, 2*np.pi, n_b, endpoint=False):
                    bx = px + (r + fcc_radius * 0.8) * np.cos(theta)
                    by = py + (r + fcc_radius * 0.8) * np.sin(theta)
                    if bx**2 + by**2 < (R_rup - fcc_radius)**2:
                        boundary_fcc.append(patches.Circle((bx, by), fcc_radius))
                        
            bound_col = PatchCollection(boundary_fcc, facecolor='#00FFFF', edgecolor='#003388', lw=0.4, alpha=1.0, zorder=3.5)
            ax.add_collection(bound_col)

            # SC Cores
            for px, py, r in zip(pts[:, 0], pts[:, 1], all_radii):
                # Adjusted line thickness (lw) to 0.65 to ensure the red matter boundary is clearly visible
                core = patches.Circle((px, py), r, facecolor='#111111', edgecolor='#CC0000', lw=0.65, zorder=5)
                ax.add_patch(core)
                grid_step = max(0.12, r / 6.0)
                for gx in np.arange(px - r, px + r, grid_step):
                    line, = ax.plot([gx, gx], [py - r, py + r], color='#2A2D34', lw=0.5, zorder=6)
                    line.set_clip_path(core)
                for gy in np.arange(py - r, py + r, grid_step):
                    line, = ax.plot([px - r, px + r], [gy, gy], color='#2A2D34', lw=0.5, zorder=6)
                    line.set_clip_path(core)

            # =======================================================
            # ANNOTATIONS FOR PANEL A (Corrected Outer Margins & Precision Targets)
            # =======================================================
            # Find the top-right core dynamically for a precise hit
            tr_idx = np.argmax(pts[:, 0] + pts[:, 1])
            core_target_x = pts[tr_idx, 0] + all_radii[tr_idx] * np.cos(np.pi/4)
            core_target_y = pts[tr_idx, 1] + all_radii[tr_idx] * np.sin(np.pi/4)
            
            ax.annotate(r"$\mathbf{State\ II\ SC\ Core}$" + "\n" + r"(Black Hole)", 
                        xy=(core_target_x, core_target_y), xytext=(11.5, 11.5),
                        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
                        color='black', fontsize=10, ha='center', va='center', bbox=text_bbox, zorder=20)
            
            # Target the actual fault line in the bottom right, not just the core
            br_idx = np.argmax(pts[:, 0] - pts[:, 1])
            fault_target_x = pts[br_idx, 0] + all_radii[br_idx] * np.cos(-np.pi/4)
            fault_target_y = pts[br_idx, 1] + all_radii[br_idx] * np.sin(-np.pi/4)
            # Find the edge connecting to this core
            for u, v in edges:
                if u == br_idx or v == br_idx:
                    other_idx = v if u == br_idx else u
                    # Shift the target point slightly to guarantee a precise visual hit on the line
                    fault_target_x = pts[br_idx, 0] * 0.65 + pts[other_idx, 0] * 0.35
                    fault_target_y = pts[br_idx, 1] * 0.65 + pts[other_idx, 1] * 0.35
                    break
            
            # Shift the arrow tip 2 granular FCC nodes (approx 0.3 units) forward along the pointing vector
            arr_dx = fault_target_x - 11.5
            arr_dy = fault_target_y - (-11.5)
            arr_len = np.hypot(arr_dx, arr_dy)
            fault_target_x += 0.3 * (arr_dx / arr_len)
            fault_target_y += 0.3 * (arr_dy / arr_len)
            
            ax.annotate(r"$\mathbf{Global\ Percolation}$" + "\n" + r"(Fault Line)", 
                        xy=(fault_target_x, fault_target_y), xytext=(11.5, -11.5),
                        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
                        color='black', fontsize=10, ha='center', va='center', bbox=text_bbox, zorder=20)

        # =======================================================
        # RIGHT PANEL: THE GREAT RUPTURE (EXPANSION & BAO)
        # =======================================================
        else:
            solid_base = patches.Circle((0, 0), R_orig, facecolor='#0055AA', edgecolor='none', alpha=1.0, zorder=2)
            ax.add_patch(solid_base)
            
            orig_horizon_solid = patches.Circle((0, 0), R_orig, fill=False, edgecolor='#002266', linestyle='-', lw=2.5, zorder=2.1)
            ax.add_patch(orig_horizon_solid)
            
            ax.add_patch(patches.Circle((0, 0), R_rup, fill=False, edgecolor='#FFFFFF', linestyle=':', lw=1.5, alpha=0.6, zorder=2.5))

            restored_text = r"$\mathbf{Restored\ Geometric\ Cosmic\ Horizon}$" + "\n" + r"($R_{\mathrm{Res}} \approx 10^{35}\ \mathrm{m}$)"
            ax.annotate(restored_text, xy=(0, R_orig), xytext=(0, R_orig + 1.5),
                        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
                        color='black', fontsize=10, ha='center', va='bottom', bbox=text_bbox, zorder=10)

            # EXPANDED FCC LATTICE (300% Bigger)
            fcc_radius_expanded = 0.24 
            spacing_expanded = fcc_radius_expanded * 1.732 
            
            xs_e = np.arange(-R_orig, R_orig, spacing_expanded)
            ys_e = np.arange(-R_orig, R_orig, spacing_expanded * np.sqrt(3)/2)
            Xe_grid, Ye_grid = np.meshgrid(xs_e, ys_e)
            
            Xe_grid[1::2] += spacing_expanded / 2
            Xe_flat, Ye_flat = Xe_grid.flatten(), Ye_grid.flatten()
            
            mask_circle_e = (Xe_flat**2 + Ye_flat**2) < (R_orig - fcc_radius_expanded * 1.5)**2
            Xe_flat, Ye_flat = Xe_flat[mask_circle_e], Ye_flat[mask_circle_e]
            
            bulk_fcc_e = [patches.Circle((x, y), fcc_radius_expanded) for x, y in zip(Xe_flat, Ye_flat)]
            bulk_col_e = PatchCollection(bulk_fcc_e, facecolor='#00E0FF', edgecolor='#0055AA', lw=0.8, alpha=0.85, zorder=3)
            ax.add_collection(bulk_col_e)

            # BARYON ACOUSTIC OSCILLATIONS
            for px, py, r in zip(pts[:, 0], pts[:, 1], all_radii):
                ax.add_patch(patches.Circle((px, py), r * 2.5, fill=False, edgecolor='#FFFFFF', lw=1.5, alpha=0.6, zorder=8))
                ax.add_patch(patches.Circle((px, py), r * 5.0, fill=False, edgecolor='#FFFFFF', lw=0.8, alpha=0.3, zorder=8))
                ax.add_patch(patches.Circle((px, py), r * 7.5, fill=False, edgecolor='#FFFFFF', lw=0.4, alpha=0.15, zorder=8))

            # TINY MATTER SIGNS
            np.random.seed(42) 
            t_knot = np.linspace(0, 2 * np.pi, 60)
            knot_scale = 0.04 
            knot_coords = []
            
            for px, py, r in zip(pts[:, 0], pts[:, 1], all_radii):
                num_knots = int(max(1, 3 * r**2))
                
                for _ in range(num_knots):
                    angle = np.random.uniform(0, 2 * np.pi)
                    ring_mult = np.random.choice([2.5, 5.0, 7.5])
                    r_periph = r * ring_mult + np.random.uniform(-r*0.2, r*0.2)
                    mx = px + r_periph * np.cos(angle)
                    my = py + r_periph * np.sin(angle)
                    
                    if mx**2 + my**2 < (R_orig - knot_scale*2)**2:
                        knot_coords.append((mx, my))
                        rot = np.random.uniform(0, 2 * np.pi)
                        kx = knot_scale * np.sin(3 * t_knot + np.pi/4)
                        ky = knot_scale * np.sin(2 * t_knot)
                        kx_rot = kx * np.cos(rot) - ky * np.sin(rot)
                        ky_rot = kx * np.sin(rot) + ky * np.cos(rot)
                        
                        # Set matter color to red (#CC0000) for visual contrast
                        ax.plot(mx + kx_rot, my + ky_rot, color='#CC0000', lw=0.8, alpha=0.75, zorder=9)

            # DECOMPRESSION VECTORS
            num_bursts = 12 
            for angle in np.linspace(0, 2*np.pi, num_bursts, endpoint=False):
                dx, dy = np.cos(angle), np.sin(angle)
                start_x, start_y = (R_rup - 0.4) * dx, (R_rup - 0.4) * dy
                end_r = R_orig - 0.02 
                end_x, end_y = end_r * dx, end_r * dy
                
                hl = 0.45  
                hw = 0.25  
                base_x, base_y = end_x - hl * dx, end_y - hl * dy
                
                ax.plot([start_x, base_x], [start_y, base_y], color='white', lw=1.0, zorder=10)
                ax.plot([start_x, base_x], [start_y, base_y], color='black', lw=1.0, ls="--", zorder=11)
                
                pt1 = [end_x, end_y]
                pt2 = [base_x - hw * dy, base_y + hw * dx]
                pt3 = [base_x + hw * dy, base_y - hw * dx]
                head = patches.Polygon([pt1, pt2, pt3], facecolor='black', edgecolor='black', lw=1.0, zorder=12)
                ax.add_patch(head)

            # =======================================================
            # ANNOTATIONS FOR PANEL B (Corrected Outer Margins & Precision Targets)
            # =======================================================
            # Target a specific FCC node inside the top-left quadrant, rather than the perimeter
            dist_to_target = (Xe_flat - (-6.0))**2 + (Ye_flat - 6.0)**2
            ul_idx = np.argmin(dist_to_target)
            fcc_target_x = Xe_flat[ul_idx]
            fcc_target_y = Ye_flat[ul_idx]
            
            ax.annotate(r"$\mathbf{Restored\ FCC\ Node}$" + "\n" + r"(State I Active Vacuum)", 
                        xy=(fcc_target_x, fcc_target_y), xytext=(-10.9, 11.5),
                        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
                        color='black', fontsize=10, ha='center', va='center', bbox=text_bbox, zorder=20)
            
            # Target the 2.5x ring (prominent white inner shockwave) of the top-right core
            tr_idx = np.argmax(pts[:, 0] + pts[:, 1])
            echo_target_x = pts[tr_idx, 0] + (all_radii[tr_idx] * 2.5) * np.cos(np.pi/4)
            echo_target_y = pts[tr_idx, 1] + (all_radii[tr_idx] * 2.5) * np.sin(np.pi/4)
            
            ax.annotate(r"$\mathbf{Phonon\ Echo}$" + "\n" + r"(BAO Shockwaves)", 
                        xy=(echo_target_x, echo_target_y), xytext=(11.5, 11.5),
                        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
                        color='black', fontsize=10, ha='center', va='center', bbox=text_bbox, zorder=20)
            
            # Target a specific knot in the bottom right
            if knot_coords:
                knot_arr = np.array(knot_coords)
                br_knot_idx = np.argmax(knot_arr[:, 0] - knot_arr[:, 1])
                matter_target_x, matter_target_y = knot_arr[br_knot_idx]
            else:
                matter_target_x, matter_target_y = 7.0, -6.0
                
            ax.annotate(r"$\mathbf{Baryonic\ Matter}$" + "\n" + r"(Topological Defects)", 
                        xy=(matter_target_x, matter_target_y), xytext=(11.5, -11.5),
                        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
                        color='black', fontsize=10, ha='center', va='center', bbox=text_bbox, zorder=20)

        # -------------------------------------------------------
        # STYLING & FORMATTING
        # -------------------------------------------------------
        # CRITICAL FIX: Applying the expanded limits
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        # Panel Identifier successfully decoupled from scientific labels
        ax.text(-limit + 0.5, limit - 0.5, panel_title, fontsize=14, ha='left', va='top', zorder=30, bbox=text_bbox)

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
    create_deflation_rupture_baseline()