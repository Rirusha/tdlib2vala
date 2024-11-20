import os
import global_args
from structures import CASE, REQ_MANAGER_CLASS
from utils import ClassData, camel_to_pascal, format_description, format_header


def create_req_manager (class_datas:dict[str,ClassData]):
    path = os.path.join(global_args.target_path, 'requests-manager.vala')

    if not os.path.exists(global_args.target_path):
        os.makedirs(global_args.target_path)

    with open(path, 'w') as file:
        file.write(format_header())
        file.write('\n\n')

        constructors = list(map(lambda x: x.name, class_datas['Update'].constructors.values()))
        
        cases = []
        for constructor in constructors:
            cases.append(CASE.format(
                case=constructor,
                return_type=camel_to_pascal(constructor)
            ))

        file.write(format_description(['Requests manager'], 0))
        file.write(REQ_MANAGER_CLASS.format(
            cases='\n'.join(cases)
        ))
