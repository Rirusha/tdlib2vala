import os
import global_args
from structures import REQ_MANAGER_CLASS
from utils import format_description, format_header


def create_req_manager ():
    path = os.path.join(global_args.target_path, 'requests-manager.vala')

    if not os.path.exists(global_args.target_path):
        os.makedirs(global_args.target_path)
        
    with open(path, 'w') as file:
        file.write(format_header())
        file.write('\n\n')
        
        file.write(format_description(['Requests manager'], 0))
        file.write(REQ_MANAGER_CLASS)
