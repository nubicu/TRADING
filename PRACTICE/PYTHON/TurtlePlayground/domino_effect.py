# -*- coding: utf-8 -*-
import bpy
bpy.ops.mesh.primitive_plane_add(radius=145, location=(0, 0, 0))
bpy.ops.rigidbody.object_add()
bpy.context.object.rigid_body.type = 'PASSIVE'

for i in range(0, 25):
    bpy.ops.mesh.primitive_cube_add(radius=1, location=(6 * i, 0, 10))
    bpy.ops.rigidbody.object_add()
    bpy.ops.transform.resize(value=(1, 6, 10), constraint_axis=(False, True, True))
    if i == 0:
        bpy.ops.transform.rotate(value=0.4, axis=(0, 1, 0))