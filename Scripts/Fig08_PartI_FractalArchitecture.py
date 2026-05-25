import numpy as np # Selected for generating parametric coordinates for the geometric lattice/vortex models
import matplotlib.pyplot as plt # Selected for 2D diagrammatic composition and LaTeX integration
import matplotlib.patches as patches # Selected for rendering discrete architectural shapes (boxes, arrows, nodes)
import os # Selected for robust directory management and path-specific file saving

# Libraries selected for executing and downloading high-fidelity vector graphics in browser/notebook environments
import base64
try:
    from IPython.display import display, HTML
    IPYTHON_AVAILABLE = True
except ImportError:
    IPYTHON_AVAILABLE = False

def create_fractal_column_visual():
    # Force strict bounding boxes for publication formatting
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'mathtext.fontset': 'cm',
        'font.size': 11
    })
    
    # Initialize full-bleed diagram canvas
    fig, ax = plt.subplots(figsize=(16, 12), dpi=150)
    ax.set_facecolor('#FAFAFA')
    
    # Setup coordinate system [-8, 100] for absolute layout positioning
    # Y-limit expanded downward to -8 to restore bottom margin clearance after shifting the box down
    ax.set_xlim(0, 100)
    ax.set_ylim(-8, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # =======================================================
    # CENTRAL ENGINE: The Structural Mass Moment Shaft
    # =======================================================
    # The physical connection bridging the tiers
    # Spans from x=46 to x=54 (width 8, center 50)
    # Extended downward to y=13.5 to fully enclose the Tier I geometry (bottom edge at 14.5)
    ax.add_patch(patches.Rectangle((46, 13.5), 8, 73.5, facecolor='#E0E8F0', edgecolor='#B0C4DE', lw=2, zorder=0))

    # Central Dotted Progression Arrows (Substrate -> Soft Floor -> Nucleon)
    center_arrow_props = dict(arrowstyle="-|>", color="#555555", ls="--", lw=2)
    # Arrow from Tier I (y=18) to Tier II (y=37)
    ax.annotate("", xy=(50, 33), xytext=(50, 22), arrowprops=center_arrow_props)
    # Arrow from Tier II (y=37) to Tier III (y=82)
    ax.annotate("", xy=(50, 78), xytext=(50, 41), arrowprops=center_arrow_props)

    # =======================================================
    # FUNDAMENTAL DEFINITIONS (Bottom Center)
    # =======================================================
    def_text = (r"$\mathbf{Fundamental\ Definitions}$" + "\n" + 
                r"Scale-Invariant Mass Moment: $J_i = \rho_i r_i^4$" + "\n" + 
                r"Absolute Substrate Area: $A_{\mathrm{S}} = \ell_{\mathrm{S}}^2$" + "\n" +
                r"Invariant Elastic Capacity: $c_{\mathrm{E}}$")
    
    # Mathematically centered directly beneath the central shaft
    ax.text(50.0, 1.0, def_text, ha='center', va='center', fontsize=13.5, color='black', linespacing=1.8,
            bbox=dict(facecolor='#F8F9FA', edgecolor='#D0D0D0', lw=1.5, boxstyle='round,pad=0.8'))

    # =======================================================
    # MASTER EQUATIONS (Flanking the Middle Column)
    # =======================================================
    # Both are strictly top-aligned to ensure the titles are perfectly level horizontally.
    
    eq_h = (r"$\mathbf{Invariant\ Action}$" + "\n" + 
            r"$h_i = (\mathrm{Geo\ Factor}) \cdot J_i c_{\mathrm{E}}$")
    ax.text(28, 64.5, eq_h, ha='left', va='top', fontsize=13.5, color='black', linespacing=2.2,
            bbox=dict(facecolor='white', edgecolor='#AABBDD', lw=1.5, boxstyle='round,pad=0.8'))

    # \dfrac is used instead of \frac to force display-style sizing for the fractional constants
    # Reduced linespacing to 1.4 to counteract the tall \dfrac bounding box and match the h_i gap
    eq_g = (r"$\mathbf{Invariant\ Gravitational\ Constant}$" + "\n" + 
            r"$G_i = (\mathrm{Form\ Factor}) \cdot \dfrac{c_{\mathrm{E}}^2 A_{\mathrm{S}}}{J_i}$")
    ax.text(56, 64.5, eq_g, ha='left', va='top', fontsize=13.5, color='black', linespacing=1.4,
            bbox=dict(facecolor='white', edgecolor='#AABBDD', lw=1.5, boxstyle='round,pad=0.8'))

    # =======================================================
    # TIER GRAPHIC RENDERING FUNCTIONS
    # =======================================================
    def draw_sc_lattice(x_c, y_c, size=3.5):
        """Tier I: Hard SC Lattice (Rigid substrate grain)"""
        # Changed facecolor to off-white and removed circular nodes for a clean sheet aesthetic
        ax.add_patch(patches.Rectangle((x_c - size, y_c - size), size*2, size*2, facecolor='#F5F5F5', edgecolor='#CCCCCC', lw=1.5, zorder=2))
        # Draw internal grid lines to indicate the square lattice geometry
        for dx in [-size, 0, size]:
            for dy in [-size, 0, size]:
                ax.plot([x_c-size, x_c+size], [y_c+dy, y_c+dy], color='#D0D0D0', lw=1.5, zorder=3)
                ax.plot([x_c+dx, x_c+dx], [y_c-size, y_c+size], color='#D0D0D0', lw=1.5, zorder=3)

    def draw_fcc_lattice(x_c, y_c, size=3.5):
        """Tier II: Soft FCC Lattice (Solid node + interstitial condensate)"""
        ax.add_patch(patches.Rectangle((x_c - size, y_c - size), size*2, size*2, facecolor='#E0F7FA', alpha=0.6, zorder=2))
        # Draw staggered packed spheres (Updated to Flagship Electric Blue)
        offsets = [(-2,-2), (2,-2), (-2,2), (2,2), (0,0)]
        for dx, dy in offsets:
            ax.add_patch(patches.Circle((x_c+dx, y_c+dy), 1.8, facecolor='#00CCFF', alpha=0.8, edgecolor='white', lw=1.5, zorder=3))

    def draw_vortex_loop(x_c, y_c, size=3.5):
        """Tier III: Cylindrical Phase Vortex (Spin 1/2 Dynamic Mass)"""
        # Clean Figure-8 (Infinity Symbol) representing a continuous Spin-1/2 twist
        t = np.linspace(0, 2 * np.pi, 300)
        
        # Parametric Lissajous curve for the infinity loop
        # A defines horizontal width, B defines vertical height bounds
        A = size * 1.4
        B = size * 0.7
        
        x_curve = x_c + A * np.sin(t)
        y_curve = y_c + B * np.sin(2 * t)
        
        # 1. Draw the continuous background ribbon
        ax.plot(x_curve, y_curve, color='#8B0000', lw=4.5, zorder=5)
        
        # 2. The Crossover Gap (Forcing the 3D Perspective)
        # Extract just the "front" segment of the curve crossing the origin (t near 0)
        t_front = np.linspace(-0.4, 0.4, 50)
        x_front = x_c + A * np.sin(t_front)
        y_front = y_c + B * np.sin(2 * t_front)
        
        # Draw a thick background-colored line to erase the back segment at the intersection
        ax.plot(x_front, y_front, color='#E0E8F0', lw=10.0, solid_capstyle='butt', zorder=6)
        
        # Re-draw the front segment perfectly over the erased gap
        ax.plot(x_front, y_front, color='#8B0000', lw=4.5, solid_capstyle='round', zorder=7)

    # =======================================================
    # RENDER THE THREE TIERS & SIDEWAYS LABELS
    # =======================================================
    tier_x = 50
    lbl_props = dict(facecolor='white', edgecolor='none', alpha=0.9)
    
    # Tier III: Nucleon
    y_N = 82
    draw_vortex_loop(tier_x, y_N)
    # Nucleon label returned to top of central column
    ax.text(50, y_N + 5, r"$\mathbf{TIER\ III:\ Nucleon\ Matter\ (Layer\ N)}$" + "\n" + r"Scale: $\approx 10^{-15}$ m | Toroidal Phase Vortex", 
            ha='center', va='bottom', fontsize=11, color='black', bbox=lbl_props)
            
    # Tier II: Soft Floor Vacuum
    y_D = 50
    y_D_geom = y_D - 13 # Offset to properly space the vertical column
    draw_fcc_lattice(tier_x, y_D_geom) 
    
    # Left-side label: Restored Vacuum Composition
    ax.text(44, y_D_geom, r"$\mathbf{Phase\ Structure}$" + "\n" + "Solid Node +\nInterstitial Condensate", 
            ha='right', va='center', fontsize=11, color='black', bbox=lbl_props)

    # Right-side label: Soft floor scale and geometry
    ax.text(56, y_D_geom, r"$\mathbf{TIER\ II:\ Soft\ Floor\ Vacuum\ (Layer\ D)}$" + "\n" + r"Scale: $\approx 10^{-26}$ m | Soft Spherical FCC", 
            ha='left', va='center', fontsize=11, color='black', bbox=lbl_props)

    # Tier I: Substrate
    y_S = 18
    draw_sc_lattice(tier_x, y_S)
    # Substrate label lifted slightly (from y_S - 5 to y_S - 4) to ensure clearance over the definitions box
    ax.text(50, y_S - 4, r"$\mathbf{TIER\ I:\ Latent\ Substrate\ (Layer\ S)}$" + "\n" + r"Scale: $\approx 10^{-35}$ m | Rigid Hard SC Lattice", 
            ha='center', va='top', fontsize=11, color='black', bbox=lbl_props)

    # =======================================================
    # LEFT PANEL: Thread A (Projection of Action, h)
    # =======================================================
    # Panel Background (Squeezed to width 22, center x=13)
    ax.add_patch(patches.Rectangle((2, 10), 22, 80, facecolor='#F8F9FA', edgecolor='#D0D0D0', lw=1.5, zorder=0))
    ax.text(13, 88, r"$\mathbf{Thread\ A:\ Projection\ of\ Action\ (h)}$", ha='center', va='top', fontsize=13, color='black')

    # Progression Nodes
    node_props = dict(boxstyle='square,pad=0.6', facecolor='white', edgecolor='#888888', lw=1.5)
    
    # Tier 3 (Left)
    ax.text(13, y_N, r"Geometric Form: $\mathbf{Topological\ Torus}$" + "\n" + r"Form Factor = $2\pi$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)
    
    # Tier 2 (Left)
    ax.text(13, y_D_geom, r"Geometric Form: $\mathbf{Solid\ Sphere}$" + "\n" + r"Form Factor = $\frac{4}{3}\pi$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)
            
    # Tier 1 (Left)
    ax.text(13, y_S, r"Geometric Form: $\mathbf{Radial\ Vector}$" + "\n" + r"Form Factor = $1$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)

    # Vertical Flow Arrows (Bottom Up Conservation)
    arrow_props = dict(arrowstyle="-|>", color="#555555", lw=2.5)
    ax.annotate("", xy=(13, y_D_geom - 4), xytext=(13, y_S + 4), arrowprops=arrow_props)
    ax.annotate("", xy=(13, y_N - 4), xytext=(13, y_D_geom + 4), arrowprops=arrow_props)
    
    # Thread A Conclusion
    h_text = (r"$\mathbf{Conservation\ of\ h:}$" + "\n\n" + 
              r"$h_{\mathrm{S}} \rightarrow h_{\mathrm{D}} \rightarrow h_{\mathrm{N}} \rightarrow h_{\mathrm{obs}}$" + "\n\n" + 
              "Geometric factor increases\nprecisely as the Structural Mass Moment\n($J_i$) decreases, perfectly\nconserving absolute Action.")
    ax.text(13, 59, h_text, ha='center', va='center', fontsize=11, color='black',
            bbox=dict(facecolor='#E8F4F8', edgecolor='#AABBDD', lw=1, boxstyle='round,pad=0.5'))

    # =======================================================
    # RIGHT PANEL: Thread B (Projection of Gravity, G)
    # =======================================================
    # Panel Background (Squeezed to width 22, center x=87, unified bluish theme)
    ax.add_patch(patches.Rectangle((76, 10), 22, 80, facecolor='#F8F9FA', edgecolor='#D0D0D0', lw=1.5, zorder=0))
    ax.text(87, 88, r"$\mathbf{Thread\ B:\ Projection\ of\ Gravity\ (G)}$", ha='center', va='top', fontsize=13, color='black')

    # Tier 3 (Right)
    ax.text(87, y_N, r"Coupling: $\mathbf{Toroidal\ (Vortex)}$" + "\n" + r"Form Factor = $1.0$" + "\n" + r"Moment: $J_{\mathrm{N}} = J_{\mathrm{D}} / 1.5$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)

    # Tier 2 (Right)
    ax.text(87, y_D_geom, r"Coupling: $\mathbf{Spherical\ Surface}$" + "\n" + r"Form Factor = $1.5$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)

    # Tier 1 (Right)
    ax.text(87, y_S, r"Coupling: $\mathbf{Self\ (Absolute)}$" + "\n" + r"Form Factor = $1.0$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)

    # Vertical Flow Arrows (Bottom Up Projection)
    ax.annotate("", xy=(87, y_D_geom - 4), xytext=(87, y_S + 4), arrowprops=arrow_props)
    ax.annotate("", xy=(87, y_N - 5), xytext=(87, y_D_geom + 4), arrowprops=arrow_props)

    # Right Thread Conclusion Box (Unified Architecture & Impedance Match, unified bluish theme)
    conc_text = (r"$\mathbf{The\ Impedance\ Match:}$" + "\n" + 
                 r"$\mathbf{J_{\mathrm{N}} \equiv J_{\mathrm{S}}}$" + "\n\n" + 
                 "Matter is a superconductive\n" + 
                 "channel that tunnels directly\n" + 
                 "to the Hard Floor.")
    ax.text(87, 59, conc_text, ha='center', va='center', fontsize=11, color='black',
            bbox=dict(facecolor='#E8F4F8', edgecolor='#AABBDD', lw=1, boxstyle='round,pad=0.5'))

    # =======================================================
    # HORIZONTAL TIE-LINES (Relating Side Panels to Center)
    # =======================================================
    # Adjusted limits to mathematically flush the tie lines between the squeezed panels and the central shaft
    line_props = dict(color='#CCCCCC', linestyle=':', lw=2, zorder=0)
    
    # Tier N
    ax.plot([24, 46], [y_N, y_N], **line_props)
    ax.plot([54, 76], [y_N, y_N], **line_props)
    
    # Tier D
    ax.plot([24, 46], [y_D_geom, y_D_geom], **line_props)
    ax.plot([54, 76], [y_D_geom, y_D_geom], **line_props)
    
    # Tier S
    ax.plot([24, 46], [y_S, y_S], **line_props)
    ax.plot([54, 76], [y_S, y_S], **line_props)

    # =======================================================
    # FINAL RENDER
    # =======================================================
    plt.tight_layout()
    
    # --- PDF EXPORT AND AUTO-DOWNLOAD LOGIC ---
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig08_PartI_FractalArchitecture.pdf")
    
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
    create_fractal_column_visual()