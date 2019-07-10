"""
Command line module for batch processing
"""
import click

import logging
logger = logging.getLogger(__name__)

from .utils import parse_fid


@click.command("drift", help="Perform batch drift operation. ")
@click.argument("folder-id", nargs=1, required=True)
@click.option("--verbose", "-v", help="Increase the verbosity", count=True)
@click.option("--norm-id", "-norm", help="ID of the normalisation image")
@click.option("--save-xmcd/--no-save-xmcd",
              help="Save XMCD image or not, default: true",
              default=True)
@click.option("--save-drift/--no-save-drift",
              help="Save drifted images or not, default: true",
              default=True)
@click.option(
    "--save-edge/--no-save-edge",
    help=
    "Save the edge images or not. This may slow down the process and has steep memory requirements",
    default=False)
@click.option("--drift-folder-name",
              help="Name of the folder used for saving the drift images",
              default="drift")
@click.option("--xmcd-folder-name",
              help="Name of the folder used for saving the drift images",
              default="xmcd")
@click.option(
    "--folder-suffix",
    help=
    "Suffix of the image folder name <ID>_<SUFFIX>. Default is to determine it automatically",
    default=None)
@click.option("--nprocs",
              "-np",
              help="Number of processes in parallel",
              type=int,
              default=2)
@click.option("--review/--no-review",
              help='Review the first drift or not',
              default=False)
@click.option(
    "--sigma",
    type=float,
    default=4,
    help=
    'Sigma of gaussian filter to suppress stational spots from the instrument')
@click.pass_context
def drift(ctx, folder_id, verbose, norm_id, save_xmcd, save_drift,
          drift_folder_name, xmcd_folder_name, folder_suffix, nprocs,
          save_edge, review, sigma):
    """
    Perform drift correction and save XMCD signals
    """
    from peempy.fileproc import get_normalisation, FolderProcesser
    import peempy.imageproc as imageproc
    import re

    if verbose:
        imageproc.set_logging(logging.DEBUG)
        logger.setLevel(logging.INFO)

    ppath = ctx.obj["ppath"]

    # Determine the folder suffix automatically
    if folder_suffix is None:
        suffixes = []
        for folder in ppath.basedir.glob("*_*"):
            match = re.match(r"\d+_(\w+Image)", folder.name)
            if match:
                suffixes.append(match.group(1))
        suffixes = set(suffixes)
        assert len(suffixes) == 1, "More than one suffix found: " +\
            ",".join(suffixes)
        folder_suffix = suffixes.pop()
        if verbose:
            click.echo("Automatic suffix: " + folder_suffix)

    # Extract the normalisation image
    if norm_id is not None:
        normfolder = ppath.basedir / "{}_{}".format(norm_id, folder_suffix)
        norm = get_normalisation(fdname=normfolder, save=False)
    else:
        import numpy as np
        norm = np.array(1)

    parsed_ids = parse_fid(folder_id)
    folders = filter_fids(ppath, parsed_ids, folder_suffix)
    if len(folders) == 0:
        click.echo("No captures found for the given ID '{}'".format(folder_id))
        raise click.exceptions.Abort()

    if verbose:
        click.echo("Capture IDs: " + ", ".join(map(str, folders)))
        click.echo("Processing {} captures, starting from {}".format(
            len(folders), folders[0]))

    # Setup the folder processor
    processor = FolderProcesser(folders, norm, mask_ratio=0.93, peempath=ppath)

    processor.DATASUFFIX = folder_suffix
    processor.SAVESUFFIX = folder_suffix
    processor.nprocs = nprocs
    # Disable threading if using multiple processes
    if nprocs > 1:
        processor.nthreads = 1
    processor.save_xmcd = save_xmcd
    processor.save_drifted = save_drift
    processor.save_edge = save_edge
    processor.review_first_frame = review
    processor.drift_sigma = sigma

    processor.adjust_crop()
    processor.process_all()


def filter_fids(ppath, ids, suffix, fcount=40):
    """
    Scan a list of folder ids, exclude those not valid
    """
    res = []
    for id_str in ids:

        fpath = ppath.basedir / "{}_{}".format(id_str, suffix)
        if not fpath.is_dir():
            continue
        # check the number of tif files
        tifs = list(fpath.glob('*.tif'))
        if len(tifs) != fcount:
            continue
        else:
            res.append(id_str)
    return res


@click.command("view-drift", help="view the drift corrected images")
@click.argument("capture_id", type=int)
@click.option("--folder_suffix", default='PCOImage')
@click.pass_context
def view_drift(ctx, capture_id, folder_suffix):
    from peempy.imageproc import load_image_set, XMCDImageSeries, show_images_series
    ppath = ctx.obj["ppath"]

    fpath = (ppath.driftdir /
             "{}_{}".format(capture_id, folder_suffix)).as_posix()
    frames = load_image_set(fpath)
    show_images_series(frames)
