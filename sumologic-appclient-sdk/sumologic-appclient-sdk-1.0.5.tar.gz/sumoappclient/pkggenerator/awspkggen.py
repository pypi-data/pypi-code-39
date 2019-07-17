import os
import sys
import shutil
import yaml

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, cur_dir)

from common.config import Config
from common.logger import get_logger
from pkggenerator.base import PkgGenerator
from pkggenerator.utils import upload_code_in_S3, copytree
from common.utils import create_dir


class AWSPkgGen(PkgGenerator):
    def __init__(self, configpath):
        self.base_config, self.deploy_config = self.get_config(configpath)
        self.log = get_logger(__name__, **self.base_config['Logging'])
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.expanduser(configpath))))
        self.setup_env()

    def setup_env(self):
        self.remove_unwanted_files(self.project_dir)
        target_dir = os.path.join(self.project_dir, "target")
        create_dir(target_dir)
        self.aws_target_dir = os.path.join(target_dir, "aws")
        self.log.info(f"creating aws target directory {self.aws_target_dir}")
        create_dir(self.aws_target_dir)

    def get_param_name(self, s):
        return s.title().replace("_", "")

    def create_parameters(self, sam_template_path):
        self.log.debug(f"adding parameters {sam_template_path}")
        cfg = Config()
        sam_config = cfg.read_config(sam_template_path)
        function_name = "%sFunction" % self.deploy_config["APPNAME_SINGLE"]
        vars = sam_config["Resources"][function_name]["Properties"]['Environment']["Variables"]
        sam_config["Parameters"] = params = sam_config["Parameters"] or {}
        self.template_params = set()
        for section, section_cfg in self.base_config.items():
            for k, v in section_cfg.items():
                if v is None:
                    param_name = self.get_param_name(k)
                    params[param_name] = {"Type": "String"}
                    vars[k] = {"Ref": param_name}
                    self.template_params.add(param_name)
        with open(sam_template_path, "w") as f:
            f.write(yaml.dump(sam_config, default_flow_style=False))
            # yaml.dump(sam_config, f)

    def generate_template(self):
        base_sam_template_path = os.path.join(self.RESOURCE_FOLDER, "aws", "basesamtemplate.yaml")
        target_filepath = os.path.join(self.aws_target_dir, "samtemplate.yaml")
        self.log.info(f"generating_template {target_filepath}")
        self.generate_file(base_sam_template_path, self.deploy_config, target_filepath)
        self.create_parameters(target_filepath)
        template_path = os.path.join(self.project_dir, "template.yaml")
        shutil.copy(target_filepath, template_path)
        return template_path

    def deploy_package(self, packaged_template_path, aws_region):
        # Todo create layer, create and publish SAM
        # sam package --template-file MongoDBAtlas.yaml --s3-bucket $SAM_S3_BUCKET  --output-template-file packaged_MongoDBAtlas.yaml

        self.log.info(f"deploying template in {os.getenv('AWS_PROFILE')} Region: {aws_region}")
        env_vars = []
        cfg = Config()
        cfg_locations = cfg.get_config_locations('', self.deploy_config['COLLECTION_CONFIG'])
        user_cfg = cfg.get_user_config(cfg_locations)
        for section, section_cfg in user_cfg.items():
            for k, v in section_cfg.items():
                param_name = self.get_param_name(k)
                if param_name in self.template_params:
                    env_vars.append(f"{param_name}={v}")
        cmd = ["sam", "deploy", "--template-file", packaged_template_path, "--stack-name", f"testing{self.deploy_config['APPNAME_SINGLE']}", "--capabilities", "CAPABILITY_IAM", "--region", aws_region, "--parameter-overrides", *env_vars]
        self.run_command(cmd)

        # aws cloudformation get-template --stack-name testingMongoDBAtlas  --region $AWS_REGION > MongoDBAtlasCFTemplate.json
        # aws cloudformation describe-stack-events --stack-name testingsecurityhublambda --region $AWS_REGION
        # aws serverlessrepo create-application-version --region us-east-1 --application-id arn:aws:serverlessrepo:us-east-1:$AWS_ACCOUNT_ID:applications/sumologic-securityhub-connector --semantic-version 1.0.1 --template-body file://packaged.yaml

    def create_build(self):
        # Todo convert pip/zip to non command based
        aws_build_folder = os.path.join(self.aws_target_dir, "build")
        create_dir(aws_build_folder)
        os.chdir(aws_build_folder)
        self.log.debug(f"changing to build dir: {os.getcwd()}")
        requirement_filepath = os.path.join(self.project_dir, "requirements.txt")
        shutil.copy(requirement_filepath, aws_build_folder)
        self.run_command(["pip", "install", "-r", "requirements.txt", "-t", "."])
        self.log.debug(f"installing dependencies {requirement_filepath}")
        src_dir = os.path.join(self.project_dir, self.deploy_config['SRC_FOLDER_NAME'])
        self.log.debug(f"copying src {src_dir}")
        copytree(src_dir, aws_build_folder)
        for filename in ["concurrent", "futures-3.1.1.dist-info"]:
            filepath = os.path.join(aws_build_folder, filename)
            if os.path.isdir(filepath):
                shutil.rmtree(filepath)
        return aws_build_folder

    def create_zip(self, aws_build_folder):
        import zipfile
        os.chdir(aws_build_folder)
        self.log.debug(f"changing to build dir: {os.getcwd()}")
        zip_file_path = os.path.join(self.aws_target_dir, self.deploy_config["APPNAME_SINGLE"]+".zip")
        self.log.info(f"creating zip file {zip_file_path}")
        # subprocess.run(["zip", "-r", zip_file_path, "."])
        zipf = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(aws_build_folder):
            for file in files:
                zipf.write(os.path.join(root, file))

        zipf.close()
        return zip_file_path

    def generate_packaged_template(self, template_file_path, SAM_S3_BUCKET):
        os.chdir(self.project_dir)
        packaged_template_path = os.path.join(self.project_dir, "packaged.yaml")
        self.run_command(["sam", "package", "--template-file", template_file_path, "--output-template-file", packaged_template_path,  "--s3-bucket", SAM_S3_BUCKET])
        return packaged_template_path

    def publish_package(self, packaged_template_path, AWS_REGION):
        os.chdir(self.project_dir)
        self.run_command(["sam", "publish", "--template", packaged_template_path, "--region", AWS_REGION])

    def build_and_deploy(self, deploy=False):
        template_file_path = self.generate_template()
        aws_build_folder = self.create_build()

        # zip_file_path = self.create_zip(aws_build_folder)
        if deploy:
            if deploy == "prod":
                SAM_S3_BUCKET = "appdevstore"
                AWS_REGION = "us-east-1"
                packaged_template_path = self.generate_packaged_template(template_file_path, SAM_S3_BUCKET)
                self.publish_package(packaged_template_path, AWS_REGION)
            else:
                SAM_S3_BUCKET = "appdevstore-us-east-1"
                AWS_REGION = "us-east-1"
                with open(template_file_path, "r+") as f:
                    data = f.read()
                    data = data.replace("appdevstore", SAM_S3_BUCKET)
                    f.seek(0)
                    f.write(data)
                    f.truncate()
                packaged_template_path = self.generate_packaged_template(template_file_path, SAM_S3_BUCKET)
                self.deploy_package(packaged_template_path, AWS_REGION)


if __name__ == "__main__":
    deploy = False
    if len(sys.argv) > 1:
        configpath = sys.argv[1]
        if len(sys.argv) > 2:
            deploy = sys.argv[2]
    else:
        raise Exception("pass collection config path as param")
    AWSPkgGen(configpath).build_and_deploy(deploy)


