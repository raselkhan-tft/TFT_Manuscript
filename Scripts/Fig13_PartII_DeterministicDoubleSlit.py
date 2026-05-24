import numpy as np # Selected for efficient grid mapping and wave interference calculations
import matplotlib.pyplot as plt # Selected for publication-grade 2D vector graphic control
from matplotlib.patches import Rectangle, Circle # Selected for precise geometric barrier construction
import os # Selected for robust local directory management and path-specific file saving

# ============================================================
# Hydrodynamic Steering (Deterministic Double-Slit)
# Updated:
# - Reduced streamline seeds to 9 to completely eliminate the 
#   fragmented peripheral streamlines at the top and bottom.
# - Retained natural wave masking to prevent contour edge artifacts.
# - Changed global font to sans-serif (Arial/Helvetica) for cleaner look.
# - Thinned label indicator lines and added/updated specified labels.
# - Deterministic particle path now curves into the central constructive
#   interference line and collapses at y = 0.
# - Saves as vector PDF via robust local compilation.
# ============================================================

# ----------------------------------------
# Plot style
# ----------------------------------------
plt.rcParams.update({
    "figure.dpi": 160,
    "savefig.dpi": 300,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "mathtext.fontset": "cm",
    "font.size": 11,
    "pdf.fonttype": 42,   # embed fonts as TrueType in PDF
    "ps.fonttype": 42
})

LABEL_BOX = dict(
    boxstyle="round,pad=0.22",
    facecolor="white",
    edgecolor="none",
    alpha=0.85
)

# ----------------------------------------
# Domain
# ----------------------------------------
xmin, xmax = -8.0, 8.2
ymin, ymax = -4.5, 4.5

nx, ny = 900, 500
x = np.linspace(xmin, xmax, nx)
y = np.linspace(ymin, ymax, ny)
X, Y = np.meshgrid(x, y)

# ----------------------------------------
# Geometry
# ----------------------------------------
x_source = -6.2
source = np.array([x_source, 0.0])

x_barrier = -0.45
barrier_w = 0.28

slit_sep = 1.6
slit_half_h = 0.40
upper_slit_y = slit_sep / 2
lower_slit_y = -slit_sep / 2

slit_x = x_barrier + barrier_w / 2
x_screen = 7.0
screen_thickness = 0.42
screen_inner = x_screen + screen_thickness

# ----------------------------------------
# Wave / wake model
# ----------------------------------------
lam = 0.95
k = 2 * np.pi / lam
sigma = 0.60

def rdist(x0, y0):
    return np.sqrt((X - x0) ** 2 + (Y - y0) ** 2)

def smooth_step(z, w=0.05):
    return 0.5 * (1 + np.tanh(z / w))

# Incident wave from source
R0 = rdist(source[0], source[1])
incident = np.cos(k * R0) * np.exp(-(Y ** 2) / 5.5)
incident *= (1 - smooth_step(X - x_barrier, 0.05))

# Waves emerging from two slits
R1 = rdist(slit_x, upper_slit_y)
R2 = rdist(slit_x, lower_slit_y)

A1 = np.exp(-((Y - upper_slit_y) ** 2) / (2 * sigma ** 2))
A2 = np.exp(-((Y - lower_slit_y) ** 2) / (2 * sigma ** 2))

psi1 = np.cos(k * R1) * A1 / np.sqrt(R1 + 0.35)
psi2 = np.cos(k * R2) * A2 / np.sqrt(R2 + 0.35)

right_gate = smooth_step(X - slit_x, 0.05)

# hard stop of the coherent wake at the detector
screen_stop = 1.0 - smooth_step(X - x_screen, 0.03)

wake = (psi1 + psi2) * right_gate * screen_stop
wave = incident + 1.10 * wake

# ----------------------------------------
# Interference intensity and steering field
# ----------------------------------------
I = ((psi1 + psi2) ** 2) * right_gate * screen_stop + 1e-5
S = np.sqrt(I)

dx = x[1] - x[0]
dy = y[1] - y[0]

Sxx = np.gradient(np.gradient(S, dx, axis=1), dx, axis=1)
Syy = np.gradient(np.gradient(S, dy, axis=0), dy, axis=0)
Q = -(Sxx + Syy) / (S + 1e-6)
Q *= right_gate * screen_stop
Q = np.tanh(0.18 * Q)

dQy, dQx = np.gradient(Q, dy, dx)
Fx = -dQx + 0.55 * right_gate * screen_stop
Fy = -dQy

# Reduce clutter immediately near slit mouths
relief = 1.0 - 0.45 * (
    np.exp(-((X - slit_x) ** 2 + (Y - upper_slit_y) ** 2) / 0.08) +
    np.exp(-((X - slit_x) ** 2 + (Y - lower_slit_y) ** 2) / 0.08)
)
Fx *= relief
Fy *= relief

# ----------------------------------------
# Detector-side edge masks
# ----------------------------------------
edge_margin = 0.66
edge_mask = (Y > ymin + edge_margin) & (Y < ymax - edge_margin)

wave_masked = np.where(X <= x_screen, wave, np.nan)

Iplot = np.where((X > slit_x) & (X <= x_screen) & edge_mask, I, np.nan)
Fx_stream = np.where((X > slit_x) & (X < x_screen - 0.02) & edge_mask, Fx, np.nan)
Fy_stream = np.where((X > slit_x) & (X < x_screen - 0.02) & edge_mask, Fy, np.nan)

# ----------------------------------------
# Deterministic particle path:
# source -> one slit -> constructive path -> detector centerline
# ----------------------------------------
def interp_field(px, py, field):
    if px < xmin or px > xmax or py < ymin or py > ymax:
        return np.nan
    ix = np.searchsorted(x, px) - 1
    iy = np.searchsorted(y, py) - 1
    ix = np.clip(ix, 0, nx - 2)
    iy = np.clip(iy, 0, ny - 2)

    x1, x2 = x[ix], x[ix + 1]
    y1, y2 = y[iy], y[iy + 1]
    tx = (px - x1) / (x2 - x1 + 1e-12)
    ty = (py - y1) / (y2 - y1 + 1e-12)

    f11 = field[iy, ix]
    f21 = field[iy, ix + 1]
    f12 = field[iy + 1, ix]
    f22 = field[iy + 1, ix + 1]

    return ((1 - tx) * (1 - ty) * f11 +
            tx * (1 - ty) * f21 +
            (1 - tx) * ty * f12 +
            tx * ty * f22)

# definite passage through upper slit
p0 = np.array([x_source + 0.12, 0.20])
p_slit = np.array([slit_x + 0.03, upper_slit_y - 0.03])

n1 = 140
seg1_x = np.linspace(p0[0], p_slit[0], n1)
seg1_y = np.linspace(p0[1], p_slit[1], n1)

pts = [p_slit.copy()]
dt = 0.055
target_y = 0.0

for _ in range(900):
    px, py = pts[-1]
    if px >= x_screen - 0.20:
        break
    if py <= ymin + 0.15 or py >= ymax - 0.15:
        break

    fx = interp_field(px, py, Fx)
    fy = interp_field(px, py, Fy)

    if np.isnan(fx) or np.isnan(fy):
        fx, fy = 1.0, 0.0

    v_field = np.array([fx, fy])
    v_field /= (np.linalg.norm(v_field) + 1e-12)

    v_drift = np.array([1.35, 0.0])
    v_drift /= (np.linalg.norm(v_drift) + 1e-12)

    detector_pull = np.clip((px - slit_x) / (x_screen - slit_x), 0.0, 1.0)
    v_center = np.array([0.0, target_y - py])
    v_center /= (np.linalg.norm(v_center) + 1e-12)

    v = (0.22 * v_field + 0.50 * v_drift + 0.70 * detector_pull * v_center)
    v /= (np.linalg.norm(v) + 1e-12)

    newp = np.array([px, py]) + dt * v
    pts.append(newp)

traj2 = np.array(pts)

end_pt = traj2[-1]
impact_y = 0.0

n_tail = 100
tail_x = np.linspace(end_pt[0], x_screen, n_tail)
tail_y = np.linspace(end_pt[1], impact_y, n_tail)

particle_x = np.concatenate([seg1_x, traj2[:, 0], tail_x])
particle_y = np.concatenate([seg1_y, traj2[:, 1], tail_y])

impact = np.array([x_screen, impact_y])

target_x_for_marker = 2.2
idx_particle = np.argmin(np.abs(particle_x - target_x_for_marker))
particle_marker = np.array([particle_x[idx_particle], particle_y[idx_particle]])

# ----------------------------------------
# Streamline seed points
# ----------------------------------------
seed_ys = np.linspace(-1.8, 1.8, 9)
start_points = np.column_stack([np.full_like(seed_ys, slit_x + 0.55), seed_ys])

# ----------------------------------------
# Plot
# ----------------------------------------
fig, ax = plt.subplots(figsize=(13.6, 6.4))
ax.set_facecolor("white")

# Wave contours stop at the screen
levels = np.linspace(-1.05, 1.05, 18)
ax.contour(
    X, Y, wave_masked,
    levels=levels,
    colors="#6f92c9",
    linewidths=0.75,
    alpha=0.82,
    linestyles="solid",
    zorder=1
)

# Interference shading stops at the screen
ax.imshow(
    Iplot / np.nanmax(Iplot),
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    cmap="Blues",
    alpha=0.16,
    aspect="auto",
    zorder=0
)

# Steering streamlines stop at the screen
ax.streamplot(
    x, y, Fx_stream, Fy_stream,
    color="#2f5d8a",
    density=1.35,
    arrowsize=0.0,
    linewidth=0.9,
    start_points=start_points,
    integration_direction="forward",
    zorder=2
)

# ----------------------------------------
# Barrier blocks
# ----------------------------------------
bar_color = "#444444"

ax.add_patch(Rectangle(
    (x_barrier, upper_slit_y + slit_half_h),
    barrier_w,
    ymax - (upper_slit_y + slit_half_h),
    facecolor=bar_color, edgecolor="black", lw=0.8, zorder=5
))

ax.add_patch(Rectangle(
    (x_barrier, lower_slit_y + slit_half_h),
    barrier_w,
    (upper_slit_y - slit_half_h) - (lower_slit_y + slit_half_h),
    facecolor=bar_color, edgecolor="black", lw=0.8, zorder=5
))

ax.add_patch(Rectangle(
    (x_barrier, ymin),
    barrier_w,
    (lower_slit_y - slit_half_h) - ymin,
    facecolor=bar_color, edgecolor="black", lw=0.8, zorder=5
))

# ----------------------------------------
# Detector screen as a finite wall
# ----------------------------------------
ax.add_patch(Rectangle(
    (x_screen, ymin),
    screen_thickness,
    ymax - ymin,
    facecolor="#f1f1f1",
    edgecolor="black",
    lw=1.5,
    zorder=6
))

ax.text(
    x_screen + screen_thickness + 0.12, 0.0,
    "Detector Screen",
    rotation=90,
    va="center",
    ha="left",
    fontsize=11,
    bbox=LABEL_BOX,
    zorder=20
)

# ----------------------------------------
# Source
# ----------------------------------------
ax.add_patch(Circle(source, 0.085, facecolor="none", edgecolor="#8B0000", lw=2.0, zorder=7))
ax.text(
    source[0] - 0.02, source[1] + 0.38, "Source",
    ha="center", va="bottom", fontsize=11,
    bbox=LABEL_BOX, zorder=20
)

# ----------------------------------------
# Deterministic particle path and collapse
# ----------------------------------------
# Changed the source-to-collapse path to navy blue
ax.plot(
    particle_x, particle_y,
    color="#000080",
    lw=2.0,
    zorder=8
)

# Changed the matter design to a maroon ring (hollow circle)
ax.add_patch(Circle(
    particle_marker, 0.085,
    facecolor="none", edgecolor="#8B0000", lw=2.0,
    zorder=9
))

burst_r = 0.17
for th in np.linspace(0, 2 * np.pi, 14, endpoint=False):
    x1, y1 = impact
    x2 = x1 + burst_r * np.cos(th)
    y2 = y1 + burst_r * np.sin(th)
    ax.plot([x1, x2], [y1, y2], color="#8B0000", lw=1.0, zorder=9)

ax.add_patch(Circle(impact, 0.085, facecolor="none", edgecolor="#8B0000", lw=2.0, zorder=10))

# ----------------------------------------
# Tiny chaotic heat vibrations inside the wall
# ----------------------------------------
rng = np.random.default_rng(7)
n_heat = 22
for _ in range(n_heat):
    x0 = x_screen + rng.uniform(0.06, screen_thickness - 0.05)
    y0 = impact_y + rng.normal(0, 0.22)
    amp = rng.uniform(0.03, 0.08)
    xs = np.linspace(x0 - 0.03, x0 + 0.03, 20)
    ys = y0 + amp * np.sin(np.linspace(0, 3*np.pi, 20))
    ax.plot(xs, ys, color="#888888", lw=0.7, alpha=0.7, zorder=7)

# ----------------------------------------
# Arrow-style annotations with white masks
# ----------------------------------------
arrow_style = dict(arrowstyle="->", lw=0.6, color="#444444")

ax.annotate(
    r"Extended Pilot Wave ($\Psi$)",
    xy=(-3.2, 1.55), xytext=(-5.7, 3.2),
    arrowprops=arrow_style,
    fontsize=11, ha="left",
    bbox=LABEL_BOX, zorder=20
)

ax.annotate(
    r"Quantum Force ($-\nabla Q$)",
    xy=(2.3, 0.95), xytext=(0.8, 3.55),
    arrowprops=arrow_style,
    fontsize=11, ha="left",
    bbox=LABEL_BOX, zorder=20
)

ax.annotate(
    "Deterministic trajectory\nthrough one slit only",
    xy=(slit_x + 0.02, upper_slit_y - 0.03), xytext=(-5.2, -2.8),
    arrowprops=arrow_style,
    fontsize=11, ha="left",
    bbox=LABEL_BOX, zorder=20
)

ax.annotate(
    "Localized particle\n(Impedance Artifact $m$)",
    xy=(particle_marker[0], particle_marker[1]), xytext=(2.9, -2.7),
    arrowprops=arrow_style,
    fontsize=11, ha="left",
    bbox=LABEL_BOX, zorder=20
)

# Changed the friction annotation text
ax.annotate(
    r"Viscous Collapse ($-F_{\mathrm{fr}}$)",
    xy=(impact[0], impact[1]), xytext=(5.15, 1.75),
    arrowprops=dict(arrowstyle="->", lw=0.6, color="#444444", shrinkB=12),
    fontsize=11, ha="left",
    bbox=LABEL_BOX, zorder=20
)

ax.annotate(
    "Destructive Interference\n(High Static Tension)",
    xy=(4.0, 1.2), xytext=(4.0, 2.8),
    arrowprops=arrow_style,
    fontsize=11, ha="center",
    bbox=LABEL_BOX, zorder=20
)

ax.annotate(
    "Constructive Interference\n(Low Static Tension)",
    xy=(5.0, 0.0), xytext=(6.5, -3.5),
    arrowprops=dict(arrowstyle="->", lw=0.6, color="#444444", shrinkB=10),
    fontsize=11, ha="center",
    bbox=LABEL_BOX, zorder=20
)

ax.annotate(
    "Double-Slit Barrier",
    xy=(x_barrier, 0.0), xytext=(-2.0, -3.5),
    arrowprops=arrow_style,
    fontsize=11, ha="center",
    bbox=LABEL_BOX, zorder=20
)

# ----------------------------------------
# Final formatting
# ----------------------------------------
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")
ax.axis("off")

# =======================================================
# FINAL RENDER & PDF EXPORT
# =======================================================
plt.tight_layout()

output_dir = "Figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
pdf_filename = os.path.join(output_dir, "Fig13_PartII_DeterministicDoubleSlit.pdf")

try:
    # Saving as high-fidelity vector PDF for publication
    plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
    print(f"High-fidelity vector PDF saved to: {pdf_filename}")
except PermissionError:
    print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

plt.show()