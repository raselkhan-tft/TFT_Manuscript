import numpy as np # Selected for generating coordinate indices and meshgrids
import matplotlib.pyplot as plt # Selected for precise 2D/3D diagrammatic layout and LaTeX rendering
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import os # Selected for directory management and robust file saving

def create_substrate_ghost_canvas():
    # Final version: Unified Ghost White Gravy Substrate (The Canvas)
    # Optimized for academic publication (PRL Standard)
    fig = plt.figure(figsize=(12, 6), dpi=120)

    # Define "Ghost" appearance
    # Face: Pure White with full transparency (Invisible/Potential)
    ghost_face = (1.0, 1.0, 1.0, 0.0) 
    # Edge: Faint Light Gray lines to show structure
    ghost_edge = '#CCCCCC' 
    # Label Color Depth: Standardized to 'gray' for technical markers
    label_color = 'gray'

    # ---------------- 3D panel ----------------
    ax3d = fig.add_subplot(1, 2, 1, projection="3d")

    n = 3
    filled = np.ones((n, n, n), dtype=bool)
    x, y, z = np.indices((n + 1, n + 1, n + 1))

    # Set 3D blocks to Ghost Face
    colors = np.empty(filled.shape + (4,), dtype=float)
    colors[:] = ghost_face

    # Render voxels: Transparent faces, faint edges
    ax3d.voxels(x, y, z, filled, facecolors=colors, 
                edgecolor=ghost_edge, linewidth=0.5)

    # Clean 3D axes
    for axis in [ax3d.xaxis, ax3d.yaxis, ax3d.zaxis]:
        axis.line.set_linewidth(0)
    ax3d.set_xticks([]); ax3d.set_yticks([]); ax3d.set_zticks([])
    ax3d.grid(False)
    ax3d.set_facecolor("white")
    ax3d.set_box_aspect((1, 1, 1))

    # Updated nomenclature: l_G -> l_S
    ax3d.set_xlabel(r"$x$ ($\ell_S$ units)", labelpad=-6, color=label_color)
    ax3d.set_ylabel(r"$y$ ($\ell_S$ units)", labelpad=-6, color=label_color)
    ax3d.set_zlabel(r"$z$ ($\ell_S$ units)", labelpad=-6, color=label_color)

    # Academic Label (a) - Positioned top-left in axis coordinates
    ax3d.text2D(0.05, 0.95, r"$\mathbf{(a)}$", transform=ax3d.transAxes, 
                fontsize=14, fontweight='bold', ha='left', va='top')

    # ---------------- 2D panel ----------------
    ax2d = fig.add_subplot(1, 2, 2)
    nx, ny = 6, 6

    for i in range(nx):
        for j in range(ny):
            # Create solid Ghost tiles (White/Transparent with faint edge)
            rect = plt.Rectangle((i, j), 1, 1, 
                                 facecolor=ghost_face, 
                                 edgecolor=ghost_edge, 
                                 linewidth=0.8)
            ax2d.add_patch(rect)

    # Final 2D Styling
    ax2d.set_xlim(0, nx + 0.5)
    ax2d.set_ylim(-1.8, ny + 0.5)
    ax2d.set_aspect("equal")
    ax2d.set_xticks([]); ax2d.set_yticks([])
    ax2d.set_facecolor("white")
    for spine in ax2d.spines.values():
        spine.set_visible(False)

    # Mu annotation - Updated to muS and set to gray for depth consistency
    ax2d.text(5.5, 0.5, r"$\mu_S \rightarrow 0$",
              ha="center", va="center", color=label_color, 
              fontsize=10, fontweight='bold')

    # Unit-cell length annotation
    x1, x2, y_arrow = 2.0, 3.0, -0.55
    # Arrow and text color synchronized to the 3D axis label color depth ('gray')
    ax2d.annotate("", xy=(x2, y_arrow), xytext=(x1, y_arrow),
                  arrowprops=dict(arrowstyle="<->", color=label_color, linewidth=1.2))
    
    ax2d.text((x1 + x2) / 2.0, y_arrow - 0.20, r"$\ell_S \approx 10^{-35}\ \mathrm{m}$",
              ha="center", va="top", fontsize=9, color=label_color)

    # Academic Label (b) - Repositioned horizontally to -0.15 to sit outside the diagram frame
    ax2d.text(-0.15, 0.95, r"$\mathbf{(b)}$", transform=ax2d.transAxes, 
              fontsize=14, fontweight='bold', ha='left', va='top')

    # ---------------- Layout ----------------
    # Titles removed to adhere to the Strict Academic Standard.
    # Defining descriptions entirely in the LaTeX figure caption.
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.1, top=0.95, wspace=0.15)

    # ---------------- PDF Export Logic ----------------
    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf_filename = os.path.join(output_dir, "Fig02_PartI_Substrate.pdf")
    
    try:
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        print(f"Vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"Permission denied: Please close {pdf_filename} before running.")
    except Exception as e:
        print(f"Export error: {e}")

    plt.show()

if __name__ == "__main__":
    create_substrate_ghost_canvas()