import numpy as np # Selected for efficient spatial array generation and coordinate mapping
import matplotlib.pyplot as plt # Selected for precise 2D vector graphic control and native LaTeX text rendering
import matplotlib.patches as patches # Selected for rendering pure geometric primitives (Ellipses, Arcs, Rectangles)
import os # Selected for robust directory management

# =============================================================================
# Figure 4.4: The Macroscopic Thermal Projection & Viscous Acoustic Drag
# Updated for Euclidean consistency: Single Horizon & Radius-based Ruler
# =============================================================================

# Constants for TFT (Tension Field Theory)
R_U = 13.39  # Absolute Optical Horizon (Gly)
R_S_VISUAL = 2.0 # Arbitrary visual scale for the acoustic radius

def create_cosmic_horizon_visual():
    # Setup Figure - White background for strict academic submission
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
    ax.set_facecolor('white')

    # -------------------------------------------------------
    # 1. THE MEDIUM: The Spacetime Gravitational Floor (SGF) Grid
    # -------------------------------------------------------
    grid_x = np.linspace(0, 16, 41)
    grid_y = np.linspace(-6, 6, 25)
    for x in grid_x:
        ax.axvline(x, color='lightgray', linestyle='-', lw=0.4, alpha=0.4, zorder=0)
    for y in grid_y:
        ax.axhline(y, color='lightgray', linestyle='-', lw=0.4, alpha=0.4, zorder=0)

    # -------------------------------------------------------
    # 2. THE MACROSCOPIC LAYOUT & HORIZON
    # -------------------------------------------------------
    # Absolute Optical Horizon - Thinned to lw=1.2 to allow vector dimension visibility
    ax.axvline(R_U, color='black', linestyle='-', lw=1.2, zorder=5)
    ax.text(R_U + 0.3, -5.0, r'$\mathbf{Absolute\ Optical\ Horizon}$' + '\n' + r'($R_U \approx 13.39\ \mathrm{Gly}$)', 
            color='black', fontweight='bold', rotation=90, va='bottom', ha='left', fontsize=11, zorder=10)

    # Local Detector
    ax.scatter(0, 0, marker='s', s=120, color='black', zorder=10)
    ax.text(0, -0.6, r"$\mathbf{Local\ Detector}$" + "\n" + r"($R_{obs} = 0$)", 
            ha='center', va='top', fontsize=11, zorder=10)

    # -------------------------------------------------------
    # 3. THE THERMODYNAMIC SHADOW
    # -------------------------------------------------------
    # Grey oval representing the overall temperature deficit
    shadow = patches.Ellipse((R_U, 0.0), width=1.0, height=R_S_VISUAL * 2, facecolor='#888888', alpha=0.5, zorder=4)
    ax.add_patch(shadow)
    
    # Inner dark shadow representing the dense core of the monopole deficit (restored from original)
    inner_shadow = patches.Ellipse((R_U, 0.0), width=0.4, height=0.8, facecolor='black', alpha=0.3, zorder=5)
    ax.add_patch(inner_shadow)
    
    # Shadow Label
    ax.text(R_U + 0.6, 0.0, r"$\mathbf{Thermodynamic\ Impedance\ Shadow}$" + "\n" + r"($\Delta T \approx \pm 30\ \mu\mathrm{K}$)", 
            ha='left', va='center', fontsize=11, zorder=10, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=2))

    # -------------------------------------------------------
    # 4. GEOMETRIC PROJECTIONS (The Core Corrections)
    # -------------------------------------------------------
    # Horizon Line of Sight
    ax.plot([0, R_U], [0, 0], color='black', linestyle=':', lw=1.5, zorder=3)

    # Foundational Anchor (Positioned right-shifted under the line of sight)
    anchor_text = r"$\mathbf{Vacuum\ Damping\ Rate}$ ($\Gamma_D \equiv H_0 = 73.0\ \mathrm{km/s/Mpc}$)"
    ax.text(R_U * 0.65, -0.25, anchor_text, ha='center', va='top', fontsize=11, 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=3), zorder=10)

    # Angular Traces (Top and Bottom Edges)
    ax.plot([0, R_U], [0, R_S_VISUAL], color='black', linestyle='--', lw=1.2, zorder=3)
    ax.plot([0, R_U], [0, -R_S_VISUAL], color='black', linestyle='--', lw=1.2, zorder=3)

    # Full Angle Label
    # Draw arc mapping the full enclosed angle
    theta_arc = np.degrees(np.arctan2(R_S_VISUAL, R_U))
    angle_arc = patches.Arc((0, 0), width=4.0, height=4.0, angle=0, theta1=-theta_arc, theta2=theta_arc, color='black', lw=1.5, zorder=4)
    ax.add_patch(angle_arc)
    
    # ENHANCED MASK: Set alpha to 1.0 and increased padding to fully block underlying dotted lines
    ax.text(2.2, 0.0, r"$100\theta_* \approx 1.041$", ha='left', va='center', fontsize=12, fontweight='bold', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=1.0, pad=4), zorder=10)

    # The Physical Radius (True Acoustic Ruler)
    # UPDATED: xy shifted slightly upward (+0.05) to ensure the arrowhead touches the perimeter/trace intersection
    ax.annotate('', xy=(R_U, R_S_VISUAL + 0.05), xytext=(R_U, 0.0),
                arrowprops=dict(arrowstyle='-|>', color='black', lw=3.0, mutation_scale=20), zorder=6)
    
    ax.text(R_U - 0.2, R_S_VISUAL / 2, r"$\mathbf{True\ Acoustic\ Ruler}$" + "\n" + r"($r_s \approx 42.7\ \mathrm{Mpc}$)", 
            ha='right', va='center', fontsize=11, bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3), zorder=10)

    # -------------------------------------------------------
    # STYLING & FORMATTING
    # -------------------------------------------------------
    ax.set_xlim(-1, 16)
    ax.set_ylim(-5.5, 5.5) 
    ax.axis('off')

    plt.tight_layout() 
    
    # -----------------------
    # PDF Export Logic
    # -----------------------
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pdf_filename = os.path.join(output_dir, "FigX_PartIII_CMB.pdf")
    
    try:
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"Export error: {e}")

    plt.show()

if __name__ == "__main__":
    create_cosmic_horizon_visual()