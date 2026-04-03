import numpy as np # Selected for efficient trigonometric mapping and coordinate array generation
import matplotlib.pyplot as plt # Selected for precise 3D/2D diagrammatic composition and LaTeX rendering
from mpl_toolkits.mplot3d import Axes3D
import os # Selected for directory management and file system robust execution

# =============================================================================
# FCC UNIT CELL (Electric Blue / Slate Gray) - CLEAN BASE FOR VECTOR EXPORT
# =============================================================================

# -------------------- Parameters --------------------
a = 1.0
r = a / (2.0 * np.sqrt(2.0)) # FCC: a*sqrt(2) = 4r

# -------------------- COLORS --------------------
# Sphere surface: Electric Blue
sphere_color = (0.0, 0.8, 1.0) # Hex #00CCFF
sphere_alpha = 1.0

# Interstitial: derived from sphere color but lighter/transparent
void_color = tuple(min(1.0, 0.60 + 0.40*c) for c in sphere_color)
void_alpha = 0.13

# Cut-face color: Slate Gray
cut_face_color = (0.44, 0.50, 0.56) # Hex #708090

# -------------------- Rendering controls --------------------
grid_n = 46          # interstitial voxel resolution
n_theta = 170        # sphere surface resolution
n_phi = 130
cap_res = 150        # cap surface resolution

ELEV = 18
AZIM = -55

# Tiny offset to prevent z-fighting on cut faces
EPS = 1e-4 * a

# Pull back sphere surface from cube boundary so caps define the cut plane
CLIP = 2.0 * EPS

CROSS_CENTER = (0.0, a/2, a/2)

# -------------------- Helpers --------------------
def draw_cube_wireframe(ax, x0=0, y0=0, z0=0, size=1.0, lw=2.2, color="0.0"):
    X = np.array([0, 1, 1, 0, 0, 1, 1, 0]) * size + x0
    Y = np.array([0, 0, 1, 1, 0, 0, 1, 1]) * size + y0
    Z = np.array([0, 0, 0, 0, 1, 1, 1, 1]) * size + z0
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    for i, j in edges:
        ax.plot([X[i], X[j]], [Y[i], Y[j]], [Z[i], Z[j]], color=color, linewidth=lw, zorder=10)

def compute_void_voxels(centers, r, a=1.0, n=40):
    xs = (np.arange(n) + 0.5) * (a / n)
    ys = (np.arange(n) + 0.5) * (a / n)
    zs = (np.arange(n) + 0.5) * (a / n)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    inside_any = np.zeros((n, n, n), dtype=bool)
    r2 = r * r
    for (cx, cy, cz) in centers:
        inside_any |= ((X - cx)**2 + (Y - cy)**2 + (Z - cz)**2) <= r2
    return ~inside_any

def plot_clipped_sphere(ax, center, r, a=1.0, color=(0.7,0.8,0.95),
                        alpha=1.0, n_theta=120, n_phi=90, clip=0.0):
    cx, cy, cz = center
    u = np.linspace(0, 2*np.pi, n_theta)
    v = np.linspace(0, np.pi, n_phi)
    U, V = np.meshgrid(u, v)
    X = cx + r*np.cos(U)*np.sin(V)
    Y = cy + r*np.sin(U)*np.sin(V)
    Z = cz + r*np.cos(V)
    inside = (X >= 0 + clip) & (X <= a - clip) & \
             (Y >= 0 + clip) & (Y <= a - clip) & \
             (Z >= 0 + clip) & (Z <= a - clip)
    X = np.where(inside, X, np.nan)
    Y = np.where(inside, Y, np.nan)
    Z = np.where(inside, Z, np.nan)
    ax.plot_surface(X, Y, Z, color=color, alpha=alpha, edgecolor="none", linewidth=0, antialiased=True, shade=True, zorder=5)

def plot_cap_surface(ax, center, r, axis, plane_val, a=1.0,
                     color=(0.7,0.8,0.95), alpha=1.0, cap_res=70,
                     plane_offset=0.0, zsort=None, shade=False):
    cx, cy, cz = center
    pv = plane_val + plane_offset
    if axis == "x":
        d = abs(cx - plane_val)
        if d >= r: return
        rho = np.sqrt(r*r - d*d)
        y = np.linspace(max(0, cy - rho), min(a, cy + rho), cap_res)
        z = np.linspace(max(0, cz - rho), min(a, cz + rho), cap_res)
        Y, Z = np.meshgrid(y, z, indexing="xy")
        X = np.full_like(Y, pv)
        mask = ((Y - cy)**2 + (Z - cz)**2) <= rho*rho
    elif axis == "y":
        d = abs(cy - plane_val)
        if d >= r: return
        rho = np.sqrt(r*r - d*d)
        x = np.linspace(max(0, cx - rho), min(a, cx + rho), cap_res)
        z = np.linspace(max(0, cz - rho), min(a, cz + rho), cap_res)
        X, Z = np.meshgrid(x, z, indexing="xy")
        Y = np.full_like(X, pv)
        mask = ((X - cx)**2 + (Z - cz)**2) <= rho*rho
    else:  # "z"
        d = abs(cz - plane_val)
        if d >= r: return
        rho = np.sqrt(r*r - d*d)
        x = np.linspace(max(0, cx - rho), min(a, cx + rho), cap_res)
        y = np.linspace(max(0, cy - rho), min(a, cy + rho), cap_res)
        X, Y = np.meshgrid(x, y, indexing="xy")
        Z = np.full_like(X, pv)
        mask = ((X - cx)**2 + (Y - cy)**2) <= rho*rho
    
    # FIXED: Masking each coordinate array individually to avoid ValueError
    X = np.where(mask, X, np.nan)
    Y = np.where(mask, Y, np.nan)
    Z = np.where(mask, Z, np.nan)
    
    kwargs = dict(color=color, alpha=alpha, edgecolor="none", linewidth=0, antialiased=True, shade=shade, zorder=6)
    if zsort is not None:
        kwargs["zsort"] = zsort
    ax.plot_surface(X, Y, Z, **kwargs)

# -------------------- FCC centers --------------------
centers = [
    (0,0,0),(a,0,0),(0,a,0),(a,a,0),(0,0,a),(a,0,a),(0,a,a),(a,a,a),
    (a/2,a/2,0),(a/2,a/2,a),
    (a/2,0,a/2),(a/2,a,a/2),
    (0,a/2,a/2),(a,a/2,a/2)
]

# -------------------- Plot Initialization --------------------
fig = plt.figure(figsize=(10, 10), dpi=160)
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor("white")

# ---- Interstitial fill (Volume Rendering) ----
void_full = compute_void_voxels(centers, r, a=a, n=grid_n)
xe, ye, ze = np.linspace(0, a, grid_n + 1), np.linspace(0, a, grid_n + 1), np.linspace(0, a, grid_n + 1)
Xv, Yv, Zv = np.meshgrid(xe, ye, ze, indexing="ij")
fc = np.zeros(void_full.shape + (4,), dtype=float)
fc[..., 0], fc[..., 1], fc[..., 2], fc[..., 3] = void_color[0], void_color[1], void_color[2], void_alpha
ax.voxels(Xv, Yv, Zv, void_full, facecolors=fc, edgecolor="none", zorder=1)

# ---- Spheres + Caps Rendering ----
planes = [("x", 0.0), ("x", a), ("y", 0.0), ("y", a), ("z", 0.0), ("z", a)]
for c in centers:
    plot_clipped_sphere(ax, c, r, a=a, color=sphere_color, alpha=sphere_alpha, n_theta=n_theta, n_phi=n_phi, clip=CLIP)
    for axis, p in planes:
        offset = +EPS if p == 0.0 else -EPS
        plot_cap_surface(ax, c, r, axis=axis, plane_val=p, a=a, color=cut_face_color, alpha=0.95, cap_res=cap_res, plane_offset=offset, zsort="max", shade=False)

# ---- Cube wireframe ----
draw_cube_wireframe(ax, 0, 0, 0, size=a, lw=2.4, color="0.0")

# ---- Clean axes / view ----
ax.set_xlim(0, a); ax.set_ylim(0, a); ax.set_zlim(0, a)
ax.set_box_aspect((1, 1, 1))
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
ax.grid(False)

for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.pane.set_facecolor((1, 1, 1, 0))
    axis.pane.set_edgecolor((1, 1, 1, 0))

ax.view_init(elev=ELEV, azim=AZIM)
plt.tight_layout()

# ---- PDF Export Logic ----
output_dir = "Figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
pdf_filename = os.path.join(output_dir, "Fig03_PartI_FCClatticeSimple.pdf")

try:
    # Save as vector PDF for Adobe Acrobat post-processing
    plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
    print(f"High-fidelity vector PDF saved to: {pdf_filename}")
except PermissionError:
    print(f"Permission denied: Please ensure {pdf_filename} is closed before running.")
except Exception as e:
    print(f"Export error: {e}")

plt.show()