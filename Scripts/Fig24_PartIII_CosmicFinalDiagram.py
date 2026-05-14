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
    
    # Outer Structural Boundaries
    lS_log = -35
    Rres_log = 35
    Rrup_log = 34 # Rupture Radius
    
    # Inner Causal Boundaries
    rD_log = -26
    Ru_log = 26
    
    # -----------------------------------------
    # 2. The Vertical Boundary Lines & Regions
    # -----------------------------------------
    # State 0 Substrate Region (Filled vertical span, trimmed to 1.22 to show N_S arrowhead)
    ax.fill_between([lS_log, rD_log], 0, 1.22, color='lightgray', alpha=0.4, zorder=0)
    ax.text((lS_log + rD_log) / 2.0, 0.5, "State 0\nSubstrate", ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#444444', zorder=1)

    # Outer structural boundaries extended to the upper bracket
    ax.plot([lS_log, lS_log], [0, 1.25], linestyle="-", linewidth=1.5, color="darkgray", zorder=1)
    ax.plot([Rres_log, Rres_log], [0, 1.25], linestyle="-", linewidth=1.5, color="black", zorder=1)

    # Rupture Radius line
    ax.plot([Rrup_log, Rrup_log], [0, 1.22], linestyle=":", linewidth=1.8, color="red", zorder=2)

    # Inner causal boundaries
    ax.plot([rD_log, rD_log], [0, 1.22], linestyle="--", linewidth=1.8, color="blue", zorder=2)
    # Changed RU dotted vertical line color to gray
    ax.plot([Ru_log, Ru_log], [0, 1.22], linestyle="--", linewidth=1.8, color="gray", zorder=2)

    # -----------------------------------------
    # 3. The Main Wave Curve (Uniform Line: Redshift + Decay)
    # -----------------------------------------
    # Create unified domain for continuous phase generation (Truncated at 28)
    x_all = np.linspace(rD_log, 28, 2800)
    
    # Exact Equation: True exponential decay mapped over a logarithmic spatial axis
    # Stays perfectly flat at 1.0 until approaching 10^26, then plunges
    envelope_all = np.exp(-10**(x_all - Ru_log))
    
    # KINEMATIC COMPONENT 1: Horizontal Elongation (Redshift)
    k_vals = np.linspace(6.0, 0.25, len(x_all)) 
    phase_all = np.cumsum(k_vals) * (x_all[1] - x_all[0]) * np.pi
    
    # KINEMATIC COMPONENT 2: Vertical Compression
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
    
    # Exhaust Label (Shifted back to sit at the end of the wave tail)
    ax.text(27.0, 0.15, "CMB\nNoise Floor", ha='center', va='bottom', color='#555555', 
            fontsize=10, fontweight='bold', zorder=10,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=2))

    # -----------------------------------------
    # 4. The Mathematical Equation
    # -----------------------------------------
    # Placed centrally above the decay curve. 
    decay_eq = r"$E_{\mathrm{obs}} = E_{\mathrm{emit}} e^{-\Gamma_{\mathrm{D}} x / c_{\mathrm{E}}}$"
    # Gap increased by 25% (Y shifted from 0.865 to 0.831)
    ax.text(0, 0.831, decay_eq, ha='center', va='bottom', fontsize=15, fontweight='bold', color='black', zorder=10)

    # -----------------------------------------
    # 5. The 1/e Intersection
    # -----------------------------------------
    y_e = 1.0 / np.e # ~0.368
    # Dotted line strictly stopped at the RU vertical line
    ax.plot([lS_log, Ru_log], [y_e, y_e], color='#888888', linestyle=':', linewidth=1.5, zorder=1)
    
    # Precise collision node at the viscous horizon
    ax.scatter([Ru_log], [y_e], color='red', s=60, zorder=6)

    # -----------------------------------------
    # 6. Exponential Mass Growth Curve
    # -----------------------------------------
    M_DG = 10.625
    R_U_actual = 10**26.0

    # Calculate exact logarithmic x-coordinate where Mass reaches 10^78 kg
    x_end_actual = R_U_actual * np.log((10**78.0) / M_DG)
    x_end_log = np.log10(x_end_actual) # ~28.25
    
    # Generate domain from microscopic boundary strictly to the mathematical 10^78 kg limit
    x_mass_log = np.linspace(rD_log, x_end_log, 1000)
    x_mass_actual = 10**x_mass_log
    
    # Exact Equation: M_p(x) = M_{D,G} * e^(x/R_U)
    # Computed in log10 space to avoid float overflow, mapped to left Y-axis scale (0 to 1.0 represents 0 to 78)
    log10_M_p = np.log10(M_DG) + (x_mass_actual / R_U_actual) * np.log10(np.e)
    y_mass = log10_M_p / 78.0
    
    # Updated curve to Muted Maroon to map to the established Matter legend
    ax.plot(x_mass_log, y_mass, color='#8B0000', lw=2.5, linestyle='-', zorder=5)
    
    # Label placed exactly near x=0, above the mass curve
    # Gap increased by 25% (Y shifted from 0.07 to 0.088)
    ax.text(0, 0.088, r"$M_p(x) = M_{\mathrm{D,G}} \cdot e^{\Gamma_{\mathrm{D}} x / c_{\mathrm{E}}}$", 
            color='black', fontsize=15, fontweight='bold', ha='center', va='center', zorder=10)

    # -----------------------------------------
    # 7. The Dimension Brackets & Region Labels
    # -----------------------------------------
    # Inner Causal Bracket (N_D)
    bracket_y = 1.08
    ax.annotate('', xy=(rD_log, bracket_y), xytext=(Ru_log, bracket_y),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5), zorder=10)
                
    # Font matches Kinematic Coherence Label
    ax.text(0, bracket_y + 0.02, r"Kinematic Lattice Index ($N_{\mathrm{D}} \approx 10^{52}$)",
            ha='center', va='bottom', fontsize=11, color='black', zorder=10)

    # L_max Bracket (Maximum Cycle Distance)
    # Positioned at y=0.60, precisely between the 1/e line (0.37) and the State I label (0.84)
    y_lmax = 0.60
    ax.annotate('', xy=(rD_log, y_lmax), xytext=(x_end_log, y_lmax),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5), zorder=10)
                
    # Flipped equation to rest below the annotation line
    ax.text(0, y_lmax - 0.02, r"$L_{\mathrm{max}} = T_{\mathrm{cyc}} \cdot c_{\mathrm{E}} \approx 2.24 \times 10^{28}\ \mathrm{m}$",
            ha='center', va='top', fontsize=11, color='black', zorder=10,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3))

    # State I Active Vacuum Label
    # Center-aligned, shifted horizontally by 5x the previous gap (12.5 units from Ru_log)
    ax.text(13.5, bracket_y - 0.24, "State I\nActive Vacuum",
            ha='center', va='top', fontsize=11, color='black',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3), zorder=10)

    # Target Mass Label (M_trg)
    # M_trg dot placed exactly at the mathematical terminus of the truncated mass curve (10^28 m)
    ax.scatter([x_end_log], [1.0], color='black', s=50, zorder=10)
    
    # Placed in the hatched area, vertically between 60 and 80 on the y-axis
    mtrg_x = (x_end_log + Rrup_log) / 2.0
    mtrg_y = 70.0 / 78.0
    ax.text(mtrg_x, mtrg_y, r"$M_{\mathrm{trg}}$" + "\n" + r"($\approx 10^{78}\ \mathrm{kg}$)",
            ha='center', va='center', fontsize=11, color='black',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=0.8), zorder=10)

    # Annotation arrow from M_trg explicitly pointing to the black dot at the end of the mass curve
    ax.annotate("", xy=(x_end_log, 1.0), xytext=(mtrg_x - 1.2, mtrg_y),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.2, connectionstyle="arc3,rad=0.1"), zorder=9)

    # Opaque Causality Region (Hatched)
    # Filled strictly between the mass curve terminus and R_rup, up to height 1.22
    ax.fill_between([x_end_log, Rrup_log], 0, 1.22, facecolor='none', edgecolor='#999999', hatch='//', alpha=0.4, zorder=0)
    
    y_opaque = 50.0 / 78.0 
    ax.text((x_end_log + Rrup_log) / 2.0, y_opaque, "Opaque\nCausality\nDomain", 
            ha='center', va='center', fontsize=10, color='black',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=0.2), zorder=10)

    # Outer Structural Bracket (N_S)
    bracket_y2 = 1.25
    ax.annotate('', xy=(lS_log, bracket_y2), xytext=(Rres_log, bracket_y2),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5), zorder=10, annotation_clip=False)
                
    # Font matches Kinematic Coherence Label
    ax.text(0, bracket_y2 + 0.02, r"Absolute Substrate Index ($N_{\mathrm{S}} \approx 10^{70}$)",
            ha='center', va='bottom', fontsize=11, color='black', zorder=10)

    # Rupture Radius Label 
    # Gap reduced by 50% from 1.25 line -> shifted up to 1.165
    new_y = 1.165
    ax.annotate(r"$R_{\mathrm{rup}}$" + "\n" + r"($\approx 10^{34}\ \mathrm{m}$)",
                xy=(Rrup_log, new_y), xytext=((Ru_log + Rrup_log) / 2.0, new_y),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
                ha='center', va='center', fontsize=10, color='black',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3), zorder=12, annotation_clip=False)

    # Deflation annotation and arrows (Decoupled on Y-axis)
    y_def_text = 28.0 / 78.0 
    y_def_arrow = 35.0 / 78.0 
    
    text_x = (x_end_log + Rrup_log) / 2.0
    
    # Target X is placed exactly at 40% distance from the 10^35 vertical line
    target_x = Rres_log - 0.4 * (Rres_log - Rrup_log)
    
    # Text center-aligned horizontally inside the hatched domain
    ax.text(text_x, y_def_text, "Deflation\n" + r"($\Delta R \approx 10^{33}\ \mathrm{m}$)", 
            ha='center', va='center', multialignment='center', fontsize=10, color='black', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=0.2), zorder=10)
            
    # Curved leader line from the text gap directly to the virtual horizontal line (Curve flipped inward)
    ax.annotate("", xy=(target_x, y_def_arrow), xytext=(text_x + 1.8, y_def_text),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.0, connectionstyle="arc3,rad=0.2"), zorder=9)
    
    # Arrow pointing from outside toward the 10^34 dotted line (Original 1.5 length)
    ax.annotate("", xy=(Rrup_log, y_def_arrow), xytext=(Rrup_log - 1.5, y_def_arrow),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5), zorder=10)
                
    # Arrow pointing from outside to the 10^35 line (Original 1.5 length)
    ax.annotate("", xy=(Rres_log, y_def_arrow), xytext=(Rres_log + 1.5, y_def_arrow),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5), zorder=10)

    # -----------------------------------------
    # 8. Axes, Limits, and Labels
    # -----------------------------------------
    # Frame locked strictly from -35 to 35
    ax.set_xlim(lS_log, Rres_log)
    ax.set_ylim(0, 1.35) 
    
    # X-Axis configuration
    ticks_x = [lS_log, rD_log, -10, 0, 10, Ru_log, Rres_log]
    ax.set_xticks(ticks_x)
    ax.set_xticklabels([f"${t}$" for t in ticks_x])
    
    # Y-Axis configuration
    ticks_y = [0.0, 0.2, y_e, 0.6, 0.8, 1.0]
    ax.set_yticks(ticks_y)
    ax.set_yticklabels(["0.0", "0.2", r"$1/e \approx 0.37$", "0.6", "0.8", "1.0"])
    ax.set_ylabel(r"Kinematic Coherence $(E_{\mathrm{obs}} / E_{\mathrm{emit}})$", fontsize=11, labelpad=0)
    
    # Bottom anchor labels
    y_align = -0.11 
    ax.text(lS_log, y_align, r"$\ell_{\mathrm{S}} \approx 10^{-35}\ \mathrm{m}$", ha="center", va="top", 
            fontsize=11, fontweight='bold', color="black", clip_on=False)
    ax.text(rD_log, y_align, r"$r_{\mathrm{D}} \approx 10^{-26}\ \mathrm{m}$", ha="center", va="top", 
            fontsize=11, fontweight='bold', color="black", clip_on=False)
    ax.text(Ru_log, y_align, r"$R_{\mathrm{U}} \approx 10^{26}\ \mathrm{m}$", ha="center", va="top", 
            fontsize=11, fontweight='bold', color="black", clip_on=False)
    ax.text(Rres_log, y_align, r"$R_{\mathrm{Res}} \approx 10^{35}\ \mathrm{m}$", ha="center", va="top", 
            fontsize=11, fontweight='bold', color="black", clip_on=False)
    ax.text(0, y_align, r"Coordinate Distance, $\log_{10}(x/\mathrm{m})$", ha="center", va="top", 
            fontsize=11, color="black", clip_on=False)

    # -----------------------------------------
    # 9. Spines and Secondary Y-Axis
    # -----------------------------------------
    # Clean academic aesthetic with solid black axes matching left and right boundaries
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    
    # Create secondary axis for Aggregate Percolating Mass (M_p)
    ax2 = ax.twinx()
    # Scale ax2 such that y=1.0 on ax1 corresponds to M=10^78
    ax2.set_ylim(0, 1.35 * 78.0) 
    
    # Set ticks so 80 is just above the curve (at y=1.025) and 100 is at the top (y=1.28)
    ax2.set_yticks([0, 20, 40, 60, 80, 100])
    ax2.set_yticklabels(["0", "20", "40", "60", "80", "100"], fontsize=11, color='black')
    ax2.set_ylabel(r"Aggregate Percolating Mass, $\log_{10}(M_p/\mathrm{kg})$", fontsize=11, color='black', labelpad=10)
    
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color('black')

    # -----------------------------------------
    # 10. Robust Render and File Export
    # -----------------------------------------
    plt.subplots_adjust(bottom=0.18, top=0.92, left=0.08, right=0.92)
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig24_PartIII_CosmicFinalDiagram.pdf")
    
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