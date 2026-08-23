import numpy as np
import matplotlib.pyplot as plt
import os


def create_quantum_tunneling_visual():
    # ============================================================
    # PUBLICATION TYPOGRAPHY
    # ============================================================
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm',
        'font.size': 11
    })

    # ============================================================
    # FIGURE
    # ============================================================
    fig, ax = plt.subplots(figsize=(16, 7), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)

    # ============================================================
    # COLORS
    # ============================================================
    wave_color = '#000080'       # Deep Navy
    matter_color = '#8B0000'     # Muted Maroon
    driver_color = '#8B4513'     # Deep Bronze
    lattice_color = '#B0C4DE'    # Light Steel Blue
    barrier_fill = '#E8ECEF'
    structure_color = '#2F4F4F'
    separator_color = '#808080'

    # ============================================================
    # GLOBAL GEOMETRY
    # ============================================================
    y_min = -4.4
    y_max = 4.4

    # Left panel: Passive
    passive_x0 = 0.0
    passive_x1 = 11.2
    passive_barrier_start = 3.8
    passive_barrier_end = 7.5

    # Right panel: Active
    active_x0 = 12.4
    active_x1 = 24.0
    active_barrier_start = 16.2
    active_barrier_end = 19.9

    panel_separator = 11.8

    # Common wave parameters
    amplitude = 0.85
    k = np.pi / 1.8
    kappa_B = 0.38

    y_base_levels = np.linspace(-3.2, 3.2, 12)

    text_bbox = dict(
        facecolor='white',
        edgecolor='none',
        alpha=0.85,
        pad=2
    )

    # ============================================================
    # HELPER: CONTINUUM GRID
    # ============================================================
    def draw_background_grid(x0, x1, barrier_start, barrier_end):
        for yb in y_base_levels:
            ax.plot(
                [x0, barrier_start],
                [yb, yb],
                color=lattice_color,
                lw=0.9,
                alpha=0.35,
                zorder=0
            )
            ax.plot(
                [barrier_end, x1],
                [yb, yb],
                color=lattice_color,
                lw=0.9,
                alpha=0.35,
                zorder=0
            )

        for xv in np.arange(x0, x1 + 0.01, 0.5):
            if xv <= barrier_start or xv >= barrier_end:
                ax.plot(
                    [xv, xv],
                    [-3.2, 3.2],
                    color=lattice_color,
                    lw=0.9,
                    alpha=0.35,
                    zorder=0
                )

    # ============================================================
    # HELPER: BARRIER REGION
    # ============================================================
    def draw_barrier(
        barrier_start,
        barrier_end,
        deformation_x,
        deformation_y,
        title_y=3.58
    ):
        ax.axvspan(
            barrier_start,
            barrier_end,
            color=barrier_fill,
            alpha=0.65,
            zorder=0
        )

        # Vertical dense lattice members
        for xv in np.linspace(barrier_start, barrier_end, 15):
            ax.plot(
                [xv, xv],
                [-3.2, 3.2],
                color=lattice_color,
                lw=1.25,
                alpha=0.75,
                zorder=1
            )

        # Horizontal lattice links deformed by local field
        for yb in y_base_levels:
            localization = np.exp(-(yb / 2.8) ** 2)
            y_lattice = yb + 0.26 * localization * deformation_y

            ax.plot(
                deformation_x,
                y_lattice,
                color=wave_color,
                lw=1.55,
                alpha=0.30,
                zorder=2
            )

        ax.text(
            (barrier_start + barrier_end) / 2,
            title_y,
            r"Effective Barrier Region ($V_{\mathrm{B}}$)",
            fontsize=11,
            fontweight='bold',
            ha='center',
            va='bottom',
            color='black',
            bbox=text_bbox
        )

    # ============================================================
    # HELPER: TOPOLOGICAL KNOT
    # ============================================================
    def draw_topological_knot(
        x_center,
        y_center,
        text_dx=0.0,
        text_dy=0.4,
        text_ha='center',
        label="Topological Knot\n(Incident State)"
    ):
        t = np.linspace(0, 2 * np.pi, 300)

        knot_x = x_center + 0.32 * np.sin(3 * t + np.pi / 4)
        knot_y = y_center + 0.32 * np.sin(2 * t)

        ax.plot(
            knot_x,
            knot_y,
            color=matter_color,
            lw=1.8,
            zorder=8
        )

        ax.fill(
            knot_x,
            knot_y,
            color=matter_color,
            alpha=0.35,
            zorder=7
        )

        ax.scatter(
            [x_center],
            [y_center],
            color=matter_color,
            s=35,
            zorder=9
        )

        if label:
            ax.text(
                x_center + text_dx,
                y_center + text_dy,
                label,
                fontsize=9.5,
                fontweight='bold',
                ha=text_ha,
                va='bottom',
                color='black',
                bbox=text_bbox,
                zorder=15
            )

    # ============================================================
    # PANEL (a): PASSIVE EVANESCENT COUPLING
    # ============================================================
    draw_background_grid(
        passive_x0,
        passive_x1,
        passive_barrier_start,
        passive_barrier_end
    )

    # Exact Analytic Boundary-Matched Solution for Panel (a)
    L_pass = passive_barrier_end - passive_barrier_start
    a_L_pass = amplitude

    M_pass = np.array([
        [1, -1, -1, 0],
        [-1j * k, -kappa_B, kappa_B, 0],
        [
            0,
            np.exp(kappa_B * L_pass),
            np.exp(-kappa_B * L_pass),
            -1
        ],
        [
            0,
            kappa_B * np.exp(kappa_B * L_pass),
            -kappa_B * np.exp(-kappa_B * L_pass),
            -1j * k
        ]
    ])

    v_pass = np.array([
        -a_L_pass,
        -1j * k * a_L_pass,
        0,
        0
    ])

    b_L_pass, B_pass, C_pass, b_R_pass = np.linalg.solve(
        M_pass,
        v_pass
    )

    # Plot Left-Side Field
    x_inc = np.linspace(passive_x0, passive_barrier_start, 400)
    xi_L = x_inc - passive_barrier_start
    y_inc = np.real(
        a_L_pass * np.exp(1j * k * xi_L)
        +
        b_L_pass * np.exp(-1j * k * xi_L)
    )

    ax.plot(
        x_inc,
        y_inc,
        color=wave_color,
        lw=2.7,
        alpha=0.90,
        zorder=5
    )

    # Plot Evanescent Field Inside Barrier
    x_ev = np.linspace(passive_barrier_start, passive_barrier_end, 350)
    xi_B = x_ev - passive_barrier_start
    y_ev = np.real(
        B_pass * np.exp(kappa_B * xi_B)
        +
        C_pass * np.exp(-kappa_B * xi_B)
    )

    draw_barrier(
        passive_barrier_start,
        passive_barrier_end,
        x_ev,
        y_ev
    )

    ax.plot(
        x_ev,
        y_ev,
        color=wave_color,
        lw=3.0,
        alpha=0.95,
        zorder=6
    )

    # Plot Small Transmitted Field
    x_trans = np.linspace(passive_barrier_end, passive_x1, 300)
    xi_R_pass = x_trans - passive_barrier_end
    y_trans = np.real(
        b_R_pass * np.exp(1j * k * xi_R_pass)
    )

    ax.plot(
        x_trans,
        y_trans,
        color=wave_color,
        lw=2.4,
        alpha=0.90,
        zorder=5
    )

    # Topological Knot
    knot_x_a = 2.4
    xi_knot_a = knot_x_a - passive_barrier_start
    knot_y_a = np.real(
        a_L_pass * np.exp(1j * k * xi_knot_a)
        +
        b_L_pass * np.exp(-1j * k * xi_knot_a)
    )

    draw_topological_knot(
        knot_x_a,
        knot_y_a,
        text_dx=-0.1,
        text_dy=0.5,
        text_ha='center'
    )

    # Labels for Panel (a)
    ax.text(
        1.5,
        -2.45,
        "Incident Matter-Order-Parameter Field",
        fontsize=9.5,
        fontweight='bold',
        ha='center',
        va='top',
        color='black',
        bbox=text_bbox
    )

    idx_inc = np.argmin(np.abs(x_inc - 1.5))
    ax.annotate(
        "",
        xy=(1.5, y_inc[idx_inc] - 0.2),
        xytext=(1.5, -2.35),
        arrowprops=dict(
            arrowstyle="-|>",
            color=wave_color,
            lw=1.2
        )
    )

    # a_L and b_L horizontal arrows
    ax.text(
        2.1,
        3.2,
        r"$a_{\mathrm{L}}$",
        fontsize=11,
        ha='right',
        va='center',
        color='black'
    )
    ax.annotate(
        "",
        xy=(3.3, 3.2),
        xytext=(2.4, 3.2),
        arrowprops=dict(
            arrowstyle="-|>",
            color=wave_color,
            lw=1.5
        )
    )

    ax.text(
        3.5,
        2.5,
        r"$b_{\mathrm{L}}$",
        fontsize=11,
        ha='left',
        va='center',
        color='black'
    )
    ax.annotate(
        "",
        xy=(2.4, 2.5),
        xytext=(3.3, 2.5),
        arrowprops=dict(
            arrowstyle="-|>",
            color=wave_color,
            lw=1.5
        )
    )

    ax.text(
        5.65,
        -0.85,
        r"Evanescent Barrier Field" + "\n" + r"($\psi \propto e^{-\kappa_{\mathrm{B}}x}$)",
        fontsize=9.5,
        fontweight='bold',
        ha='center',
        va='top',
        color='black',
        bbox=text_bbox
    )
    ax.annotate(
        "",
        xy=(5.65, y_ev[175] - 0.2),
        xytext=(5.65, -0.75),
        arrowprops=dict(
            arrowstyle="-|>",
            color=wave_color,
            lw=1.2
        )
    )

    x_lbl = 9.5
    idx_lbl = np.argmin(np.abs(x_trans - x_lbl))
    ax.text(
        x_lbl,
        -1.2,
        r"Transmitted Field ($b_{\mathrm{R}}$)",
        fontsize=9.5,
        fontweight='bold',
        ha='center',
        va='top',
        color='black',
        bbox=text_bbox
    )
    ax.annotate(
        "",
        xy=(x_lbl, y_trans[idx_lbl] - 0.2),
        xytext=(x_lbl, -1.1),
        arrowprops=dict(
            arrowstyle="-|>",
            color=wave_color,
            lw=1.2
        )
    )

    ax.text(
        (passive_barrier_start + passive_barrier_end) / 2,
        -3.55,
        r"$T_{\mathrm{pass}} \propto e^{-2\kappa_{\mathrm{B}}L}$",
        fontsize=12,
        ha='center',
        va='top',
        color='black',
        bbox=text_bbox
    )

    ax.text(
        (passive_x0 + passive_x1) / 2,
        4.08,
        r"$\mathbf{(a)\ Passive\ Evanescent\ Coupling}$",
        fontsize=13,
        ha='center',
        va='bottom',
        color='black'
    )

    # ============================================================
    # PANEL SEPARATOR
    # ============================================================
    ax.plot(
        [panel_separator, panel_separator],
        [-4.0, 4.1],
        color=separator_color,
        lw=1.0,
        alpha=0.35,
        linestyle=':',
        zorder=20
    )

    # ============================================================
    # PANEL (b): COHERENT BOUNDARY CONTROL
    # ============================================================
    draw_background_grid(
        active_x0,
        active_x1,
        active_barrier_start,
        active_barrier_end
    )

    # ------------------------------------------------------------
    # Analytic coherent-control state
    # ------------------------------------------------------------
    # Incoming ports:  a_L from the left, a_R from the right
    # Outgoing ports:  b_L to the left, b_R to the right
    # Coherent cancellation condition: b_L = 0
    a_L_act = amplitude

    B_act = (a_L_act / 2) * (1 + 1j * k / kappa_B)
    C_act = (a_L_act / 2) * (1 - 1j * k / kappa_B)

    L_act = active_barrier_end - active_barrier_start
    U_act = (
        B_act * np.exp(kappa_B * L_act)
        + C_act * np.exp(-kappa_B * L_act)
    )
    U_prime_act = kappa_B * (
        B_act * np.exp(kappa_B * L_act)
        - C_act * np.exp(-kappa_B * L_act)
    )

    a_R_act = 0.5 * (U_act - U_prime_act / (1j * k))
    b_R_act = 0.5 * (U_act + U_prime_act / (1j * k))

    # ------------------------------------------------------------
    # Left exterior: incident pilot/order-parameter field a_L
    # ------------------------------------------------------------
    x_source = np.linspace(active_x0, active_barrier_start, 400)
    xi_L_act = x_source - active_barrier_start
    y_source = np.real(
        a_L_act * np.exp(1j * k * xi_L_act)
    )

    ax.plot(
        x_source,
        y_source,
        color=wave_color,
        lw=2.7,
        alpha=0.90,
        zorder=5
    )

    # ------------------------------------------------------------
    # Coherently driven evanescent barrier field
    # ------------------------------------------------------------
    x_active_barrier = np.linspace(active_barrier_start, active_barrier_end, 350)
    xi_B_act = x_active_barrier - active_barrier_start
    y_barrier_active = np.real(
        B_act * np.exp(kappa_B * xi_B_act)
        + C_act * np.exp(-kappa_B * xi_B_act)
    )

    draw_barrier(
        active_barrier_start,
        active_barrier_end,
        x_active_barrier,
        y_barrier_active
    )

    ax.plot(
        x_active_barrier,
        y_barrier_active,
        color=wave_color,
        lw=3.0,
        alpha=0.95,
        zorder=6
    )

    # ============================================================
    # RIGHT EXTERIOR: PILOT-WAVE / TWO-PORT VISUALIZATION
    # ============================================================
    # A moving topological knot must remain visibly embedded in the
    # coherent order-parameter/pilot-wave field. Therefore b_R is
    # drawn as a solid blue outgoing pilot-wave segment that leaves
    # the barrier continuously and passes through the transmitted knot.
    # The counter-propagating control input a_R remains a separate
    # dashed brown component in a lower visual lane.
    # ============================================================

    driver_x = 23.2

    # ------------------------------------------------------------
    # Physical coherent driver at the far right
    # ------------------------------------------------------------
    ax.plot(
        [driver_x, driver_x],
        [-2.55, 2.45],
        color=structure_color,
        lw=3.0,
        zorder=4
    )

    ax.text(
        driver_x,
        2.62,
        "Coherent Driver",
        fontsize=9.0,
        fontweight='bold',
        ha='center',
        va='bottom',
        color='black',
        bbox=text_bbox,
        zorder=15
    )

    # ------------------------------------------------------------
    # Solid blue outgoing pilot field associated with b_R
    # ------------------------------------------------------------
    bR_x0 = active_barrier_end
    bR_x1 = 22.10
    x_bR = np.linspace(bR_x0, bR_x1, 360)

    y_exit = y_barrier_active[-1]
    slope_exit = np.real(U_prime_act)

    bR_display_lambda = 2.80
    bR_display_amp = slope_exit * bR_display_lambda / (2.0 * np.pi)

    xi_bR_display = x_bR - active_barrier_end
    y_bR = y_exit + bR_display_amp * np.sin(
        2.0 * np.pi * xi_bR_display / bR_display_lambda
    )

    ax.plot(
        x_bR,
        y_bR,
        color=wave_color,
        lw=2.7,
        alpha=0.95,
        zorder=6
    )

    # Clear b_R arrow on the solid pilot-wave branch, upstream of the
    # transmitted knot.
    bR_arrow_x0 = 20.18
    bR_arrow_x1 = 20.58
    bR_arrow_offset = 0.10
    bR_arrow_y0 = np.interp(bR_arrow_x0, x_bR, y_bR) + bR_arrow_offset
    bR_arrow_y1 = np.interp(bR_arrow_x1, x_bR, y_bR) + bR_arrow_offset

    ax.annotate(
        "",
        xy=(bR_arrow_x1, bR_arrow_y1),
        xytext=(bR_arrow_x0, bR_arrow_y0),
        arrowprops=dict(
            arrowstyle='-|>',
            color=wave_color,
            lw=1.7,
            mutation_scale=11,
            shrinkA=0,
            shrinkB=0
        ),
        zorder=12
    )

    ax.text(
        20.42,
        2.58,
        r"Outgoing Field ($b_{\mathrm{R}}$)",
        fontsize=9.1,
        fontweight='bold',
        ha='center',
        va='bottom',
        color='black',
        bbox=text_bbox,
        zorder=15
    )

    # ------------------------------------------------------------
    # Coherent downstream input a_R
    # ------------------------------------------------------------
    # The dashed brown component is the only segmented signal in the
    # right exterior. It starts at the coherent driver and extends
    # leftward for slightly less than one display wavelength.
    aR_x0 = 20.55
    aR_x1 = driver_x
    x_aR = np.linspace(aR_x0, aR_x1, 320)

    aR_center = -1.38
    aR_display_amp = 0.22
    aR_cycles = 0.90
    aR_display_lambda = (aR_x1 - aR_x0) / aR_cycles

    distance_from_driver = driver_x - x_aR
    phase_aR = 2.0 * np.pi * distance_from_driver / aR_display_lambda
    y_aR = aR_center + aR_display_amp * np.sin(phase_aR)

    ax.plot(
        x_aR,
        y_aR,
        color=driver_color,
        lw=2.1,
        alpha=0.98,
        linestyle=(0, (4.0, 3.0)),
        zorder=7
    )

    # ------------------------------------------------------------
    # Left-pointing propagation arrow for a_R
    # ------------------------------------------------------------
    # Keep the arrow visually associated with the dashed input
    # signal, but place it on its own horizontal lane so the arrow
    # shaft and arrowhead never merge with the sinusoidal dashes.
    aR_arrow_x_left = 22.12
    aR_arrow_x_right = 22.66

    # Crest level plus a small publication-spacing offset
    aR_arrow_y = aR_center + aR_display_amp + 0.10

    ax.annotate(
        "",
        xy=(aR_arrow_x_left, aR_arrow_y),
        xytext=(aR_arrow_x_right, aR_arrow_y),
        arrowprops=dict(
            arrowstyle='-|>',
            color=driver_color,
            lw=1.6,
            mutation_scale=11,
            shrinkA=0,
            shrinkB=0
        ),
        zorder=12
    )

    ax.text(
        21.98,
        -0.78,
        "Coherent Downstream Input\n" + r"($a_{\mathrm{R}}$)",
        fontsize=8.9,
        fontweight='bold',
        ha='center',
        va='bottom',
        color='black',
        bbox=text_bbox,
        zorder=15
    )

    # ============================================================
    # TOPOLOGICAL KNOTS
    # ============================================================

    # Incident knot: embedded directly in the incident blue pilot field
    active_knot_x = 14.8
    xi_knot_act = active_knot_x - active_barrier_start
    active_knot_y = np.real(
        a_L_act * np.exp(1j * k * xi_knot_act)
    )

    draw_topological_knot(
        active_knot_x,
        active_knot_y,
        label=""
    )

    ax.text(
        active_knot_x - 0.05,
        active_knot_y - 0.62,
        "Topological Knot\n(Incident State)",
        fontsize=9.0,
        fontweight='bold',
        ha='center',
        va='top',
        color='black',
        bbox=text_bbox,
        zorder=15
    )

    # Transmitted knot: must sit on the outgoing blue pilot field
    active_knot_x2 = 21.08
    active_knot_y2 = np.interp(active_knot_x2, x_bR, y_bR)

    draw_topological_knot(
        active_knot_x2,
        active_knot_y2,
        label=""
    )

    # Small right-pointing red arrow beside the knot indicates knot transport
    ax.annotate(
        "",
        xy=(active_knot_x2 + 0.72, active_knot_y2),
        xytext=(active_knot_x2 + 0.31, active_knot_y2),
        arrowprops=dict(
            arrowstyle='-|>',
            color=matter_color,
            lw=1.5,
            mutation_scale=11
        ),
        zorder=12
    )

    ax.text(
        active_knot_x2,
        active_knot_y2 - 0.66,
        "Transmitted Knot State",
        fontsize=9.1,
        fontweight='bold',
        ha='center',
        va='top',
        color='black',
        bbox=text_bbox,
        zorder=15
    )

    # ============================================================
    # LABELS AND INTERFACE CONDITIONS
    # ============================================================

    # Incident input direction encoded inside the label
    ax.text(
        14.72,
        3.12,
        r"Incident Input ($a_{\mathrm{L}}\rightarrow$)",
        fontsize=9.8,
        fontweight='bold',
        ha='center',
        va='bottom',
        color='black',
        bbox=text_bbox,
        zorder=15
    )

    # Incident-side reflection cancellation
    reflection_y = -2.43

    ax.text(
        15.20,
        -2.78,
        "Incident-Side Reflection Cancelled\n" + r"($b_{\mathrm{L}}=0$)",
        fontsize=8.8,
        fontweight='bold',
        ha='center',
        va='top',
        color='black',
        bbox=text_bbox,
        zorder=15
    )

    ax.annotate(
        "",
        xy=(active_barrier_start, reflection_y),
        xytext=(15.72, reflection_y),
        arrowprops=dict(
            arrowstyle='-|>',
            color='black',
            lw=1.05,
            mutation_scale=9
        ),
        zorder=11
    )

    # Barrier field label retained
    ax.text(
        18.05,
        -1.02,
        "Coherently Driven\nEvanescent Barrier Field",
        fontsize=9.3,
        fontweight='bold',
        ha='center',
        va='top',
        color='black',
        bbox=text_bbox,
        zorder=15
    )

    ax.annotate(
        "",
        xy=(18.05, y_barrier_active[175] - 0.18),
        xytext=(18.05, -0.90),
        arrowprops=dict(
            arrowstyle='-|>',
            color=wave_color,
            lw=1.2,
            mutation_scale=10
        ),
        zorder=11
    )

    # Coherent-control condition
    ax.text(
        (active_barrier_start + active_barrier_end) / 2,
        -3.55,
        r"$\frac{a_{\mathrm{R}}}{a_{\mathrm{L}}} = -\frac{r_{\mathrm{B}}}{t_{\mathrm{B}}}$",
        fontsize=12,
        ha='center',
        va='top',
        color='black',
        bbox=text_bbox
    )

    ax.text(
        (active_x0 + active_x1) / 2,
        4.08,
        r"$\mathbf{(b)\ Coherent\ Boundary\ Control}$",
        fontsize=13,
        ha='center',
        va='bottom',
        color='black'
    )

    # ============================================================
    # FINAL FORMATTING & PDF EXPORT
    # ============================================================
    ax.set_xlim(passive_x0 - 0.1, active_x1 + 1.5)
    ax.set_ylim(y_min, y_max)
    plt.tight_layout()

    output_dir = "Figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_filename = os.path.join(
        output_dir,
        "Fig15_PartII_QuantumTunneling.pdf"
    )

    try:
        plt.savefig(
            pdf_filename,
            format='pdf',
            bbox_inches='tight'
        )
        print(f"High-fidelity vector PDF saved to: {pdf_filename}")
    except PermissionError:
        print(f"CRITICAL ERROR: Permission denied. Please close {pdf_filename} before re-running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    plt.show()


if __name__ == "__main__":
    create_quantum_tunneling_visual()