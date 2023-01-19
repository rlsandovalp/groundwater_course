import numpy as np
import pygimli as pg
import pygimli.meshtools as mt
from pygimli.viewer.pv import drawStreamLines, drawSlice, drawMesh

rect1 = mt.createRectangle(start=[0, 0], end=[100, 30], marker = 1)
rect2 = mt.createRectangle(start=[0, 30], end=[100, 50], marker = 2)

rect = rect1 + rect2

mesh = mt.createMesh(rect, quality=33, area=20)

for bound in mesh.boundaries():
    x = bound.center().x()
    if x == mesh.xmin():
        bound.setMarker(1)
    elif x == mesh.xmax():
        bound.setMarker(2)

for bound in mesh.boundaries():
    y = bound.center().y()
    if y == mesh.ymin():
        bound.setMarker(3)
    elif y == mesh.ymax():
        bound.setMarker(4)


kMap = {1: 1e-4, 2: 1e-6}
kArray = pg.solver.parseMapToCellArray(list(kMap), mesh)
kArray = np.column_stack([kArray] * 3)

bc = {"Dirichlet": {1: 20.0, 2: 5.0}}

h = pg.solver.solveFiniteElements(mesh, kMap, bc=bc)
vel = -pg.solver.grad(mesh, h) * kArray

pg.show(mesh, h, label="Hydraulic head (m)")

# ax, _ = pg.show(mesh, alpha=0.8, hold=True, colorBar=False)

# ax.show()
