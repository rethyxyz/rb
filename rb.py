#!/usr/bin/env python3.10
import os
import sys
import math
import uuid
import json
import color
import shutil
import platform

''' The Item data type. Used for files, directories, and whatnot. '''
class Item:
    path = ""
    name = ""
    size = ""
    type = ""
    ''' TODO: We have a few states. d = deleted, e = exists, and 0 = extinct.
              All are chars. '''
    #state = ""

DEFAULT_RECYCLE_BIN = f"{os.path.expanduser('~')}/.rb"
DEFAULT_MAX_MIB = f"{20000000000}"

def main():
    item = Item()
    ''' I have to manipulate these arguments later, so they're assigned to a
        duplicate variable. '''
    argument_list = sys.argv

    ''' Check length of arguments. '''
    if len(argument_list) < 2:
        print(f"Missing arguments. Try '{item_basename(argument_list[0])} --help' for usage information.")
        exit(1)

    argument_list, get_help, force, max_mib, recycle_bin = process_arguments(argument_list)

    ''' Call help() function if in argument list. '''
    if get_help:
        help(recycle_bin)
        exit(0)

    ''' mkdir recycle_bin if it doesn't exist. '''
    if item_type(recycle_bin) == '0':
        if mkdir(recycle_bin):
            print(f"Created directory {recycle_bin}.")
        else:
            exit(1)

    for i in argument_list[1:]:
        item.path = i
        item.type = item_type(i)
        item.name = item_basename(i)
        item.size = item_size(i)
        ''' TODO: I'll use this in the future. '''
        #item.state = ""

        if item.type == '0':
            print(f"\"{item.path}\" doesn't exist.")
            continue

        if not item.size:
            item_remove(item.path)
            print(f"Removed \"{item.path}\". Item is empty.")
            continue

        if item.size > bytes_to_gb(max_mib):
            if force or handle_max_mib(item.path, max_mib):
                item_remove(item.path)
                print(f"Removed \"{item.path}\". Size over {str(bytes_to_gb(max_mib))} GiB.")
                continue

        if not item_type(f"{recycle_bin}/{item.name}") == '0' and not force:
            item.name = handle_item_exists(item.path, recycle_bin)

        if not force:
            rename(item.name, f"{recycle_bin}/{item.name}")
            print(f"Moved \"{item.name}\" to \"{recycle_bin}/{item.name}\".")
        else:
            item_remove(item.name)
            print(f"Removed \"{item.name}\".")

def bytes_to_gb(bytes):
    bytes_to_gb = math.ceil(int(bytes) / 1024 / 1024 / 1024)
    return bytes_to_gb

def item_basename(i):
    match item_type(i):
        case 'f':
            basename = os.path.basename(i)
        case 'd':
            basename = os.path.basename(os.path.normpath(i))
        case '0':
            basename = '0'
    return basename

def handle_item_exists(item_path, recycle_bin):
    item_prefix = 0
    item_new = f"{item_prefix}_{item_basename(item_path)}"
    path = os.path.dirname(item_path)

    while os.path.exists(f"{recycle_bin}/{item_new}"):
        item_prefix += 1
        item_new = f"{item_prefix}_{item_basename(item_path)}"

    rename(item_path, f"{path}{item_new}")
    return item_new

def item_remove(i):
    return_code = '0'

    try:
        match item_type(i):
            case 'd':
                return_code = shutil.rmtree(i)
            case 'f':
                return_code = os.remove(i)
    except PermissionError:
        print(f"Can't remove {i}. Invalid permissions.")
    except OSError:
        print(f"Can't remove {i}. OSError.")

    return return_code

def rename(source, destination):
    return shutil.move(source, destination)

def mkdir(i):
    try:
        os.mkdir(i)
    except OSError as e:
        print(f"TODO HANDLE THIS : {str(e)}")
        sys.exit(1)
    return True

def handle_max_mib(item, max_mib):
    print(f"{item} is greater than {str(bytes_to_gb(max_mib))} GiB.")
    print("Would you like to fully remove it? ", end="")

    while 1:
        user_input = input().lower()

        if user_input == "y" or user_input == "yes":
            return True
        elif user_input == "n" or user_input == "no":
            return False
        else:
            pass

def item_size(i):
    size = 0

    match item_type(i):
        case "f":
            size = os.path.getsize(i)
        case "d":
            for path, dirs, files in os.walk(i):
                for f in files:
                    fp = os.path.join(path, f)
                    size += os.path.getsize(fp)
        case _:
            return
    return bytes_to_gb(size)

def item_type(i):
    if os.path.isfile(i):
        return 'f'
    elif os.path.isdir(i):
        return 'd'
    else:
        return '0'

def help(recycle_bin):
    print(f"{item_basename(sys.argv[0])} [ITEM] [ITEM2] [ITEM3] ...")
    print(f"Takes files and directories, and places them them inside of the \"{recycle_bin}\" directory.")
    print(f"By default, {item_basename(sys.argv[0])} removes directories recursively. This is unlike rm, where you must specify -r, -d, or -f flags.")

def process_arguments(arguments):
    counter = 0
    force = False
    get_help = False
    max_mib = DEFAULT_MAX_MIB
    recycle_bin = DEFAULT_RECYCLE_BIN

    for argument in arguments:
        match argument:
            case "--help" | "-h":
                get_help = True
            case "-f" | "--force":
                force = True

            case "-rb" | "--recycle-bin":
                try:
                    recycle_bin = arguments[counter+1]
                except IndexError:
                    print(f"{argument}: No recycle_bin was provided. Quitting.")
                    sys.exit(1)
            case "-m" | "--max-mib":
                try:
                    max_mib = arguments[counter+1]
                except IndexError:
                    print(f"{argument}: No max_mib was provided. Quitting.")
                    sys.exit(1)

        counter += 1

    if not recycle_bin == DEFAULT_RECYCLE_BIN:
        try: arguments.remove("-rb")
        except ValueError: pass
        try: arguments.remove("--recycle-bin")
        except ValueError: pass
        arguments.remove(recycle_bin)
    if not max_mib == DEFAULT_MAX_MIB:
        try: arguments.remove("-m")
        except ValueError: pass
        try: arguments.remove("--max-mib")
        except ValueError: pass
        arguments.remove(max_mib)

    if get_help:
        try: arguments.remove("-h")
        except ValueError: pass
        try: arguments.remove("--help")
        except ValueError: pass
    if force:
        try: arguments.remove("-f")
        except ValueError: pass
        try: arguments.remove("--force")
        except ValueError: pass
    
    return arguments, get_help, force, max_mib, recycle_bin

if __name__ == '__main__' and not platform.system() == "Windows":
    main()