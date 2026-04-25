import numpy as np # Chosen for efficient vectorized mapping of the coherence envelope and phase integration
import matplotlib.pyplot as plt # Chosen for precise 2D vector graphic control and publication-grade output
from matplotlib.collections import LineCollection # Chosen for applying linear color gradients to the wave path
import os # Chosen to handle directory creation and file system permissions checks

def create_scale_hierarchy_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    # -----------------------------------------
    # 1. Figure and Axis Setup
    # -----------------------------------------
    fig, ax = plt.subplots(figsize=(12, 6.0), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    rD_log = -26
    Ru_log = 26
    
    # -----------------------------------------
    # 2. The Vertical Boundary Lines
    # -----------------------------------------
    # Blue dotted line exactly up to the origin point of the wave (y=1.0)
    ax.plot([rD_log, rD_log], [0, 1.0], linestyle="--", linewidth=1.8, color="blue", zorder=2)
    # Red dotted line up to the dimension bracket (y=1.08)
    ax.plot([Ru_log, Ru_log], [0, 1.08], linestyle="--", linewidth=1.8, color="red", zorder=2)

    # -----------------------------------------
    # 3. The Main Wave Curve (Uniform Line: Redshift + Decay)
    # -----------------------------------------
    # The mathematical energy envelope drops from 1.0 to 1/e exactly over the 52 orders of magnitude
    decay_constant = 52.0
    
    # Create unified domain for continuous phase generation (Truncated at 28)
    x_all = np.linspace(rD_log, 28, 2800)
    envelope_all = np.exp(-(x_all - rD_log) / decay_constant)
    
    # KINEMATIC COMPONENT 1: Horizontal Elongation (Redshift)
    # Dynamically integrating a decreasing wavenumber to precisely simulate cosmological redshift.
    k_vals = np.linspace(6.0, 0.25, len(x_all)) 
    phase_all = np.cumsum(k_vals) * (x_all[1] - x_all[0]) * np.pi
    
    # KINEMATIC COMPONENT 2: Vertical Compression
    # Ripple strictly bounds to the decay envelope. Thin, uniform digital line (no calligraphy/transverse swell).
    ripple_all = 0.04 * np.sin(phase_all) * envelope_all
    y_all = envelope_all + ripple_all
    
    # Split into Active Domain and Exhaust Domain for styling
    mask_active = x_all <= Ru_log
    mask_exhaust = x_all > Ru_log
    
    x_act = x_all[mask_active]
    y_act = y_all[mask_active]
    
    # --- LineCollection Gradient (Blue to Red) ---
    points = np.array([x_act, y_act]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    # Normalize mapping so rD_log is the start of the colormap and Ru_log is the end
    norm = plt.Normalize(rD_log, Ru_log)
    lc = LineCollection(segments, cmap='coolwarm', norm=norm, linewidth=1.2, zorder=4)
    lc.set_array(x_act)
    ax.add_collection(lc)
    
    # Exhaust Tail (Dotted, faded red/grey to continue beyond the horizon)
    ax.plot(x_all[mask_exhaust], y_all[mask_exhaust], color='#CC0000', lw=1.2, linestyle=':', alpha=0.5, zorder=4)
    
    # Exhaust Label (Positioned with a white bbox to cleanly cut through the dotted tail)
    ax.text(27.0, 0.15, "CMB\nNoise Floor", ha='center', va='bottom', color='#555555', 
            fontsize=10, fontweight='bold', zorder=10,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=2))

    # -----------------------------------------
    # 4. The Mathematical Equation
    # -----------------------------------------
    # Placed centrally above the decay curve. 
    decay_eq = r"$E_{obs} = E_{emit} e^{-\Gamma_D x / c_E}$"
    ax.text(0, 0.73, decay_eq, ha='center', va='bottom', fontsize=15, fontweight='bold', color='black', zorder=10)

    # -----------------------------------------
    # 5. The 1/e Intersection
    # -----------------------------------------
    y_e = 1.0 / np.e # ~0.368
    ax.axhline(y_e, color='#888888', linestyle=':', linewidth=1.5, zorder=1)
    
    # Precise collision node at the Viscous Cosmic Horizon
    ax.scatter([Ru_log], [y_e], color='red', s=60, zorder=6)

    # -----------------------------------------
    # 6. The Dimension Bracket
    # -----------------------------------------
    bracket_y = 1.08
    ax.annotate('', xy=(rD_log, bracket_y), xytext=(Ru_log, bracket_y),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5), zorder=10)
                
    ax.text(0, bracket_y + 0.02, r"Lattice Scale Ratio ($N_D \approx 10^{52}$)",
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='black', zorder=10)

    # -----------------------------------------
    # 7. Axes, Limits, and Labels
    # -----------------------------------------
    # Frame locked strictly from the microscopic boundary to the exhausted limit at 28
    ax.set_xlim(rD_log, 28)
    ax.set_ylim(0, 1.2)
    
    # X-Axis configuration
    ticks_x = [-26, -15, 0, 15, 26, 28]
    ax.set_xticks(ticks_x)
    ax.set_xticklabels([str(t) for t in ticks_x])
    
    # Y-Axis configuration
    ticks_y = [0.0, 0.2, y_e, 0.6, 0.8, 1.0]
    ax.set_yticks(ticks_y)
    ax.set_yticklabels(["0.0", "0.2", r"$1/e \approx 0.37$", "0.6", "0.8", "1.0"])
    ax.set_ylabel(r"Kinematic Coherence ($E_{obs} / E_{emit}$)", fontsize=11, labelpad=0)
    
    # Bottom anchor labels (Mathematically forced to the exact same Y-coordinate for perfect alignment)
    y_align = -0.09
    ax.text(rD_log, y_align, r"$r_D \approx 10^{-26}\ \mathrm{m}$", ha="center", va="top", 
            fontsize=11, fontweight='bold', color="blue", clip_on=False)
    ax.text(Ru_log, y_align, r"$R_U \approx 10^{26}\ \mathrm{m}$", ha="center", va="top", 
            fontsize=11, fontweight='bold', color="red", clip_on=False)
    ax.text(0, y_align, r"$\log_{10}(\ell\ \text{in meters})$", ha="center", va="top", 
            fontsize=11, color="black", clip_on=False)

    # Spine adjustments: Clean academic aesthetic with solid black Y-axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('black')
    ax.spines['left'].set_linewidth(1.0)

    # -----------------------------------------
    # 8. Robust Render and File Export
    # -----------------------------------------
    # Increase bottom margin explicitly to protect the dropped labels from being clipped
    plt.subplots_adjust(bottom=0.18, top=0.92, left=0.08, right=0.96)
    
    # Ensure the directory exists to prevent path-related errors
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig01_PartI_CosmicBoundary.pdf")
    
    try:
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied when saving to {pdf_filename}.")
        print("Please ensure the PDF file is closed in all other applications and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()

if __name__ == "__main__":
    create_scale_hierarchy_visual()