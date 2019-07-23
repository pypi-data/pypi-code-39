import data
import store
import db
import argparse
from parser import validate_home_arg
from logger import logger


def run(args):
    logger.debug("Starting Netatmo-to-InfluxDB")
    user = args.user

    # Create db if not exist
    db.init_db(clear_db=args.clear_db)

    # Get user home data
    all_homes = data.get_home(user)

    # If --get-home: print home information and exit
    if args.get_home:
        for home_id in all_homes.keys():
            home = all_homes[home_id]
            print(f"\t{home['name']} ({home_id}) has the following rooms:")
            for room in home["rooms"]:
                print(f"\t\t{room['name']} ({room['id']})")
        return

    # Validate home arguments if available
    homes, err = validate_home_arg(args, all_homes)
    if err is not None:
        return

    # Get measurements
    measurements = data.get_measurements(user, homes, args.dry)

    # Prepare custom_tags
    custom_tags = {}
    if args.custom_tags:
        logger.debug("Preparing custom tags")
        try:
            [
                custom_tags.update({tag: value})
                for tag, value in (ct.split(":") for ct in args.custom_tags)
            ]
        except Exception:
            logger.error("Failed unpacking custom tags")

    # Store measurements
    if not args.dry:
        logger.debug("Preparing data for transfer to InfluxDB")
        for home_id, home_data in measurements.items():
            home_name = home_data["name"]
            for room_id, room_values in home_data["rooms"].items():
                room_name = room_values["name"]
                room_data = room_values["data"]
                if len(room_data.keys()) > 0:
                    logger.debug(
                        f"Sending [home] {home_name} [room] {room_name} data to InfluxDB"
                    )
                    store.store_measurements(
                        user,
                        home_id,
                        home_name,
                        room_id,
                        room_name,
                        room_data,
                        custom_tags,
                    )

    else:
        logger.debug("Using --dry, terminating.")


if __name__ == "__main__":
    username = []
    parser = argparse.ArgumentParser(description="Gather thermostat data from Netatmo")

    # User
    parser.add_argument("user", help="User to parse")

    # Arguments
    parser.add_argument(
        "--home",
        action="append",
        nargs="*",
        metavar=("home_id", ["room_id"]),
        help="Homes and rooms to parse.\
            Use format --home {home_id_1} {room_id_1} {room_id2} ...\
                --home {home_id_2} ...",
    )
    parser.add_argument(
        "--custom-tags",
        nargs="*",
        metavar=("tag:value"),
        help="Provide custom tags for InfluxDB.\
            Format: --custom-tags tag:value tag:value",
    )

    # Functional
    parser.add_argument(
        "--get-home", action="store_true", help="Get home and room information"
    )
    parser.add_argument("--all", action="store_true", help="Parse all homes and rooms")
    parser.add_argument(
        "--dry", action="store_true", help="Do a dry-run (don't store in InfluxDB)"
    )
    parser.add_argument(
        "--clear-db",
        action="store_true",
        help="Wipes database from users and import history",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Allows interactive use (ignores all other args)",
    )

    args = parser.parse_args()
    if not args.interactive:
        run(args)
