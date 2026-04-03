import numpy as np # Chosen for efficient vectorized mapping of the coherence envelope
import matplotlib.pyplot as plt # Chosen for precise 2D vector graphic control and publication-grade output
from matplotlib import transforms
import os # Chosen to handle directory creation and file system permissions checks

def create_duality_visual():
    # -----------------------------------------
    # 1. X range and coherence curve
    # -----------------------------------------
    x = np.linspace(-35, 30, 2400)
    
    # Symmetric coordinate limited to the duality region [-26, 26]
    x_sym = np.clip(x, -26, 26)
    t = x_sym / 26.0  # Normalized in [-1, 1]
    
    # Base coherence profile: low at center, high at edges
    # Lower coherence at l = 1m represents the "Valley of Logic"
    base = 0.1 + 0.9 * (1 - (np.cos(np.pi * t) + 1) / 2)  # 0.1 at 0, 1.0 at ±26
    
    # Zig-zag ripples representing localized scale tension
    ripples = 0.06 * np.sin(4.0 * x_sym) * np.exp(-(x_sym / 15.0) ** 2)
    y = base + ripples
    y = np.clip(y, 0.0, 1.0)
    
    # -----------------------------------------
    # 2. Figure and axis setup
    # -----------------------------------------
    fig, ax = plt.subplots(figsize=(11, 4), dpi=150)
    ax.set_facecolor('white')
    
    ax.plot(x, y, linewidth=2, color="black")
    
    # Vertical dashed lines for r_D and R_U
    rD_log = -26
    Ru_log = 26
    ax.axvline(rD_log, ymax=0.94, linestyle="--", linewidth=1.5, color="red")
    ax.axvline(Ru_log, ymax=0.94, linestyle="--", linewidth=1.5, color="blue")
    
    # Axis labels using LaTeX notation
    # Adjusted horizontal placement using x=0.58 (0.5 is center)
    ax.set_xlabel(r"$\log_{10}(\ell\ \text{in meters})$", labelpad=15, fontsize=11, x=0.54)
    ax.set_ylabel(r"Tension Field Coherence $(\tau / \tau_S)$", fontsize=11)
    
    # Title removed per Strict Academic Standard requirements.
    
    # Limits
    ax.set_xlim(-35, 30)
    ax.set_ylim(-0.02, 1.12)
    
    # Remove top and right spines for a clean academic aesthetic
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # -----------------------------------------
    # 3. X-ticks and labels
    # -----------------------------------------
    ticks = list(range(-30, 31, 10))   # -30, -20, -10, 0, 10, 20, 30
    ticks.extend([-35, -26, 26])
    ticks = sorted(set(ticks))
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks])
    
    # -----------------------------------------
    # 4. Top labels for r_D and R_U
    # -----------------------------------------
    ax.text(rD_log, 1.08, r"Duality Scale $r_D$",
            ha="center", va="bottom", fontsize=10, fontweight='bold', color="red")
    ax.text(Ru_log, 1.08, r"Cosmic Horizon $R_U$",
            ha="center", va="bottom", fontsize=10, fontweight='bold', color="blue")
    
    # -----------------------------------------
    # 5. Duality relation in the valley
    # -----------------------------------------
    ax.text(0, 0.38,
            r"$\log_{10}(r_D) + \log_{10}(R_U) \approx \log_{10}(A)$",
            ha="center", va="center", fontsize=11, fontweight='bold')
    
    # -----------------------------------------
    # 6. Bottom labels: A, r_D, R_U
    # -----------------------------------------
    blend = transforms.blended_transform_factory(ax.transData, ax.transAxes)
    
    # Vertical position parameters (normalized relative to axes)
    y_under_edges = -0.15  
    y_under_A = -0.082 
    
    # A under x = 0
    ax.text(0, y_under_A, r"$A \approx 1\ \mathrm{m}^2$",
            ha="center", va="top", fontsize=10, transform=blend)
    
    # r_D numeric under x = -26
    ax.text(rD_log, y_under_edges, r"$r_D \approx 10^{-26}\ \mathrm{m}$",
            ha="center", va="top", fontsize=9, color="red", transform=blend)
    
    # R_U numeric under x = +26
    ax.text(Ru_log, y_under_edges, r"$R_U \approx 10^{26}\ \mathrm{m}$",
            ha="center", va="top", fontsize=9, color="blue", transform=blend)
    
    # -----------------------------------------
    # 7. Robust Render and File Export
    # -----------------------------------------
    plt.tight_layout()
    
    # Ensure the directory exists to prevent path-related Permission/FileNotFound errors
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig01_PartI_Logarithmicduality.pdf")
    
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
    create_duality_visual()