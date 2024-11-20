# Copyright (C) 2024 Vladimir Vaskov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os
import global_args
from structures import ABSTRACT_CLASS_DEFINITION, CLASS_DEFINITION, CONSTRUCTOR, INTERNAL_CLASS_DEFINITION, INTERNAL_PROPERTY, PROPERTY
from utils import ArgData, ClassData, FuncData, camel_to_kebeb, camel_to_pascal, camel_to_snake, format_args_const, format_args_obj, format_description, format_header, pascal_to_kebeb, snake_to_kebab


def create_td_object ():
    objects_path = os.path.join(global_args.target_path, 'objects')
    path = os.path.join(objects_path, 't-d-object.vala')

    if not os.path.exists(objects_path):
        os.makedirs(objects_path)
        
    with open(path, 'w') as file:
        file.write(format_header())
        file.write('\n\n')
        
        file.write(format_description(['Base TDLib object'], 0))
        file.write('\n')
        
        file.write((ABSTRACT_CLASS_DEFINITION + ' {{\n').format(
            global_args.namespace,
            'TDObject',
            'Object'
        ))
        file.write('\n')
        file.write(format_description(['TDObject @type']))
        file.write('\n')
        file.write(INTERNAL_PROPERTY.format(
            'string',
            'tdlib_type',
            ''
        ))
        file.write('\n')
        file.write(format_description(['TDObject @extra']))
        file.write('\n')
        file.write(INTERNAL_PROPERTY.format(
            'string',
            'tdlib_extra',
            ''
        ))
        file.write('}\n')

def create_object (class_data:ClassData):
    objects_path = os.path.join(global_args.target_path, 'objects')
    path = os.path.join(objects_path, pascal_to_kebeb(class_data.name) + '.vala')

    if not os.path.exists(objects_path):
        os.makedirs(objects_path)

    with open(path, 'w') as file:
        file.write(format_header())
        file.write('\n\n')

        has_base_constructor:bool = False

        for constructor in class_data.constructors.values():
            if constructor.name.lower() == class_data.name.lower():
                has_base_constructor = True
                break

        if has_base_constructor:
            if len(class_data.constructors) > 1:
                raise TypeError ('Too many constructors')
            
            constructor = list(class_data.constructors.values())[0]

            file.write(format_description(constructor.description, 0))
            file.write('\n')
            file.write((CLASS_DEFINITION + ' {{\n').format(
                global_args.namespace,
                class_data.name,
                'TDObject' if class_data.name == 'Error' else 'Error'
            ))

            file.write('\n')

            for arg in constructor.args.values():
                file.write(format_description(arg.description))
                file.write('\n')
                file.write(PROPERTY.format(
                    arg.type_ if not arg.nullable else arg.type_ + '?',
                    arg.name,
                    f'default = new {arg.type_} (); ' if arg.type_.startswith('Gee.ArrayList') else ''
                ))
                file.write('\n')

            if class_data.name != 'Error':
                type_arg = ArgData()
                type_arg.name = 'tdlib_type'
                type_arg.tdlib_value = f'"{constructor.name}"'
                type_arg.type_ = 'string'

                extra_arg = ArgData()
                extra_arg.name = 'tdlib_extra'
                extra_arg.tdlib_value = 'Uuid.string_random ()'
                extra_arg.type_ = 'string'

                args = ',\n        '.join(format_args_const(list(constructor.args.values())))
                o_args=',\n            '.join(format_args_obj(list(constructor.args.values()) + [type_arg, extra_arg]))

                file.write(CONSTRUCTOR.format(
                    constructor_name=camel_to_pascal(constructor.name),
                    args='\n        ' + args + '\n    ' if len(args) > 0 else '',
                    o_args='\n            ' + o_args + '\n        ' if len(o_args) > 0 else ''
                ))
                
            file.write('}\n')

        else:
            file.write(format_description(class_data.description, 0))
            file.write('\n')

            file.write((ABSTRACT_CLASS_DEFINITION + ' {{}}\n').format(
                global_args.namespace,
                class_data.name,
                'TDObject' if class_data.name == 'Error' else 'Error'
            ))

            for constructor in class_data.constructors.values():
                file.write('\n')
                file.write(format_description(constructor.description, 0))
                file.write('\n')
                file.write((CLASS_DEFINITION + ' {{\n').format(
                    global_args.namespace,
                    camel_to_pascal(constructor.name),
                    class_data.name
                ))

                file.write('\n')

                for arg in constructor.args.values():
                    file.write(format_description(arg.description))
                    file.write('\n')
                    file.write(PROPERTY.format(
                        arg.type_ if not arg.nullable else arg.type_ + '?',
                        arg.name,
                        f'default = new {arg.type_} (); ' if arg.type_.startswith('Gee.ArrayList') else ''
                    ))
                    file.write('\n')
                    
                type_arg = ArgData()
                type_arg.name = 'tdlib_type'
                type_arg.tdlib_value = f'"{constructor.name}"'
                type_arg.type_ = 'string'

                extra_arg = ArgData()
                extra_arg.name = 'tdlib_extra'
                extra_arg.tdlib_value = 'Uuid.string_random ()'
                extra_arg.type_ = 'string'

                args = ',\n        '.join(format_args_const(list(constructor.args.values())))
                o_args=',\n            '.join(format_args_obj(list(constructor.args.values()) + [type_arg, extra_arg]))

                file.write(CONSTRUCTOR.format(
                    constructor_name=camel_to_pascal(constructor.name),
                    args='\n        ' + args + '\n    ' if len(args) > 0 else '',
                    o_args='\n            ' + o_args + '\n        ' if len(o_args) > 0 else ''
                ))
                
                file.write('}\n')

def create_func_object(func_data:FuncData):
    objects_path = os.path.join(global_args.target_path, 'objects')
    path = os.path.join(objects_path, snake_to_kebab(func_data.name) + '.vala')

    if not os.path.exists(objects_path):
        os.makedirs(objects_path)

    with open(path, 'w') as file:
        file.write(format_header())
        file.write('\n\n')
        
        constructor = func_data.constructor

        file.write(format_description(constructor.description, 0))
        file.write('\n')
        file.write((INTERNAL_CLASS_DEFINITION + ' {{\n').format(
            global_args.namespace,
            camel_to_pascal(constructor.name),
            'TDObject'
        ))

        file.write('\n')

        for arg in constructor.args.values():
            file.write(format_description(arg.description))
            file.write('\n')
            file.write(PROPERTY.format(
                arg.type_ if not arg.nullable else arg.type_ + '?',
                arg.name,
                f'default = new {arg.type_} (); ' if arg.type_.startswith('Gee.ArrayList') else ''
            ))
            file.write('\n')

        type_arg = ArgData()
        type_arg.name = 'tdlib_type'
        type_arg.tdlib_value = f'"{constructor.name}"'
        type_arg.type_ = 'string'

        extra_arg = ArgData()
        extra_arg.name = 'tdlib_extra'
        extra_arg.tdlib_value = 'Uuid.string_random ()'
        extra_arg.type_ = 'string'

        args = ',\n        '.join(format_args_const(list(constructor.args.values())))
        o_args=',\n            '.join(format_args_obj(list(constructor.args.values()) + [type_arg, extra_arg]))

        file.write(CONSTRUCTOR.format(
            constructor_name=camel_to_pascal(constructor.name),
            args='\n        ' + args + '\n    ' if len(args) > 0 else '',
            o_args='\n            ' + o_args + '\n        ' if len(o_args) > 0 else ''
        ))
        
        file.write('}\n')
