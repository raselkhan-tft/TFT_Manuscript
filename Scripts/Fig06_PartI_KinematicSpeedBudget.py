import numpy as np # Selected for rapid vector calculation and trigonometric mapping
import matplotlib.pyplot as plt # Selected for precise 2D vector graphic control and native LaTeX rendering
from matplotlib.patches import Arc
import os # Selected for robust directory management and path-specific file saving

def create_kinematic_triangle():
    # Setup Figure (Minimalist Architectural Styling)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    ax.set_facecolor('white')
    
    # -------------------------------------------------------
    # PARAMETERS
    # -------------------------------------------------------
    c_E = 1.0  # Total Action Budget (Hypotenuse)
    
    # Primary Triangle (State 1: Rest/Slow motion)
    phi_1 = np.radians(55)  
    x_1 = c_E * np.cos(phi_1)
    y_1 = c_E * np.sin(phi_1)
    
    # Secondary Triangle (State 2: High velocity, approaching limit)
    phi_2 = np.radians(20)  
    x_2 = c_E * np.cos(phi_2)
    y_2 = c_E * np.sin(phi_2)

    # -------------------------------------------------------
    # THE INVARIANT BOUNDARY (The Pythagorean Limit)
    # -------------------------------------------------------
    # Drawing a faint quarter-circle to prove the hypotenuse is fixed
    theta = np.linspace(0, np.pi/2, 100)
    arc_x = c_E * np.cos(theta)
    arc_y = c_E * np.sin(theta)
    ax.plot(arc_x, arc_y, color='#CCCCCC', linestyle='-', linewidth=2, zorder=1)

    # Label the Boundary (Positioned at 45 degrees, tangent to the arc)
    arc_label_angle = np.pi / 4
    arc_label_radius = c_E + 0.03 # Slight radial offset to keep it outside the line
    label_arc_x = arc_label_radius * np.cos(arc_label_angle)
    label_arc_y = arc_label_radius * np.sin(arc_label_angle)
    
    # A rotation of -45 degrees perfectly matches the tangent of the circle at 45 degrees
    ax.text(label_arc_x, label_arc_y, 
            r"Kinematic Boundary ($c_{\mathrm{E}}$)", color='#999999', 
            fontsize=11, rotation=-45, ha='center', va='center')

    # -------------------------------------------------------
    # SECONDARY OVERLAY (Approaching the Limit)
    # -------------------------------------------------------
    # Drawn first so it sits behind the primary triangle
    # Hypotenuse (Matched to Black, alpha-faded)
    ax.plot([0, x_2], [0, y_2], color='black', linestyle='--', linewidth=2, alpha=0.5, zorder=2)
    # Vertical Leg (Matched to Maroon, alpha-faded)
    ax.plot([x_2, x_2], [0, y_2], color='#800000', linestyle='--', linewidth=2, alpha=0.5, zorder=2)
    # Horizontal Base (Matched to Deep Navy Blue, alpha-faded)
    ax.plot([0, x_2], [0, 0], color='#000080', linestyle='--', linewidth=2, alpha=0.5, zorder=2)
    
    # Transition Arrow (Pulled toward origin and shortened to fit cleanly between hypotenuses)
    R_arc = 0.45  
    start_x = R_arc * np.cos(phi_1 - 0.08)  
    start_y = R_arc * np.sin(phi_1 - 0.08)
    end_x = R_arc * np.cos(phi_2 + 0.08)
    end_y = R_arc * np.sin(phi_2 + 0.08)

    ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
                arrowprops=dict(arrowstyle="->", color="#888888", lw=1.5, connectionstyle="arc3,rad=-0.15"))
    
    # Position text precisely at the geometric midpoint of the arc, tangent to its curve
    phi_mid = (phi_1 + phi_2) / 2.0
    R_label = R_arc + 0.05 # Offset slightly outside the arc
    lbl_x = R_label * np.cos(phi_mid)
    lbl_y = R_label * np.sin(phi_mid)
    
    # Tangent angle for a circle going downwards is theta - 90 degrees
    tangent_angle = np.degrees(phi_mid) - 90
    
    ax.text(lbl_x, lbl_y, r"As $\Delta\phi \to 0$", color='#555555', 
            fontsize=10, rotation=tangent_angle, ha='center', va='center')

    # -------------------------------------------------------
    # PRIMARY TRIANGLE (The Kinematic Speed Budget)
    # -------------------------------------------------------
    # 1. Horizontal Base (External Velocity) - Deep Navy Blue
    ax.plot([0, x_1], [0, 0], color='#000080', linestyle='-', linewidth=3.5, zorder=3)
    # Label Base
    ax.text(x_1 / 2, -0.02, r"$v_{\mathrm{ext}} = c_{\mathrm{E}} \cos(\Delta\phi)$", color='#000080', 
            fontsize=14, fontweight='bold', ha='center', va='top')

    # 2. Vertical Leg (Internal Vibration/Time) - Maroon
    ax.plot([x_1, x_1], [0, y_1], color='#800000', linestyle='-', linewidth=3.5, zorder=3)
    # Label Vertical
    ax.text(x_1 + 0.045, y_1 / 2, r"$v_{\mathrm{int}} = c_{\mathrm{E}} \sin(\Delta\phi)$", color='#800000', 
            fontsize=14, fontweight='bold', ha='center', va='bottom', rotation=90)

    # 3. The Hypotenuse (Total Budget)
    ax.plot([0, x_1], [0, y_1], color='black', linestyle='-', linewidth=4, zorder=3)
    
    # Label Hypotenuse (Calculated perpendicular offset for close, parallel alignment)
    mid_x, mid_y = x_1 / 2, y_1 / 2
    perp_offset = 0.045  
    hyp_label_x = mid_x - perp_offset * np.sin(phi_1)
    hyp_label_y = mid_y + perp_offset * np.cos(phi_1)
    
    # Placed precisely at 50% length
    ax.text(hyp_label_x, hyp_label_y, r"$c_{\mathrm{E}}$ (Kinematic Speed Budget)", color='black', 
            fontsize=14, fontweight='bold', ha='center', va='center', rotation=np.degrees(phi_1))

    # 4. The Angle (Phase Slip)
    arc = Arc((0, 0), 0.3, 0.3, angle=0, theta1=0, theta2=np.degrees(phi_1), color='black', lw=2, zorder=4)
    ax.add_patch(arc)
    ax.text(0.20, 0.11, r"$\Delta\phi$", color='black', fontsize=16, fontweight='bold', ha='center', va='center')

    # -------------------------------------------------------
    # STYLING & FORMATTING
    # -------------------------------------------------------
    # Removing standard bounding boxes for a clean mathematical aesthetic
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    
    # Hide axis ticks, keep it abstract
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Force 1:1 Aspect Ratio (CRITICAL: Proves the geometry visually)
    ax.set_aspect('equal')
    
    # Set explicit limits to frame the geometry perfectly
    ax.set_xlim(-0.1, 1.2)
    ax.set_ylim(-0.1, 1.1)
    
    plt.tight_layout()

    # -----------------------
    # PDF Export Logic
    # -----------------------
    # Use relative pathing to allow execution across different machine environments
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig06_PartI_KinematicSpeedBudget.pdf")
    
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
    create_kinematic_triangle()