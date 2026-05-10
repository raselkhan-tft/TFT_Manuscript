import numpy as np # Selected for efficient, vectorized array math to evaluate the Gaussian envelope equation
import matplotlib.pyplot as plt # Selected for precise 2D/3D vector graphics and native CM text rendering
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
    # Faded to a very light grey with a thin linewidth to emphasize the solitons
    x_grid = np.linspace(0, 18, 7)
    y_grid = np.linspace(-3, 3, 5)
    z_grid = np.linspace(-8, 7, 11)
    
    grid_color = '#E8E8E8'
    grid_alpha = 0.6
    grid_lw = 0.5
    
    # Draw longitudinal lines
    for y in y_grid:
        for z in z_grid:
            ax.plot([x_grid[0], x_grid[-1]], [y, y], [z, z], color=grid_color, lw=grid_lw, alpha=grid_alpha)
            
    # Draw transverse lines (Y-axis)
    for x in x_grid:
        for z in z_grid:
            ax.plot([x, x], [y_grid[0], y_grid[-1]], [z, z], color=grid_color, lw=grid_lw, alpha=grid_alpha)
            
    # Draw transverse lines (Z-axis)
    for x in x_grid:
        for y in y_grid:
            ax.plot([x, x], [y, y], [z_grid[0], z_grid[-1]], color=grid_color, lw=grid_lw, alpha=grid_alpha)

    # Overarching context: Largest text size (13) for semantic hierarchy
    ax.text(0.0, 3.0, 7.5, "Static SGF Lattice\n(Grid coordinates do not expand)", 
            color='black', fontsize=13, fontweight='normal', ha='center', va='bottom')

    # -------------------------------------------------------
    # 2. STRICT MATHEMATICAL WAVE PACKET MODELING
    # -------------------------------------------------------
    def draw_soliton(ax, center_x, sigma, k, R, A, color, top_label, bottom_label=None, 
                     y_shift=0, z_shift=0, top_x_offset=0.0, bottom_x_offset=0.0, bottom_z_drop=0.0, 
                     top_z_gap=0.9, top_ha='center'):
        """
        Draws a 3D wave packet driven purely by the Gaussian envelope equation:
        Psi(x,t) = A * exp(-x^2 / 2sigma^2) * sin(kx - wt)
        """
        # Dynamic visual boundary based on spatial variance
        L_bound = 3.5 * sigma 
        
        # 1. The 3D Translucent Envelope (Ellipsoid)
        u = np.linspace(0, 2 * np.pi, 60)
        v = np.linspace(0, np.pi, 30)
        U, V = np.meshgrid(u, v)
        
        X = center_x + L_bound * np.cos(U) * np.sin(V)
        Y = y_shift + R * np.sin(U) * np.sin(V)
        Z = z_shift + R * np.cos(V)
        
        # shade=False removes the "shiny plastic" specular highlights
        ax.plot_surface(X, Y, Z, color=color, alpha=0.15, edgecolor=color, linewidth=0.2, zorder=3, rstride=2, cstride=2, shade=False)
        
        # 2. The Internal Carrier Wave (Snapshot at t=0)
        x_wave = np.linspace(center_x - L_bound, center_x + L_bound, 200)
        
        # Exact Gaussian envelope applied to the amplitude
        envelope = np.exp(-((x_wave - center_x)**2) / (2 * sigma**2))
        z_wave = z_shift + A * envelope * np.sin(k * np.pi * (x_wave - center_x))
        y_wave = np.full_like(x_wave, y_shift)
        
        ax.plot(x_wave, y_wave, z_wave, color=color, lw=2.5, zorder=4)
        
        # Top Annotation (State Title): Font size reduced from 11 to 10
        ax.text(center_x + top_x_offset, y_shift, z_shift + R + top_z_gap, top_label, color='black', 
                fontsize=10, fontweight='normal', ha=top_ha, zorder=5)
                
        # Bottom Annotation (Data List): Smallest text size (9)
        if bottom_label:
            ax.text(center_x + bottom_x_offset, y_shift, z_shift - R - bottom_z_drop, bottom_label, 
                    color='black', fontsize=9, ha='left', zorder=5)

    # --- GEOMETRIC PARAMETERS ---
    # State 1: Emission (Compact Soliton)
    sigma_0 = 0.35
    k_0 = 4.0
    R_0 = 0.8
    A_0 = 0.8
    
    draw_soliton(ax, center_x=2.0, sigma=sigma_0, k=k_0, R=R_0, A=A_0, 
                 color='#000080', top_label="Emission\n(Compact Soliton)", 
                 bottom_label=None,
                 y_shift=-2.0, z_shift=2.0, bottom_x_offset=-1.0, bottom_z_drop=1.5,
                 top_ha='center')

    # State 2: Observation (Relaxed Soliton)
    z_factor = 2.0
    
    # 1. Longitudinal stretch scales the spatial variance (\sigma)
    sigma_obs = sigma_0 * z_factor
    # 2. Wavenumber stretches (frequency drops)
    k_obs = k_0 / z_factor
    # 3. Transverse radius stretches linearly by (1+z), resulting in Area expanding by (1+z)^2
    R_obs = R_0 * z_factor
    # 4. Amplitude drops proportionally to the specified damping factor
    A_obs = A_0 / (z_factor**2) 

    bottom_txt_obs = (r"Longitudinal Stretch: $(1+z)$" + "\n" + 
                      r"Transverse Spread: $(1+z)^2$" + "\n" + 
                      r"Temporal Stretch: $(1+z)$" + "\n" + 
                      r"Total Dimming: $(1+z)^{-4}$")
    
    # Corrected projection mechanics: 
    # ha='right' anchors the text edge to the offset, keeping it precisely clear of the boundary.
    # top_z_gap increased significantly to 2.2 to overcome the 15-degree camera compression.
    draw_soliton(ax, center_x=15.0, sigma=sigma_obs, k=k_obs, R=R_obs, A=A_obs, 
                 color='#B22222', top_label="Observation\n(Relaxed Soliton)",
                 bottom_label=bottom_txt_obs,
                 y_shift=2.0, z_shift=-2.0, top_x_offset=2.8, bottom_x_offset=-4.0, bottom_z_drop=5.0, 
                 top_z_gap=1.5, top_ha='right')

    # -------------------------------------------------------
    # 3. PROPAGATION VECTOR & MECHANISM
    # -------------------------------------------------------
    # Diagonal Propagation Arrow
    ax.quiver(4.0, -1.5, 1.5, 9.0, 3.0, -3.0, color='black', lw=0.75, arrow_length_ratio=0.08)
    
    vector_direction = (9.0, 3.0, -3.0)
    
    # Masking properties to ensure the equations are clearly legible over the grid lines
    eq_mask = dict(facecolor='white', edgecolor='none', alpha=0.85, pad=3)
    
    # EXACT 3D INTERSECTION CALCULATION:
    # At X=5.5, the vector perfectly intersects Y=-1.0 and Z=1.0.
    
    # Decoupled Title: Font size reduced from 11 to 10
    ax.text(5.5, -1.0, 1.64, "Propagation & Dissipation", color='black', 
            fontsize=10, fontweight='normal', ha='left', va='bottom', zdir=vector_direction, zorder=10, bbox=eq_mask)
            
    # Top Equation (Energy Decay): Original gap 0.4 * 0.60 (40% reduction) = 0.24 gap (Z = 1.0 + 0.24 = 1.24)
    ax.text(5.5, -1.0, 0.7, r"$E_{\mathrm{obs}} = E_{\mathrm{emit}} e^{-\Gamma_D x / c_E}$", color='black', 
            fontsize=11, fontweight='normal', ha='left', va='bottom', zdir=vector_direction, zorder=10, bbox=eq_mask)
            
    # Bottom Equation (Redshift Factor): Maintained original -0.4 gap below the line (Z = 1.0 - 0.4 = 0.60)
    ax.text(5.5, -1.0, 0.60, r"$(1+z) = e^{\Gamma_D x / c_E}$", color='black', 
            fontsize=11, fontweight='normal', ha='left', va='top', zdir=vector_direction, zorder=10, bbox=eq_mask)

    # -------------------------------------------------------
    # 4. FINAL LAYOUT & RENDERING
    # -------------------------------------------------------
    ax.set_xlim(0, 18)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-8, 7)
    
    # Isometric viewing angle for best 3D perspective
    ax.view_init(elev=15, azim=-60)
    
    # Explicit manual bounds bypass the Matplotlib tight_layout() MemoryError in 3D
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig22_PartIII_PhotonRelaxation.pdf")
    
    try:
        plt.savefig(pdf_filename, format='pdf')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()

if __name__ == "__main__":
    create_volumetric_relaxation_visual()