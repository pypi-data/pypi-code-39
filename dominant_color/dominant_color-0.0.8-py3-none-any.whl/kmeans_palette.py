from PIL import Image
from collections import Counter
import numpy as np
import scipy
import scipy.misc
import scipy.cluster


def kmeans_palette(image, bins=5, workimage_width=150, workimage_height=150):
    im = Image.open(image).convert("RGB")
    im = im.resize((workimage_width, workimage_height))
    ar = np.asarray(im)
    shape = ar.shape

    # Flatten as a list of pixels
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    # Finding clusters
    codebook, _ = scipy.cluster.vq.kmeans(ar, bins)
    # codebook contain 5 middle of bins, as [r, g, b]
    code, _ = scipy.cluster.vq.vq(ar, codebook)
    # code contains bin ids of each pixel
    counts = Counter(code)
    palette = sorted(
        [
            (100 * counts[i] / (workimage_width * workimage_height), list(codebook[i]))
            for i in range(len(codebook))
            if not (
                codebook[i][0] > 250 and codebook[i][1] > 250 and codebook[i][2] > 250
            )
        ],
        reverse=True,
    )
    return palette
