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
    # Expanded grid generation to x=20 to cover the extended text bounding box
    grid_x = np.linspace(0, 20, 51)
    grid_y = np.linspace(-6, 6, 25)
    for x in grid_x:
        ax.axvline(x, color='lightgray', linestyle='-', lw=0.4, alpha=0.4, zorder=0)
    for y in grid_y:
        ax.axhline(y, color='lightgray', linestyle='-', lw=0.4, alpha=0.4, zorder=0)

    # -------------------------------------------------------
    # 2. THE MACROSCOPIC LAYOUT & HORIZON
    # -------------------------------------------------------
    # Absolute Optical Horizon - Updated to gray dotted line
    ax.axvline(R_U, color='gray', linestyle=':', lw=1.5, zorder=5)
    ax.text(R_U + 0.3, -5.0, r'$\mathbf{Viscous\ Cosmic\ Horizon}$', 
            color='black', fontweight='bold', rotation=90, va='bottom', ha='left', fontsize=11, zorder=10)

    # Local Detector
    ax.scatter(0, 0, marker='s', s=120, color='black', zorder=10)
    ax.text(0, -0.6, r"$\mathbf{Local\ Detector}$" + "\n" + r"($R_{\mathrm{obs}} = 0$)", 
            ha='center', va='top', fontsize=11, zorder=10)
            
    # Formal Radial Dimension Line (R_U) - Moved to top with vertical extension lines (CAD style)
    # The tip of the r_s arrow is at y = 2.0.
    # To reduce the gap (previously 5.0 - 2.0 = 3.0) by 50%, the new gap should be 1.5.
    # Therefore, dim_y = 2.0 + 1.5 = 3.5.
    dim_y = 3.5
    # Left vertical extension line from detector
    ax.plot([0, 0], [0.5, dim_y + 0.3], color='black', lw=0.8, zorder=4)
    # Right vertical extension line from horizon
    ax.plot([R_U, R_U], [R_S_VISUAL + 0.5, dim_y + 0.3], color='black', lw=0.8, zorder=4)
    
    # Horizontal dimension bracket
    ax.annotate("", xy=(0, dim_y), xytext=(R_U, dim_y),
                arrowprops=dict(arrowstyle="<|-|>", lw=1.2, color='black', mutation_scale=10), zorder=4)
    ax.text(R_U / 2, dim_y - 0.2, r"$R_{\mathrm{U}} \approx 13.39\ \mathrm{Gly}$", 
            ha='center', va='top', fontsize=12, fontweight='bold', color='black', zorder=10,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=3))

    # -------------------------------------------------------
    # 3. THE THERMODYNAMIC SHADOW
    # -------------------------------------------------------
    # 1. The Faint Electric Blue Field (Fill Only)
    shadow_fill = patches.Ellipse((R_U, 0.0), width=1.0, height=R_S_VISUAL * 2, 
                                  facecolor='#00CCFF', alpha=0.2, edgecolor='none', zorder=4)
    ax.add_patch(shadow_fill)
    
    # 2. The Solid Maroon Perimeter (Edge Only)
    # Decoupled to enforce 100% opacity on the ring, preventing it from washing out to gray
    shadow_edge = patches.Ellipse((R_U, 0.0), width=1.0, height=R_S_VISUAL * 2, 
                                  facecolor='none', edgecolor='#8B0000', lw=2.5, alpha=1.0, zorder=5)
    ax.add_patch(shadow_edge)
    
    # Inner depleted core (Dotted maroon perimeter, transparent interior)
    inner_shadow = patches.Ellipse((R_U, 0.0), width=0.4, height=0.8, 
                                   facecolor='none', edgecolor='#8B0000', ls=':', lw=1.5, zorder=6)
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
    anchor_text = r"$\mathbf{Vacuum\ Damping\ Rate}$ ($\Gamma_{\mathrm{D}} \equiv H_0 = 73.0\ \mathrm{km/s/Mpc}$)"
    ax.text(R_U * 0.65, -0.25, anchor_text, ha='center', va='top', fontsize=11, 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=3), zorder=10)

    # Angular Traces (Top and Bottom Edges)
    ax.plot([0, R_U], [0, R_S_VISUAL], color='black', linestyle='--', lw=1.2, zorder=3)
    ax.plot([0, R_U], [0, -R_S_VISUAL], color='black', linestyle='--', lw=1.2, zorder=3)

    # Half Angle Label (Angular Radius)
    # Pushed the arc further right (radius 4.0 -> width/height 8.0) where the cone is wider
    theta_arc = np.degrees(np.arctan2(R_S_VISUAL, R_U))
    angle_arc = patches.Arc((0, 0), width=8.0, height=8.0, angle=0, theta1=0, theta2=theta_arc, color='black', lw=1.5, zorder=4)
    ax.add_patch(angle_arc)
    
    # Position text dynamically: Just to the right of the arc, vertically centered between the traces
    text_x = 4.2
    text_y = (4.0 * R_S_VISUAL / R_U) / 2.0
    
    ax.text(text_x, text_y, r"$\theta_* \approx 0.01041\ \mathrm{rad}$", ha='left', va='center', fontsize=12, fontweight='bold', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=1.0, pad=2), zorder=10)

    # The Physical Radius (True Acoustic Ruler)
    # Updated color strictly back to Black as requested
    ax.annotate('', xy=(R_U, R_S_VISUAL + 0.05), xytext=(R_U, 0.0),
                arrowprops=dict(arrowstyle='-|>', color='black', lw=3.5, mutation_scale=20), zorder=8)
    
    # Label restored to formal Black, value corrected to 42.75 Mpc
    ax.text(R_U - 0.2, R_S_VISUAL / 2, r"$\mathbf{True\ Acoustic\ Ruler}$" + "\n" + r"($r_{\mathrm{s}} \approx 42.75\ \mathrm{Mpc}$)", 
            ha='right', va='center', fontsize=11, color='black', fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3), zorder=10)

    # -------------------------------------------------------
    # STYLING & FORMATTING
    # -------------------------------------------------------
    # Expanded X-limit to 20 to ensure the background grid encompasses the shadow label
    ax.set_xlim(-1, 20)
    ax.set_ylim(-5.5, 5.5) 
    ax.axis('off')

    plt.tight_layout() 
    
    # -----------------------
    # PDF Export Logic
    # -----------------------
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pdf_filename = os.path.join(output_dir, "Fig22_PartIII_CMB.pdf")
    
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