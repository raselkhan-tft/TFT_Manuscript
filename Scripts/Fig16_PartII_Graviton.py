import numpy as np # Selected for efficient, vectorized array math to generate smooth continuous waveforms
import matplotlib.pyplot as plt # Selected for precise, coordinate-level control over diagrammatic rendering
import os # Selected for robust local directory management and path-specific file saving

def create_strain_shadow_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })
    
    # Setup Figure with standard academic margins (allows room for axis labels)
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # -------------------------------------------------------
    # 2. ESTABLISH THE COORDINATE FRAME
    # -------------------------------------------------------
    # Remove top and right boundary lines for a cleaner academic aesthetic
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # X-axis label pad adjusted to center it vertically in the bottom margin clearance
    ax.set_xlabel(r"Propagation Space ($x$)", fontsize=13, labelpad=20)
    
    # Y-axis label pad reduced to 0 to pull the label inward, aligning with the brackets
    ax.set_ylabel(r"Scale Depth ($Z$)", fontsize=13, labelpad=0)
    
    # Enable specific Y-ticks for the dual-floor architecture
    ax.set_yticks([1.0, 5.0])
    ax.set_yticklabels([
        r"Hard Floor" + "\n" + r"($\ell_{\mathrm{S}} \approx 10^{-35}$ m)",
        r"Soft Floor" + "\n" + r"($r_{\mathrm{D}} \approx 10^{-26}$ m)"
    ], fontsize=11)
    
    # Empty X ticks maintain the theoretical schema look
    ax.set_xticks([])
    
    # X Domain (2000 points provide high resolution for smooth curves)
    x = np.linspace(0, 12, 2000)
    
    # -------------------------------------------------------
    # 1. THE SOFT FLOOR (Top - The Photon)
    # -------------------------------------------------------
    x_c = 6.0 # Center anchor point
    wavelength = 3.0
    k = 2 * np.pi / wavelength
    
    # Soft Floor Equilibrium: Faint Grey Dashed Line at Y=5
    ax.axhline(y=5, color='#CCCCCC', linestyle='--', linewidth=1.5, zorder=0)
    
    # Photon Wave: Muted to Deep Navy Blue for academic formality
    y_photon = 5 + 0.8 * np.cos(k * (x - x_c))
    ax.plot(x, y_photon, color='#000080', linewidth=2.5, label='Photon Wave', zorder=2)
    
    # Dynamic Action Label
    ax.text(x_c, 6.2, r"Dynamic Action ($E=hf$)", color='black', fontsize=11, ha='center', va='bottom')

    # -------------------------------------------------------
    # 3. THE HARD FLOOR (Bottom - The Graviton/Strain)
    # -------------------------------------------------------
    y_base = 1.0
    dip_depth = 0.0 
    dip_width = 0.3 
    
    # Gaussian dip equation evaluates flat, maintaining underlying math framework
    y_gravity = y_base - dip_depth * np.exp(-((x - x_c)**2) / (2 * dip_width**2))
    
    # Plot Hard Floor
    ax.fill_between(x, 0.0, y_gravity, facecolor='#E5E5E5', alpha=1.0, zorder=1, edgecolor='none')
    
    # Anchor point: Updated to Dark Crimson for formal contrast
    ax.scatter([x_c], [y_base], color='#8B0000', s=60, zorder=4)
    
    # State 0 Substrate Label: Moved to the bottom-left corner
    ax.text(0.5, 0.4, "State 0 Substrate", color='#666666', fontsize=12, ha='left', va='center', zorder=5)

    # -------------------------------------------------------
    # 4. THE TENSION COLUMN (Vertical Strain Coupling)
    # -------------------------------------------------------
    peak_y = 5 + 0.8
    dip_y_bottom = y_base - dip_depth
    
    # Streamlined to a solid vertical tether
    ax.plot([x_c, x_c], [dip_y_bottom, peak_y], color='black', linestyle='-', linewidth=1.5, zorder=0)
    
    # Horizontal label rendering
    ax.text(x_c + 0.2, 3.0, "Vertical Strain\n" + r"Coupling ($\alpha_{\mathrm{G}}$)", 
            color='black', fontsize=11, rotation=0, va='center', ha='left')
            
    # Anchor Energy Label
    ax.text(x_c, dip_y_bottom - 0.2, r"$E_{\mathrm{g}}$", color='black', fontsize=12, ha='center', va='top')

    # -------------------------------------------------------
    # 5. UNIFIED KINEMATIC VECTORS
    # -------------------------------------------------------
    # Vectors aligned at the exact same X-coordinate with identical geometry
    arrow_start_x = x_c + 0.2
    arrow_length = 1.5
    arrow_head_w = 0.15
    arrow_head_l = 0.25
    
    # Top Wave Arrow
    ax.arrow(arrow_start_x, peak_y, arrow_length, 0, 
             head_width=arrow_head_w, head_length=arrow_head_l, fc='black', ec='black')
             
    # Bottom Shadow Arrow
    ax.arrow(arrow_start_x, y_base + 0.3, arrow_length, 0, 
             head_width=arrow_head_w, head_length=arrow_head_l, fc='black', ec='black')
    
    # Unified Velocity Condition Label (Moved to the top of the bottom annotation arrow)
    ax.text(arrow_start_x, y_base + 0.45, r"Lockstep Propagation" + "\n" + r"($v \leq c_{\mathrm{E}}$)", 
            ha='left', va='bottom', fontsize=11, color='black')
    
    # Set absolute limits to frame mathematically perfectly
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5) 
    
    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    # Explicitly calculate and lock the margin layout
    # Left=0.18 provides clearance for the multi-line Y-axis tick labels
    # Bottom=0.12 allows the X-axis label to sit directly in the center of the bottom padding
    plt.subplots_adjust(left=0.18, bottom=0.12, right=0.95, top=0.95)
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig16_PartII_Graviton.pdf")
    
    try:
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()

if __name__ == "__main__":
    create_strain_shadow_visual()