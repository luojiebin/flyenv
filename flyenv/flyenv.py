#!/usr/bin/env python

#######################################################################
#
# flyenv - a tool helps manage environment variable portably and safely
# written by luojiebin (luo.jiebin@foxmail.com)
#
#######################################################################

import argparse
import os
import warnings
from Crypto.Cipher import AES


IV = '\xa9{+^\xfa\xf4hB2E\xc2\x08\xca\xa0\x16\xe8'
ENV_FILE = 'flyenv.txt'
ENV_ENCRYPT_FILE = 'flyenv_encrypt.txt'


def _parse_file(file):
    pairs = {}
    with open(file, 'r') as f:
        for line in f.readlines():
            if line.strip() and not line.strip().startswith('#'):
                key, val = line.strip().split('=')
                pairs[key] = val
    return pairs


def get_env(key):
    msg = 'Please set environment variable: {key}.'.format(key=key)
    try:
        pairs = _parse_file(ENV_FILE)
        return pairs.get(key, None) or os.environ[key]
    except KeyError:
        raise KeyError(msg)


def _dump_file(pairs):
    with open(ENV_FILE, 'w') as f:
        for key, value in sorted(pairs.items()):
            f.write('{key}={value}\n'.format(key=key, value=value))


def set_env(key, val):
    pairs = _parse_file(ENV_FILE)
    pairs[key] = val
    os.environ[key] = val
    _dump_file(pairs)


def _get_env_string(file):
    env_string = ''
    with open(file, 'r') as f:
        for line in f.readlines():
            if line.strip() and not line.strip().startswith('#'):
                env_string += line
    print(env_string)
    return env_string


def encrypt_env(key, iv=IV):
    env_string = _get_env_string(ENV_FILE)
    os.rename(ENV_FILE, ENV_ENCRYPT_FILE)

    try:
        cipher = AES.new(key, AES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(env_string)
        with open(ENV_ENCRYPT_FILE, 'w') as f:
            f.write(ciphertext)
    except ValueError:
        os.rename(ENV_ENCRYPT_FILE, ENV_FILE)
        raise


def encrypt_env_command(args):
    key = args.key
    encrypt_env(key)


def _get_encrypted_env(file):
    encrypted_env = ''
    with open(ENV_ENCRYPT_FILE, 'r') as f:
        encrypted_env = f.read()
    return encrypted_env


def decrypt_env(key, iv=IV):
    encrypted_env = _get_encrypted_env(ENV_ENCRYPT_FILE)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted_env = cipher.decrypt(encrypted_env)
    os.rename(ENV_ENCRYPT_FILE, ENV_FILE)
    with open(ENV_FILE, 'w') as f:
        f.write(decrypted_env)


def decrypt_env_command(args):
    key = args.key
    decrypt_env(key)


def clear(args):
    pairs = _parse_file(ENV_FILE)
    for key in pairs.keys():
        pairs[key] = ''
        os.environ[key] = ''
    _dump_file(pairs)


def _required_environment_variable(args):
    pairs = _parse_file(ENV_FILE)
    return sorted(key for key, val in pairs.items() if val == '')


def required_environment_variable_print(args):
    keys = _required_environment_variable(args)
    for key in keys:
        print(key)


def set(args):
    pair_dict = {}
    for p in args.pairs:
        key, val = p.strip().split('=')
        pair_dict[key] = val

    with open(ENV_FILE, 'a') as f:
        pairs = _parse_file(ENV_FILE)
        flag = False
        for key, value in pair_dict.items():
            os.environ.setdefault(key, value)
            if key in pairs and pairs[key] != value:
                pairs[key] = value
                flag = True
            else:
                f.write('{key}={value}\n'.format(key=key, value=value))
        if flag:
            _dump_file(pairs)


def unset(args):
    pairs = _parse_file(ENV_FILE)
    for key in args.keys:
        if key in pairs:
            pairs[key] = ''
            os.environ.pop(key, None)
        else:
            warnings.warn("environment variable {key} not setted".format(key))
    _dump_file(pairs)


def delete(args):
    pairs = _parse_file(ENV_FILE)
    for key in args.keys:
        if key in pairs:
            pairs.pop(key)
            os.environ.pop(key, None)
        else:
            warnings.warn("environment variable {key} not setted".format(key))
    _dump_file(pairs)


def _get(args):
    pairs = _parse_file(ENV_FILE)
    return pairs.get(args.key, None) or os.environ.get(args.key)


def get_print(args):
    print(_get(args))


def _list_env(args):
    pairs = _parse_file(ENV_FILE)
    return sorted('{key}={val}'.format(key=key, val=val) for key, val in pairs.items())


def list_env_print(args):
    pairs = _list_env(args)
    for pair in pairs:
        print(pair)


def load(args):
    pairs = _parse_file(ENV_FILE)
    for key, val in pairs.items():
        os.environ[key] = val


def get_parser():
    parser = argparse.ArgumentParser(
        description='a tool helps manage environment variable portably and safely')
    subparsers = parser.add_subparsers(dest='subparser_name')

    # set command
    parser_set = subparsers.add_parser('set',
                                       description='set one or more environment variable')
    parser_set.add_argument('pairs',
                            type=str,
                            nargs='+',
                            help='key, value pairs of environment variables to add')
    parser_set.set_defaults(func=set)

    # unset command
    parser_unset = subparsers.add_parser('unset',
                                         description='delete one or more environment variable')
    parser_unset.add_argument('keys',
                              type=str,
                              nargs='+',
                              help='keys of environment variables to remove')
    parser_unset.set_defaults(func=unset)

    # delete command
    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('keys',
                               type=str,
                               nargs='+',
                               help='keys of environment variables to delete')
    parser_delete.set_defaults(func=delete)

    # get command
    parser_get = subparsers.add_parser('get')
    parser_get.add_argument('key',
                            type=str,
                            help='key of environment variable to get')
    parser_get.set_defaults(func=get_print)

    # list command
    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(func=list_env_print)

    # require command
    parser_require = subparsers.add_parser('require')
    parser_require.set_defaults(func=required_environment_variable_print)

    # clear command
    parser_clear = subparsers.add_parser('clear')
    parser_clear.set_defaults(func=clear)

    # load command
    parser_load = subparsers.add_parser('load')
    parser_load.set_defaults(func=load)

    # encrypt env
    parser_encrypt = subparsers.add_parser('encrypt')
    parser_encrypt.add_argument('key',
                                type=str,
                                help='key of the cipher')
    parser_encrypt.set_defaults(func=encrypt_env_command)

    # decrypt env
    parser_decrypt = subparsers.add_parser('decrypt')
    parser_decrypt.add_argument('key',
                                type=str,
                                help='key of the cipher')
    parser_decrypt.set_defaults(func=decrypt_env_command)

    return parser


def flyenv(args):
    if args.subparser_name != 'decrypt' and not os.path.exists(ENV_FILE):
        warnings.warn('Please create flyenv.txt first!')
    else:
        args.func(args)


def command_line_runner():
    parser = get_parser()
    args = parser.parse_args()

    flyenv(args)


if __name__ == '__main__':
    command_line_runner()
