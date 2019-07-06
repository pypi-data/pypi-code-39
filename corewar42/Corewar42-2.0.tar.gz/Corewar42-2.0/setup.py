from distutils.core import setup, Extension
import os

corewar = Extension('Corewar42',
                    include_dirs=['/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/includes',
                                  '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/libft/includes'],

                    sources=['/Users/' + os.getlogin() + '/Desktop/Arena/corewar_modul.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/free_args.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/ft_custom_tools.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/globals.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/helpers.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/initialization.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/main.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/read_arguments.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/vm_game.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/vm_map_ops.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/vm_operations1.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/vm_operations2.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/vm_operations3.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/vm_operations4.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/vm_ops_methods.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/vm_print_dump.c',
                             '/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/corewar/sources/vm_processes_ops.c'],
                    libraries=['ft'],
                    library_dirs=['/Users/' + os.getlogin() + '/Desktop/Arena/VM_srcs/libft'],
                    )

setup(name='Corewar42',
      version='2.0',
      description='This is a modul with 42coreawr',
      author='bmiklaz',
      author_email='alodsta@yandex.ru',
      ext_modules=[corewar]
      )
