import numpy as np # Selected for efficient trigonometric mapping and coordinate array generation
import matplotlib.pyplot as plt # Selected for precise 3D/2D diagrammatic composition and LaTeX rendering
from mpl_toolkits.mplot3d import Axes3D
import os # Selected for directory management and file system robust execution

# =============================================================================
# FCC OCTAHEDRAL VOIDS (Maximum Mass Capacity Limit)
# =============================================================================

def create_octahedral_void_visual():
    # -------------------- PRL Formatting --------------------
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm', 
        'font.size': 11
    })

    # -------------------- Parameters --------------------
    a = 1.0
    r_D = a / (2.0 * np.sqrt(2.0)) # FCC Node Radius
    r_O = (np.sqrt(2.0) - 1.0) * r_D # Octahedral Void Radius

    # -------------------- COLORS --------------------
    # FCC Nodes (Ghost scaffolding, opacity retained at baseline 0.25)
    fcc_color = (0.0, 0.8, 1.0) # Electric Blue
    fcc_alpha = 0.25 
    # Cut-faces slightly deepened from baseline (0.7, 0.85, 0.95) to (0.4, 0.75, 0.95) for subtle edge definition
    fcc_cut_color = (0.4, 0.75, 0.95) 

    # Octahedral Voids (Solid matter representation)
    void_color = '#8B0000' # Maroon
    void_cut_color = '#550000' # Darker Maroon for flat boundary cuts
    void_alpha = 0.95

    # -------------------- Rendering controls --------------------
    n_theta = 120        # sphere surface resolution
    n_phi = 90
    cap_res = 100        # cap surface resolution

    ELEV = 20
    AZIM = -55
    EPS = 1e-4 * a
    CLIP = 2.0 * EPS

    # -------------------- Helpers --------------------
    def draw_cube_wireframe(ax, x0=0, y0=0, z0=0, size=1.0, lw=1.5, color="#666666"):
        X = np.array([0, 1, 1, 0, 0, 1, 1, 0]) * size + x0
        Y = np.array([0, 0, 1, 1, 0, 0, 1, 1]) * size + y0
        Z = np.array([0, 0, 0, 0, 1, 1, 1, 1]) * size + z0
        edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        for i, j in edges:
            ax.plot([X[i], X[j]], [Y[i], Y[j]], [Z[i], Z[j]], color=color, linewidth=lw, linestyle=':', zorder=10)

    def plot_clipped_sphere(ax, center, r, color, alpha, clip=0.0):
        cx, cy, cz = center
        u = np.linspace(0, 2*np.pi, n_theta)
        v = np.linspace(0, np.pi, n_phi)
        U, V = np.meshgrid(u, v)
        
        X = cx + r*np.cos(U)*np.sin(V)
        Y = cy + r*np.sin(U)*np.sin(V)
        Z = cz + r*np.cos(V)
        
        # Mathematical clipping bounds the sphere perfectly within the unit cell
        inside = (X >= 0 + clip) & (X <= a - clip) & (Y >= 0 + clip) & (Y <= a - clip) & (Z >= 0 + clip) & (Z <= a - clip)
        X = np.where(inside, X, np.nan)
        Y = np.where(inside, Y, np.nan)
        Z = np.where(inside, Z, np.nan)
        
        ax.plot_surface(X, Y, Z, color=color, alpha=alpha, edgecolor="none", linewidth=0, antialiased=True, shade=True, zorder=5)

    def plot_cap_surface(ax, center, r, axis, plane_val, color, alpha, plane_offset=0.0):
        cx, cy, cz = center
        pv = plane_val + plane_offset
        d = abs((cx if axis=="x" else cy if axis=="y" else cz) - plane_val)
        
        if d >= r: return 
        rho = np.sqrt(r*r - d*d)
        
        if axis == "x":
            y = np.linspace(max(0, cy - rho), min(a, cy + rho), cap_res)
            z = np.linspace(max(0, cz - rho), min(a, cz + rho), cap_res)
            Y, Z = np.meshgrid(y, z, indexing="xy")
            X = np.full_like(Y, pv)
            mask = ((Y - cy)**2 + (Z - cz)**2) <= rho*rho
        elif axis == "y":
            x = np.linspace(max(0, cx - rho), min(a, cx + rho), cap_res)
            z = np.linspace(max(0, cz - rho), min(a, cz + rho), cap_res)
            X, Z = np.meshgrid(x, z, indexing="xy")
            Y = np.full_like(X, pv)
            mask = ((X - cx)**2 + (Z - cz)**2) <= rho*rho
        else:  # "z"
            x = np.linspace(max(0, cx - rho), min(a, cx + rho), cap_res)
            y = np.linspace(max(0, cy - rho), min(a, cy + rho), cap_res)
            X, Y = np.meshgrid(x, y, indexing="xy")
            Z = np.full_like(X, pv)
            mask = ((X - cx)**2 + (Y - cy)**2) <= rho*rho
        
        X = np.where(mask, X, np.nan)
        Y = np.where(mask, Y, np.nan)
        Z = np.where(mask, Z, np.nan)
        
        ax.plot_surface(X, Y, Z, color=color, alpha=alpha, edgecolor="none", linewidth=0, antialiased=True, shade=False, zorder=6)

    # -------------------- Geometry Data Generation --------------------
    fcc_centers = [
        (0,0,0),(a,0,0),(0,a,0),(a,a,0),(0,0,a),(a,0,a),(0,a,a),(a,a,a),
        (a/2,a/2,0),(a/2,a/2,a), (a/2,0,a/2),(a/2,a,a/2), (0,a/2,a/2),(a,a/2,a/2)
    ]
    void_centers = [(a/2, a/2, a/2)]
    edges = []
    for f1 in [0, a]:
        for f2 in [0, a]:
            edges.append((a/2, f1, f2))
            edges.append((f1, a/2, f2))
            edges.append((f1, f2, a/2))
    void_centers.extend(list(set(edges)))

    # -------------------- Plot Initialization --------------------
    fig = plt.figure(figsize=(12, 10), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("white")

    planes = [("x", 0.0), ("x", a), ("y", 0.0), ("y", a), ("z", 0.0), ("z", a)]

    for c in fcc_centers:
        plot_clipped_sphere(ax, c, r_D, color=fcc_color, alpha=fcc_alpha, clip=CLIP)
        for axis, p in planes:
            offset = +EPS if p == 0.0 else -EPS
            # Cut plane alpha restored to baseline fcc_alpha (0.25)
            plot_cap_surface(ax, c, r_D, axis=axis, plane_val=p, color=fcc_cut_color, alpha=fcc_alpha, plane_offset=offset)

    for c in void_centers:
        plot_clipped_sphere(ax, c, r_O, color=void_color, alpha=void_alpha, clip=CLIP)
        for axis, p in planes:
            offset = +EPS if p == 0.0 else -EPS
            plot_cap_surface(ax, c, r_O, axis=axis, plane_val=p, color=void_cut_color, alpha=1.0, plane_offset=offset)

    draw_cube_wireframe(ax, 0, 0, 0, size=a, lw=1.5, color="#666666")

    ax.set_xlim(0, a); ax.set_ylim(0, a); ax.set_zlim(0, a)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.grid(False)

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor((1, 1, 1, 0))

    ax.view_init(elev=ELEV, azim=AZIM)
    plt.tight_layout()

    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pdf_filename = os.path.join(output_dir, "FigY_PartIII_OctahedralVoid.pdf")

    try:
        plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except Exception as e:
        print(f"Export error: {e}")

    plt.show()

if __name__ == "__main__":
    create_octahedral_void_visual()