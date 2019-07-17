import argparse

from pkggenerator.awspkggen import AWSPkgGen
from pkggenerator.onprempkggen import OnPremPkgGen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", '--env', dest='env', choices=["onprem", "aws", "gcp", "azure"],
                        default="onprem", help='Select the environment on which the package is deployed.')

    parser.add_argument("-d", '--deploy', dest='deploy', choices=["prod", "test"],
                         default=False, help='To deploy the package (default: False)')

    parser.add_argument("-c", '--config', required=True, dest='configpath', help='Path of the metadata file')


    args = parser.parse_args()
    if args.env == "onprem":
        OnPremPkgGen(args.configpath).build_and_deploy(args.deploy)
    elif args.env == "aws":
        AWSPkgGen(args.configpath).build_and_deploy(args.deploy)
    else:
        print("%s environment is currently not supported" % args.env)


if __name__ == '__main__':
    main()