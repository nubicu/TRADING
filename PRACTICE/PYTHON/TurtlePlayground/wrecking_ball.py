# -*- coding: utf-8 -*-
import bpy

# Wrecking ball effect in Blender Python

bpy.ops.mesh.primitive_plane_add(radius=100, location=(0, 0, 0))  # create Plane
bpy.ops.rigidbody.object_add()
bpy.context.object.rigid_body.type = 'PASSIVE'
for x in range(1, 19):  # create Toruses
    bpy.ops.mesh.primitive_torus_add(location=(0, x * 4.3, 110), rotation=(0, 1.5708 * (x % 2), 0), major_radius = 3.5,
         minor_radius =.5, abso_major_rad = 1.25, abso_minor_rad = 0.75)
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.collision_shape = 'MESH'
    if x == 1:
        bpy.context.object.rigid_body.enabled = False
    for z in range(0, 9):  # create Cubes
        bpy.ops.mesh.primitive_cube_add(radius=3, location=(x * 6 - 60, 2, 2.8 + z * 6))
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.mass = 0.0001

"""
bpy.ops.mesh.primitive_torus_add(location=(x*2, x*4.3, 110), rotation=(0,1.5708*(x%2), 0), major_radius=3.5+1*(x==18),
    minor_radius=.5+1*(x==18), abso_major_rad=1.25, abso_minor_rad=0.75)
"""

"""
Change lines 16-19 with:
for z in range(1,10):
        bpy.ops.mesh.primitive_cube_add(radius=3, location=(z*6-60,0,x*6-3))
        bpy.ops.transform.resize(value=(1, .5+10*math.cos(x/3.14)*math.sin(z/3.14),1), constraint_axis=(False, True, False))
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.mass=0.0001
"""