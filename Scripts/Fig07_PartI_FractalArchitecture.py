import numpy as np # Selected for generating parametric coordinates for the geometric lattice/vortex models
import matplotlib.pyplot as plt # Selected for 2D diagrammatic composition and LaTeX integration
import matplotlib.patches as patches # Selected for rendering discrete architectural shapes (boxes, arrows, nodes)
import os # Selected for robust directory management and relative pathing

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
    ax.set_xlim(0, 100)
    ax.set_ylim(-8, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # =======================================================
    # CENTRAL ENGINE: The Torsional Invariant Shaft
    # =======================================================
    # The physical connection bridging the tiers
    ax.add_patch(patches.Rectangle((46, 13.5), 8, 73.5, facecolor='#E0E8F0', edgecolor='#B0C4DE', lw=2, zorder=0))

    # Central Dotted Progression Arrows
    center_arrow_props = dict(arrowstyle="-|>", color="#555555", ls="--", lw=2)
    ax.annotate("", xy=(50, 33), xytext=(50, 22), arrowprops=center_arrow_props)
    ax.annotate("", xy=(50, 78), xytext=(50, 41), arrowprops=center_arrow_props)

    # =======================================================
    # FUNDAMENTAL DEFINITIONS (Bottom Center)
    # =======================================================
    def_text = (r"$\mathbf{Fundamental\ Definitions}$" + "\n" + 
                r"Torsional Invariant: $J_i = \rho_i r_i^4$" + "\n" + 
                r"Absolute Substrate Area: $A_S = \ell_S^2$" + "\n" +
                r"Invariant Action Budget: $c_E$")
    
    ax.text(39.0, 1.0, def_text, ha='left', va='center', fontsize=13.5, color='black', linespacing=1.8,
            bbox=dict(facecolor='#F8F9FA', edgecolor='#D0D0D0', lw=1.5, boxstyle='round,pad=0.8'))

    # =======================================================
    # MASTER EQUATIONS (Flanking the Middle Column)
    # =======================================================
    eq_h = (r"$\mathbf{Invariant\ Action}$" + "\n" + 
            r"$h_i \propto (\mathrm{Geo\ Factor}) \cdot J_i c_E$")
    ax.text(28, 64.5, eq_h, ha='left', va='top', fontsize=13.5, color='black', linespacing=2.2,
            bbox=dict(facecolor='white', edgecolor='#AABBDD', lw=1.5, boxstyle='round,pad=0.8'))

    eq_g = (r"$\mathbf{Invariant\ Gravitational\ Constant}$" + "\n" + 
            r"$G_i \propto (\mathrm{Form\ Factor}) \cdot \dfrac{c_E^2 A_S}{J_i}$")
    ax.text(56, 64.5, eq_g, ha='left', va='top', fontsize=13.5, color='black', linespacing=1.4,
            bbox=dict(facecolor='white', edgecolor='#AABBDD', lw=1.5, boxstyle='round,pad=0.8'))

    # =======================================================
    # TIER GRAPHIC RENDERING FUNCTIONS
    # =======================================================
    def draw_sc_lattice(x_c, y_c, size=3.5):
        """Tier I: Hard SC Lattice"""
        ax.add_patch(patches.Rectangle((x_c - size, y_c - size), size*2, size*2, facecolor='#F5F5F5', edgecolor='#CCCCCC', lw=1.5, zorder=2))
        for dx in [-size, 0, size]:
            for dy in [-size, 0, size]:
                ax.plot([x_c-size, x_c+size], [y_c+dy, y_c+dy], color='#D0D0D0', lw=1.5, zorder=3)
                ax.plot([x_c+dx, x_c+dx], [y_c-size, y_c+size], color='#D0D0D0', lw=1.5, zorder=3)

    def draw_fcc_lattice(x_c, y_c, size=3.5):
        """Tier II: Soft FCC Lattice"""
        ax.add_patch(patches.Rectangle((x_c - size, y_c - size), size*2, size*2, facecolor='#B0D0FF', alpha=0.6, zorder=2))
        offsets = [(-2,-2), (2,-2), (-2,2), (2,2), (0,0)]
        for dx, dy in offsets:
            ax.add_patch(patches.Circle((x_c+dx, y_c+dy), 1.8, facecolor='#0088FF', alpha=0.8, edgecolor='white', lw=1.5, zorder=3))

    def draw_vortex_loop(x_c, y_c, size=3.5):
        """Tier III: Cylindrical Vortex Loop"""
        ax.add_patch(patches.Ellipse((x_c, y_c), size*2.5, size*1.2, fill=False, edgecolor='#CC0000', lw=3, zorder=3))
        ax.add_patch(patches.Ellipse((x_c, y_c), size*1.5, size*0.5, facecolor='#FFDDDD', edgecolor='#AA0000', lw=2, zorder=2))
        t = np.linspace(0, 2*np.pi, 50)
        ax.plot(x_c + size*1.2*np.cos(t), y_c + size*0.6*np.sin(t), color='#FF0000', linestyle=':', lw=1.5, zorder=4)

    # =======================================================
    # RENDER THE THREE TIERS & SIDEWAYS LABELS
    # =======================================================
    tier_x = 50
    lbl_props = dict(facecolor='white', edgecolor='none', alpha=0.9)
    
    # Tier III: Nucleon
    y_N = 82
    draw_vortex_loop(tier_x, y_N)
    ax.text(50, y_N + 5, r"$\mathbf{TIER\ III:\ Nucleon\ Matter\ (Layer\ N)}$" + "\n" + r"Scale: $\approx 10^{-15}$ m | Dynamic Cylindrical Vortex", 
            ha='center', va='bottom', fontsize=11, color='black', bbox=lbl_props)
            
    # Tier II: Soft Floor Vacuum
    y_D = 50
    y_D_geom = y_D - 13
    draw_fcc_lattice(tier_x, y_D_geom) 
    
    ax.text(44, y_D_geom, r"$\mathbf{Phase\ Structure}$" + "\n" + "Solid Node +\nInterstitial Condensate", 
            ha='right', va='center', fontsize=11, color='black', bbox=lbl_props)

    ax.text(56, y_D_geom, r"$\mathbf{TIER\ II:\ Soft\ Floor\ Vacuum\ (Layer\ D)}$" + "\n" + r"Scale: $\approx 10^{-26}$ m | Soft Spherical FCC", 
            ha='left', va='center', fontsize=11, color='black', bbox=lbl_props)

    # Tier I: Substrate
    y_S = 18
    draw_sc_lattice(tier_x, y_S)
    ax.text(50, y_S - 4, r"$\mathbf{TIER\ I:\ Latent\ Substrate\ (Layer\ S)}$" + "\n" + r"Scale: $\approx 10^{-35}$ m | Rigid Hard SC Lattice", 
            ha='center', va='top', fontsize=11, color='black', bbox=lbl_props)

    # =======================================================
    # LEFT PANEL: Thread A (Projection of Action, h)
    # =======================================================
    ax.add_patch(patches.Rectangle((2, 10), 22, 80, facecolor='#F8F9FA', edgecolor='#D0D0D0', lw=1.5, zorder=0))
    ax.text(13, 88, r"$\mathbf{Thread\ A:\ Projection\ of\ Action\ (h)}$", ha='center', va='top', fontsize=13, color='black')

    node_props = dict(boxstyle='square,pad=0.6', facecolor='white', edgecolor='#888888', lw=1.5)
    
    ax.text(13, y_N, r"Geometric Form: $\mathbf{Cylindrical\ Vortex}$" + "\n" + r"Form Factor = $2\pi$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)
    
    ax.text(13, y_D_geom, r"Geometric Form: $\mathbf{Solid\ Sphere}$" + "\n" + r"Form Factor = $\frac{4}{3}\pi$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)
            
    ax.text(13, y_S, r"Geometric Form: $\mathbf{Radial\ Vector}$" + "\n" + r"Form Factor = $1$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)

    arrow_props = dict(arrowstyle="-|>", color="#555555", lw=2.5)
    ax.annotate("", xy=(13, y_D_geom - 4), xytext=(13, y_S + 4), arrowprops=arrow_props)
    ax.annotate("", xy=(13, y_N - 4), xytext=(13, y_D_geom + 4), arrowprops=arrow_props)
    
    h_text = (r"$\mathbf{Conservation\ of\ h:}$" + "\n\n" + 
              r"$h_S \rightarrow h_D \rightarrow h_N \rightarrow h_{obs}$" + "\n\n" + 
              "Geometric factor increases\nprecisely as Torsional Invariant\n($J_i$) decreases, perfectly\nconserving absolute Action.")
    ax.text(13, 59, h_text, ha='center', va='center', fontsize=11, color='black',
            bbox=dict(facecolor='#E8F4F8', edgecolor='#AABBDD', lw=1, boxstyle='round,pad=0.5'))

    # =======================================================
    # RIGHT PANEL: Thread B (Projection of Gravity, G)
    # =======================================================
    ax.add_patch(patches.Rectangle((76, 10), 22, 80, facecolor='#F8F9FA', edgecolor='#D0D0D0', lw=1.5, zorder=0))
    ax.text(87, 88, r"$\mathbf{Thread\ B:\ Projection\ of\ Gravity\ (G)}$", ha='center', va='top', fontsize=13, color='black')

    ax.text(87, y_N, r"Coupling: $\mathbf{Cylindrical\ (Vortex)}$" + "\n" + r"Form Factor = $1.0$" + "\n" + r"Torsion: $J_N = J_D / 1.5$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)

    ax.text(87, y_D_geom, r"Coupling: $\mathbf{Spherical\ Surface}$" + "\n" + r"Form Factor = $1.5$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)

    ax.text(87, y_S, r"Coupling: $\mathbf{Self\ (Absolute)}$" + "\n" + r"Form Factor = $1.0$", 
            ha='center', va='center', fontsize=11, color='black', bbox=node_props)

    ax.annotate("", xy=(87, y_D_geom - 4), xytext=(87, y_S + 4), arrowprops=arrow_props)
    ax.annotate("", xy=(87, y_N - 5), xytext=(87, y_D_geom + 4), arrowprops=arrow_props)

    conc_text = (r"$\mathbf{The\ Impedance\ Match:}$" + "\n" + 
                 r"$\mathbf{J_N \equiv J_S}$" + "\n\n" + 
                 "Matter is a superconductive\n" + 
                 "channel that tunnels directly\n" + 
                 "to the Hard Floor.")
    ax.text(87, 59, conc_text, ha='center', va='center', fontsize=11, color='black',
            bbox=dict(facecolor='#E8F4F8', edgecolor='#AABBDD', lw=1, boxstyle='round,pad=0.5'))

    # =======================================================
    # HORIZONTAL TIE-LINES (Relating Side Panels to Center)
    # =======================================================
    line_props = dict(color='#CCCCCC', linestyle=':', lw=2, zorder=0)
    
    ax.plot([24, 46], [y_N, y_N], **line_props)
    ax.plot([54, 76], [y_N, y_N], **line_props)
    
    ax.plot([24, 46], [y_D_geom, y_D_geom], **line_props)
    ax.plot([54, 76], [y_D_geom, y_D_geom], **line_props)
    
    ax.plot([24, 46], [y_S, y_S], **line_props)
    ax.plot([54, 76], [y_S, y_S], **line_props)

    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()
    
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig07_PartI_FractalArchitecture.pdf")
    
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