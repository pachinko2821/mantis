from mantis.constants import ASSET_TYPE_SUBDOMAIN
from mantis.utils.crud_utils import CrudUtils
from mantis.tool_base_classes.toolScanner import ToolScanner
from mantis.models.args_model import ArgsModel
from mantis.utils.tool_utils import get_assets_grouped_by_type
from mantis.constants import ASSET_TYPE_TLD
import logging
from os import environ

'''
Chaos module enumerates subdomain of the TLDs which are fetched from database.
The Chaos project provides a DNS dataset created using live certificate streams.
chaos-client is a go-based client to interact with that dataset.
Output file: .txt separated by new line.
Each subdomain discovered is inserted into the database as a new asset.
'''

class Chaos(ToolScanner):

    def __init__(self) -> None:
        super().__init__()

    async def get_commands(self, args: ArgsModel):
        self.CHAOS_API_KEY = None # Provide the Chaos API key here. Generate from https://chaos.projectdiscovery.io/

        if self.CHAOS_API_KEY is None:
            logging.warning("CHAOS_API_KEY token not provided, chaos will not run successfully")
            raise Exception("CHAOS_API_KEY token not provided!!")
        else:
            environ['PDCP_API_KEY'] = self.CHAOS_API_KEY

        self.org = args.org
        # Run chaos with update check disabled
        self.base_command = 'chaos -duc -d {input_domain} -o {output_file_path}'
        self.outfile_extension = ".txt"
        self.assets = await get_assets_grouped_by_type(self, args, ASSET_TYPE_TLD)
        return super().base_get_commands(self.assets)

    def parse_report(self,outfile):
        output_dict_list = []
        chaos_output = open(outfile).readlines()

        for domain in chaos_output:
            domain_dict = {
                '_id': domain.rstrip('\n'),
                'asset': domain.rstrip('\n'),
                'asset_type': ASSET_TYPE_SUBDOMAIN,
                'org': self.org,
                'tool_source': 'chaos'
            }
            output_dict_list.append(domain_dict)

        return output_dict_list
    
    async def db_operations(self, tool_output_dict, asset=None):
        await CrudUtils.insert_assets(tool_output_dict)
