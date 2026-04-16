import numpy as np # Selected for efficient spatial array generation and geometric alignment
import matplotlib.pyplot as plt # Selected for precise 2D coordinate control and native LaTeX text rendering
import os # Selected for robust local directory management and path-specific file saving

def create_entanglement_visual():
    # Force matplotlib to remove all white padding when saving/rendering
    plt.rcParams['savefig.pad_inches'] = 0
    plt.rcParams['axes.xmargin'] = 0
    plt.rcParams['axes.ymargin'] = 0
    
    # Setup Figure (Full Bleed Architecture)
    fig = plt.figure(figsize=(12, 8), dpi=120)
    fig.patch.set_facecolor('white')
    
    # [left, bottom, width, height] forces axes to the absolute edge (100% span)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_facecolor('white')
    
    # Remove standard axes for a clean, diagrammatic aesthetic
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # X Domain strictly bound to the limits
    x = np.linspace(0, 12, 2000)
    
    # -------------------------------------------------------
    # 1. THE SOFT FLOOR (Top - The Localized Particles)
    # -------------------------------------------------------
    # Soft Floor Equilibrium: Lowered gap to compress vertical space
    y_soft = 4.5
    ax.axhline(y=y_soft, color='#ADD8E6', linestyle='--', linewidth=1.5, zorder=0)
    
    # Wave Packet Parameters (Squeezed inward to x=3.5 and x=8.5 to clear left margin)
    x_A = 3.5
    x_B = 8.5
    wavelength = 1.5
    k = 2 * np.pi / wavelength
    packet_width = 0.5
    peak_amplitude = 0.8
    
    # Hierarchical Stack for Soft Floor Labels
    # Shifted slightly left (from 1.15 to 1.0) and down (y offsets reduced)
    label_x_left = 1.0 
    
    ax.text(label_x_left, y_soft + 0.25, "Soft Floor", color='black', fontsize=11, fontweight='bold', ha='center', va='bottom')
    ax.text(label_x_left, y_soft + 0.05, r"($Z_{soft} \approx 10^{-26}$ m)", color='black', fontsize=10, ha='center', va='bottom')
    
    # Particle A & B (Gaussian-modulated sine waves to show localized energy bursts)
    y_packet_A = peak_amplitude * np.cos(k * (x - x_A)) * np.exp(-((x - x_A)**2) / (2 * packet_width**2))
    y_packet_B = peak_amplitude * np.cos(k * (x - x_B)) * np.exp(-((x - x_B)**2) / (2 * packet_width**2))
    
    # Apply masking to explicitly break the cyan line across the cosmic separation
    threshold = 0.01
    mask_A = np.abs(y_packet_A) > threshold
    mask_B = np.abs(y_packet_B) > threshold
    
    ax.plot(x[mask_A], y_soft + y_packet_A[mask_A], color='#00CCFF', linewidth=3, zorder=2)
    ax.plot(x[mask_B], y_soft + y_packet_B[mask_B], color='#00CCFF', linewidth=3, zorder=2)
    
    # Labels for Particles
    ax.text(x_A, y_soft + 1.4, "Particle A", color='black', fontsize=12, fontweight='bold', ha='center', va='bottom')
    ax.text(x_B, y_soft + 1.4, "Particle B", color='black', fontsize=12, fontweight='bold', ha='center', va='bottom')

    # Cosmic Separation Bracket
    ax.annotate('', xy=(x_A + 1.2, y_soft), xytext=(x_B - 1.2, y_soft), arrowprops=dict(arrowstyle='<->', color='#888888', lw=1.5, linestyle='--'))
    ax.text(6.0, y_soft + 0.15, "Vast Cosmic Separation", color='black', fontsize=11, fontweight='bold', ha='center', va='bottom')

    # Outward Separation Velocity Vectors
    ax.arrow(x_A - 0.9, y_soft, -0.6, 0, head_width=0.15, head_length=0.25, fc='#00CCFF', ec='#00CCFF', zorder=3)
    ax.text(x_A - 1.2, y_soft + 0.2, r"$v \leq c_E$", color='#00CCFF', fontsize=10, fontweight='bold', ha='center', va='bottom')
    
    ax.arrow(x_B + 0.9, y_soft, 0.6, 0, head_width=0.15, head_length=0.25, fc='#00CCFF', ec='#00CCFF', zorder=3)
    ax.text(x_B + 1.2, y_soft + 0.2, r"$v \leq c_E$", color='#00CCFF', fontsize=10, fontweight='bold', ha='center', va='bottom')

    # -------------------------------------------------------
    # 2. THE HARD FLOOR (Bottom - The Substrate Anchors)
    # -------------------------------------------------------
    # Thickened Hard Floor slab for massive rigidity representation
    y_base = 2.0
    dip_depth = 0.0 # Set to zero for a perfectly flat floor
    dip_width = 0.3 
    
    y_gravity = y_base - dip_depth * np.exp(-((x - x_A)**2) / (2 * dip_width**2))
    
    # Plot Hard Floor Substrate (fill_between ensuring it drops to y=0 for maximum thickness)
    ax.fill_between(x, 0.0, y_gravity, facecolor='#E5E5E5', alpha=1.0, zorder=1, edgecolor='none')
    
    # Hierarchical Stack for Hard Floor Labels
    # Centered horizontally exactly between the Z-axis (0.3) and Tension Column A (3.5)
    label_x_hard = (0.3 + x_A) / 2.0 

    # Title placed directly on the substrate surface
    ax.text(label_x_hard, y_base + 0.05, "Hard Floor", color='black', fontsize=11, fontweight='bold', ha='center', va='bottom')
    # Depth label embedded just below the surface line
    ax.text(label_x_hard, y_base - 0.05, r"($Z_{hard} \approx 10^{-35}$ m)", color='black', fontsize=10, ha='center', va='top')

    # Centralized Substrate Label at the bottom of the canvas
    ax.text(6.0, 0.35, "State 0 Substrate", color='#999999', fontsize=14, fontweight='bold', ha='center', va='center', zorder=5)

    # Anchor Geometry
    y_anchor = y_base - dip_depth
    ax.scatter([x_A, x_B], [y_anchor, y_anchor], color='red', s=60, zorder=4)
    ax.text(x_A, y_anchor - 0.15, r"$g_A$", color='black', fontsize=12, fontweight='bold', ha='center', va='top')
    ax.text(x_B, y_anchor - 0.15, r"$g_B$", color='black', fontsize=12, fontweight='bold', ha='center', va='top')

    # -------------------------------------------------------
    # 3. Z-DIMENSION AXIS (Far Left)
    # -------------------------------------------------------
    # Vertical double-headed arrow spanning from Soft Floor to Hard Floor, moved far left
    ax.annotate('', xy=(0.3, y_soft), xytext=(0.3, y_base), arrowprops=dict(arrowstyle='<->', color='#555555', lw=1.5))
    
    # Z-Dimension Label
    ax.text(0.45, (y_soft + y_base) / 2.0, r"$Z$-Dimension (Scale Depth)", color='#555555', fontsize=11, fontweight='bold', rotation=90, ha='left', va='center')

    # -------------------------------------------------------
    # 4. THE TENSION COLUMNS & RESIDUAL TETHER
    # -------------------------------------------------------
    peak_y = y_soft + peak_amplitude
    
    # Perpendicular Columns
    ax.plot([x_A, x_A], [peak_y, y_anchor], color='#BBBBBB', linestyle='-', linewidth=2.5, zorder=0)
    ax.plot([x_B, x_B], [peak_y, y_anchor], color='#BBBBBB', linestyle='-', linewidth=2.5, zorder=0)
    
    # Residual Topological Tether: Native to the Substrate (Off-White/White Dotted Line)
    ax.plot([x_A, x_B], [y_anchor, y_anchor], color='white', linestyle=':', linewidth=2.5, zorder=3)
    
    # Label the Native Tether
    ax.text(6.0, y_anchor - 0.2, r"Residual Phase-Tether (Continuous Strain)", color='#666666', fontsize=11, fontweight='bold', ha='center', va='top')

    # Label the Perpendicular Columns
    y_col_label = (y_soft + y_anchor) / 2.0
    ax.text(x_A - 0.2, y_col_label, "Tension Column A", color='#888888', fontsize=10, rotation=90, va='center', ha='right')
    ax.text(x_B + 0.2, y_col_label, "Tension Column B", color='#888888', fontsize=10, rotation=270, va='center', ha='left')

    # -------------------------------------------------------
    # 5. MECHANISM OF ACTION (The "Aha!" Element)
    # -------------------------------------------------------
    # Measurement Torque (Placed tightly between the wave peak and the Particle A label)
    ax.annotate('', xy=(x_A + 0.55, y_soft + 0.65), xytext=(x_A - 0.55, y_soft + 0.65), arrowprops=dict(arrowstyle='->', color='red', lw=2, connectionstyle="arc3,rad=-0.5"))
    ax.text(x_A, y_soft + 1.05, "Measurement (Torque)", color='red', fontsize=10, fontweight='bold', ha='center', va='bottom')
    
    # Instantaneous Stress Transfer Route
    ax.annotate('', xy=(x_A, y_anchor + 0.5), xytext=(x_A, y_soft - 0.2), arrowprops=dict(arrowstyle='-|>', color='red', lw=2, ls='-'))
    
    center_offset = (x_B - x_A) * 0.1 # 20% span centered
    ax.annotate('', xy=(6.0 + center_offset, y_anchor), xytext=(6.0 - center_offset, y_anchor), arrowprops=dict(arrowstyle='-|>', color='red', lw=2.5, ls='-'))
    
    ax.annotate('', xy=(x_B, y_soft - 0.2), xytext=(x_B, y_anchor + 0.5), arrowprops=dict(arrowstyle='-|>', color='red', lw=2, ls='-'))
    
    # Relocated Label for the Instantaneous Pathway (Adjusted to sit clearly above the Substrate label)
    ax.text(6.0, y_anchor - 0.55, r"Instantaneous Stress Transfer", color='red', fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(6.0, y_anchor - 0.85, r"($\Delta t \to 0$, $c_S \to \infty$)", color='black', fontsize=11, fontweight='bold', ha='center', va='center')

    # -------------------------------------------------------
    # 6. FINAL RENDER & PDF EXPORT
    # -------------------------------------------------------
    # Set absolute limits to frame mathematically perfectly
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5) 
    
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig17_PartII_QuantamEntanglement.pdf")
    
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
    create_entanglement_visual()