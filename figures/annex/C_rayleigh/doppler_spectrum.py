import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "font.size": 14,
    "axes.labelsize": 15,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
})

def plot_doppler_spectrum(y_max=3.0):
    # Normalized: nu = f / f_D, S_h(nu) = 1 / (pi * sqrt(1 - nu^2)) for |nu| < 1
    eps = 1e-4
    nu = np.linspace(-1 + eps, 1 - eps, 2000)
    psd = 1 / (np.pi * np.sqrt(1 - nu**2))

    fig, ax = plt.subplots(figsize=(8, 4))

    # PSD curve inside [-f_D, f_D]
    ax.plot(nu, psd, color='black', linewidth=2)

    # Zero regions outside [-f_D, f_D]
    ax.plot([-5/4, -1], [0, 0], color='black', linewidth=2)
    ax.plot([ 1,  5/4], [0, 0], color='black', linewidth=2)

    # Boundary markers at ±f_D
    ax.axvline( 1.0, color='gray', linestyle=':', linewidth=1.1)
    ax.axvline(-1.0, color='gray', linestyle=':', linewidth=1.1)
    ax.axhline( 0.0, color='black', linestyle='-', linewidth=1.1)

    tick_positions = [-1, -3/4, -1/2, -1/4, 0, 1/4, 1/2, 3/4, 1]
    tick_labels = [
        r'$-f_D$',
        r'$-\frac{3}{4}f_D$',
        r'$-\frac{1}{2}f_D$',
        r'$-\frac{1}{4}f_D$',
        r'$0$',
        r'$\frac{1}{4}f_D$',
        r'$\frac{1}{2}f_D$',
        r'$\frac{3}{4}f_D$',
        r'$f_D$',
    ]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)

    ax.set_xlabel(r'$f\,[Hz]$')
    ax.set_ylabel(r'$S_h(f)$')
    ax.set_xlim(-5/4, 5/4)
    ax.set_ylim(0, y_max)
    ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()

    out_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(os.path.join(out_dir, 'doppler_spectrum.png'), dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_doppler_spectrum(y_max=2.5)