flyenv
=============================================================
a tool helps manage environment variable portably and safely
-------------------------------------------------------------

Installation
------------

::
    pip install pycrypto
    
    pip install flyenv


Usage
-----

::

    usage: flyenv.py [-h]
                     {set,unset,delete,get,list,require,clear,load,encrypt,decrypt}
                     ...

    a tool helps manage environment variable portably and safely

    positional arguments:
      {set,unset,delete,get,list,require,clear,load,encrypt,decrypt}

    optional arguments:
      -h, --help            show this help message and exit


Usage in Django or Flask or others
----------------------------------
1. In the same directory with manage.py, create a file name "flyenv.txt", then you can add environment variables in this file directly with this format "name=value", one key-value
   pair a line, this file allow empty lines and comment lines starts with "#". You can also set environment variables in the command line.

2. In any source file you want to use environment variables

::

    from flyenv import set_env, get_env

    set_env(name, val)
    get_env(name)

3. You can encrypt your env file to protect sensitive data.
   In the command line:

::

    $flyenv encrypt secret_key[a string with length 16]

flyenv will remove "flyenv.txt" and generate a file name "flyenv_encrypt.txt" with encrypted environment variables in it.
Then you can add this file to your git repository.

4. When you want to use the encrypted environment variables, you can decrypt the file in command line:

::

   flyenv descrypt secret_key[a string with length 16]
