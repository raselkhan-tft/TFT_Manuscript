import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_nuclear_lattice_visual():
    # Enforce strict academic typography
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_aspect('equal')

    # -------------------------------------------------------
    # 1. THE NUCLEAR BOUNDARY (Strong Force Threshold)
    # -------------------------------------------------------
    R_nucleus = 7.0
    
    # -------------------------------------------------------
    # 2. GENERATE THE COMPACT ROSETTE
    # -------------------------------------------------------
    # Keeping the crossing point fixed at the origin, we incrementally rotate 
    # the Figure-8 (infinity sign) to create a dense, compact interior circle.
    
    def draw_nucleon_8(angle, scale=6.8):
        t_full = np.linspace(0, 2 * np.pi, 400)
        A = scale        # Radial reach to the boundary
        B = scale * 0.25 # Lobe thickness (tuned for tight, gapless side-by-side packing)
        
        # Base Lissajous curve
        x_base = A * np.sin(t_full)
        y_base = B * np.sin(2 * t_full)
        
        # Rotate by angle
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        x_rot = x_base * cos_a - y_base * sin_a
        y_rot = x_base * sin_a + y_base * cos_a
        
        # 1. Solid Body Fill (Opaque pale maroon to block white space)
        ax.fill(x_rot, y_rot, color='#FFDDDD', alpha=0.95, zorder=5)
        
        # 2. Outer Ribbon (Muted Maroon)
        ax.plot(x_rot, y_rot, color='#8B0000', lw=2.5, zorder=6)
        
        # 3. 3D Crossover Gap at the fixed origin
        t_front = np.linspace(-0.25, 0.25, 50)
        x_f = (A * np.sin(t_front)) * cos_a - (B * np.sin(2 * t_front)) * sin_a
        y_f = (A * np.sin(t_front)) * sin_a + (B * np.sin(2 * t_front)) * cos_a
        
        # Eraser line to force perspective
        ax.plot(x_f, y_f, color='#FFDDDD', lw=6.0, solid_capstyle='butt', zorder=7)
        # Front line
        ax.plot(x_f, y_f, color='#8B0000', lw=2.5, solid_capstyle='round', zorder=8)

    # Density increased by 50% (from 32 to 48 nucleons/knots)
    num_nodes = 48
    for i in range(num_nodes):
        # An infinity sign has 180-degree symmetry, so we divide pi by the number of nodes
        angle = i * (np.pi / num_nodes)
        draw_nucleon_8(angle)

    # -------------------------------------------------------
    # 3. THE NUCLEAR BOUNDARY
    # -------------------------------------------------------
    # Re-draw the dotted boundary perfectly on top of the rosette
    ax.add_patch(patches.Circle((0, 0), R_nucleus, fill=False, edgecolor='#666666', linestyle=':', lw=3.0, zorder=11))

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    # -------------------------------------------------------
    # 4. EXPORT
    # -------------------------------------------------------
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig_Dense_Nucleus.pdf")
    
    try:
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight', pad_inches=0.2)
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"Export error: {e}")

    plt.show()

if __name__ == "__main__":
    create_nuclear_lattice_visual()