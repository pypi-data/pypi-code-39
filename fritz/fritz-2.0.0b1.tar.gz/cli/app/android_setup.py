"""
This module contains the code for setting up an Android app.
"""
import re
from xml.etree import ElementTree

import click

from cli import print_utils
from cli import file_utils
from cli.app.setup_utils import pause_confirmation, setup_app_info


ANDROID_APP_BUILD_DEPENDENCIES = """dependencies {
    implementation 'ai.fritz:core:+'
}"""


ANDROID_PROJECT_BUILD_REPO = """allprojects {
    repositories {
        // Add this.
        maven { url 'https://raw.github.com/fritzlabs/fritz-repository/master' }
    }
}"""


ANDROID_MANIFEST_SERVICE = """<application ...>
    <service
        android:name="ai.fritz.core.FritzCustomModelService"
        android:exported="true"
        android:permission="android.permission.BIND_JOB_SERVICE" />
</application>"""


def create_fritz_configure_content(api_key):
    """Sample code for Android."""
    return (
        """public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // Initialize Fritz
        Fritz.configure(this, "%s");
    }
}"""
        % api_key
    )


def show_android_setup_steps(cwd):
    """Show all Android setup steps

    Args:
        cwd: current working directory (in Android project)
    """
    file_paths = file_utils.find_all("AndroidManifest.xml", cwd)
    gradle_file_paths = file_utils.find_all("build.gradle", cwd)
    android_manifest_file = None
    for file_path in file_paths:
        if "src/main/AndroidManifest.xml" in file_path:
            android_manifest_file = file_path
            break

    app_build_gradle_file_path = None
    for gradle_file_path in gradle_file_paths:
        if file_utils.find_text_in_file(
            "apply plugin: 'com.android.application'", gradle_file_path
        ):
            app_build_gradle_file_path = gradle_file_path
            break

    if not android_manifest_file:
        print("No AndroidManifest.xml file found")
        return

    app_name = search_and_find_app_name(cwd, android_manifest_file)
    package_name = search_and_find_package_name(
        android_manifest_file, gradle_file_paths
    )

    print_utils.title("Step 1: Register your app with Fritz")
    app_info = setup_app_info(app_name, package_name, "android")

    print_utils.title("Step 2: Update your AndroidManifest")
    update_android_manifest(android_manifest_file)

    print_utils.title("Step 3: Update your app dependencies")
    project_build_gradle_path = cwd + "/build.gradle"
    update_dependencies_with_fritz(
        app_build_gradle_file_path, project_build_gradle_path
    )

    print_utils.title("Step 4: Initialize the SDK")
    click.echo(
        "Initialize the SDK in the Application / MainActivity "
        "onCreate lifecycle method.\n"
    )

    print_utils.code(create_fritz_configure_content(app_info["api_key"]))

    pause_confirmation()
    print_utils.ack("\n\nGreat! Run the app in order to finish setup")


def search_and_find_app_name(cwd, path_to_manifest):
    """Find the app name with the label tag in the AndroidManifest.

    Follow the string tag if it exists.
    This isn't 100% robust but it makes a
    best effort attempt to find the app name.

    Args:
        cwd
        path_to_manifest

    Returns:
        the app name if it's found.
    """

    tree = ElementTree.parse(path_to_manifest)
    root = tree.getroot()
    application_node = root.find("application")
    app_label = application_node.get(
        "{http://schemas.android.com/apk/res/android}label"
    )

    if "@string/" in app_label:
        label_key = app_label.split("@string/")[1]
        string_files = file_utils.find_all("strings.xml", cwd)
        for string_file in string_files:
            tree_string = ElementTree.parse(string_file)
            root_string = tree_string.getroot()
            string_nodes = root_string.findall("string")

            for string_node in string_nodes:
                if string_node.get("name") == label_key:
                    return string_node.text

        return None
    return app_label


def update_dependencies_with_fritz(
    app_build_gradle_file_path, app_project_gradle_file
):
    """Update the project and app build.gradle files to include fritz.

    Args:
        app_build_gradle_file_path
        app_project_gradle_file
    """

    requires_mod = False
    repo = "https://raw.github.com/fritzlabs/fritz-repository/master"
    if not file_utils.find_text_in_file(repo, app_project_gradle_file):
        click.echo(
            "Include the Maven Repository on the project "
            "level to access Fritz dependencies."
            + "\n[{app_project_gradle_file}]\n".format(
                app_project_gradle_file=app_project_gradle_file
            )
        )
        print_utils.code(ANDROID_PROJECT_BUILD_REPO)
        requires_mod = True
    else:
        print_utils.ack("Fritz Maven repository already exists")

    if not file_utils.find_text_in_file(
        "ai.fritz:core", app_build_gradle_file_path
    ):
        click.echo(
            "\n\nInclude the SDK in your app build.gradle file\n"
            "[{app_project_gradle_file}].\n".format(
                app_project_gradle_file=app_project_gradle_file
            )
        )
        print_utils.code(ANDROID_APP_BUILD_DEPENDENCIES)
        requires_mod = True
    else:
        print_utils.ack("Fritz Core dependency already added")

    if requires_mod:
        click.echo("\nSync the gradle dependencies.")
        pause_confirmation()


def search_and_find_package_name(path_to_manifest, gradle_file_paths):
    """Search and find the Android package name.

    This will first search the gradle file and then fall back to using
    the package name in the manifest.

    Args:
        path_to_manifest: path to AndroidManifest.xml
        gradle_file_paths: path to the app/build.gradle

    Returns:
        the package name.
    """
    package_name = search_for_apk_id_in_gradle(gradle_file_paths)
    if package_name:
        return package_name

    tree = ElementTree.parse(path_to_manifest)
    root = tree.getroot()
    package_name = root.get("package")
    return package_name


def search_for_apk_id_in_gradle(gradle_file_paths):
    """Search for the apk_id in the app gradle file.

    Args:
        gradle_file_paths: app/build.gradle
    """
    for file_path in gradle_file_paths:
        line = file_utils.find_text_in_file("applicationId", file_path)
        if line:
            matched_items = re.findall(r'"(.*?)"', line)
            if matched_items:
                return matched_items[0]
    return None


def update_android_manifest(manifest_path):
    """Update the AndroidManifest.xml file

    Args:
        manifest_path: the path to the manifest file.
    """
    if file_utils.find_text_in_file(
        "ai.fritz.core.FritzCustomModelService", manifest_path
    ):
        print_utils.ack("Already added the service to the AndroidManifest")
        return

    click.echo("Update your AndroidManifest.xml\n\n")
    print_utils.code(ANDROID_MANIFEST_SERVICE)

    if not click.confirm(
        "\nAdd to the manifest found at {manifest_path}?".format(
            manifest_path=manifest_path
        )
    ):
        return
    code_to_insert = """
        <service
            android:name="ai.fritz.core.FritzCustomModelService"
            android:exported="true"
            android:permission="android.permission.BIND_JOB_SERVICE" />
"""
    file_utils.insert_code_before(
        "</application>", code_to_insert, manifest_path
    )
