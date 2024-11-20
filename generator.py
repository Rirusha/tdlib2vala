#!/usr/bin/python3
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

import os
import shutil
import requests
import sys
from functions_defs import create_functions
from object_defs import create_func_object, create_object, create_td_object
from req_manager import create_req_manager
from utils import ArgData, ConstructorData, ClassData, FuncData, camel_to_snake, escape_name, escape_name, resolve_type, types_conversion

import global_args


TAG_PREFIX = '@'
COMMENT_PREFIX = '//'
CLASS_TAG =  TAG_PREFIX + 'class'
DESCRIPTION_TAG = TAG_PREFIX + 'description'


# author = sys.argv[1]
# target_path = sysys.argv[2]
author = 'Vladimir Vaskov'
target_path = '/home/rirusha/Projects/libvalagram'
target_path_lib = os.path.join(target_path, 'lib')

td_api_url = 'https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/td_api.tl'
namespace = 'TDLib'

global_args.author = author
global_args.namespace = namespace
global_args.target_path = target_path_lib

td_api_doc_lines = requests.get(td_api_url).text.split('\n')

td_api_doc_lines_format:list[str] = []

for td_api_doc_line in td_api_doc_lines:
    if (td_api_doc_line and td_api_doc_line.strip() != ''):
        td_api_doc_lines_format.append(td_api_doc_line.strip())

is_start:bool = False
is_finctions:bool = False
class_datas:dict[str,ClassData] = {}
func_datas:dict[str,FuncData] = {}

last_constructor:ConstructorData = None
last_description_entity = None

for line in td_api_doc_lines_format:
    if '---functions---' in line:
        is_finctions = True
        continue

    if line.startswith(COMMENT_PREFIX) and not is_start:
        is_start = True

    if not is_finctions and is_start:
        if line.startswith(COMMENT_PREFIX + CLASS_TAG):
            class_data = ClassData ()

            class_data.description.append(line.split(DESCRIPTION_TAG)[1].strip())
            last_description_entity = class_data
            class_data.name = line.split(DESCRIPTION_TAG)[0].strip().split(' ')[-1].strip()

            class_datas[class_data.name] = class_data

        elif line.startswith(COMMENT_PREFIX + DESCRIPTION_TAG):
            last_constructor = ConstructorData ()
            
            for desc in line.split('@'):
                if desc == COMMENT_PREFIX:
                    continue
                elif desc.startswith('description'):
                    last_constructor.description.append(desc.replace('description', '').strip())
                    last_description_entity = last_constructor
                else:
                    arg_data = ArgData ()

                    if desc.startswith('param_'):
                        arg_data.name = desc.split(' ')[0].strip().replace('param_', '')
                    else:
                        arg_data.name = desc.split(' ')[0].strip()

                    desc_line = ' '.join(desc.split(' ')[1:]).strip()
                    arg_data.nullable = 'may be null' in desc_line
                    arg_data.description.append(desc_line)

                    last_description_entity = arg_data

                    last_constructor.args[arg_data.name] = arg_data

        elif line.startswith(COMMENT_PREFIX + TAG_PREFIX):
            arg_data = ArgData ()

            if line.startswith(COMMENT_PREFIX + TAG_PREFIX + 'param_'):
                arg_data.name = line.split(' ')[0].strip('/@').replace('param_', '')
                desc_line = line.replace(COMMENT_PREFIX + TAG_PREFIX + 'param_' + arg_data.name, '').strip()
            else:
                arg_data.name = line.split(' ')[0].strip('/@')
                desc_line = line.replace(COMMENT_PREFIX + TAG_PREFIX + arg_data.name, '').strip()
                
            
            arg_data.nullable = 'may be null' in desc_line
            arg_data.description.append(desc_line)

            last_description_entity = arg_data

            last_constructor.args[arg_data.name] = arg_data

        elif line.startswith(COMMENT_PREFIX + '-'):
            last_description_entity.description.append(line.replace(COMMENT_PREFIX + '-', '').strip())

        else:
            strs = line.rstrip(';').split(' ')
            construct_name = strs[0]
            class_name = strs[-1].strip()

            if class_name.lower() == construct_name.lower():
                class_data = ClassData ()

                class_data.description.append('')
                class_data.name = class_name

                class_datas[class_name] = class_data

            last_constructor.name = construct_name
            class_datas[class_name].constructors[construct_name] = last_constructor

            for arg in strs:
                if arg == construct_name or arg == class_name or arg == '=':
                    continue

                try:
                    arg_name, arg_type = arg.split(':')
                except ValueError:
                    print(arg)
                    sys.exit(1)
                    
                if arg_name == 'type':
                    last_constructor.args[arg_name].name = 'type_'

                last_constructor.args[arg_name].type_ = resolve_type(arg_type)

    elif is_finctions and is_start:
        if line.startswith(COMMENT_PREFIX + DESCRIPTION_TAG):
            last_constructor = ConstructorData ()
            
            for desc in line.split('@'):
                if desc == COMMENT_PREFIX:
                    continue
                elif desc.startswith('description'):
                    last_constructor.description.append(desc.replace('description', '').strip())
                    last_description_entity = last_constructor
                else:
                    arg_data = ArgData ()

                    if desc.startswith('param_'):
                        arg_data.name = desc.split(' ')[0].strip().replace('param_', '')
                    else:
                        arg_data.name = desc.split(' ')[0].strip()

                    desc_line = ' '.join(desc.split(' ')[1:]).strip()
                    arg_data.nullable = 'may be null' in desc_line
                    arg_data.description.append(desc_line)

                    last_description_entity = arg_data

                    last_constructor.args[arg_data.name] = arg_data

        elif line.startswith(COMMENT_PREFIX + TAG_PREFIX):
            arg_data = ArgData ()

            if line.startswith(COMMENT_PREFIX + TAG_PREFIX + 'param_'):
                arg_data.name = line.split(' ')[0].strip('/@').replace('param_', '')
                desc_line = line.replace(COMMENT_PREFIX + TAG_PREFIX + 'param_' + arg_data.name, '').strip()
            else:
                arg_data.name = line.split(' ')[0].strip('/@')
                desc_line = line.replace(COMMENT_PREFIX + TAG_PREFIX + arg_data.name, '').strip()
                
            
            arg_data.nullable = 'may be null' in desc_line
            arg_data.description.append(desc_line)

            last_description_entity = arg_data

            last_constructor.args[arg_data.name] = arg_data

        elif line.startswith(COMMENT_PREFIX + '-'):
            last_description_entity.description.append(line.replace(COMMENT_PREFIX + '-', '').strip())

        else:
            strs = line.rstrip(';').split(' ')
            construct_name = strs[0]
            return_type = strs[-1].strip()
            
            func_data = FuncData ()
            func_data.constructor = last_constructor
            func_data.name = camel_to_snake(construct_name)
            func_data.return_type = return_type

            last_constructor.name = construct_name
            func_datas[construct_name] = func_data
            
            for desc in last_constructor.description:
                if 'Can be called synchronously' in desc:
                    func_data.can_be_sync = True
                    break

            for arg in strs:
                if arg == construct_name or arg == return_type or arg == '=':
                    continue

                try:
                    arg_name, arg_type = arg.split(':')
                except ValueError:
                    print(arg)
                    sys.exit(1)

                if arg_name == 'type':
                    last_constructor.args[arg_name].name = 'type_'

                last_constructor.args[arg_name].type_ = resolve_type(arg_type)

for class_data in class_datas.values():
    class_data.name = escape_name(class_data.name)
    
    for constructor in class_data.constructors.values():
        for arg in constructor.args.values():
            arg.name = escape_name(arg.name)

for func_data in func_datas.values():
    escape_name(func_data.return_type)
    
    for arg in func_data.constructor.args.values():
        arg.name = escape_name(arg.name)

for class_data in class_datas.values():
    create_object(class_data)
create_td_object()
for func_data in func_datas.values():
    create_func_object(func_data)
create_functions(list(func_datas.values()), class_datas)
create_req_manager()

lib_file_names = os.listdir('lib')
for file_name in lib_file_names:
    shutil.copy(os.path.join('lib', file_name), target_path_lib)
vapi_file_names = os.listdir('vapi')
for file_name in vapi_file_names:
    shutil.copy(os.path.join('vapi', file_name), os.path.join(target_path, 'vapi'))
