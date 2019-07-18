#! /bin/env python

import os
import sys
import codecs
try:
    import yaml
except:
    print("\n\nNot found pyyaml, please install: \nsudo pip install pyyaml")
    sys.exit(0)

# toolchains options
CROSS_TOOL_PATH   = '/opt/gcc-csky-abiv2/bin'

class Build(object):
    def __init__(self, tool):
        self.conf = tool
        self.env = tool.env.Clone()
        self.YOC_SDK = tool.YOC_SDK
        self.BUILD = 'release'
        self.INSTALL_PATH = tool.INSTALL_PATH
        self.lib_path = tool.lib_path
        self.yoc_lib_path = os.path.join(tool.YOC_SDK, "lib/" + self.conf.CHIP + '/' + self.conf.CPU)

        self.env.Replace(
            AS   = self.conf.AS, ASFLAGS = self.conf.AFLAGS,
            CC   = self.conf.CC, CCFLAGS = self.conf.CFLAGS,
            CXX  = self.conf.CXX, CXXFLAGS = self.conf.CXXFLAGS,
            AR   = self.conf.AR, ARFLAGS = '-rc',
            LINK = self.conf.LINK, LINKFLAGS = self.conf.LDFLAGS
        )

        self.env.PrependENVPath('TERM', "xterm-256color")
        self.env.PrependENVPath('PATH', os.getenv('PATH'))

        self.def_includes = [
            'boards/' + self.conf.BOARD + '/include',
            'include/csi/chip/' + self.conf.CHIP,
            'include',
            'include/csi',
            'include/rhino',
        ]
        for p in self.def_includes:
            path_name = os.path.join(self.YOC_SDK, p)
            self.env.Append(CPPPATH=[path_name])

    def SetInstallPath(self, path):
        if not path:
            path = self.YOC_SDK
        self.INSTALL_PATH = path
        self.lib_path = os.path.join(path, "lib/" + self.conf.CHIP + '/' + self.conf.CPU)

    def library(self, name, src, **parameters):
        group = parameters

        objs = None

        if name and src:
            if 'CCFLAGS' in group:
                self.env.AppendUnique(CCFLAGS = ' ' + group['CCFLAGS'])
            if 'CPPPATH' in group:
                if type(group['CPPPATH']) == type('str'):
                    self.env.AppendUnique(CPPPATH=group['CPPPATH'])
                else:
                    for path in group['CPPPATH']:
                        self.env.AppendUnique(CPPPATH=path)

            if 'CPPFLAGS' in group:
                self.env.AppendUnique(CPPFLAGS=' ' + group['CPPFLAGS'])
            objs = self.env.StaticLibrary(name, src)

        jobs = []
        if objs:
            jobs += objs
            jobs += self.env.Install(self.lib_path, objs)

        if 'INSTALL' in group:
            for item in group['INSTALL']:
                if len(item) == 2:
                    inc_path = os.path.join(self.INSTALL_PATH, item[0])
                    jobs += self.env.Install(inc_path, item[1])

        self.env.Default(jobs)

        return objs

    def load_package(self):
        filename = 'package.yaml'
        if not os.path.exists(filename):
            return None

        with codecs.open(filename, encoding='utf-8') as fh:
            text = fh.read()
            try:
                conf = yaml.safe_load(text)

                source = []
                installs = []
                incs = []
                cflags = ''
                cppflags = ''
                asmflags = ''
                defines = ''
                libs = []


                name = conf['name']
                for src in conf['source_file']:
                    for f in self.env.Glob(src):
                        source.append(f)

                if 'build_config' in conf:
                    build_conf = conf['build_config']
                    if 'include' in build_conf:
                        incs = build_conf['include']

                    if 'libs' in build_conf:
                        libs = build_conf['libs']

                    if 'cflag' in build_conf:
                        cflags = build_conf['cflag']

                    if 'cxxflag' in build_conf:
                        cppflags = build_conf['cxxflag']


                    if 'asmflag' in build_conf:
                        asmflags = build_conf['asmflag']

                    if 'define' in build_conf:
                        for d in build_conf['define']:
                            defines += ' -D' + d

                if 'install' in conf:
                    for ins in conf['install']:
                        dest = ins['dest']
                        for src in ins['source']:
                            v = (dest, self.env.Glob(src))
                            installs.append(v)


                cflags += defines
                cppflags += defines

                package = {}

                package['name']     = name
                if source:
                    package['source'] = source

                if cflags:
                    package['CCFLAGS'] = cflags

                if cppflags:
                    package['CPPFLAGS'] = cppflags

                if incs:
                    package['CPPPATH'] = incs

                if source:
                    package['LIBS'] = libs

                if installs:
                    package['INSTALL'] = installs

                return package
            except Exception as e:
                print(str(e))
        return None


    def program(self, name, source, **parameters):
        if 'CPPPATH' in parameters:
            for path in parameters['CPPPATH']:
                self.env.AppendUnique(CPPPATH=path)
            del parameters['CPPPATH']

        parameters['LIBPATH'] = self.yoc_lib_path + ':' + self.lib_path

        linkflags =  ' -Wl,--whole-archive -l' + ' -l'.join(parameters['LIBS'])
        linkflags += ' -Wl,--no-whole-archive -nostartfiles -Wl,--gc-sections -lm -T boards/fangtang_cpu0/configs/gcc_eflash.ld'
        linkflags += ' -Wl,-ckmap="yoc.map" -Wl,-zmax-page-size=1024'



	# $(CPRE) $(CC) -o $@.elf -Wl,--whole-archive $^ $(YOC_LIBS:%=-l%) $(THIRD_PARTY_LIBS) -Wl,--no-whole-archive $(L_LDFLAGS) -Wl,-zmax-page-size=1024


        self.env.AppendUnique(LINKFLAGS=linkflags)

        del parameters['LIBS']

        v = self.env.Program(target=name, source=source, **parameters)

        self.env.Default(v)

class DefaultConfig(object):
    def __init__(self, env, YOC_SDK):
        self.YOC_SDK = YOC_SDK
        self.env = env
        self.INSTALL_PATH = self.YOC_SDK

        self.CROSS_TOOL_PATH = CROSS_TOOL_PATH
        self.PREFIX  = 'csky-elfabiv2-'
        self.CC      = self.PREFIX + 'gcc'
        self.CXX     = self.PREFIX + 'g++'
        self.AS      = self.PREFIX + 'gcc'
        self.AR      = self.PREFIX + 'ar'
        self.LINK    = self.PREFIX + 'g++'
        self.SIZE    = self.PREFIX + 'size'
        self.OBJDUMP = self.PREFIX + 'objdump'
        self.OBJCPY  = self.PREFIX + 'objcopy'
        self.STRIP   = self.PREFIX + 'strip'
        self.CFLAGS = '-MP -MMD '
        self.DEBUG = 'release'
        self.def_incs = []

        self.conf = {}

        self.load_config('defconfig')
        self.SetInstallPath(self.YOC_SDK)

    def GenConfig(self):
        config_file = os.path.join(self.YOC_SDK, 'include/yoc_config.h')
        if self.save_yoc_config(config_file):
            config_file = os.path.join(self.YOC_SDK, 'include/csi_config.h')
            self.save_csi_config(config_file)

    def SetInstallPath(self, path):
        if not path:
            path = self.YOC_SDK
        self.INSTALL_PATH = path
        self.lib_path = os.path.join(path, "lib/" + self.CHIP + '/' + self.CPU)

    def yoc_path(self, path):
        return os.path.join(self.YOC_SDK, path)

    def load_config(self, conf_file):
        try:
            f = open(conf_file, 'r')
            contents = f.readlines()
            f.close()


            for line in contents:
                line = line.strip()
                if len(line) > 0 and line[0] != "#":
                    kv = line.split('=')
                    if len(kv) >= 2:
                        self.conf[kv[0]] = kv[1]
                        if kv[0] == 'CONFIG_CHIP_NAME':
                            self.CHIP = eval(kv[1])
                        elif kv[0] == 'CONFIG_BOARD_NAME':
                            self.BOARD = eval(kv[1])
                        elif kv[0] == 'CONFIG_VENDOR_NAME':
                            self.VENDOR = eval(kv[1])
                        elif kv[0][:10] == 'CONFIG_CPU':
                            self.CPU = kv[0][11:].lower()

            self.set_cpu()

            # print(self.CHIP, self.BOARD, self.VENDOR, self.CPU)
        except :
            print("Open defconfig file failed.")

        if not self.CHIP:
            print("no defind `CONFIG_CHIP_NAME` in defconfig")
            exit(-1)

        if not self.BOARD:
            print("no defind `CONFIG_BOARD_NAME` in defconfig")
            exit(-1)

        if not self.VENDOR:
            print("no defind `CONFIG_VENDOR_NAME` in defconfig")
            exit(-1)


    def save_csi_config(self, filename):
        text = '''/* don't edit, auto generated by tools/toolchain.py */

#ifndef __CSI_CONFIG_H__
#define __CSI_CONFIG_H__

#include <yoc_config.h>

#endif

'''
        try:
            p = os.path.dirname(filename)
            try:
                os.makedirs(p)
            except:
                pass

            with open(filename, 'w') as f:
                f.write(text)
                print("Generate %s done!" % filename)
        except:
            print("Generate %s file failed." % filename)


    def save_yoc_config(self, filename):
        contents = ""

        try:
            with open(filename, 'r') as f:
                contents = f.read()
        except:
            pass


        text = '''/* don't edit, auto generated by tools/toolchain.py */\n
#ifndef __YOC_CONFIG_H__
#define __YOC_CONFIG_H__\n\n'''
        for (k,v) in self.conf.items():
            if v.lower() == 'y':
                text += '#define %s 1\n' % k
            elif v.lower() == 'n':
                text += '// #define %s 1\n' % k
            else:
                text += '#define %s %s\n' % (k, v)
        text += '\n#endif\n'

        if text == contents:
            return False

        try:
            p = os.path.dirname(filename)
            try:
                os.makedirs(p)
            except:
                pass

            with open(filename, 'w') as f:
                f.write(text)
                print("Generate %s done!" % filename)
            return True
        except:
            print("Generate %s file failed." % filename)

    def __getattr__(self, name):
        if name in self.conf:
            return self.conf[name]
        else:
            return None

    def set_cpu(self):
        if self.CPU in ['ck801', 'ck802', 'ck803', 'ck805']:
            DEVICE = '-mcpu=' + self.CPU
        elif self.CPU in ['ck803f', 'ck803ef', 'ck803efr1', 'ck803efr2', 'ck803efr3', 'ck804ef', 'ck805f']:
            DEVICE = '-mcpu=' + self.CPU + ' -mhard-float'
            if self.CPU == 'ck803ef':
                DEVICE += ' -mhigh-registers -mdsp'
        else:
            print ('Please make sure your cpu mode')
            exit(0)


        self.CFLAGS  = '-MP -MMD ' + DEVICE
        self.AFLAGS  = ' -c ' + DEVICE
        self.LDFLAGS  = DEVICE

        if self.BUILD == 'debug':
            self.CFLAGS += ' -O0 -g'
        else:
            self.CFLAGS += ' -Os'

        self.CXXFLAGS = self.CFLAGS

        if self.CPU in ['ck803ef', 'ck803efr1']:
            self.config_ck803efr1()

        elif self.CPU in ['ck804ef','ck805','ck805f']:
            self.config_ck804ef()

    def config_ck803efr1(self):
        config = \
            ' -ffunction-sections -fdata-sections' + \
            ' -g -Wpointer-arith -Wundef -Wall -Wl,-EL' + \
            ' -fno-inline-functions -nostdlib -fno-builtin -mistack' + \
            ' -fno-strict-aliasing -fno-strength-reduce'

        self.CFLAGS += config
        self.CXXFLAGS += config


    def config_ck804ef(self):
        config = \
            ' -ffunction-sections -fdata-sections' + \
            ' -g -Wpointer-arith -Wundef -Wall -Wl,-EL' + \
            ' -fno-inline-functions -nostdlib -fno-builtin -mistack' + \
            ' -fno-strict-aliasing -fno-strength-reduce'

        self.CFLAGS += config
        self.CXXFLAGS += config

    def build(self):
        return Build(self)

    def library(self, name, src, **parameters):
        build = Build(self)
        build.library(name, src, **parameters)

    def library_yaml(self):
        build = Build(self)
        pack = build.load_package()
        if pack:
            name = pack['name']
            source = pack['source']
            del pack['name']
            del pack['source']

            build.library(name, source, **pack)

    def program(self, **parameters):
        build = Build(self)
        pack = build.load_package()

        if pack:
            name = pack['name']
            source = pack['source']
            del pack['name']
            del pack['source']

            build.program(name, source, **pack)


def main():
    if len(sys.argv) >= 2:
        sdk = sys.argv[1]
    else:
        sdk = 'yoc_sdk'
    conf = DefaultConfig(None, sdk)
    conf.GenConfig()

if __name__ == "__main__":
    main()
