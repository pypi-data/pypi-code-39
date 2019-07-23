from logger import logger


def validate_home_arg(args, homes):
    """
    Validates and parses supplied home details against all known home- and room-objects.
    """
    logger.debug("Validating home args")
    user = args.user
    if args.home and args.all:
        logger.critical("Only use one of the following arguments: --all OR --home ...")
        return None, True

    if not (args.home or args.all):
        logger.critical("Use one of --all or --home ...")
        return None, True

    if args.home:
        arg_homes = {}
        for home in args.home:
            # Home ID provided in the argument
            if len(home) == 0:
                logger.critical(f"No data provided for --home")
                return None, True
            arg_home_id = home[0]
            # Home IDs that are found for the user
            home_ids = homes.keys()
            # Verify if home ID is valid
            if arg_home_id not in home_ids:
                logger.critical(f"Home {arg_home_id} not found for user {user}")
                return None, True

            arg_homes[arg_home_id] = {"name": homes[arg_home_id]["name"], "rooms": []}

            # Room IDs provided in argument
            arg_room_ids = home[1:]
            # Room IDs that are found for the user
            room_ids = [room["id"] for room in homes[arg_home_id]["rooms"]]
            # Verify if room ID is at least a subset of the available room IDs
            if not all(x in room_ids for x in arg_room_ids):
                logger.critical(f"Invalid rooms supplied for user {user}")
                return False

            if len(arg_room_ids) == 0:
                logger.critical(f"No room data provided for --home {arg_home_id}")
                return None, True

            for room in room_ids:
                room_names = [
                    {room["id"]: room["name"]} for room in homes[arg_home_id]["rooms"]
                ]
                arg_homes[arg_home_id]["rooms"].append(
                    {"id": room, "name": room_names[0][room]}
                )
        return arg_homes, None
    logger.debug("Using all homes and rooms")
    return homes, None
