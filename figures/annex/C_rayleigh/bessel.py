
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.special import j0
from scipy.optimize import brentq
 
matplotlib.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "font.size": 14,
    "axes.labelsize": 15,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
})

def plot_acf(num_Tc=5, ticks_sep=1):
    
    # Find x0 such that J0(x0) = 0.5 (i.e. 2*pi*f_D*T_c)
    x0 = brentq(lambda x: j0(x) - 0.5, 1.0, 2.0)  # x0 ≈ 1.5196

    # Normalized time axis u = tau / T_c
    u = np.linspace(-num_Tc, num_Tc, 500)
    acf = j0(x0 * u)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(u, acf, color='black', linewidth=2)
    ax.axhline(0.5, color='gray', linestyle='--', linewidth=1.1)
    ax.axhline(0.0, color='black', linestyle='-', linewidth=1.1)
    ax.axvline( 1.0, color='gray', linestyle=':', linewidth=1.1)
    ax.axvline(-1.0, color='gray', linestyle=':', linewidth=1.1)

    # Tick labels in units of T_c
    ticks = np.arange(-num_Tc, num_Tc + 1)
    labels = ['' for _ in ticks]
    for i, t in enumerate(ticks[::ticks_sep]):
        if   t ==  0: labels[i * ticks_sep] = r'$0$'
        elif t ==  1: labels[i * ticks_sep] = r'$T_c$'
        elif t == -1: labels[i * ticks_sep] = r'$-T_c$'
        else:         labels[i * ticks_sep] = rf'${t}T_c$'
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)

    ax.set_xlabel(r'$\tau [s]$')
    ax.set_ylabel(r'$R_h(\tau)$')
    ax.set_xlim(-num_Tc, num_Tc)
    ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()

    out_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(os.path.join(out_dir, f'acf_jakes_model_{num_Tc}.png'), dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_acf(num_Tc=4)
    plot_acf(num_Tc=25, ticks_sep=5)
