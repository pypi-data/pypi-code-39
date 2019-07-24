import json
import yaml
import os.path
import aiofiles

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

dumps = lambda x: yaml.dump(x, Dumper=Dumper, default_flow_style=False)

class Config:
    def __init__(self, filename, default={}):
        if not os.path.exists(filename):
            self.content = default
            self.default = default
            # with open(filename, 'w') as f:
            #     f.write(default)
        else:
            with open(filename,) as f:
                data = yaml.safe_load(f) or {}
                self.content = {**default, **data}
        self.filename = filename
        
    
    def write(self, prop, value):
        content = self.content
        for part in prop.split('.')[:-1]:
            content[part] = content[part] if part in content else {}
            content = content[part]
        content[prop.split('.')[-1]] = value
        with open(self.filename, 'w') as f:
            data = dumps(self.content, )
            f.write(data)

    def push(self, prop, value):
        content = self.content
        for part in prop.split('.')[:-1]:
            content[part] = content[part] if part in content else {}
            content = content[part]
        field = prop.split('.')[-1]
        if field in content:
            if isinstance(content[field], (list, tuple)):
                content[field].append(value)
            else:
                content[field] = [value]    
        else:
            content[field] = [value]
        with open(self.filename, 'w') as f:
            data = dumps(self.content, )
            f.write(data)

    def __getitem__(self, name):
        filename = self.filename
        if os.path.exists(filename):
            with open(filename,) as f:
                data = yaml.safe_load(f) or {}
                self.content = {**self.default, **data, **self.content}
        return self.content[name]
    
    def delete(self):
        try:
            os.remove(self.filename)
        except Exception:
            pass
    
    def __repr__(self):
        return 'Config(filename="' + self.filename + '", data= ' + json.dumps(self.content, indent=4, default=str) + ')\n'

async def AsyncConfig(filename, default={}):
    self = _AsyncConfig()
    if not os.path.exists(filename):
        self.content = default
        self.default = default
        # with open(filename, 'w') as f:
        #     f.write(default)
    else:
        async with aiofiles.open(filename,) as f:
            s = await f.read()
            data = yaml.safe_load(s) or {}
            self.content = {**default, **data}

    self.filename = filename
    return self

class _AsyncConfig:

    async def write(self, prop, value):
        content = self.content
        for part in prop.split('.')[:-1]:
            content[part] = content[part] if part in content else {}
            content = content[part]
        content[prop.split('.')[-1]] = value
        async with aiofiles.open(self.filename, 'w') as f:
            data = dumps(self.content, )
            await f.write(data)

    async def push(self, prop, value):
        content = self.content
        for part in prop.split('.')[:-1]:
            content[part] = content[part] if part in content else {}
            content = content[part]
        field = prop.split('.')[-1]
        if field in content:
            if isinstance(content[field], (list, tuple)):
                content[field].append(value)
            else:
                content[field] = [value]    
        else:
            content[field] = [value]
        async with aiofiles.open(self.filename, 'w') as f:
            data = dumps(self.content, )
            await f.write(data)

    def __getitem__(self, name):
        filename = self.filename
        if os.path.exists(filename):
            with open(filename,) as f:
                data = yaml.safe_load(f) or {}
                self.content = {**self.default, **data, **self.content}
        return self.content[name]
    
    async def delete(self):
        try:
            os.remove(self.filename)
        except Exception:
            pass
    
    def __repr__(self):
        return 'Config(filename="' + self.filename + '", data= ' + json.dumps(self.content, indent=4, default=str) + ')\n'

