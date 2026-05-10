import numpy as np
import matplotlib.pyplot as plt
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
    # GENERATE THE COMPACT ROSETTE CORE
    # -------------------------------------------------------
    # This generates a tight, overlapping weave that mimics the dense interior 
    # of the previous figure-8 model, but without the large outer loops.
    
    def draw_dense_lobe(angle, inner_radius=0.6, outer_reach=4.5):
        # We use a modified parametric curve to create a tight petal/teardrop 
        # that overlaps heavily near the center to create the woven core.
        t = np.linspace(0, 2 * np.pi, 200)
        
        # A creates the radial length, B creates the lateral thickness
        A = (outer_reach - inner_radius) / 2.0
        B = A * 0.8  # Thicker lateral profile creates a tighter weave
        
        # Shift the center of the petal outward so the inner edge rests on inner_radius
        x_center_offset = inner_radius + A
        
        # Base parametric curve (a squashed ellipse/petal)
        x_base = x_center_offset + A * np.cos(t)
        # Using sin(t) * (1 - alpha * cos(t)) creates a teardrop shape pointing inward
        y_base = B * np.sin(t) * (1.0 - 0.4 * np.cos(t))
        
        # Rotate by the assigned radial angle
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        x_rot = x_base * cos_a - y_base * sin_a
        y_rot = x_base * sin_a + y_base * cos_a
        
        # 1. Solid Body Fill (Opaque pale maroon)
        ax.fill(x_rot, y_rot, color='#FFDDDD', alpha=0.95, zorder=5)
        
        # 2. Outer Ribbon (Muted Maroon)
        ax.plot(x_rot, y_rot, color='#8B0000', lw=2.5, zorder=6)

    # We maintain high density to ensure the overlap creates the complex lattice pattern
    num_nodes = 60
    for i in range(num_nodes):
        angle = i * (2 * np.pi / num_nodes)
        draw_dense_lobe(angle)

    # Frame limits adjusted to the new compact size
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)

    # -------------------------------------------------------
    # EXPORT
    # -------------------------------------------------------
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig_Dense_Nucleon_Core.pdf")
    
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