import numpy as np # Selected for efficient spatial array generation and continuous waveform modeling
import matplotlib.pyplot as plt # Selected for precise 2D coordinate control and native LaTeX text rendering
import os # Selected for robust local directory management and path-specific file saving

def create_entanglement_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })
    
    # Setup Figure (Expanded to 14x8 to guarantee absolute margin clearance)
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # -------------------------------------------------------
    # 1. ESTABLISH THE FORMAL COORDINATE FRAME
    # -------------------------------------------------------
    # X Domain strictly bound to the limits
    x = np.linspace(0, 12, 2000)
    y_soft = 4.5
    y_base = 2.0
    
    # Y-Axis Setup (Scale Depth)
    ax.spines['left'].set_color('black')
    ax.spines['left'].set_linewidth(1.0)
    
    # Disable native y-label to prevent auto-layout collisions
    ax.set_ylabel("") 
    
    # Render blank tick marks at the correct heights to keep physical tick lines
    ax.set_yticks([y_base, y_soft])
    ax.set_yticklabels([])
    
    # Manual Tick Labels: Placed safely outside the spine
    ax.text(-0.2, y_base, r"Hard Floor" + "\n" + r"($\ell_{\mathrm{S}} \approx 10^{-35}$ m)", 
            fontsize=11, ha='right', va='center', color='black', clip_on=False)
            
    ax.text(-0.2, y_soft, r"Soft Floor" + "\n" + r"($r_{\mathrm{D}} \approx 10^{-26}$ m)", 
            fontsize=11, ha='right', va='center', color='black', clip_on=False)
            
    # Manual Y-Axis Label: Centered exactly between y=2.0 and y=4.5 (y=3.25)
    # Shifted to x=-2.0 to perfectly align with the calculated left-edge of the tick labels
    ax.text(-2.0, 3.25, r"Scale Depth ($Z$)", 
            fontsize=13, rotation=90, ha='center', va='center', color='black', clip_on=False)
    
    # X-Axis Setup (Macroscopic Spatial Separation)
    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_linewidth(1.0)
    ax.set_xlabel(r"Macroscopic Spatial Separation ($x$)", fontsize=13, labelpad=10)
    ax.set_xticks([]) # Hide arbitrary numerical ticks
    
    # Remove top and right boundary lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # -------------------------------------------------------
    # 2. THE SOFT FLOOR (Top - The Localized Particles)
    # -------------------------------------------------------
    # Soft Floor Equilibrium (Faint Dashed Line)
    ax.axhline(y=y_soft, color='#CCCCCC', linestyle='--', linewidth=1.5, zorder=0)
    
    # Wave Packet Parameters
    x_A = 3.5
    x_B = 8.5
    wavelength = 1.5
    k = 2 * np.pi / wavelength
    packet_width = 0.5
    peak_amplitude = 0.8
    peak_y = y_soft + peak_amplitude
    
    # Particle A & B (Gaussian-modulated sine waves to show localized energy bursts)
    y_packet_A = peak_amplitude * np.cos(k * (x - x_A)) * np.exp(-((x - x_A)**2) / (2 * packet_width**2))
    y_packet_B = peak_amplitude * np.cos(k * (x - x_B)) * np.exp(-((x - x_B)**2) / (2 * packet_width**2))
    
    # Apply masking to strictly isolate the wave packets
    threshold = 0.01
    mask_A = np.abs(y_packet_A) > threshold
    mask_B = np.abs(y_packet_B) > threshold
    
    # Plotting with formal Deep Navy Blue
    navy_blue = '#000080'
    ax.plot(x[mask_A], y_soft + y_packet_A[mask_A], color=navy_blue, linewidth=2.5, zorder=2)
    ax.plot(x[mask_B], y_soft + y_packet_B[mask_B], color=navy_blue, linewidth=2.5, zorder=2)
    
    # Labels for Particles (Shifted up to clear the new vector positions)
    ax.text(x_A, peak_y + 0.4, "Particle A", color='black', fontsize=12, fontweight='bold', ha='center', va='bottom')
    ax.text(x_B, peak_y + 0.4, "Particle B", color='black', fontsize=12, fontweight='bold', ha='center', va='bottom')

    # Faint dashed line continuing the Soft Floor connection between wave packets
    ax.plot([x_A + 1.2, x_B - 1.2], [y_soft, y_soft], color='#888888', lw=1.5, linestyle='--')

    # Cosmic Separation Bracket (Standard Dimensioning above the line)
    bracket_y = y_soft + 0.4
    ax.annotate('', xy=(x_A + 1.2, bracket_y), xytext=(x_B - 1.2, bracket_y), 
                arrowprops=dict(arrowstyle='<->', color='#555555', lw=1.2))
    ax.text(6.0, bracket_y + 0.1, "Vast Cosmic Separation", color='black', fontsize=11, ha='center', va='bottom')

    # Outward Separation Velocity Vectors (Originating perfectly at the wave peaks)
    ax.annotate('', xy=(x_A - 1.45, peak_y), xytext=(x_A - 0.65, peak_y),
                arrowprops=dict(arrowstyle='-|>', color=navy_blue, lw=1.5), zorder=3)
    ax.text(x_A - 1.65, peak_y, r"$v \leq c_E$", color='black', fontsize=11, ha='right', va='center')
    
    ax.annotate('', xy=(x_B + 1.0, peak_y), xytext=(x_B + 0.2, peak_y),
                arrowprops=dict(arrowstyle='-|>', color=navy_blue, lw=1.5), zorder=3)
    ax.text(x_B + 1.2, peak_y, r"$v \leq c_E$", color='black', fontsize=11, ha='left', va='center')

    # -------------------------------------------------------
    # 3. THE HARD FLOOR (Bottom - The Substrate Anchors)
    # -------------------------------------------------------
    # Thickened Hard Floor slab for massive rigidity representation
    dip_depth = 0.0 
    dip_width = 0.3 
    y_gravity = y_base - dip_depth * np.exp(-((x - x_A)**2) / (2 * dip_width**2))
    
    # Plot Hard Floor Substrate
    ax.fill_between(x, 0.0, y_gravity, facecolor='#E5E5E5', alpha=1.0, zorder=1, edgecolor='none')

    # Substrate Identity Label
    ax.text(0.5, 0.5, "State 0 Substrate", color='#777777', fontsize=12, ha='left', va='center', zorder=5)

    # Anchor Geometry (Muted Maroon)
    maroon = '#8B0000'
    y_anchor = y_base - dip_depth
    ax.scatter([x_A, x_B], [y_anchor, y_anchor], color=maroon, s=60, zorder=4)
    
    ax.text(x_A, y_anchor - 0.2, r"$g_{\mathrm{A}}$", color='black', fontsize=12, ha='center', va='top')
    ax.text(x_B, y_anchor - 0.2, r"$g_{\mathrm{B}}$", color='black', fontsize=12, ha='center', va='top')

    # -------------------------------------------------------
    # 4. THE TENSION COLUMNS & RESIDUAL TETHER
    # -------------------------------------------------------
    # Perpendicular Columns
    ax.plot([x_A, x_A], [peak_y, y_anchor], color='#BBBBBB', linestyle='-', linewidth=2.0, zorder=0)
    ax.plot([x_B, x_B], [peak_y, y_anchor], color='#BBBBBB', linestyle='-', linewidth=2.0, zorder=0)
    
    # Residual Topological Tether: Native to the Substrate
    ax.plot([x_A, x_B], [y_anchor, y_anchor], color='white', linestyle=':', linewidth=2.5, zorder=3)
    ax.text(6.0, y_anchor - 0.2, r"Residual Phase-Tether (Continuous Strain)", color='#555555', fontsize=11, ha='center', va='top')

    # Label the Perpendicular Columns (Horizontal layout, anchored outside the vertical flow)
    y_col_label = (y_soft + y_anchor) / 2.0
    ax.text(x_A - 0.22, y_col_label, "Tension\nColumn A", color='#888888', fontsize=10, rotation=0, va='center', ha='right')
    ax.text(x_B + 0.22, y_col_label, "Tension\nColumn B", color='#888888', fontsize=10, rotation=0, va='center', ha='left')

    # -------------------------------------------------------
    # 5. MECHANISM OF ACTION (Unified Stealth Vectors)
    # -------------------------------------------------------
    # Measurement Torque (Placed tightly between the wave peak and the Particle A label)
    ax.annotate('', xy=(x_A + 0.55, y_soft + 0.53), xytext=(x_A - 0.55, y_soft + 0.65), 
                arrowprops=dict(arrowstyle='-|>', color=maroon, lw=1.5, connectionstyle="arc3,rad=-0.5"), zorder=10)
    ax.text(x_A, y_soft + 1.05, "Measurement (Torque)", color='black', fontsize=10, ha='center', va='center')
    
    # Instantaneous Stress Transfer Route (Unified vector geometries)
    ax.annotate('', xy=(x_A, y_anchor + 0.2), xytext=(x_A, y_soft - 0.2), 
                arrowprops=dict(arrowstyle='-|>', color=maroon, lw=2.0, ls='-'), zorder=10)
    
    center_offset = (x_B - x_A) * 0.1 # 20% span centered
    ax.annotate('', xy=(6.0 + center_offset, y_anchor), xytext=(6.0 - center_offset, y_anchor), 
                arrowprops=dict(arrowstyle='-|>', color=maroon, lw=2.5, ls='-'), zorder=10)
    
    ax.annotate('', xy=(x_B, y_soft - 0.2), xytext=(x_B, y_anchor + 0.2), 
                arrowprops=dict(arrowstyle='-|>', color=maroon, lw=2.0, ls='-'), zorder=10)
    
    # Label for the Instantaneous Pathway
    transfer_text = r"Instantaneous Stress Transfer" + "\n" + r"($\Delta t \to 0$, $c_{\mathrm{S}} \to \infty$)"
    ax.text(6.0, y_anchor - 0.65, transfer_text, color='black', fontsize=11, ha='center', va='center')

    # -------------------------------------------------------
    # 6. FINAL RENDER & PDF EXPORT
    # -------------------------------------------------------
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5) 
    
    # Explicit margins adjusted: Left and Bottom margins expanded by >20% to prevent crowding
    plt.subplots_adjust(left=0.15, bottom=0.18, right=0.95, top=0.95)
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig17_PartII_QuantumEntanglement.pdf")
    
    try:
        # Saving as high-fidelity vector PDF for publication
        # pad_inches mathematically increased by 20% (0.10 -> 0.12)
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight', pad_inches=0.12, facecolor='white')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()

if __name__ == "__main__":
    create_entanglement_visual()