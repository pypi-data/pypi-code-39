import argparse
import sys

from matplotlib import pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg

from dominant_color.kmeans_palette import kmeans_palette
from dominant_color.mediancut_palette import mediancut_palette


def parse_args():
    parser = argparse.ArgumentParser(
        description="Test different color extraction algorithms."
    )
    parser.add_argument("image")
    subparsers = parser.add_subparsers(help="Algorithms")
    kmeans = subparsers.add_parser("kmeans", help="Using K-Means clustering")
    kmeans.add_argument(
        "--bins", help="Work on this given number of color bins", type=int, default=5
    )
    kmeans.add_argument(
        "--workimage-width",
        help="Work on an reduced image of the given width",
        default=150,
    )
    kmeans.add_argument(
        "--workimage-height",
        help="Work on an reduced image of the given height",
        default=150,
    )
    kmeans.set_defaults(algo=kmeans_palette)
    mediancut = subparsers.add_parser(
        "mediancut", help="Using a median cut quantization"
    )
    mediancut.add_argument(
        "--bins", help="Work on this given number of color bins", type=int, default=5
    )
    mediancut.add_argument(
        "--quality",
        help="Only use 1/quality pixels. (1 means use every pixels)",
        type=int,
        default=10,
    )
    mediancut.set_defaults(algo=mediancut_palette)
    args = parser.parse_args()
    if not hasattr(args, 'algo'):
        parser.print_help()
        exit(1)
    return args


def full_extent(ax, pad=0.0):
    """Get the full extent of an axes, including axes labels, tick labels, and
    titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    # are undefined.
    ax.figure.canvas.draw()
    items = ax.get_xticklabels() + ax.get_yticklabels()
    items += [ax, ax.title]
    bbox = Bbox.union([item.get_window_extent() for item in items])
    return bbox.expanded(1.0 + pad, 1.0 + pad)


def display_palette(image_path, palette):
    r, g, b = palette[0][1]
    color = (r/255, g/255, b/255)
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)
    extent = full_extent(ax)
    extent = extent.transformed(fig.transFigure.inverted())
    rect = Rectangle([extent.xmin, extent.ymin], extent.width, extent.height,
                     facecolor=color, edgecolor='none', zorder=-1,
                     transform=fig.transFigure)
    fig.patches.append(rect)
    ax.imshow(mpimg.imread(image_path))
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax = fig.add_subplot(2, 1, 2)
    ax.set_title(' '.join(sys.argv[2:]))
    ax.bar(
        range(len(palette)),
        [pct for pct, color in palette],
        color=[(r / 255, g / 255, b / 255) for pct, (r, g, b) in palette],
    )
    ax.set_ylabel("percent")
    ax.set_xlabel("color")
    plt.show()


def main():
    args = vars(parse_args())
    display_palette(args["image"], args.pop("algo")(**args))


if __name__ == "__main__":
    main()
