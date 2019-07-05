from distutils.core import setup, Extension

corewar = Extension('corewar42',
                    define_macros=[('MAJOR_VERSION', '1'),
                                   ('MINOR_VERSION', '1')],
                    include_dirs=['/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/includes',
                                  '/Users/bmiklaz/Desktop/Arena/VM_srcs/libft/includes'],

                    sources=['VM_srcs/corewar/sources/free_args.c',
                             'VM_srcs/corewar/sources/ft_custom_tools.c',
                             'VM_srcs/corewar/sources/globals.c',
                             'VM_srcs/corewar/sources/helpers.c',
                             'VM_srcs/corewar/sources/initialization.c',
                             'VM_srcs/corewar/sources/main.c',
                             'VM_srcs/corewar/sources/read_arguments.c',
                             'VM_srcs/corewar/sources/vm_game.c',
                             'VM_srcs/corewar/sources/vm_map_ops.c',
                             'VM_srcs/corewar/sources/vm_operations1.c',
                             'VM_srcs/corewar/sources/vm_operations2.c',
                             'VM_srcs/corewar/sources/vm_operations3.c',
                             'VM_srcs/corewar/sources/vm_operations4.c',
                             'VM_srcs/corewar/sources/vm_ops_methods.c',
                             'VM_srcs/corewar/sources/vm_print_dump.c',
                             'VM_srcs/corewar/sources/vm_processes_ops.c'],
                    libraries=['ft'],
                    library_dirs=['VM_srcs/libft'],
                    )

setup(name='corewar42',
      version='1.1',
      description='This is a modul with 42coreawr',
      author='bmiklaz',
      author_email='alodsta@yandex.ru',
      ext_modules=[corewar]
      )
