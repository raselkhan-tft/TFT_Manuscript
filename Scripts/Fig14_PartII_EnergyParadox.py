import numpy as np # Selected for efficient array generation and mathematical transformations
import matplotlib.pyplot as plt # Selected for publication-grade 2D schematic layout and native LaTeX rendering
import os # Selected for robust directory management and path-specific file saving


def create_energy_paradox_visual():
    # Enforce strict serif typography (Computer Modern) for PRL-style aesthetics
    plt.rcParams.update({
        'savefig.pad_inches': 0.1,
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'cm',
        'font.size': 11
    })

    # Setup Figure (Minimalist Architectural Styling)
    charcoal = '#1A1A1A'
    navy = '#000080'
    maroon = '#800000'
    brick_red = '#B22222'
    light_gray = '#D9D9D9'
    medium_gray = '#BDBDBD'

    fig, ax = plt.subplots(figsize=(14, 9), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # X Domain for wave propagation
    x = np.linspace(0, 4 * np.pi, 1000)

    # =======================================================
    # 1. TOP HALF: THE COUNTER-PROPAGATING WAVE DOMAIN
    # =======================================================
    y_center_top = 3.1

    # Counter-propagating wave snapshot
    #
    # A1(x,t) = A0 sin(x - phase)
    # A2(x,t) = A0 sin(x + phase)
    #
    # At x = 2*pi:
    # A1 = -A2
    # A = A1 + A2 = 0
    # dA/dt = 0
    #
    # Thus the marked location is a stationary displacement node.
    wave_amplitude = 0.85
    phase_snapshot = 0.55

    wave_a_disp = wave_amplitude * np.sin(x - phase_snapshot)
    wave_b_disp = wave_amplitude * np.sin(x + phase_snapshot)

    wave_a = y_center_top + wave_a_disp
    wave_b = y_center_top + wave_b_disp

    # Plot the two counter-propagating component waves
    ax.plot(
        x,
        wave_a,
        color=navy,
        lw=2.2,
        alpha=0.95,
        zorder=3
    )

    ax.plot(
        x,
        wave_b,
        color=maroon,
        lw=2.2,
        alpha=0.95,
        zorder=3
    )

    # Zero-displacement reference line
    ax.axhline(
        y_center_top,
        color='#9A9A9A',
        lw=1.2,
        ls=':',
        alpha=0.8,
        zorder=1
    )

    # Stationary interference node
    cancel_x = 2 * np.pi

    ax.scatter(
        [cancel_x],
        [y_center_top],
        s=60,
        facecolor='white',
        edgecolor=charcoal,
        linewidth=1.8,
        zorder=8
    )

    # -------------------------------------------------------
    # Wave A label and propagation direction
    # -------------------------------------------------------
    ax.text(
        0.55,
        4.72,
        "Wave A",
        color=charcoal,
        fontweight='bold',
        ha='left',
        fontsize=12
    )

    ax.text(
        1.58,
        4.72,
        r"$A_1(x,t)$",
        color=charcoal,
        ha='left',
        fontsize=12
    )

    ax.annotate(
        "",
        xy=(2.95, 4.38),
        xytext=(1.85, 4.38),
        arrowprops=dict(
            arrowstyle="->",
            color=navy,
            lw=2.1
        )
    )

    ax.text(
        2.40,
        4.50,
        r"$+x$",
        color=navy,
        fontsize=10,
        fontweight='bold',
        ha='center'
    )

    # -------------------------------------------------------
    # Wave B label and propagation direction
    # -------------------------------------------------------
    ax.text(
        0.55,
        1.48,
        "Wave B",
        color=charcoal,
        fontweight='bold',
        ha='left',
        fontsize=12
    )

    ax.text(
        1.58,
        1.48,
        r"$A_2(x,t)$",
        color=charcoal,
        ha='left',
        fontsize=12
    )

    ax.annotate(
        "",
        xy=(1.85, 1.82),
        xytext=(2.95, 1.82),
        arrowprops=dict(
            arrowstyle="->",
            color=maroon,
            lw=2.1
        )
    )

    ax.text(
        2.40,
        1.60,
        r"$-x$",
        color=maroon,
        fontsize=10,
        fontweight='bold',
        ha='center'
    )

    # -------------------------------------------------------
    # Stationary interference node label
    # Moved upward with a short leader arrow
    # -------------------------------------------------------
    stationary_label_x = cancel_x + 0.10
    stationary_label_y = 4.68

    ax.text(
        stationary_label_x,
        stationary_label_y,
        "Stationary Interference Node\n"
        r"$A=0,\ \dot{A}=0$",
        color=charcoal,
        fontsize=12,
        fontweight='bold',
        ha='center',
        va='top',
        zorder=9
    )

    # Short leader arrow: starts below the math and ends at the node
    ax.annotate(
        "",
        xy=(cancel_x, y_center_top + 0.03),
        xytext=(stationary_label_x - 0.12, stationary_label_y - 0.52),
        arrowprops=dict(
            arrowstyle="->",
            color=charcoal,
            lw=1.4
        ),
        zorder=7
    )

    # =======================================================
    # 2. BOTTOM HALF: MICROSCOPIC ELASTIC SCAFFOLD
    # =======================================================

    # Grid Parameters
    num_x_nodes = 37
    x_nodes = np.linspace(0, 4 * np.pi, num_x_nodes)
    y_base_levels = np.linspace(-4.45, 0.35, 6)

    # Resultant displacement sampled at lattice columns
    node_disp_a = wave_amplitude * np.sin(x_nodes - phase_snapshot)
    node_disp_b = wave_amplitude * np.sin(x_nodes + phase_snapshot)
    node_disp_net = node_disp_a + node_disp_b

    # Visual scaling for the microscopic scaffold
    max_disp = np.max(np.abs(node_disp_net))
    if max_disp == 0:
        max_disp = 1.0

    lattice_disp = 0.42 * node_disp_net / max_disp

    # Neighbor-to-neighbor shear intensity
    local_shear = np.abs(np.diff(lattice_disp))

    max_shear = np.max(local_shear)
    if max_shear == 0:
        max_shear = 1.0

    local_shear = local_shear / max_shear

    # -------------------------------------------------------
    # Draw vertical scaffold columns
    # -------------------------------------------------------
    for j, xv in enumerate(x_nodes):
        y_nodes = y_base_levels + lattice_disp[j]

        ax.plot(
            np.full(len(y_nodes), xv),
            y_nodes,
            color=light_gray,
            lw=1.1,
            zorder=1
        )

        ax.scatter(
            np.full(len(y_nodes), xv),
            y_nodes,
            color='#333333',
            s=12,
            zorder=4
        )

    # -------------------------------------------------------
    # Draw horizontal / sheared contact bonds
    # -------------------------------------------------------
    for yb in y_base_levels:
        for j in range(num_x_nodes - 1):
            x1 = x_nodes[j]
            x2 = x_nodes[j + 1]

            y1 = yb + lattice_disp[j]
            y2 = yb + lattice_disp[j + 1]

            # Baseline elastic bond
            ax.plot(
                [x1, x2],
                [y1, y2],
                color=medium_gray,
                lw=1.2,
                zorder=2
            )

            # Highlight strained contacts
            if local_shear[j] > 0.18:
                ax.plot(
                    [x1, x2],
                    [y1, y2],
                    color=brick_red,
                    lw=1.5 + 2.2 * local_shear[j],
                    alpha=0.22 + 0.62 * local_shear[j],
                    zorder=3
                )

    # =======================================================
    # 3. MACRO-TO-MICRO CORRESPONDENCE
    # =======================================================

    # Vertical dashed arrow maps the stationary macroscopic node
    # to the microscopic strained-contact region below.
    ax.annotate(
        "",
        xy=(cancel_x, 0.15),
        xytext=(cancel_x, 2.60),
        arrowprops=dict(
            arrowstyle="->",
            color="#555555",
            lw=2.5,
            linestyle="--"
        ),
        zorder=5
    )

    # -------------------------------------------------------
    # Elastic Energy Storage label
    #
    # Kept immediately beside the vertical correspondence arrow.
    # The arrow itself points into the strained microscopic region,
    # so no second leader arrow is needed.
    # -------------------------------------------------------
    energy_label_x = cancel_x + 0.20
    energy_label_y = 1.45

    ax.text(
        energy_label_x,
        energy_label_y,
        "Elastic Energy Storage\n"
        r"$E_{\mathrm{kin}}=0,\quad E_{\mathrm{el}}>0$",
        color=charcoal,
        fontsize=11.5,
        fontweight='bold',
        ha='left',
        va='center',
        bbox=dict(
            facecolor='white',
            edgecolor='none',
            alpha=0.96,
            pad=4.5
        ),
        zorder=10
    )

    # =======================================================
    # 4. STYLING & FORMATTING
    # =======================================================
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_xlim(
        -0.5,
        4 * np.pi + 0.5
    )

    ax.set_ylim(
        -5.35,
        5.2
    )

    # =======================================================
    # FINAL RENDER & PDF EXPORT
    # =======================================================
    plt.tight_layout()

    output_dir = "Figures"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_filename = os.path.join(
        output_dir,
        "Fig14_PartII_EnergyParadox.pdf"
    )

    try:
        plt.savefig(
            pdf_filename,
            format='pdf',
            bbox_inches='tight'
        )

        print(
            f"High-fidelity vector PDF saved to: "
            f"{pdf_filename}"
        )

    except PermissionError:
        print(
            f"CRITICAL ERROR: Permission denied. "
            f"Please close {pdf_filename} before re-running."
        )

    except Exception as e:
        print(
            f"An unexpected error occurred: {e}"
        )

    plt.show()


if __name__ == "__main__":
    create_energy_paradox_visual()