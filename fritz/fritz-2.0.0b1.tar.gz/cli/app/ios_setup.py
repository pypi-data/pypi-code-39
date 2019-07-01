"""
This module contains the code for setting up an iOS app.
"""
import os
import glob
import plistlib
import click
from pbxproj import XcodeProject
import fritz
from cli import print_utils
from cli import file_utils


def build_plist_data(api_key):
    """Builds data to insert into Fritz-Info.plist file.

    Args:
        api_key (str): API Key

    Returns: Dictionary of data.
    """
    return {
        "namespace": "production",
        "apiUrl": "https://api.fritz.ai/sdk/v1",
        "apiKey": api_key,
    }


def get_app_details():
    """Get details of app in current directory. """
    product_bundle_line = os.popen(
        "xcodebuild -showBuildSettings | grep PRODUCT_BUNDLE_IDENTIFIER"
    ).read()
    product_name_line = os.popen(
        "xcodebuild -showBuildSettings | grep PRODUCT_NAME | "
        'grep -Fv "FULL_PRODUCT_NAME"'
    ).read()

    bundle_id = (
        product_bundle_line.split("=")[1].strip()
        if product_bundle_line
        else None
    )
    product_name = (
        product_name_line.split("=")[1].strip() if product_name_line else None
    )

    info_files = list(file_utils.find_all("Fritz-Info.plist"))
    if len(info_files) > 1:
        raise Exception("Found multiple Fritz-Info.plist files")

    if not info_files:
        return bundle_id, product_name, None

    plist = read_plist(info_files[0]) or {}
    if "apiKey" in plist:
        return bundle_id, product_name, plist["apiKey"]

    return bundle_id, product_name, None


def get_app_info():
    """Get all details of current app, including Fritz objects.

    Returns: dict of information.
    """
    apk_id, product_name, app_api_key = get_app_details()
    app = None
    if app_api_key:
        apps = fritz.App.list(
            apk_id=apk_id,
            platform="ios",
            app_api_key=app_api_key,
            all_projects=True,
        )
        if len(apps) > 1:
            print_utils.warn("Found more than one app, taking first")

        if apps:
            app = apps[0]
    else:
        apps = fritz.App.list(apk_id=apk_id, platform="ios", all_projects=True)
        if len(apps) > 1:
            print_utils.warn("Found more than one app, taking first")
        if apps:
            app = apps[0]

    project = fritz.Project.get()
    if app and app.project_uid != project.id:
        project = fritz.Project.get(app.project_uid)

    xcode_projs = [
        path for path in glob.glob("*.xcodeproj") if "Pods" not in path
    ]

    xcode_path = xcode_projs[0] if xcode_projs else None
    app_delegate = file_utils.find("AppDelegate.swift")
    fritz_info = file_utils.find("Fritz-Info.plist")

    return {
        "apk_id": apk_id,
        "app": app,
        "api_key": app_api_key,
        "app_name": product_name,
        "target": product_name,
        "project": project,
        "xcode_project_file": xcode_path,
        "app_delegate": app_delegate,
        "fritz_info_path": fritz_info,
    }


def summarize(app_info):
    """Summarize app info.

    Args:
        app_info (dict): Dictionary of current app info.
    """
    print_utils.title("Details of current app")
    print_utils.header("Xcode Configuration")
    print_utils.field("Bundle ID", app_info["apk_id"])
    print_utils.field("Project File", app_info["xcode_project_file"])
    print_utils.field("Target", app_info["target"])
    print_utils.field("AppDelegate Path", app_info["app_delegate"])
    print_utils.field("Path to Fritz-Info", app_info["fritz_info_path"])
    print_utils.field("API Key", app_info["api_key"])
    if app_info["app"]:
        print_utils.ack("\nApp exists with same API Key and Bundle ID\n")
        app_info["app"].summary()


def app_prompt(message, default):
    """Prompt to enter information.

    Args:
        message (str): Message to display.
        default (object): Default value.

    Returns: Formatted click prompt.
    """
    return click.prompt(
        "Please enter " + message, default=default or None, show_default=True
    )


def configure_app_files(app_info):
    """Enter desired configuration for app.

    Args:
        app_info (dict): App Info.

    Returns: updated app_info.
    """
    app_name = app_prompt("the name of your app", app_info["app_name"])
    apk_id = app_prompt("the Bundle ID for your app", app_info["apk_id"])
    xcode_path = app_info["xcode_project_file"]
    app_delegate = app_info["app_delegate"]
    xcode_path = app_prompt("the location of your .xcodeproj/ ", xcode_path)
    app_delegate = app_prompt("the location of your AppDelegate", app_delegate)
    fritz_info = app_info["fritz_info_path"]
    if fritz_info:
        print_utils.message("Found Fritz-Info.plist file at " + fritz_info)
    else:
        target = app_info["target"]
        fritz_info = app_prompt(
            "the location of your Fritz-Info.plist",
            "./{target}/Fritz-Info.plist".format(target=target),
        )

    app_info["app_name"] = app_name
    app_info["apk_id"] = apk_id
    app_info["app_delegate"] = app_delegate
    app_info["fritz_info_path"] = fritz_info
    app_info["xcode_project_file"] = xcode_path
    return app_info


def create_app(details):
    """Create fritz app from details.

    Args:
        details (dict): App info.

    Returns: Created Fritz app.
    """
    return fritz.App.create(
        app_name=details["app_name"],
        apk_id=details["apk_id"],
        platform="ios",
        project_id=details["project"].id,
    )


def read_plist(plist_path):
    """Read plist file.

    Args:
        plist_path (str): Path to plist.

    Returns: Dict if exists and is readable, None if error encountered.
    """
    try:
        # TODO: Replace with non-deprecated method.
        # pylint: disable=deprecated-method
        plist = plistlib.readPlist(plist_path)
        return plist
    # pylint: disable=broad-except
    except (plistlib.InvalidFileException, Exception):
        print_utils.warn(
            "{plist_path} does not exist".format(plist_path=plist_path)
        )
        return None


def update_plist(details):
    """Update plist with details.

    Args:
        details (dict): App info.
    """
    plist_path = details["fritz_info_path"]
    plist = read_plist(plist_path)
    if not plist:
        plist = build_plist_data(details["app"].api_key)
        # TODO: Replace with non-deprecated method.
        # pylint: disable=deprecated-method
        plistlib.writePlist(plist, plist_path)
        return

    plist["apiKey"] = details["app"].api_key
    # TODO: Replace with non-deprecated method.
    # pylint: disable=deprecated-method
    plistlib.writePlist(plist, plist_path)


def add_plist_to_xcodeproj(app_info):
    """Add plist file to xcode project.

    Args:
        app_info (dict): App info.
    """
    project_file = "{xcode_proj_file}/project.pbxproj".format(
        xcode_proj_file=app_info["xcode_project_file"]
    )
    project = XcodeProject.load(project_file)
    if project.get_files_by_name("Fritz-Info.plist"):
        print_utils.ack("Fritz-Info.plist already in project, not adding")
        return

    fritz_info_path = app_info["fritz_info_path"]
    split_info = fritz_info_path.split("/")
    if len(split_info) < 2:
        print_utils.ack("No group for file, adding to root")
        project.add_file(fritz_info_path)
        project.save()
        return

    parent_group = split_info[-2]
    groups = project.get_groups_by_name(parent_group)
    if not groups:
        print_utils.ack("No group exists, just adding")
        project.add_file(fritz_info_path)
        project.save()
        return

    project.add_file(fritz_info_path, parent=groups[0])
    project.save()


def add_configure_to_app_delegate(app_info):
    """Add Fritz configure line to app delegate.

    Args:
        app_info (dict): App info.
    """
    app_delegate = app_info["app_delegate"]
    with open(app_delegate) as f:
        lines = f.readlines()

    if file_utils.find_text_in_file("FritzCore.configure", app_delegate):
        print_utils.ack("App Delegate already contains configure, returning.")
        return

    delegate_function_hint = "didFinishLaunchingWithOptions"
    found_function = False
    in_function = False
    output_lines = []
    func_index = None
    configure_added = False
    previous_line_had_import = False
    added_import = False
    for line in lines:
        if (
            not added_import
            and previous_line_had_import
            and "import" not in line
        ):
            output_lines.append("import Fritz\n")
            added_import = True

        output_lines.append(line)

        if line.lstrip().startswith("import"):
            previous_line_had_import = True

        if delegate_function_hint in line:
            found_function = True
            func_index = line.find("func")

        # Searching for start of function
        if found_function and not in_function:
            if "{" in line:
                in_function = True
            continue

        if in_function and "}" in line:
            in_function = False
            continue

        if not in_function:
            continue

        if in_function and not configure_added:
            # Adding FritCore.configure
            message = "// Automatically added FritzCore configure."
            output_lines.append(" " * (func_index + 4) + message + "\n")
            output_lines.append(
                " " * (func_index + 4) + "FritzCore.configure()\n"
            )
            configure_added = True

    with open(app_info["app_delegate"], "w") as f:
        f.write("".join(output_lines))


def add_fritz_to_pod(podfile_path, app_info):
    """Add Fritz to podfile if it's not there.

    Args:
        podfile_path (str): Path to podfile.
        app_info (dict): App info.
    """
    podfile_path = app_info["podfile"]
    target = app_info["target"]
    default_target_line = "# Pods for {target}".format(target=target)
    line = file_utils.find_line_search_term(podfile_path, default_target_line)
    if not line:
        pod_target_line = "target '{target}'".format(target=target)
        line = file_utils.find_line_search_term(podfile_path, pod_target_line)
        if not line:
            print_utils.warn("Could not find target")
            return

    fritz_install_line = "  pod 'Fritz'\n"
    file_utils.insert_code_after_line(podfile_path, line, fritz_install_line)


def _add_file_to_project(project, filename):
    split_info = filename.split("/")
    if len(split_info) < 2:
        print_utils.ack("No group for file, adding to root")
        project.add_file(filename)
        project.save()
        return

    parent_group = split_info[-2]
    groups = project.get_groups_by_name(parent_group)
    if not groups:
        print_utils.ack("No group exists, just adding")
        project.add_file(filename)
        project.save()
        return

    project.add_file(filename, parent=groups[0])
    project.save()


def add_podfile(app_info):
    """Configure Podfile with Fritz, adding if doesn't exist.

    Args:
        app_info (dict): App info.
    """
    podfile = file_utils.find("Podfile")
    if not podfile:
        print_utils.ack("Did not find podfile, creating file")
        os.system("pod init")
        podfile = file_utils.find("Podfile")

    app_info["podfile"] = podfile

    if file_utils.is_text_in_file("pod 'Fritz", podfile):
        print_utils.ack("Fritz is already in podfile")
        return

    add_fritz_to_pod(podfile, app_info)


def is_app_setup(app_info):
    """Checks to see if app is setup with Fritz.

    Args:
        app_info (dict): App info.

    Returns: True if setup, False otherwise.
    """
    app_delegate = app_info["app_delegate"]
    app_delegate_has_fritz = file_utils.find_text_in_file(
        "FritzCore.configure", app_delegate
    )

    if (  # pylint: disable=too-many-boolean-expressions
        app_info["apk_id"]
        and app_info["xcode_project_file"]
        and app_delegate_has_fritz
        and app_info["fritz_info_path"]
        and app_info["target"]
        and app_info["app"]
    ):
        return True

    return False


def setup_ios_app():
    """Setup an iOS App."""

    details = get_app_info()
    summarize(details)

    if is_app_setup(details):
        result = click.confirm(
            "App is already setup. Would you like to continue?", default=True
        )
        if not result:
            return

    if details["api_key"] and not details["app"]:
        print_utils.warn(
            "API Key discovered but no app created. "
            "App creation will attempt to use this API key."
        )

    if click.confirm("Would you like to modify any details?"):
        details = configure_app_files(details)
        click.confirm("Are these details correct?", default=True)

    if not details["app"]:
        app = create_app(details)
        if app:
            details["app"] = app
            details["apk_id"] = app.apk_id
            details["app_name"] = app.app_name
        print_utils.ack("Successfully created " + app.app_name)

    print_utils.message(
        "Now we will modify your App files to connect to Fritz"
    )
    click.confirm("Would you like to continue?", default=True)

    update_plist(details)
    add_plist_to_xcodeproj(details)
    add_configure_to_app_delegate(details)
    print_utils.title("Add podfile")
    add_podfile(details)

    print_utils.ack("\nGreat! Run the app in order to finish setup")
    if click.confirm(
        "Would you like to update the cocoapods repo (recommended)?",
        default=True,
    ):
        os.system("pod repo update")

    os.system("pod install")
    os.system("open {target}.xcworkspace".format(target=details["target"]))
