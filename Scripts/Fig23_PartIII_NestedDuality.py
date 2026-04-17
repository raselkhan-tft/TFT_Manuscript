import numpy as np # Selected for efficient, vectorized array math to generate the coherence envelope
import matplotlib.pyplot as plt # Selected for precise 2D vector graphic control and native LaTeX text rendering
from matplotlib import transforms # Selected for blended coordinate positioning
import os # Selected for robust local directory management and path-specific file saving

def create_nested_duality_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    # -----------------------------------------
    # 1. X range and coherence curve
    # -----------------------------------------
    # Expanded the domain to +/- 38 to cleanly frame the new +/- 35 bounds
    x = np.linspace(-38, 38, 3000)
    
    # Symmetric coordinate limited to the causal duality region [-26, 26]
    x_sym = np.clip(x, -26, 26)
    t = x_sym / 26.0  # normalized in [-1, 1]
    
    # Base coherence profile: low at center, high at edges
    base = 0.1 + 0.9 * (1 - (np.cos(np.pi * t) + 1) / 2)  # 0.1 at 0, 1.0 at ±26
    
    # Zig-zag ripples representing localized scale tension
    ripples = 0.06 * np.sin(4.0 * x_sym) * np.exp(-(x_sym / 15.0) ** 2)
    y = base + ripples
    y = np.clip(y, 0.0, 1.0)
    
    # -----------------------------------------
    # 2. Figure and axis setup
    # -----------------------------------------
    fig, ax = plt.subplots(figsize=(13, 5), dpi=150) # Widened slightly to accommodate outer labels
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    ax.plot(x, y, linewidth=2, color="black")
    
    # Causal Horizons (Dashed)
    rD_log = -26
    Ru_log = 26
    ax.axvline(rD_log, ymax=0.90, linestyle="--", linewidth=1.5, color="red")
    ax.axvline(Ru_log, ymax=0.90, linestyle="--", linewidth=1.5, color="blue")

    # Structural Horizons (Solid & Thick)
    lS_log = -35
    Rres_log = 35
    # Adjusted ymax from 0.90 to 0.86 to provide clearance for the multi-line labels
    ax.axvline(lS_log, ymax=0.89, linestyle="-", linewidth=2.5, color="darkred")
    ax.axvline(Rres_log, ymax=0.89, linestyle="-", linewidth=2.5, color="darkblue")
    
    # Axis labels
    ax.set_xlabel(r"$\log_{10}(\ell\ \mathrm{in\ meters})$", labelpad=15, fontsize=11)
    ax.set_ylabel(r"Tension Field Coherence $(\tau / \tau_S)$", fontsize=11)
    
    # Limits explicitly set to frame the new outer edges
    ax.set_xlim(-39, 39)
    ax.set_ylim(-0.02, 1.15)
    
    # Clean bounding box
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # -----------------------------------------
    # 3. X-ticks and labels
    # -----------------------------------------
    ticks = [-35, -26, -10, 0, 10, 26, 35]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks])
    
    # -----------------------------------------
    # 4. Top labels for Horizons
    # -----------------------------------------
    # Causal (Inner)
    ax.text(rD_log, 1.03, r"Duality Scale $r_D$",
            ha="center", va="bottom", fontsize=10, fontweight='bold', color="red")
    ax.text(Ru_log, 1.03, r"Cosmic Horizon $R_U$",
            ha="center", va="bottom", fontsize=10, fontweight='bold', color="blue")

    # Structural (Outer) - Folded into two lines to reduce horizontal width and prevent crowding
    ax.text(lS_log, 1.03, "Substrate\nNode",
            ha="center", va="bottom", fontsize=10, fontweight='bold', color="darkred")
    ax.text(Rres_log, 1.03, "Cosmic\nReservoir",
            ha="center", va="bottom", fontsize=10, fontweight='bold', color="darkblue")
    
    # -----------------------------------------
    # 5. Duality relation in the valley
    # -----------------------------------------
    # Outer Structural Equation (Updated variable)
    ax.text(0, 0.48, r"$\log_{10}(\ell_S) + \log_{10}(R_{Res}) \approx \log_{10}(A)$",
            ha="center", va="center", fontsize=11, fontweight='bold')
    
    # Inner Causal Equation
    ax.text(0, 0.38, r"$\log_{10}(r_D) + \log_{10}(R_U) \approx \log_{10}(A)$",
            ha="center", va="center", fontsize=11, fontweight='bold')
    
    # -----------------------------------------
    # 6. Bottom labels (Area and Causal Scales)
    # -----------------------------------------
    blend = transforms.blended_transform_factory(ax.transData, ax.transAxes)
    y_under_edges = -0.12  
    y_under_A = -0.08      
    
    # A under x = 0
    ax.text(0, y_under_A, r"$A \approx 1\ \mathrm{m}^2$",
            ha="center", va="top", fontsize=10, transform=blend)
    
    # r_D numeric under x = -26
    ax.text(rD_log, y_under_edges, r"$r_D \approx 10^{-26}\ \mathrm{m}$",
            ha="center", va="top", fontsize=9, color="red", transform=blend)
    
    # R_U numeric under x = +26
    ax.text(Ru_log, y_under_edges, r"$R_U \approx 10^{26}\ \mathrm{m}$",
            ha="center", va="top", fontsize=9, color="blue", transform=blend)

    # l_S numeric under x = -35
    ax.text(lS_log, y_under_edges, r"$\ell_S \approx 10^{-35}\ \mathrm{m}$",
            ha="center", va="top", fontsize=9, color="darkred", transform=blend)

    # R_Res numeric under x = +35 (Updated variable)
    ax.text(Rres_log, y_under_edges, r"$R_{Res} \approx 10^{35}\ \mathrm{m}$",
            ha="center", va="top", fontsize=9, color="darkblue", transform=blend)
    
    # -----------------------------------------
    # 7. FINAL RENDER & PDF EXPORT
    # -----------------------------------------
    # Adjusted rect to ensure top text and bottom labels are fully visible without the title
    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig23_PartIII_NestedDuality.pdf")
    
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
    create_nested_duality_visual()