"""
rate_region.py

Generates an example figure of the MU-MIMO rate region R and sum-capacity C_sum for two users (K=2), as referenced in the thesis.

The boundary is an asymmetric superellipse (n=3), which gives a smooth strictly-convex shape that is not a quarter-ellipse and for which the sum-capacity point differs from the max-min rate point.

Output: out/rate_region.pdf  and  out/rate_region.png
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Matplotlib LaTeX style 
matplotlib.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "font.size": 11,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

def superellipse_boundary(C1_max, C2_max, n, num_points=4000):
    t      = np.linspace(0, np.pi / 2, num_points)
    r1_bnd = C1_max * np.cos(t) ** (2 / n)
    r2_bnd = C2_max * np.sin(t) ** (2 / n)
    return r1_bnd, r2_bnd

def sum_capacity_point(C1_max, C2_max, n):
    ratio = (C1_max / C2_max) ** (n / (n - 1))
    r2_sc = (ratio**n / C1_max**n + 1.0 / C2_max**n) ** (-1.0 / n)
    r1_sc = ratio * r2_sc
    return r1_sc, r2_sc

def max_min_rate_point(C1_max, C2_max, n):
    r_mm = (C1_max ** (-n) + C2_max ** (-n)) ** (-1 / n)
    return r_mm, r_mm

def plot_rate_region(C1_max, C2_max, n):
    
    # 0. Initialization.
    r1_bnd, r2_bnd = superellipse_boundary(C1_max, C2_max, n)
    r1_sc,  r2_sc  = sum_capacity_point(C1_max, C2_max, n)
    r1_mm,  r2_mm  = max_min_rate_point(C1_max, C2_max, n)
    fig, ax = plt.subplots(figsize=(5, 5))


    # 1. Rate Region

    # fill rate region area
    fill_r1 = np.concatenate([[0], r1_bnd, [0]])
    fill_r2 = np.concatenate([[0], r2_bnd, [0]])
    ax.fill(fill_r1, fill_r2, color="#aed1ef", alpha=0.85, zorder=1)

    # plot rate region boundary
    ax.plot(r1_bnd, r2_bnd, "-", color="#0c365d", linewidth=1.8, zorder=3)

    # label rate region
    cx = np.trapezoid(r1_bnd[::-1] * r2_bnd[::-1], r1_bnd[::-1]) / np.trapezoid(r2_bnd[::-1], r1_bnd[::-1])
    cy = np.trapezoid(r2_bnd[::-1] ** 2 / 2, r1_bnd[::-1]) / np.trapezoid(r2_bnd[::-1], r1_bnd[::-1])
    ax.text(cx, cy, r"$\mathcal{R}$", fontsize=20, color="#1f4e79", ha="center", va="center")


    # 2. Sum Capacity

    # plot sum-capacity point and label
    ax.plot(r1_sc, r2_sc, "o", color="#c0392b", markersize=6, zorder=5)
    ax.text(r1_sc + 0.04, r2_sc - 0.02, r"$C_{\mathrm{sum}}$", fontsize=10, color="#c0392b", ha="left", va="bottom")

    # plot dashed rate indicator lines to axes
    ax.plot([r1_sc, r1_sc], [0,     r2_sc], ":", color="gray", lw=0.9, zorder=1)
    ax.plot([0,     r1_sc], [r2_sc, r2_sc], ":", color="gray", lw=0.9, zorder=1)

    # plot tangent line
    dx_t = (0.3 * C1_max) / np.sqrt(2)
    ax.plot([r1_sc - dx_t, r1_sc + dx_t], [r2_sc + dx_t, r2_sc - dx_t], "--", color="#c0392b", linewidth=1, zorder=4)

    # plot weight vector w
    dx_w  = (0.2 * C1_max) / np.sqrt(2)
    ax.annotate("", xy=(r1_sc + dx_w, r2_sc + dx_w), xytext=(r1_sc, r2_sc), arrowprops=dict(arrowstyle="-|>", lw=1, color="#c0392b"), annotation_clip=False, zorder=6)
    ax.text(r1_sc + dx_w, r2_sc + dx_w, r"$\mathbf{w} = [1,\,1]^{\mathrm{H}}$", color="#c0392b", fontsize=9, ha="left", va="bottom")


    # 3. Max-Min Rate Point

    # plot max-min rate point and label
    ax.plot(r1_mm, r2_mm, "o", color="#c0392b", markersize=6, zorder=5)
    ax.annotate(r"$\max\,\min(r_1, r_2)$", xy=(r1_mm - 0.01, r2_mm - 0.005), xytext=(r1_mm - 0.25*C1_max, r2_mm + 0.2*C2_max), fontsize=10, color="#c0392b", ha="center", va="center", arrowprops=dict(arrowstyle="->", color="#c0392b", lw=0.75, connectionstyle="arc3,rad=0.75"), annotation_clip=False, zorder=6)

    # plot dashed rate indicator lines to axes
    ax.plot([r1_mm, r1_mm], [0,     r2_mm], ":", color="gray", lw=0.9, zorder=1)
    ax.plot([0,     r1_mm], [r2_mm, r2_mm], ":", color="gray", lw=0.9, zorder=1)

    # 4. Plot Formatting
    ax.set_xlabel(r"$r_1$ [bits/channel use]", labelpad=4)
    ax.set_ylabel(r"$r_2$ [bits/channel use]", labelpad=4)
    ax.set_xlim(0, C1_max * 1.2)
    ax.set_xticks([])
    ax.set_ylim(0, C2_max * 1.2)
    ax.set_yticks([])
    ax.set_aspect("equal")
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.annotate("", xy=(C1_max * 1.2, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
    ax.annotate("", xy=(0, C2_max * 1.2), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))

    plt.tight_layout()

    # 5. Save the figure
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir    = os.path.join(script_dir, "out")
    os.makedirs(out_dir, exist_ok=True)

    for fmt in ("pdf", "png"):
        path = os.path.join(out_dir, f"rate_region.{fmt}")
        fig.savefig(path, bbox_inches="tight", dpi=300 if fmt == "png" else None)
        print(f"Saved {path}")
    
    return fig


if __name__ == "__main__":
    fig = plot_rate_region(C1_max=1.3, C2_max=1, n=2.5)