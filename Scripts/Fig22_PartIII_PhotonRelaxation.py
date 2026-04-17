import numpy as np # Selected for efficient, vectorized array math to generate the 3D ellipsoid meshes
import matplotlib.pyplot as plt # Selected for precise 2D/3D vector graphics and native LaTeX text rendering
from mpl_toolkits.mplot3d import Axes3D # Selected for native 3D spatial projection rendering
import os # Selected for robust local directory management and path-specific file saving

def create_volumetric_relaxation_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    # Setup Figure (Textbook Architectural Styling)
    fig = plt.figure(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('white')
    
    # 3D Axis setup
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')
    
    # Clean standard axes for a pure diagrammatic look
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor('white')
    ax.grid(False)

    # -------------------------------------------------------
    # 1. THE STATIC SGF LATTICE (The Background Grid)
    # -------------------------------------------------------
    # Drawing a rigid, static 3D grid to prove the universe is NOT expanding
    x_grid = np.linspace(0, 18, 7)
    y_grid = np.linspace(-3, 3, 5)
    # Expanded Z grid to exactly match the upper bounding box plane (z=7)
    z_grid = np.linspace(-8, 7, 11)
    
    grid_color = '#CCCCCC'
    grid_alpha = 0.3
    
    # Draw longitudinal lines
    for y in y_grid:
        for z in z_grid:
            ax.plot([x_grid[0], x_grid[-1]], [y, y], [z, z], color=grid_color, lw=1, alpha=grid_alpha)
            
    # Draw transverse lines (Y-axis)
    for x in x_grid:
        for z in z_grid:
            ax.plot([x, x], [y_grid[0], y_grid[-1]], [z, z], color=grid_color, lw=1, alpha=grid_alpha)
            
    # Draw transverse lines (Z-axis)
    for x in x_grid:
        for y in y_grid:
            ax.plot([x, x], [y, y], [z_grid[0], z_grid[-1]], color=grid_color, lw=1, alpha=grid_alpha)

    # Pushed back to the left (x=0) and upwards (z=7.5) to clear the newly raised top grid line
    ax.text(0.0, 3.0, 7.5, "Static SGF Lattice\n(Grid coordinates do not expand)", 
            color='black', fontsize=9, fontweight='bold', ha='center', va='bottom')

    # -------------------------------------------------------
    # 2. WAVE PACKET MODELING (The Solitons)
    # -------------------------------------------------------
    def draw_soliton(ax, center_x, L, R, freq, color, top_label, bottom_label=None, y_shift=0, z_shift=0, top_x_offset=0.0, bottom_x_offset=0.0, bottom_z_drop=0.0, bottom_ha='center'):
        """Draws a 3D wave packet: a translucent envelope and a solid internal carrier wave."""
        # 1. The 3D Translucent Envelope (Ellipsoid)
        u = np.linspace(0, 2 * np.pi, 60)
        v = np.linspace(0, np.pi, 30)
        U, V = np.meshgrid(u, v)
        
        # Parametric equations for the ellipsoid
        X = center_x + L * np.cos(U) * np.sin(V)
        Y = y_shift + R * np.sin(U) * np.sin(V)
        Z = z_shift + R * np.cos(V)
        
        ax.plot_surface(X, Y, Z, color=color, alpha=0.15, edgecolor=color, linewidth=0.2, zorder=3)
        
        # 2. The Internal Carrier Wave (Longitudinal Kinematic Dimension)
        x_wave = np.linspace(center_x - L, center_x + L, 200)
        # Gaussian envelope multiplied by a cosine carrier
        envelope = np.exp(-((x_wave - center_x)**2) / (2 * (L/2.5)**2))
        z_wave = z_shift + R * envelope * np.cos(freq * np.pi * (x_wave - center_x))
        y_wave = np.full_like(x_wave, y_shift)
        
        ax.plot(x_wave, y_wave, z_wave, color=color, lw=2.5, zorder=4)
        
        # Top Annotation (Forced to black)
        ax.text(center_x + top_x_offset, y_shift, z_shift + R + 0.5, top_label, color='black', 
                fontsize=10, fontweight='bold', ha='center', zorder=5)
                
        # Bottom Annotation (Decoupled to allow independent pushing/pulling, forced to black)
        if bottom_label:
            ax.text(center_x + bottom_x_offset, y_shift, z_shift - R - bottom_z_drop, bottom_label, 
                    color='black', fontsize=9, ha=bottom_ha, zorder=5)

    # State 1: Emission (Compact Soliton)
    bottom_txt_emission = r"Volume: $V_0$" + "\n" + r"Energy: $E_0$"
    draw_soliton(ax, center_x=2.0, L=1.0, R=0.8, freq=4.0, 
                 color='#00CCFF', top_label="Emission\n(Compact Soliton)", 
                 bottom_label=bottom_txt_emission,
                 y_shift=-2.0, z_shift=2.0, bottom_z_drop=1.5, bottom_ha='center')

    # State 2: Observation (Relaxed Soliton)
    bottom_txt_obs = (r"Longitudinal Stretch: $(1+z)$" + "\n" + 
                      r"Transverse Spread: $(1+z)^2$" + "\n" + 
                      r"Temporal Stretch: $(1+z)$" + "\n" + 
                      r"Total Dimming: $(1+z)^{-4}$")
    
    # Adjusted bottom_x_offset to -4.0 to perfectly center the left-aligned text block under the soliton
    # while keeping it strictly within the right boundary line.
    draw_soliton(ax, center_x=16.0, L=2.0, R=1.6, freq=2.0, 
                 color='#FF00FF', top_label="Observation\n(Relaxed Soliton)",
                 bottom_label=bottom_txt_obs,
                 y_shift=2.0, z_shift=-2.0, top_x_offset=-1.5, bottom_x_offset=-4.8, bottom_z_drop=5.0, bottom_ha='left')

    # -------------------------------------------------------
    # 3. PROPAGATION VECTOR & MECHANISM
    # -------------------------------------------------------
    # Diagonal Propagation Arrow
    ax.quiver(4.0, -1.5, 1.5, 10.0, 3.0, -3.0, color='black', lw=1.5, arrow_length_ratio=0.08)
    
    # Elevated Z to 0.5 to prevent physical collision, and forced high zorder
    vector_direction = (10.0, 3.0, -3.0)
    ax.text(9.0, -0.5, 0.5, r"Propagation & Dissipation", color='black', 
            fontsize=10, fontweight='bold', ha='center', va='bottom', zdir=vector_direction, zorder=10)

    # -------------------------------------------------------
    # 4. FINAL LAYOUT & RENDERING
    # -------------------------------------------------------
    # Clean layout execution
    ax.set_xlim(0, 18)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-8, 7) # Expanded top Z limit accommodates the raised SGF label and grid
    
    # Isometric viewing angle for best 3D perspective
    ax.view_init(elev=15, azim=-60)
    
    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig22_PartIII_PhotonRelaxation.pdf")
    
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
    create_volumetric_relaxation_visual()