import click
from pyapksigner import config
from pyapksigner.apksigner import launcher 

@click.command()
@click.option('--ks_pass', default='pyapksigner123!')
@click.option('--key_pass', default='pyapksigner123!')
@click.option('--key_alias', default='pyapksigner')
@click.option('--key_path', default='pyapksigner.jks')
@click.option('--sign', is_flag=True)
@click.argument('apk')
def cli(apk: str, sign: bool, key_path: str, key_alias: str, key_pass: str, ks_pass: str):
    if sign:
        if key_path == 'pyapksigner.jks':
            key_path = str(config.ROOT_DIR.joinpath(key_path).resolve())

        launcher(apk, sign, key_path, key_alias, key_pass, ks_pass)

    return

if __name__=="__main__":
    cli()
