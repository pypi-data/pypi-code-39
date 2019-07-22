import moderngl
import numpy as np
import pyprojector


class RTexture:
    def __init__(self, size, layers, texture):
        self.size = size
        self.layers = layers
        self.texture = texture


class RTiles:
    def __init__(self, texture, vbo, vao):
        self.texture = texture
        self.vbo = vbo
        self.vao = vao
        self.vertices = 0

    def update(self, data):
        data = bytes(data)
        self.vbo.write(data)
        self.vertices = len(data) // 12

    def render(self):
        self.texture.texture.use()
        self.vao.program['Tile'].value = self.texture.size
        self.vao.render(moderngl.POINTS, self.vertices)


class Tiles:
    def __init__(self, width, height, unit, title='', fps=60):
        self.unit = unit
        self.wnd = pyprojector.window((width, height), title, fps=fps)
        self.ctx = moderngl.create_context()
        self.fbo = self.ctx.simple_framebuffer(self.wnd.size)
        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec3 in_vert;
                void main() {
                    gl_Position = vec4(in_vert, 0.0);
                }
            ''',
            geometry_shader='''
                #version 330
                layout(points) in;
                layout(triangle_strip, max_vertices=4) out;
                uniform vec2 Screen;
                uniform vec2 Tile;
                out vec3 g_text;
                void main() {
                    vec2 pos = gl_in[0].gl_Position.xy;
                    float t = gl_in[0].gl_Position.z;
                    gl_Position = vec4((pos + vec2(-Tile.x, -Tile.y)) * Screen, 0.0, 1.0);
                    g_text = vec3(0.0, 1.0, t);
                    EmitVertex();
                    gl_Position = vec4((pos + vec2(-Tile.x, Tile.y)) * Screen, 0.0, 1.0);
                    g_text = vec3(0.0, 0.0, t);
                    EmitVertex();
                    gl_Position = vec4((pos + vec2(Tile.x, -Tile.y)) * Screen, 0.0, 1.0);
                    g_text = vec3(1.0, 1.0, t);
                    EmitVertex();
                    gl_Position = vec4((pos + vec2(Tile.x, Tile.y)) * Screen, 0.0, 1.0);
                    g_text = vec3(1.0, 0.0, t);
                    EmitVertex();
                    EndPrimitive();
                }
            ''',
            fragment_shader='''
                #version 330
                uniform sampler2DArray Sampler;
                in vec3 g_text;
                out vec4 f_color;
                void main() {
                    f_color = texture(Sampler, g_text);
                }
            ''',
        )

        self.prog['Screen'].value = (2.0 * unit / width, -2.0 * unit / height)

    def tiles_texture(self, images=None):
        size = images[0].size
        if images is not None:
            data = bytearray()
            layers = len(images)
            for img in images:
                data += img.convert('RGBA').tobytes()
        if data is not None:
            layers = len(data) // (size[0] * size[1] * 4)
        texture = self.ctx.texture_array((*size, layers), 4, data)
        scale = (size[0] / 2.0 / self.unit, size[1] / 2.0 / self.unit)
        return RTexture(scale, layers, texture)

    def tiles(self, texture, reserve=0):
        vbo = self.ctx.buffer(reserve=reserve * 48)
        vao = self.ctx.simple_vertex_array(self.prog, vbo, 'in_vert')
        return RTiles(texture, vbo, vao)

    def clear(self, color=(0.0, 0.0, 0.0, 0.0)):
        self.fbo.clear(*color)
        self.ctx.enable_only(moderngl.BLEND)
        self.fbo.use()

    def flush(self):
        self.wnd.update(self.fbo.glo)
