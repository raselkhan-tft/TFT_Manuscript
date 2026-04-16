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

    # Plot the visible kinematic state
    ax.plot(x, wave_a, color='#00CCFF', lw=2, alpha=0.8, label="Wave A") # Cyan
    ax.plot(x, wave_b, color='#FF00FF', lw=2, alpha=0.8, label="Wave B") # Magenta
    
    # The Resultant Flatline (Apparent Zero Energy)
    ax.plot(x, y_net, color='black', lw=4, zorder=5)

    # Annotations for the Top Half
    ax.text(np.pi/2, y_center_top + 1.8, "Wave A (Positive Kinetic Displacement)", 
            color='#00AAFF', fontweight='bold', ha='center', fontsize=11)
            
    # Aesthetic Polish: Applied white masking background for readability
    ax.text(np.pi/2, y_center_top - 1.8, "Wave B (Negative Kinetic Displacement)", 
            color='#DD00DD', fontweight='bold', ha='center', va='top', fontsize=11,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=4))
    
    ax.text(2 * np.pi, y_center_top + 0.3, r"The Dark Spot: Apparent Vacuum ($A_{net} = 0, v = 0$)", 
            color='black', fontsize=12, fontweight='bold', ha='center')

    # =======================================================
    # 2. BOTTOM HALF: The SGF Lattice (Hidden Potential Domain)
    # =======================================================
    y_center_bottom = -2.0
    
    # Grid Parameters
    num_x_nodes = 45
    x_nodes = np.linspace(0, 4 * np.pi, num_x_nodes)
    y_base_levels = np.linspace(-4.5, 0.5, 6) # Base horizontal grid lines

    # Function to distort the lattice mathematically based on accumulated strain
    def get_distorted_y(x_val, y_base):
        # Strain is proportional to the square of the displacement amplitude
        strain = np.sin(x_val)**2
        # Stretch outward from the center of the lattice (-2.0)
        stretch_factor = 0.6 
        return y_base + stretch_factor * strain * (y_base - y_center_bottom)

    # Draw Horizontal Lattice Lines (Distorted by Tension)
    for yb in y_base_levels:
        y_line = [get_distorted_y(xv, yb) for xv in x]
        ax.plot(x, y_line, color='#DDDDDD', lw=1.5, zorder=1)

    # Draw Vertical Lattice Links (Glowing and Stretched)
    for xv in x_nodes:
        # Calculate local strain (0 to 1) at this x-coordinate
        local_strain = np.sin(xv)**2
        
        y_bottom_distorted = get_distorted_y(xv, y_base_levels[0])
        y_top_distorted = get_distorted_y(xv, y_base_levels[-1])
        
        # Base inactive link
        ax.plot([xv, xv], [y_bottom_distorted, y_top_distorted], color='#CCCCCC', lw=1.5, zorder=1)

        # Apply intense red glow where strain is maximized (destructive interference antinodes)
        if local_strain > 0.05:
            glow_alpha = 0.8 * local_strain
            # Outer diffuse glow
            ax.plot([xv, xv], [y_bottom_distorted, y_top_distorted], 
                    color='#FF0000', lw=2 + (4 * local_strain), alpha=glow_alpha, zorder=2)
            # Inner hot core
            ax.plot([xv, xv], [y_bottom_distorted, y_top_distorted], 
                    color='#FFCCCC', lw=1.5, alpha=glow_alpha, zorder=3)
            
        # Plot Lattice Nodes
        y_distorted_nodes = [get_distorted_y(xv, yb) for yb in y_base_levels]
        ax.scatter(np.full_like(y_distorted_nodes, xv), y_distorted_nodes, 
                   color='#333333', s=12, zorder=4)

    # Annotations for the Bottom Half
    # Aesthetic Polish: Applied white masking background to prevent lattice line overlap
    ax.text(2 * np.pi, -5.2, "Active SGF Lattice (Microscopic Domain)", 
            color='black', fontsize=12, fontweight='bold', ha='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=4))

    # Link the Kinetic cancellation to the Strain generation
    cancel_x = 3 * np.pi / 2
    ax.annotate("", xy=(cancel_x, 0.5), xytext=(cancel_x, 2.7),
                arrowprops=dict(arrowstyle="->", color="#555555", lw=3, linestyle="--"))
    
    # Mathematical explanation block
    math_text = (r"Kinetic energy cancels perfectly." + "\n" +
                 r"Energy converts entirely to static tension." + "\n" +
                 r"Max Potential Energy: $\frac{1}{2}\tau_{local}(\Delta x)^2$")
    
    # Aesthetic Polish: Removed hard red border, using transparent white box
    ax.text(cancel_x + 0.3, 1.2, math_text, color='#AA0000', fontsize=11, 
            fontweight='bold', ha='left', va='center', 
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=8))

    # =======================================================
    # 3. STYLING & FORMATTING
    # =======================================================
    # Clean up bounding boxes for architectural look
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.5, 4 * np.pi + 0.5)
    ax.set_ylim(-5.5, 5.5)
    
    # Note: Titles strictly removed for publication formatting.

    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig14_PartII_EnergyParadox.pdf")
    
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
    create_energy_paradox_visual()