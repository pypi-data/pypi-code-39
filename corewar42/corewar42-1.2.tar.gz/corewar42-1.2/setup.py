from distutils.core import setup, Extension

corewar = Extension('corewar42',
                    include_dirs=['/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/includes',
                                  '/Users/bmiklaz/Desktop/Arena/VM_srcs/libft/includes'],

                    sources=['/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/free_args.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/ft_custom_tools.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/globals.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/helpers.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/initialization.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/main.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/read_arguments.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/vm_game.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/vm_map_ops.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/vm_operations1.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/vm_operations2.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/vm_operations3.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/vm_operations4.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/vm_ops_methods.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/vm_print_dump.c',
                             '/Users/bmiklaz/Desktop/Arena/VM_srcs/corewar/sources/vm_processes_ops.c'],
                    libraries=['ft'],
                    library_dirs=['/Users/bmiklaz/Desktop/Arena/VM_srcs/libft'],
                    )

setup(name='corewar42',
      version='1.2',
      description='This is a modul with 42coreawr',
      author='bmiklaz',
      author_email='alodsta@yandex.ru',
      ext_modules=[corewar]
      )
