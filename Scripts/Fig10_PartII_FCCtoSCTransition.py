import matplotlib.pyplot as plt # Selected for publication-grade 2D schematic layout and native LaTeX rendering
import matplotlib.patches as patches # Selected for precise structural primitives (Circles, Rectangles)
import numpy as np # Selected for efficient spatial array generation and geometric centroid calculations
import os # Selected for robust directory management and path-specific file saving

def create_phase_transition_figure():
    # Enforce clear, publication-ready font settings
    plt.rcParams.update({
        'savefig.pad_inches': 0.05,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'mathtext.fontset': 'cm', # Ensures math symbols render cleanly in standard Computer Modern italics
        'font.size': 12
    })
    
    # Setup Figure (Pure White Theme for State 0 Representation)
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Set Diagram Limits (Y-limit expanded to 12 to provide ample clearance for headers)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Remove standard bounding box spines for a clean architectural aesthetic
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # ==========================================
    # 1. THE LEFT PANEL: (a) State I Active Vacuum
    # ==========================================
    # Left Panel Background (Matched to FLUID_FILL from mass mechanism)
    left_bg = patches.Rectangle((0, 0), 10, 10.3, facecolor='#b2bfc9', edgecolor='none', zorder=0)
    ax.add_patch(left_bg)

    # Geometry: Spheres crowded and touching (FCC close packing)
    sphere_radius = 0.85
    spacing_x = 1.7
    spacing_y = 1.5 # approx 1.7 * sin(60) for tight hexagonal packing
    
    x_grid_start = 0.8 
    rows = 8 
    cols = 7 
    
    sphere_centers = []
    
    # Calculate all sphere centers
    for c in range(cols):
        for r in range(rows):
            # Stagger every other row
            x_offset = 0 if r % 2 == 0 else spacing_x * 0.5
            cx = x_grid_start + c * spacing_x + x_offset
            cy = 0.5 + r * spacing_y
            
            # Cutoff: Only track if the sphere is mostly within the left side 
            if cx - sphere_radius > 10.0 or cy > 9.8: 
                continue 
            
            sphere_centers.append((cx, cy))

    # --- Ordered Pilot-Wave Field (Concentric waves from interstitial white voids) ---
    void_centers = set()
    for cx, cy in sphere_centers:
        # Approximate void locations relative to each sphere in a hex lattice
        dy_void = spacing_y / 3.0
        v1 = (round(cx + spacing_x/2, 3), round(cy + dy_void, 3))
        v2 = (round(cx + spacing_x/2, 3), round(cy - dy_void, 3))
        void_centers.add(v1)
        void_centers.add(v2)
        
    for vx, vy in void_centers:
        if vx > 10.0 or vx < 0 or vy > 9.8 or vy < 0:
            continue
        # Generate concentric waves propagating outward from the white gaps
        radii = np.linspace(0.05, 0.45, 5)
        for rw in radii:
            wave = patches.Circle((vx, vy), rw, fill=False, edgecolor='#00AACC', 
                                  alpha=0.45, lw=0.8, zorder=1)
            ax.add_patch(wave)

    # --- Draw the Cyan FCC Spheres ---
    for cx, cy in sphere_centers:
        # Reduced linewidth to 0.3 for a very thin boundary ring
        circle = patches.Circle((cx, cy), sphere_radius, 
                                edgecolor='#0055AA', facecolor='#00CCFF', 
                                alpha=1.0, linewidth=0.3, zorder=2)
        ax.add_patch(circle)

    # --- SEGREGATED MATTER (Maroon Gaps) ---
    # Width reduced by 50% (to 0.25) so it explicitly ends where the adjacent FCC nodes touch
    matter_fill = patches.Rectangle((9.75, 0.5), 0.25, 9.0, facecolor='#8B0000', edgecolor='none', zorder=1.5)
    ax.add_patch(matter_fill)

    # Precise geometrical target for the gap midpoint between the topmost intersecting FCC nodes
    # Node A (row=5, col=5): cx=10.15, cy=8.0 | Node B (row=6, col=5): cx=9.30, cy=9.5
    # Midpoint x = 9.725, y = 8.75. Pushed slightly right into the maroon fill block (x=9.80).
    gap_x = 9.80  
    gap_y = 8.75  

    # Annotation pointing to the precisely derived segregated matter crevice
    ax.annotate("Segregated\nMatter", xy=(gap_x, gap_y), xytext=(7.5, gap_y),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5, mutation_scale=12),
                color='black', fontsize=11, fontweight='bold', ha='right', va='center',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=2), zorder=10)

    # Specific scale dimension label for the FCC Node (Lower Left)
    ax.text(0.5, 0.5, r"$\mathbf{FCC\ Node}$" + "\n" + r"($r_{\mathrm{D}} \approx 10^{-26}\ \mathrm{m}$)", 
            color='black', fontsize=11, ha='left', va='bottom',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=2), zorder=10)

    # ==========================================
    # 2. THE TRANSITION: Event Horizon
    # ==========================================
    # Dashed line at x=10 (Maroon core linkage)
    # ymax naturally caps at 10.3 / 12.0
    ax.axvline(x=10, ymin=0, ymax=(10.3/12.0), color='#8B0000', linestyle='--', linewidth=2.0, zorder=5)
    
    # Vertical Label formatted strictly for IUPAP mathematical compliance (Color updated to black)
    ax.text(9.7, 5.0, r'Event Horizon ($R_{\mathrm{QG}}$)', color='black', fontsize=14, 
            ha='right', va='center', rotation=90, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=3), zorder=6)

    # ==========================================
    # 3. THE RIGHT PANEL: (b) State II Saturated Core
    # ==========================================
    # Geometry: Cubes packed shoulder-to-shoulder (Brick Wall)
    cube_size = 1.8 
    
    right_cols = 6
    right_rows = 6
    
    for c in range(right_cols):
        for r in range(right_rows):
            # Start exactly at x=10
            rx = 10.0 + c * cube_size 
            ry = 0.0 + r * cube_size - 0.5 
            
            if ry > 10: continue

            # Draw Cube (Solid Black field with dark gray grid lines)
            rect = patches.Rectangle((rx, ry), cube_size, cube_size, 
                                     edgecolor='#333333', facecolor='black', 
                                     linewidth=1.5, alpha=1.0, zorder=2)
            ax.add_patch(rect)

    # Specific scale dimension label for the SC Node (Lower Right)
    ax.text(19.5, 0.5, r"$\mathbf{SC\ Node}$" + "\n" + r"($\ell_{\mathrm{S}} \approx 10^{-35}\ \mathrm{m}$)", 
            color='black', fontsize=11, ha='right', va='bottom',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=2), zorder=10)

    # ==========================================
    # TOP CANVAS AREA MASK & LABELS
    # ==========================================
    # Absolute geometric mask to ensure no rendering bleed occurs above the strict 10.3 cutoff
    top_mask = patches.Rectangle((0, 10.3), 20, 2.0, facecolor='white', edgecolor='none', zorder=8)
    ax.add_patch(top_mask)

    # Left Header - Top Left of Panel (a)
    ax.text(0.2, 11.2, r"$\mathbf{(a)\ State\ I\ Active\ Vacuum}$", 
            color='black', fontsize=16, ha='left', va='bottom', zorder=10)

    # Right Header - Top Left of Panel (b)
    ax.text(10.2, 11.2, r"$\mathbf{(b)\ State\ II\ Saturated\ Core}$", 
            color='black', fontsize=16, ha='left', va='bottom', zorder=10)

    # ==========================================
    # EXPORT LOGIC
    # ==========================================
    # Fixed margins to prevent window shaking during interactive renders
    plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig10_PartII_FCCtoSCTransition.pdf")
    
    try:
        # Saving as high-fidelity vector PDF for publication
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()

if __name__ == "__main__":
    create_phase_transition_figure()