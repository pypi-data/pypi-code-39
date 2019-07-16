#!/bin/python3

import os
import sys
import time
import subprocess
from subprocess import call
from configparser import ConfigParser


def _print(msg, index=1):
    os.system('echo "\n"')
    os.system('echo "{}"'.format(msg))
    if index == 1:
        os.system('echo "{}"'.format("=" * len(msg)))
    elif index == 2:
        os.system('echo "{}"'.format("-" * len(msg)))
    elif index == 3:
        os.system('echo "{}"'.format("." * min(len(msg), 7)))
    else:
        os.system('echo "{}"'.format(msg))
    os.system('echo "\n"')


def sh(cmd):
    try:
        result = call(cmd, shell=True)
        if result != 0:
            raise OSError()
    except subprocess.CalledProcessError as e:
        _print("Error executing command: " + cmd, index=None)
        _print(e, index=None)
        exit(1)
    except OSError as e:
        _print("Error executing command: " + cmd, index=None)
        _print(e, index=None)
        exit(1)


class Target(object):
    @staticmethod
    def service(key, *args, **kwargs):
        """
        Helper to get a certain server target type based on a key.

          - gcloud=GoogleCloudTarget

        :return {Target}: An instance of the target.
        """
        services = {"gcloud": GoogleCloudTarget}
        if key in services:
            return services[key](*args, **kwargs)
        else:
            raise Exception("Unsupported server target.")
            exit(1)

    def configure_keys(self):
        """
        Configure the access keys required to deploy to this target.

        :return {NoneType}:
        """
        raise NotImplementedError()

    def ssh(self, cmd, user=None, chdir=None, dry_run=False):
        """
        Run a command via SSH on the target server/instance.

        :return {NoneType}:
        """
        raise NotImplementedError()


class GoogleCloudTarget(Target):
    def __init__(self, secret=None, zone=None, instance=None, project=None, parse_args=False):
        """
        Initialize the google cloud server target object.

        :param zone {str}: The name of an environment variable for the zone.
        :param secret {str}:
        :param zone {str}:
        :param instance {str}:
        :param project {str}:
        :param parse_args {bool}:

        :return {NoneType}
        """
        if parse_args:
            try:
                secret = sys.argv[4]
                zone = sys.argv[5]
                instance = sys.argv[6]
                project = sys.argv[7]
            except IndexError:
                raise Exception("A google cloud deployment requires more parameters.")
                exit(1)

        self.secret = secret.strip()
        self.zone = zone.strip()
        self.instance = instance.strip()
        self.project = project.strip()

    def configure_keys(self):
        sh("python3 .om/gkey.py {}".format(self.secret))
        sh("gcloud config set project {}".format(self.project))
        sh("gcloud config set compute/zone {}".format(self.zone))
        sh("gcloud auth activate-service-account --key-file key.json")
        sh(
            "gcloud compute os-login describe-profile | grep fingerprint | cut -c 18-100 | xargs -I {} gcloud compute os-login ssh-keys remove --key={}"
        )

    def ssh(self, cmd, user=None, chdir=None, dry_run=False):
        if isinstance(cmd, list):
            for command in cmd:
                self.ssh(command)
        else:
            _print("Executing ssh command: {}".format(cmd), index=3)
            if user:
                cmd = "sudo su odoo -c '{}'".format(cmd)
            if chdir:
                cmd = "cd {} && {}".format(chdir, cmd)
            if not dry_run:
                sh('gcloud compute ssh --zone {} {} -- "{}"'.format(self.zone, self.instance, cmd))

    def scp(self, src, dest):
        sh("gcloud compute scp --zone {} {} {}:{}".format(self.zone, src, self.instance, dest))


class Deployer(object):
    supported_targets = ["gcloud"]

    def __init__(self, target, path):
        self.target = target
        self.path = path.strip()
        self.branch = None
        self.commit = None

    def configure(self):
        """
        Configure the server, instance, vm, or docker container that is
        performing the deploy process.
        """
        _print("Configuring the deployer...")
        if os.path.isfile("tasks"):
            sh("rm tasks")

        _print("Configuring dependencies.", index=2)
        self._configure_dependencies()
        _print("Configuring ssh keys.", index=2)
        self.target.configure_keys()
        _print("Configuring git data.", index=2)
        self._configure_git()

    def deploy(self, configure=False):
        """
        Deploy and run the application.

        Use the server target to actually SSH out to the appropriate instance
        and update the application.

        :param configure {bool}: True if you want to run `configure` first.
        """
        _print("Deploying...")
        if configure:
            self.configure()

        now = str(time.time()).replace(".", "")
        tmp_build_path = "/tmp/.builds/{}/{}-{}".format(self.path, self.commit, now)
        build_path = "/{path}-{branch}-current".format(path=self.path, branch=self.branch)

        _print("Zipping the current files.", index=2)
        sh("zip -qr deploy.zip ./. -x *.git*")

        _print("Scanning git repository keys", index=2)
        self.target.ssh("sudo su odoo -c 'ssh-keyscan github.com >> ~/.ssh/known_hosts'")
        self.target.ssh("sudo su odoo -c 'ssh-keyscan gitlab.com >> ~/.ssh/known_hosts'")
        self.target.ssh("sudo su odoo -c 'ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts'")

        _print("Migrating files to the target instance", index=2)
        self.target.ssh("sudo rm -rf {path} && sudo mkdir -p {path}".format(path=tmp_build_path))
        self.target.ssh("sudo chmod -R 777 /tmp/.builds")
        self.target.scp("deploy.zip", "{}/deploy.zip".format(tmp_build_path))
        self.target.ssh("cd {} && unzip -q deploy.zip".format(tmp_build_path))

        _print("Building and running the project", index=2)

        self.target.ssh(
            cmd=[
                "ls > /dev/null && [ -d {build_path} ] && sudo su odoo -c 'cd {build_path} && docker-compose rm -f -s web' || ls > /dev/null".format(
                    build_path=build_path
                ),
                "sudo mkdir -p {build_path} && sudo rm -rf {build_path}".format(build_path=build_path),
                "sudo mv {tmp_path} {build_path}".format(tmp_path=tmp_build_path, build_path=build_path),
                "sudo chown -R odoo:odoo {build_path}".format(build_path=build_path),
                "sudo chmod 775 {build_path}".format(build_path=build_path),
                "sudo su odoo -c 'cd {build_path} && ([ -f .pipeline/configs/env/.env.{branch} ] && cp .pipeline/configs/env/.env.{branch} .env || (echo \"The proper .env does not exist for this branch\" && exit 1))'".format(
                    build_path=build_path, branch=self.branch
                ),
                "sudo su odoo -c 'cd {build_path} && ln -s .om/tasks tasks'".format(build_path=build_path),
                "sudo su odoo -c 'cd {build_path} && mkdir -p .container/log'".format(build_path=build_path),
                "sudo su odoo -c 'cd {build_path} && touch .container/log/odoo.log'".format(build_path=build_path),
                "sudo su odoo -c 'cd {build_path} && pip3 install -r requirements.txt'".format(build_path=build_path),
                "sudo su odoo -c 'cd {build_path} && cp .pipeline/configs/compose/docker-compose.{branch}.yml docker-compose.yml'".format(
                    build_path=build_path, branch=self.branch
                ),
                "echo 'cd {build_path} && invoke build --no-pip -v && invoke run -dv' > /tmp/.builds/build-{branch} && sudo su - odoo < /tmp/.builds/build-{branch}".format(
                    build_path=build_path, branch=self.branch
                ),
            ]
        )

        # TODO: Do we need some way to auto upgrade all of the modules on the
        # site since we are rolling out new features?
        pass

    def monitor(self, configure=False):
        """
        Start the monitoring processes for the server.
        """
        now = str(time.time()).replace(".", "")
        monitor_build_path = "/tmp/.builds/monitor-{}.py".format(now)

        self.target.scp(".om/server/monitor/prometheus.py", monitor_build_path)
        self.target.ssh("sudo python3 {} configure.agent".format(monitor_build_path))
        self.target.ssh("sudo rm {}".format(monitor_build_path))

    def serve(self, services=None, configure=False):
        """
        Serve the application via an nginx web server.
        """
        if services:
            for service in services:
                method = "_serve_{}".format(service)
                if hasattr(self, method):
                    getattr(self, method)()

    def _serve_odoo(self):
        conf = """
server {{
    server_name {hostname};
    access_log /var/log/nginx/{hostname}.access.log combined;
    error_log /var/log/nginx/{hostname}.error.log;
    client_max_body_size 500M;
    gzip on;
    proxy_read_timeout 600s;
    root /var/www/html;
    index index.html index.htm index.php;
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $http_host;

    location / {{
        proxy_pass http://localhost:{rpc_port};
        proxy_read_timeout 6h;
        proxy_connect_timeout 5s;
        proxy_redirect off;
        add_header X-Static no;
        proxy_buffer_size 64k;
        proxy_buffering off;
        proxy_buffers 4 64k;
        proxy_busy_buffers_size 64k;
        proxy_intercept_errors on;
    }}

    location /longpolling/ {{
        proxy_pass http://localhost:{longpolling_port};
    }}

    location ~ /[a-zA-Z0-9_-]*/static/ {{
        proxy_pass http://localhost:{rpc_port};
        proxy_cache_valid 200 60m;
        proxy_buffering on;
        expires 864000;
    }}

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {{
        root /usr/share/nginx/html;
        internal;
    }}

    listen 80;
}}
"""

        config_path = ".pipeline/configs/env/.env.{branch}".format(branch=self.branch)
        if os.path.isfile(config_path):
            config = ConfigParser()
            config.read(config_path)
            now = str(time.time()).replace(".", "")
            hostname = config["options"]["HOSTNAME"]
            rpc_port = config["options"]["LOCAL_PORT"]
            longpolling_port = config["options"]["LONGPOLLING_PORT"]
            sample_nginx = "sample_nginx.conf"

            with open(sample_nginx, "w") as nginx_conf:
                nginx_conf.write(conf.format(hostname=hostname, rpc_port=rpc_port, longpolling_port=longpolling_port))

            self.target.scp(".om/server/templates/nginx/50x.html", "~/50x.html-{}".format(now))
            self.target.ssh("sudo mv ~/50x.html-{} /usr/share/nginx/html/50x.html".format(now))
            self.target.scp("sample_nginx.conf", "~/{}.conf-{}".format(hostname, now))
            self.target.ssh(
                "sudo mv ~/{hostname}.conf-{timestamp} /etc/nginx/sites-available/{hostname}.conf".format(
                    hostname=hostname, timestamp=now
                )
            )
            self.target.ssh("sudo rm -rf /etc/nginx/sites-enabled/{hostname}.conf".format(hostname=hostname))
            self.target.ssh(
                "sudo ln -s /etc/nginx/sites-available/{hostname}.conf /etc/nginx/sites-enabled/{hostname}.conf".format(
                    hostname=hostname
                )
            )
            sh("rm {}".format(sample_nginx))
            self.target.ssh("sudo service nginx restart")

        # TODO: Enable certbot, and maybe check the crontab for a certbot auto
        # renew process.
        pass

    def _serve_exporter(self):
        # TODO
        # site-agent
        pass

    def _serve_cadvisor(self):
        # TODO
        # site-cadviser
        pass

    def _configure_git(self):
        sh('git config user.email "odoo@bluestingray.com"')
        sh('git config user.name "CI Server"')
        sh("git stash")

    def _configure_dependencies(self):
        raise NotImplementedError()


class DroneDeployer(Deployer):
    def __init__(self, target, path):
        super().__init__(target, path)
        self.branch = os.getenv("DRONE_BRANCH")
        self.commit = os.getenv("DRONE_COMMIT")

    def _configure_dependencies(self):
        sh("apt-get install -y python3 python3-pip zip nginx")


# The main function will be called like the following:
#
# ```
# python3 deploy.py {deployed_via} {cloud_provider} {additional_options}
#
# python3 deploy.py drone gcloud $COMPUTE_ZONE
# ```
try:
    _print("Gathering arguments...")
    deploy_via = sys.argv[1]
    deploy_to = sys.argv[2]
    deploy_to_path = sys.argv[3]
except IndexError:
    raise Exception("Unsupported or missing argument.")
    exit(1)

if deploy_via == "drone":
    deployer = DroneDeployer(Target.service(deploy_to, parse_args=True), deploy_to_path)

    deployer.configure()
    deployer.deploy()
    deployer.monitor()
    deployer.serve(["odoo", "cadvisor", "exporter"])
else:
    raise Exception("Unsupported or missing arguments.")
    exit(1)
