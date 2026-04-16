import numpy as np # Selected for efficient, vectorized array math to generate smooth waveforms
import matplotlib.pyplot as plt # Selected for precise, coordinate-level control over diagrammatic rendering
import os # Selected for robust local directory management and path-specific file saving

def create_strain_shadow_visual():
    # Force matplotlib to remove all white padding when saving/rendering
    # Modifying rcParams prevents the backend from applying a default bounding box margin
    plt.rcParams['savefig.pad_inches'] = 0
    plt.rcParams['axes.xmargin'] = 0
    plt.rcParams['axes.ymargin'] = 0
    
    # Setup Figure
    fig = plt.figure(figsize=(12, 8), dpi=120)
    fig.patch.set_facecolor('white')
    
    # [left, bottom, width, height] forces axes to the absolute edge (100% span)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_facecolor('white')
    
    # Remove standard axes for a clean, diagrammatic look
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # X Domain (matched exactly to xlim to prevent bbox expansion)
    # 2000 points provide high resolution for smooth continuous curves
    x = np.linspace(0, 12, 2000)
    
    # -------------------------------------------------------
    # 1. THE SOFT FLOOR (Top - The Photon)
    # -------------------------------------------------------
    # Sine wave centered at Y=5
    x_c = 6.0 # Center point
    wavelength = 3.0
    k = 2 * np.pi / wavelength
    
    # Soft Floor Equilibrium: Faint Blue Dashed Line at Y=5
    ax.axhline(y=5, color='#ADD8E6', linestyle='--', linewidth=1.5, zorder=0)
    
    # Updated Label Position: Vertically aligned with Hard Floor at x=1.5
    ax.text(1.5, 5.2, "Soft Floor", color='black', fontsize=11, fontweight='bold', ha='center', va='bottom')
    
    # Photon Wave: Bright Cyan Solid Sine Wave
    y_photon = 5 + 0.8 * np.cos(k * (x - x_c))
    ax.plot(x, y_photon, color='#00CCFF', linewidth=3, label='Photon Wave', zorder=2)
    
    # Dynamic Action Label moved to the top of the tension column
    ax.text(x_c, 6.0, r"Dynamic Action ($E=hf$)", color='#00CCFF', fontsize=11, fontweight='bold', ha='center', va='bottom')

    # -------------------------------------------------------
    # 2. THE HARD FLOOR (Bottom - The Graviton/Strain)
    # -------------------------------------------------------
    y_base = 1.0
    # Removed dimple to make the hard floor perfectly flat
    dip_depth = 0.0 
    dip_width = 0.3 
    
    # Gaussian dip equation (Now evaluates flat, kept for structural consistency)
    y_gravity = y_base - dip_depth * np.exp(-((x - x_c)**2) / (2 * dip_width**2))
    
    # Plot Hard Floor: Filled region only (no top boundary line)
    # Using 'edgecolor=none' to prevent microscopic border rendering artifacts
    ax.fill_between(x, 0.0, y_gravity, facecolor='#E5E5E5', alpha=1.0, zorder=1, edgecolor='none')
    
    # Anchor point (dot) underneath the tension column
    # Scatter plot chosen for precise, scale-independent point rendering
    ax.scatter([x_c], [y_base], color='red', s=60, zorder=4)
    
    # Hard Floor Label: Vertically aligned with Soft Floor at x=1.5
    ax.text(1.5, y_base + 0.1, "Hard Floor", color='black', fontsize=11, fontweight='bold', ha='center', va='bottom')

    # Centralized Substrate Label at the bottom of the canvas
    ax.text(6.0, 0.35, "State 0 Substrate", color='#999999', fontsize=14, fontweight='bold', ha='center', va='center', zorder=5)

    # -------------------------------------------------------
    # 3. THE TENSION COLUMN (Connector)
    # -------------------------------------------------------
    # Color changed to off-white/grey (not bright)
    peak_y = 5 + 0.8
    dip_y_bottom = y_base - dip_depth
    
    ax.plot([x_c, x_c], [dip_y_bottom, peak_y], color='#BBBBBB', linestyle='-', linewidth=2, zorder=0)
    
    # Label: Vertical text along the column
    ax.text(x_c - 0.15, 3.0, "Tension Column (Mechanically Inseparable)", 
            color='black', fontsize=10, rotation=90, va='center', ha='right')
            
    # Label Eg shifted slightly down to clear the anchor dot
    ax.text(x_c, dip_y_bottom - 0.15, r"$E_g$", color='black', fontsize=12, fontweight='bold', ha='center', va='top')

    # -------------------------------------------------------
    # 4. MOTION VECTORS (Lockstep Propagation)
    # -------------------------------------------------------
    # Arrow on Top Wave
    ax.arrow(x_c + 1.0, 5.0, 1.5, 0, head_width=0.2, head_length=0.25, fc='#00CCFF', ec='#00CCFF')
    
    # Arrow on Bottom: 
    # Shortened length from 1.5 to 1.0
    ax.arrow(x_c + 0.2, 1.25, 1.0, 0, head_width=0.15, head_length=0.25, fc='#CCCCCC', ec='#CCCCCC')
    
    # Label for Shared Velocity
    ax.text(x_c + 1.55, 1.25, r"Lockstep Propagation ($v \leq c_E$)", 
            ha='left', va='center', fontsize=11, fontweight='bold', color='black')
    
    # Set absolute limits to frame mathematically perfectly
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5) 
    
    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig16_PartII_Graviton.pdf")
    
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
    create_strain_shadow_visual()