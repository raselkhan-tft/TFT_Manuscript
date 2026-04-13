import matplotlib.pyplot as plt # Selected for publication-grade 2D schematic layout and native LaTeX rendering
import matplotlib.ticker as ticker # Selected for precise control over logarithmic axis ticks
import numpy as np # Selected for efficient array generation and log-space interpolation
import os # Selected for robust directory management and path-specific file saving

def create_gravitational_saturation_plot():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 12
    })

    # Data Definition
    r_N = 1e-15; rho_N = 5e17       # Nucleon Start (Now strictly enforced)
    r_QG = 1e-29; rho_QG = 4.7e70   # Saturation Knee (Trigger)
    
    r_G = 3e-31  # Theoretical Yield Radius
    
    # Calculate rho_G exactly based on the projection from r_QG
    # We keep the r^-4 projection for the yield limit ghost line (theoretical scaling)
    rho_G = rho_QG * (r_QG / r_G)**4 
    
    rho_S = 1e96 # Substrate Limit (Renamed from rho_G to avoid collision)
          
    r_end = 1e-35
    
    # Setup Plot
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.xscale('log')
    plt.yscale('log')
    
    # Y-limit set exactly from 10^10 to 10^100
    ymin_limit = 1e10
    ymax_limit = 1e100
    xmin_visual_limit = 1e-14
    
    # 1. Elastic Slope (Nucleon -> Saturation)
    # Interpolate directly between (r_N, rho_N) and (r_QG, rho_QG)
    # This ensures the line passes exactly through 5e17 at the start.
    r_slope = np.logspace(np.log10(r_N), np.log10(r_QG), 100)
    
    # Calculate slope (m) and intercept (b) in log-log space
    log_r = np.log10(r_slope)
    log_rN = np.log10(r_N); log_rhoN = np.log10(rho_N)
    log_rQG = np.log10(r_QG); log_rhoQG = np.log10(rho_QG)
    
    slope_m = (log_rhoQG - log_rhoN) / (log_rQG - log_rN)
    intercept_b = log_rhoN - slope_m * log_rN
    
    log_rho_slope = slope_m * log_r + intercept_b
    rho_slope = 10**log_rho_slope
    
    plt.plot(r_slope, rho_slope, 'b-', linewidth=2, label=r'Elastic Compression ($\rho \propto r^{-4}$)')
    
    # 2. The Phase Jump (Vertical at r_QG)
    plt.plot([r_QG, r_QG], [rho_QG, rho_S], 'r-', linewidth=3, label='Phase Transition Jump')
    
    # 3. The Hard Floor (Horizontal from r_QG to r_end)
    plt.plot([r_QG, r_end], [rho_S, rho_S], 'k-', linewidth=3, label=r'Substrate Limit ($\rho_S$)')
    
    # 4. The Ghost Line (Yield Limit)
    r_ghost = np.logspace(np.log10(r_QG), np.log10(r_G), 10)
    rho_ghost = rho_QG * (r_QG / r_ghost)**4
    plt.plot(r_ghost, rho_ghost, 'k--', alpha=0.5)
    
    # Mark the Theoretical Yield Point
    plt.scatter([r_G], [rho_G], color='red', marker='x', s=100, zorder=5)
    
    # Labels for Yield Limit
    plt.text(r_G * 0.3, rho_G, r'$(r_G, \rho_G)$', color='red', fontsize=10, va='bottom', ha='left')
    plt.text(r_G * 0.3, rho_G / 50, 'Yield Limit', color='red', fontsize=10, va='top', ha='left')
    
    # Axis Projections
    points_x_only = [
        (r_N, rho_N, r'$r_N$') # Using actual rho_N
    ]
    
    for r_val, rho_val, label_r in points_x_only:
        # Vertical line to bottom (X-axis)
        plt.plot([r_val, r_val], [ymin_limit, rho_val], 'k:', linewidth=1, alpha=0.6)
        # Label on X-axis
        plt.text(r_val, ymin_limit * 0.3, label_r, color='black', ha='center', va='top')
    
    # QG: Keep both X and Y for the critical knee point
    plt.plot([r_QG, r_QG], [ymin_limit, rho_QG], 'k:', linewidth=1, alpha=0.6)
    
    # ---------------------------------------------------------
    # MANUAL ADJUSTMENT BLOCK FOR r_QG APPROX LABEL
    # ---------------------------------------------------------
    label_x_multiplier = 12.0  
    label_y_position = -0.02 
    
    plt.text(r_QG * label_x_multiplier, label_y_position, 
             r'$r_{QG} \approx$', color='black', ha='center', va='top', 
             transform=ax.get_xaxis_transform())
    # ---------------------------------------------------------
    
    plt.plot([xmin_visual_limit, r_QG], [rho_QG, rho_QG], 'k:', linewidth=1, alpha=0.6)
    
    # Move rho_QG label slightly ABOVE the line (va='bottom')
    # Applied a larger vertical multiplier (5.0x) on the log scale to create a visible upward nudge
    plt.text(xmin_visual_limit * 1.5, rho_QG * 5.0, r'$\rho_{QG}$', color='black', ha='right', va='bottom')
    
    # Slope annotation
    r_text = 1e-22
    # Calculate rho_text ON the actual line using the calculated slope/intercept
    log_r_text = np.log10(r_text)
    log_rho_text_actual = slope_m * log_r_text + intercept_b
    rho_text = 10**log_rho_text_actual
    plt.text(r_text, rho_text * 10, r'$\rho \propto r^{-4}$', color='blue', fontsize=12, rotation=30, ha='center', va='bottom')
    
    # Limits
    plt.ylim(ymin_limit, ymax_limit)
    plt.xlim(xmin_visual_limit, 1e-35) 
    
    # Force Major Y-axis ticks to exact decades
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
    y_ticks = [10.0**i for i in range(10, 102, 10)]
    ax.set_yticks(y_ticks)
    
    # Labels
    plt.xlabel(r'Radius $r$ (meters) [Collapse Direction $\rightarrow$]', fontsize=12)
    plt.ylabel(r'Density $\rho$ ($\mathrm{kg/m}^3$)', fontsize=12)
    
    plt.legend(loc='upper left') 
    
    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig11_PartII_PhaseTransitionLogLog.pdf")
    
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
    create_gravitational_saturation_plot()