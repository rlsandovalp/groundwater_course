import numpy as np
import matplotlib.pyplot as plt
import pygimli as pg
import pygimli.meshtools as mt
from pygimli.viewer.mpl import drawStreams

world = mt.createWorld(start=[-20, 0], end=[20, -16], layers=[-2, -8],
                       worldMarker=False)

# Merge geometrical entities
geom = world
pg.show(geom, markers=True)

mesh = mt.createMesh(geom, quality=33, area=5)
pg.show(mesh)

kMap = {1: 1.0, 2: 1.0, 3: 1.0}
kArray = pg.solver.parseMapToCellArray(list(kMap), mesh)

print (kArray)

kArray = np.column_stack([kArray] * 3)
print (kArray)



h = pg.solver.solveFiniteElements(mesh, kMap, bc={'Dirichlet': {1: 1.0, 2: 1.0, 3: 1.0, 5: 0.0, 6: 0.0, 7: 0.0}}, verbose=True)
v = -pg.solver.grad(mesh, h) * kArray
ax, _ = pg.show(mesh, data=h, label='Temperature $T$',
                cMap="hot_r", nCols=8, contourLines=True)

drawStreams(ax, mesh, v, color='green', quiver=True)

pg.wait()
# ax, _ = pg.show(mesh, data=v, label='Velocity $v$')
