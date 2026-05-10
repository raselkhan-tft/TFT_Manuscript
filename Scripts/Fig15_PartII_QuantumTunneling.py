import numpy as np # Selected for efficient array generation and mathematical transformations
import matplotlib.pyplot as plt # Selected for publication-grade 2D schematic layout
from matplotlib.patches import Arc # Selected for precise geometric rendering of resonance waves
import os # Selected for robust directory management and path-specific file saving

def create_acoustic_tunneling_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    # Setup Figure (Textbook Architectural Styling)
    fig, ax = plt.subplots(figsize=(15, 7), dpi=150)
    fig.patch.set_facecolor('white')

    # Remove standard axes for a clean diagrammatic look
    for ax_obj in [ax]:
        ax_obj.set_facecolor('white')
        ax_obj.set_xticks([])
        ax_obj.set_yticks([])
        for spine in ax_obj.spines.values():
            spine.set_visible(False)

    # -------------------------------------------------------
    # PARAMETERS
    # -------------------------------------------------------
    x_max = 11.5
    x = np.linspace(0, x_max, 1000)
    
    # Wave parameters (Impedance Matched Resonance)
    k = np.pi / 2  
    amplitude = 1.5
    
    # The Pilot Wave (Continuous standing wave through the entire domain)
    y_wave = amplitude * np.cos(k * (x - 3.0))

    # Barrier Boundaries
    barrier_start = 4.0
    barrier_end = 8.0

    # -------------------------------------------------------
    # 0. THE UNIFIED MEDIUM (Implicit Continuum Grid)
    # -------------------------------------------------------
    # Establishing the omnipresent SGF lattice to prevent the "void" paradox
    num_h_lines = 13
    y_base_levels = np.linspace(-3.5, 3.5, num_h_lines)
    
    # Extend faint unwarped grid outside the barrier (Alpha reduced to 0.4)
    for yb in y_base_levels:
        ax.plot([0, barrier_start], [yb, yb], color='#B0C4DE', lw=1.0, alpha=0.4, zorder=0)
        ax.plot([barrier_end, x_max], [yb, yb], color='#B0C4DE', lw=1.0, alpha=0.4, zorder=0)

    for x_v in np.arange(0, x_max, 0.5):
        if x_v <= barrier_start or x_v >= barrier_end:
            ax.plot([x_v, x_v], [-3.5, 3.5], color='#B0C4DE', lw=1.0, alpha=0.4, zorder=0)

    # -------------------------------------------------------
    # 1. THE DENSE BARRIER (Central Region)
    # -------------------------------------------------------
    # Background shading for the barrier density (Alpha reduced to 0.5)
    ax.axvspan(barrier_start, barrier_end, color='#E8ECEF', alpha=0.5, zorder=0)
    
    x_barrier = np.linspace(barrier_start, barrier_end, 300)
    y_wave_barrier = amplitude * np.cos(k * (x_barrier - 3.0))

    # Vertical stiff lattice pillars (Alpha set to 0.8 to soften infrastructure)
    for x_v in np.linspace(barrier_start, barrier_end, 15):
        ax.plot([x_v, x_v], [-3.5, 3.5], color='#B0C4DE', lw=1.5, alpha=0.8, zorder=1)

    # Horizontal lattice links (Oscillating in phase with the standing wave - Alpha reduced to 0.4)
    for yb in y_base_levels:
        osc_factor = np.exp(-(yb / 3.0)**2) 
        y_lattice = yb + (y_wave_barrier * osc_factor * 0.3)
        # Standardized to Deep Navy Blue
        ax.plot(x_barrier, y_lattice, color='#000080', lw=2.0, alpha=0.4, zorder=2)

    # --- Standing Wave Envelope & Superposition Components ---
    # Ghost envelope for standing wave resonance
    y_ghost = -y_wave_barrier
    ax.plot(x_barrier, y_ghost, color='#000080', lw=2, linestyle=':', alpha=0.4, zorder=3)
    
    # Superposition: Suction Wave (Driver) - Standardized to Deep Bronze/Ocher
    y_bw = -amplitude * 0.6 * np.sin(k * (x_barrier - barrier_start))
    ax.plot(x_barrier, y_bw, color='#8B4513', lw=1.5, linestyle='--', alpha=0.8, zorder=4)
    
    ax.annotate(r"$\leftarrow$ Suction Wave (Driver)", 
                xy=(5.0, -0.9), xytext=(5.0, -0.3),
                arrowprops=dict(arrowstyle="->", color="#8B4513", lw=1.5),
                color='black', fontsize=9, ha='center', va='bottom', zorder=12)

    # --- Pinned Boundary Nodes ---
    # Standardized to Muted Maroon
    ax.scatter([barrier_start, barrier_end], [0.0, 0.0], color='#8B0000', s=80, zorder=10)
    
    # Typographic fix applied to descriptive subscript (Z_wall -> Z_{\mathrm{wall}})
    ax.annotate(r"Zero-Displacement Node" + "\n" + r"($Z_{\mathrm{wall}}$ Canceled)", 
                xy=(barrier_start, 0.0), xytext=(3.0, -2.5),
                arrowprops=dict(arrowstyle="->", color="#8B0000", lw=1.5),
                color='black', fontsize=10, fontweight='bold', ha='center',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3), zorder=11)

    # Annotations for Barrier
    ax.text(6, 3.8, "Dense Geometric Lattice Barrier", color='black', 
            fontsize=12, fontweight='bold', ha='center', va='bottom')
    ax.text(6, -3.8, "Standing Wave Bridge\n(Mechanically Transparent / Impedance Matched)", 
            color='black', fontsize=11, fontweight='bold', ha='center', va='top')

    # -------------------------------------------------------
    # 2. THE PILOT WAVE & TOPOLOGICAL KNOT (Left Side)
    # -------------------------------------------------------
    # Continuous pilot wave (Standardized to Deep Navy Blue)
    ax.plot(x, y_wave, color='#000080', lw=3, alpha=0.85, zorder=5)
    
    # Topological Knot
    knot_x_center = 3.0
    knot_y_center = amplitude 
    
    t = np.linspace(0, 2 * np.pi, 300)
    knot_x = knot_x_center + 0.35 * np.sin(3 * t + np.pi/4)
    knot_y = knot_y_center + 0.35 * np.sin(2 * t)
    
    # Mass knot updated to Muted Maroon to standardize matter representation
    ax.plot(knot_x, knot_y, color='#8B0000', lw=2, zorder=6)
    ax.fill(knot_x, knot_y, color='#8B0000', alpha=0.4, zorder=6)
    
    # Add central mass anchor dot to unify matter representation
    ax.scatter([knot_x_center], [knot_y_center], color='#8B0000', s=50, zorder=7)
    
    # Labels and Vectors
    ax.text(knot_x_center, knot_y_center + 0.6, "Topological Knot\n(Particle)", 
            color='black', fontsize=11, fontweight='bold', ha='center', va='bottom')
            
    ax.annotate("Incoming Pilot Wave", 
                xy=(1.5, -1.1), xytext=(1.5, -2.5),
                arrowprops=dict(arrowstyle="->", color="#000080", lw=2),
                color='black', fontsize=11, fontweight='bold', ha='center')

    # Motion Vector (Replaced clunky arrow with standard LaTeX kinematic stealth vector)
    ax.annotate("", xy=(knot_x_center + 1.2, knot_y_center), xytext=(knot_x_center + 0.5, knot_y_center),
                arrowprops=dict(arrowstyle="-|>", color="#000080", lw=2), zorder=7)

    # -------------------------------------------------------
    # 3. THE EXTERNAL DRIVER (Right Side)
    # -------------------------------------------------------
    driver_x = 10.5
    
    ax.plot([driver_x, driver_x], [-2.5, 2.5], color='#2F4F4F', lw=6, zorder=4)
    ax.scatter([driver_x], [0], color='#8B4513', s=100, zorder=5) # Standardized Bronze source node
    
    # Radiating resonance arcs
    for radius in [0.5, 1.0, 1.5]:
        arc = Arc((driver_x, 0), radius*2, radius*2, angle=180, theta1=-45, theta2=45, 
                  color='#8B4513', lw=2, alpha=0.7 - (radius*0.1))
        ax.add_patch(arc)

    # Labels for the Driver (Typographic fix applied: Z_drive -> Z_{\mathrm{drive}})
    ax.text(driver_x, 2.8, r"External Driver ($Z_{\mathrm{drive}}$)", 
            color='black', fontsize=12, fontweight='bold', ha='center', va='bottom')
    ax.text(driver_x, -2.8, r"Stabilizing Frequency ($\omega_0$)", 
            color='black', fontsize=11, fontweight='bold', ha='center', va='top')

    # -------------------------------------------------------
    # STYLING & FORMATTING
    # -------------------------------------------------------
    ax.set_xlim(0, x_max)
    ax.set_ylim(-4.5, 4.5)

    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig15_PartII_QuantumTunneling.pdf")
    
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
    create_acoustic_tunneling_visual()