# coding=utf-8
import os
from ibm_ai_openscale_cli.utility_classes.utils import remove_port_from_url
from ibm_ai_openscale_cli.setup_classes.setup_services import SetupServices
from ibm_ai_openscale_cli.utility_classes.fastpath_logger import FastpathLogger
from ibm_ai_openscale_cli.api_environment import ApiEnvironment

logger = FastpathLogger(__name__)

class SetupIBMCloudPrivateServices(SetupServices):

    def __init__(self, args):
        super().__init__(args)

    def setup_aios(self):
        logger.log_info('Setting up {} instance'.format('Watson OpenScale'))
        aios_icp_credentials = {}
        if self._args.iam_token:
            aios_icp_credentials['iam_token'] = self._args.iam_token
        else:
            aios_icp_credentials['username'] = self._args.username
            aios_icp_credentials['password'] = self._args.password
        aios_icp_credentials['url'] = '{}'.format(self._args.url)
        aios_icp_credentials['hostname'] = ':'.join(self._args.url.split(':')[:2])
        aios_icp_credentials['port'] = self._args.url.split(':')[2]
        return aios_icp_credentials

    def setup_wml(self):
        def format_wml_credentials(credentials):
            credentials['url'] = remove_port_from_url(credentials['url'])
            return credentials
        logger.log_info('Setting up {} instance'.format('Watson Machine Learning'))
        wml_credentials = {}
        if self._args.wml:
            wml_credentials = format_wml_credentials(self.read_credentials_from_file(self._args.wml))
        elif self._args.wml_json:
            wml_credentials = format_wml_credentials(self._args.wml_json)
        else:
            if self._args.iam_token:
                wml_credentials['iam_token'] = self._args.iam_token
            else:
                wml_credentials['username'] = self._args.username
                wml_credentials['password'] = self._args.password
            wml_credentials['url'] = ':'.join(self._args.url.split(':')[:2])
            if wml_credentials['url'] == ApiEnvironment().icp_gateway_url:
                icp4d_ns = os.environ.get('ICP4D_NAMESPACE') if os.environ.get('ICP4D_NAMESPACE') else 'zen'
                wml_credentials['url'] = 'https://wmlproxyservice.{}'.format(icp4d_ns)
                # wml_credentials['url'] = 'https://mlscoring-v3.{}'.format(icp4d_ns)
            wml_credentials['instance_id'] = 'icp'
        return wml_credentials

