import numpy as np # Selected for efficient array generation and mathematical transformations
import matplotlib.pyplot as plt # Selected for publication-grade 2D schematic layout and native LaTeX rendering
import os # Selected for robust directory management and path-specific file saving

def create_energy_paradox_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    # Setup Figure (Minimalist Architectural Styling)
    # Using Very Dark Charcoal (#1A1A1A) for consistent "etched" look across all labels
    charcoal = '#1A1A1A'
    navy = '#000080'
    maroon = '#800000'
    brick_red = '#B22222'
    
    fig, ax = plt.subplots(figsize=(14, 9), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # X Domain for wave propagation
    x = np.linspace(0, 4 * np.pi, 1000)

    # =======================================================
    # 1. TOP HALF: The Kinetic Wave Domain (Standard Physics)
    # =======================================================
    y_center_top = 3.0
    
    # Waveform Equations
    wave_a = y_center_top + 1.5 * np.sin(x)
    wave_b = y_center_top - 1.5 * np.sin(x)
    y_net = np.full_like(x, y_center_top)

    # Plot the visible kinematic state - Unified palette
    ax.plot(x, wave_a, color=navy, lw=2.2, alpha=0.9, label="Wave A") 
    ax.plot(x, wave_b, color=maroon, lw=2.2, alpha=0.9, label="Wave B") 
    
    # The Resultant Flatline (Apparent Zero Energy)
    ax.plot(x, y_net, color=charcoal, lw=4, zorder=5)

    # Annotations for the Top Half - Updated to uniform charcoal color
    ax.text(np.pi/2, y_center_top + 1.8, "Wave A (Positive Kinetic Displacement)", 
            color=charcoal, fontweight='bold', ha='center', fontsize=11)
            
    ax.text(np.pi/2, y_center_top - 1.8, "Wave B (Negative Kinetic Displacement)", 
            color=charcoal, fontweight='bold', ha='center', va='top', fontsize=11,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=4))
    
    # Mathematical variables italicized; descriptive 'net' upright
    # Applied white mask to clear the wave background
    ax.text(2 * np.pi, y_center_top + 0.3, r"The Dark Spot: Apparent Vacuum ($A_{\mathrm{net}} = 0, v = 0$)", 
            color=charcoal, fontsize=12, fontweight='bold', ha='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=4))

    # =======================================================
    # 2. BOTTOM HALF: The SGF Lattice (Hidden Potential Domain)
    # =======================================================
    y_center_bottom = -2.0
    
    # Grid Parameters
    num_x_nodes = 45
    x_nodes = np.linspace(0, 4 * np.pi, num_x_nodes)
    y_base_levels = np.linspace(-4.5, 0.5, 6) 

    def get_distorted_y(x_val, y_base):
        # Strain proportional to square of displacement
        strain = np.sin(x_val)**2
        stretch_factor = 0.6 
        return y_base + stretch_factor * strain * (y_base - y_center_bottom)

    # Draw Horizontal Lattice Lines (Distorted by Tension)
    for yb in y_base_levels:
        y_line = [get_distorted_y(xv, yb) for xv in x]
        ax.plot(x, y_line, color='#DDDDDD', lw=1.5, zorder=1)

    # Draw Vertical Lattice Links (Glowing and Stretched)
    for xv in x_nodes:
        local_strain = np.sin(xv)**2
        
        y_bottom_distorted = get_distorted_y(xv, y_base_levels[0])
        y_top_distorted = get_distorted_y(xv, y_base_levels[-1])
        
        # Base inactive link
        ax.plot([xv, xv], [y_bottom_distorted, y_top_distorted], color='#CCCCCC', lw=1.5, zorder=1)

        # Apply Matte Terracotta glow where strain is maximized
        if local_strain > 0.05:
            glow_alpha = 0.7 * local_strain
            # Matte Brick Red for strain
            ax.plot([xv, xv], [y_bottom_distorted, y_top_distorted], 
                    color=brick_red, lw=2 + (4 * local_strain), alpha=glow_alpha, zorder=2)
            
        # Plot Lattice Nodes
        y_distorted_nodes = [get_distorted_y(xv, yb) for yb in y_base_levels]
        ax.scatter(np.full_like(y_distorted_nodes, xv), y_distorted_nodes, 
                   color='#333333', s=12, zorder=4)

    # Annotations for the Bottom Half - Updated to charcoal color
    ax.text(2 * np.pi, -5.2, "Active SGF Lattice (Microscopic Domain)", 
            color=charcoal, fontsize=12, fontweight='bold', ha='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=4))

    cancel_x = 3 * np.pi / 2
    ax.annotate("", xy=(cancel_x, 0.5), xytext=(cancel_x, 2.7),
                arrowprops=dict(arrowstyle="->", color="#555555", lw=3, linestyle="--"))
    
    # Mathematical explanation block - Updated to uniform charcoal color
    math_text = (r"Kinetic energy cancels perfectly." + "\n" +
                 r"Potential Energy Reaches its Maximum." + "\n" +
                 r"Energy stored in static tension: $\frac{1}{2}\tau_{\mathrm{local}}(\Delta x)^2$")
    
    ax.text(cancel_x + 0.3, 1.2, math_text, color=charcoal, fontsize=11, 
            fontweight='bold', ha='left', va='center', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=8))

    # =======================================================
    # 3. STYLING & FORMATTING
    # =======================================================
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.5, 4 * np.pi + 0.5)
    ax.set_ylim(-5.5, 5.5)
    
    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig14_PartII_EnergyParadox.pdf")
    
    try:
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()

if __name__ == "__main__":
    create_energy_paradox_visual()