import numpy as np # Selected for efficient vectorization of the parametric knot equations and grid distortion
import matplotlib.pyplot as plt # Selected for precise 2D vector graphic control, custom annotations, and LaTeX rendering
import os # Selected for robust directory management and path-specific file saving

def create_doppler_coupling_visual():
    # Setup Figure (Minimalist Architectural Styling)
    fig, ax = plt.subplots(figsize=(14, 6), dpi=150)
    ax.set_facecolor('white')
    
    # -------------------------------------------------------
    # 1. THE FCC SUBSTRATE GRID & SHEAR WAVE DISTORTION
    # -------------------------------------------------------
    x_grid = np.linspace(0, 15, 400)
    y_grid = np.linspace(-4, 4, 17)
    
    # Wave parameters (Boson / Transverse Shear)
    wave_center = 3.5
    wave_amplitude = 1.0
    wave_width = 1.5
    k = 2.0  # Wavenumber
    
    # The distortion envelope: A localized Gaussian wave packet
    def shear_distortion(x):
        return wave_amplitude * np.sin(k * (x - wave_center)) * np.exp(-((x - wave_center) / wave_width)**2)

    # Draw Horizontal Grid Lines (Strained by the wave)
    for y in y_grid:
        y_distorted = y + shear_distortion(x_grid)
        ax.plot(x_grid, y_distorted, color='#E0E0E0', lw=1.2, zorder=1)
        
    # Draw Vertical Grid Lines (Strained by the wave)
    x_verts = np.linspace(0, 15, 31)
    y_verts = np.linspace(-4, 4, 100)
    for x_v in x_verts:
        x_line = np.full_like(y_verts, x_v)
        y_distorted = y_verts + shear_distortion(x_v)
        ax.plot(x_line, y_distorted, color='#E0E0E0', lw=1.2, zorder=1)

    # Highlight the primary Force Carrier Waveform
    ax.plot(x_grid, shear_distortion(x_grid), color='#00CCFF', lw=4, alpha=0.8, zorder=2)
    
    # Source Carrier Vector (c_E)
    ax.annotate("", xy=(5.5, 2.5), xytext=(2.5, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#0088CC", lw=3))
    ax.text(4.0, 2.7, r"$c_E$ (Wave Speed)", color='#0088CC', 
            fontsize=12, fontweight='bold', ha='center', va='bottom')
            
    # Updated Force Carrier Label
    ax.text(4.0, -2.5, "Force Carrier\n(Transverse Shear Wave)", color='#0088CC', 
            fontsize=11, fontweight='bold', ha='center', va='top')

    # -------------------------------------------------------
    # 2. THE TARGET (MATTER KNOT)
    # -------------------------------------------------------
    particle_center = 11.5
    
    # Parametric topological knot (Lissajous curve) to represent localized matter
    t = np.linspace(0, 2 * np.pi, 500)
    knot_x = particle_center + 0.8 * np.sin(3 * t + np.pi/4)
    knot_y = 0.8 * np.sin(2 * t)
    
    ax.plot(knot_x, knot_y, color='#333333', lw=2, zorder=3)
    ax.fill(knot_x, knot_y, color='#333333', alpha=0.2, zorder=3)
    ax.scatter([particle_center], [0], color='#111111', s=50, zorder=4)

    # Target Particle Vector (v_ext -> c_E)
    ax.annotate("", xy=(14.0, 2.5), xytext=(11.5, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#CC0000", lw=3))
    ax.text(12.75, 2.7, r"$v_{ext} \to c_E$", color='#CC0000', 
            fontsize=12, fontweight='bold', ha='center', va='bottom')
    ax.text(particle_center, -2.5, "Target Mass (Matter)\nTopological Structural Knot", color='#333333', 
            fontsize=11, fontweight='bold', ha='center', va='top')

    # -------------------------------------------------------
    # 3. THE INTERACTION GAP (Mechanical Failure)
    # -------------------------------------------------------
    wave_leading_edge = 5.5
    particle_trailing_edge = 10.5
    
    # Draw the compressed relative vector (Right-pointing arrow only)
    ax.annotate("", xy=(particle_trailing_edge, 0), xytext=(wave_leading_edge, 0),
                arrowprops=dict(arrowstyle="-|>", color="#FF8800", lw=2, linestyle='--'))
    
    # Relative Impact Velocity Label
    ax.text((wave_leading_edge + particle_trailing_edge) / 2, 0.2, 
            r"Relative Impact Velocity $\approx 0$", color='#FF8800', 
            fontsize=11, fontweight='bold', ha='center', va='bottom')
    ax.text((wave_leading_edge + particle_trailing_edge) / 2, -0.2, 
            r"($c_E - v_{ext}$)", color='#FF8800', 
            fontsize=12, fontweight='bold', ha='center', va='top')

    # -------------------------------------------------------
    # STYLING & FORMATTING
    # -------------------------------------------------------
    # Clean up bounding boxes for architectural look
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 15)
    ax.set_ylim(-4, 4)

    plt.tight_layout()
    
    # -----------------------
    # PDF Export Logic
    # -----------------------
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig06_PartI_ForceCoupling.pdf")
    
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
    create_doppler_coupling_visual()