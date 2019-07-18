import argparse 
from mvg_monitor.monitor import Request


def main():
    """Main entry point when using via command line interface. """

    parser = argparse.ArgumentParser(description='Retrieving MVG departures and routes.')
    parser.add_argument('station',
                        help='station where the journey begins')
    parser.add_argument('-p', '--product', default='UBAHN', type=str,
                        help='selecting means of transport; usually U-Bahn')
    parser.add_argument('-n', '--num-connections', default=1, type=int,
                        help='showing the next n commutes')
    parser.add_argument('--debug', action='store_true',
                        help='printing provided args for debugging')

    args = parser.parse_args()

    if args.debug == 1:
        print('provided arguments: ', args)

    request = Request(station=args.station, product=args.product, n_connections=args.num_connections)
    request.next_departures()


if __name__ == '__main__':
    main()
