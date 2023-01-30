import pygimli as pg
import pygimli.meshtools as mt
from pygimli.viewer import showMesh
from pygimli.viewer.mpl import drawStreams, drawStreamLines

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Horizontal flow", page_icon="🌵", layout="wide")

st.title("**Two dimensional steady-state** groundwater flow")
"*****"

cols = st.columns(2)

## Domain extent
east = -100
west = 100
north = 50
south = -50
world = mt.createWorld(start = [west,north], end = [east, south])

## Zone delimitation
zone_A = mt.createPolygon([[-50,-50], [-10,-50], [20,50], [-30,50]], isClosed=True, marker = 1)
zone_B = mt.createPolygon([[-10,-50], [20,-50], [50,50], [20,50]], isClosed=True, marker = 2)
zone_C = mt.createPolygon([[-100,50], [20,50], [0,70], [-100,60]], isClosed=True, marker = 3)
geometry = world + zone_A + zone_B + zone_C

with st.sidebar:
    with st.expander("🕸️ **Meshing controls**", expanded=True):
        mesh_quality = st.slider("Mesh quality", min_value=10, max_value=40, value=34, step=1, help="Minimum angle constraint") 
        mesh_area    = st.slider("Mesh area", min_value=5, max_value=30, value=15, step=1, help="Maximum element size (global)") 

mesh = mt.createMesh(geometry, quality =mesh_quality, area=mesh_area, smooth=True)

for bound in mesh.boundaries():
    x = bound.center().x()
    y = bound.center().y()
    if x == mesh.xmin():
        bound.setMarker(-3)
    elif x == mesh.xmax():
        bound.setMarker(-4)

with cols[0]:
    "## 🕸️ Meshing"
    fig, ax = plt.subplots()
    pg.show(mesh, markers = True, showMesh = True, ax=ax)
    st.pyplot(fig)

with st.sidebar:
    with st.expander("🗺️ **Hydraulic conductivities**", expanded=True):
        K_kwargs = dict(min_value=1.0, max_value=20.0, step=0.5, help="Hydraulic conductivity (m/day)")
        K_values = [st.number_input(f"Zone {i} (m/day)", **K_kwargs, value=float(i)) for i in range(1,5)]

kMap = [[i, k] for i,k in enumerate(K_values)]
kArray_0 = pg.solver.parseMapToCellArray(list(kMap), mesh) # dict does not work
kArray = np.column_stack([kArray_0] * 3)

with cols[1]:
    "## 🗺️ Assign hydraulic conductivity"
    fig, ax = plt.subplots()
    showMesh(mesh, kMap, label='$K$ [m/day]', ax=ax)
    st.pyplot(fig)

with st.sidebar:
    with st.expander("🧱 **Set boundary conditions**", expanded=True):
        dirichletBC = {
            -3: st.number_input("Left-side head value (m)", min_value=0, max_value=100, value=60, step=1),
            -4: st.number_input("Right-side head value (m)", min_value=0, max_value=100, value=40, step=1)}

"******"
"## 🧮 Results"
with st.spinner("Solving system..."):
    h = pg.solve(mesh, a = kMap, bc={'Dirichlet': dirichletBC}, verbose = True)
    vel = -pg.solver.grad(mesh, h) * kArray

fig, ax = plt.subplots()
_ , cbar = showMesh(mesh, data=h, label='Head $h$ (m)', nLevs=11, ax=ax)
ax.set_ylabel('Depth [m]')
if st.checkbox("Show stream lines?", True):
    drawStreams(ax, mesh, vel, quiver = True)
st.pyplot(fig)