import argparse 
from app.mvg_monitor import Request

def main():
    """Main entry point when using via command line interface. """

    print('started cli')

    parser = argparse.ArgumentParser(description='Retrieving MVG departures and routes.')
    parser.add_argument('station',
                        help='station where the journey begins')
    parser.add_argument('-p', '--product', default='UBAHN', type=str,
                        help='selecting means of transport; usually U-Bahn')
    parser.add_argument('-n', '--num-connections', default=1, type=int,
                        help='showing the next n commutes')

    args = parser.parse_args()

    # TODO: remove for production
    print('hello', args)

    request = Request(station=args.station, product=args.product, n_connections=args.num_connections)
    request.next_departures()
