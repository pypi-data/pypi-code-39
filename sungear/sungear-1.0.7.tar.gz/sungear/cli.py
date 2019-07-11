import svgwrite
from svgwrite.text import Text
from svgwrite.shapes import Circle

drawing = svgwrite.Drawing(width=1000, height=1000)
t = Text("test", insert=(100, 100))
print(dir(t))
drawing.add(t)
drawing.add(Circle(center=(100, 100), r=1, fill='red'))

with open('test.svg', 'w') as f:
    drawing.write(f)
