import os
import global_args
from structures import CASE, CLIENT_CONSTR, CLIENT_FINAL, PROPERTY, SYNC_BODY, BODY, CLIENT_CLASS, CLIENT_ID, INIT_BODY, METHOD, REQ_MANAGER
from utils import ClassData, FuncData, camel_to_pascal, format_args_const, format_args_desc, format_description, format_header, format_init_method, format_method, snake_to_pascal


def create_functions(func_datas:list[FuncData], class_datas:dict[str,ClassData]):
    path = os.path.join(global_args.target_path, 'client.vala')

    if not os.path.exists(global_args.target_path):
        os.makedirs(global_args.target_path)

    with open(path, 'w') as file:
        file.write(format_header())
        file.write('\n\n')
        
        file.write((CLIENT_CLASS + ' {{\n').format(
            namespace=global_args.namespace
        ))
        
        file.write('\n')
        file.write(CLIENT_ID);
        file.write('\n\n')
        file.write(REQ_MANAGER);
        file.write('\n\n')
        
        file.write(PROPERTY.format(
            'double',
            'timeout',
            ''
        ))

        file.write('\n')
        file.write(format_description(['@param timeout']))
        file.write(CLIENT_CONSTR);
        file.write(CLIENT_FINAL);
        
        file.write('\n')
        file.write(format_description(['Init client: create request manager and set client_id']))
        file.write('\n')
        file.write(format_init_method())
        file.write('\n')

        for func_data in func_datas:
            descrition = format_description(func_data.constructor.description + format_args_desc(list(func_data.constructor.args.values())))
            body_args = ',\n            '.join(list(map(lambda x: x.name, func_data.constructor.args.values())))

            target_obj = snake_to_pascal(func_data.name)
            
            constructors = list(map(lambda x: x.name, class_datas[func_data.return_type].constructors.values()))
            cases = []
            for constructor in constructors:
                cases.append(CASE.format(
                    return_type=camel_to_pascal(constructor),
                    case=constructor,
                ))
            
            if func_data.can_be_sync:
                file.write('\n')
                file.write(descrition)
                file.write('\n')
                file.write(format_method(
                    func_data.return_type,
                    func_data.name,
                    format_args_const(list(func_data.constructor.args.values())),
                    SYNC_BODY.format(
                        target_obj=target_obj,
                        args='\n            ' + body_args + '\n        ' if body_args else '',
                        return_type=func_data.return_type,
                        func_name=func_data.name,
                        cases='\n'.join(cases)
                    ),
                    False
                ))
                file.write('\n')

            file.write('\n')
            file.write(descrition)
            file.write('\n')
            file.write(format_method(
                func_data.return_type,
                func_data.name,
                format_args_const(list(func_data.constructor.args.values())),
                BODY.format(
                    target_obj=target_obj,
                    args='\n            ' + body_args + '\n        ' if body_args else '',
                    return_type=func_data.return_type,
                    func_name=func_data.name,
                    cases='\n'.join(cases)
                ),
                True
            ))
            file.write('\n')
            
        file.write('}')
