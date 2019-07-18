try:
    import click
    import pathlib
    import plx
    import sys

    @click.group(help="Command-line tools for PLX files.")
    def main():
        pass

    @main.command(name="export", help="Split a PLX file into several pieces.")
    @click.argument("file_path", type=click.types.Path(exists=True, readable=True))
    @click.option(
        "--outdir",
        "-d",
        type=click.types.Path(
            exists=True, writable=True, dir_okay=True, file_okay=False
        ),
        help="Output directory. If not specified, defaults to the same directory where the file is.",
        default=None,
    )
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["bin", "json"]),
        default="bin",
        help="Output format.",
    )
    def main_export(file_path, format, outdir):
        if outdir is None:
            outdir = pathlib.Path(file_path).parent
        plx.PlxFile(file_path, export_base_dir=outdir).export_file(format=format)
        return 0

    if __name__ == "__main__":
        sys.exit(main(prog_name=f"python -m {plx.__name__}"))

except ImportError:
    if __name__ == "__main__":
        sys.stderr.write(
            "Error: click is not installed, so the command-line interface is not available."
        )
        sys.exit(1)
