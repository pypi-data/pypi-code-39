#!/usr/bin/python3

import argparse
import datetime
import json
import subprocess
from enum import Enum


def is_clean_repo() -> bool:
    status = subprocess.check_output(["git", "status", "--short"])
    return status.strip() == b""


def get_current_git_hash() -> str:
    return (
        subprocess.check_output(["git", "rev-parse", "HEAD"])
        .strip()
        .decode("utf-8")
    )


def tag_docker_image(existing_image: str, new_tag: str) -> None:
    subprocess.check_call(
        ["sudo", "docker", "tag", existing_image, new_tag],
        stdout=subprocess.DEVNULL,
    )


def build_image(image_cfg, tag):
    subprocess.check_call(
        [
            "sudo",
            "docker",
            "image",
            "build",
            image_cfg.get("dir", "src"),
            "-t",
            tag,
            "-f",
            image_cfg.get("dockerfile", "deploy/docker/Dockerfile"),
        ],
        stdout=subprocess.DEVNULL,
    )


def push_image(tag):
    subprocess.check_call(
        ["sudo", "docker", "image", "push", tag], stdout=subprocess.DEVNULL
    )


def redeploy(k8s_config, tag):
    subprocess.check_call(
        [
            "kubectl",
            "set",
            "image",
            "--namespace",
            k8s_config["namespace"],
            "deployment/{}".format(k8s_config["deployment"]),
            "{}={}".format(k8s_config["container"], tag),
        ],
        stdout=subprocess.DEVNULL,
    )


def get_current_image(k8s_config):
    container = k8s_config["container"]
    jsonpath = f'{{..containers[?(@.name=="{container}")].image}}'
    return subprocess.check_output(
        [
            "kubectl",
            "get",
            "deployment",
            "--namespace",
            k8s_config["namespace"],
            f"-o=jsonpath={jsonpath}",
        ]
    ).decode("utf-8")


def build_all(config, push, deploy, version):
    for name, element in config.items():
        tag = "{}:{}".format(element["docker"]["image"], version)
        if "docker" in element:
            print("[-] Building {}".format(name))
            build_image(element["docker"], tag)
            print("[-] Built image {}".format(tag))
            if push:
                print("[-] Pushing image {}".format(tag))
                push_image(tag)
        if deploy is not None:
            key = "k8s" if deploy == "production" else "k8s-staging"
            if key not in element:
                print("[!] {} is missing a {} config".format(name, key))
                continue
            if deploy == "production":
                master = "{}:{}".format(element["docker"]["image"], "master")
                print("[-] Pushing image {}".format(master))
                tag_docker_image(tag, master)
            latest = "{}:{}".format(element["docker"]["image"], "latest")
            print("[-] Pushing image {}".format(latest))
            tag_docker_image(tag, latest)
            push_image(latest)
            print("[-] Redeploying {} to {}".format(name, deploy))
            redeploy(element[key], tag)


class ImageTagSource(Enum):
    commit_hash = "commit_hash"
    date = "date"
    latest = "latest"

    def __str__(self) -> str:
        return self.value


def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy the application.")
    parser.add_argument(
        "service", default=None, nargs="?", help="Service to deploy"
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force deploy. It's probably a bad idea.",
    )
    parser.add_argument(
        "--build", "-b", action="store_true", help="Only build images"
    )
    parser.add_argument(
        "--push", action="store_true", help="Build and push images"
    )
    parser.add_argument(
        "--production",
        "-p",
        action="store_true",
        help="Build, push and redeploy images TO PRODUCTION",
    )
    parser.add_argument(
        "--staging",
        "-s",
        action="store_true",
        help="Build, push and redeploy images to the staging environment",
    )
    parser.add_argument(
        "--promote",
        "-P",
        action="store_true",
        help="Promote image from staging to the production environment",
    )
    parser.add_argument(
        "--tag",
        "-t",
        type=ImageTagSource,
        default=ImageTagSource.commit_hash,
        choices=list(ImageTagSource),  # type: ignore
        help="How to name a docker image.",
    )
    args = parser.parse_args()

    if args.build:
        push, deploy = False, None
    elif args.push:
        push, deploy = True, None
    elif args.production:
        push, deploy = True, "production"
    elif args.staging:
        push, deploy = True, "staging"
    elif args.promote:
        pass
    else:
        print("What do you want to do? (try --production or --help)")
        return

    if not is_clean_repo():
        if args.force:
            if args.tag == ImageTagSource.commit_hash:
                print("Dirty repo, can't tag with git hash. Try --tag=date.")
                return
            if args.production:
                print("Is everything OK at home?. Ok, deploying...")
        else:
            print("You have uncommited changes. Commit them (or --force).")
            return

    with open("deploy/deploy.json", "r") as configfile:
        config = json.loads(configfile.read())

    if args.service is not None:
        config = {args.service: config[args.service]}

    if args.promote:
        for _name, element in config.items():
            tag = get_current_image(element["k8s-staging"])
            print(f"[-] Redeploying {tag} to production")
            redeploy(element["k8s"], tag)
            base, _version = tag.split(":")
            new_tag = f"{base}:master"
            print("[-] Tagging {} as {}".format(tag, new_tag))
            tag_docker_image(tag, new_tag)
    else:
        if args.tag == ImageTagSource.commit_hash:
            version = get_current_git_hash()
        elif args.tag == ImageTagSource.date:
            version = datetime.datetime.utcnow().strftime("v%Y%m%d%H%M%S")
        elif args.tag == ImageTagSource.latest:
            version = "latest"
        else:
            raise RuntimeError("[!] Unsupported tag type")
        build_all(config, push, deploy, version)


if __name__ == "__main__":
    main()
