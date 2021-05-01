import bpy
import math

class AddSplitFlap(bpy.types.Operator):
	bl_idname = "maki.add_split_flap"
	bl_label = "Add Split Flap"
	bl_options = {"REGISTER", "UNDO", "INTERNAL"}

	def execute(self, context):
		# set to view 3d and 0,0,0
		bpy.context.area.type = "VIEW_3D"
		bpy.context.scene.cursor.location[0] = 0.0
		bpy.context.scene.cursor.location[1] = 0.0
		bpy.context.scene.cursor.location[2] = 0.0

		# set framerate to 60 and end frame to 1048574
		bpy.context.scene.render.fps = 60
		bpy.context.scene.frame_end = 1048574
		# bpy.context.scene.rigidbody_world.point_cache.frame_end = 1048574

		# create cylinder
		bpy.ops.mesh.primitive_cylinder_add(
		    vertices=128,
		    radius=1.0,
		    depth=2.0,
		    calc_uvs=False,
		    location=(0.0, 0.0, 0.0),
		    rotation=(math.pi / 2, 0.0, 0.0),
		    scale=(0.9, 0.9, 1.0)
		)
		cylinder = bpy.context.active_object

		bpy.ops.rigidbody.objects_add(type="PASSIVE")
		cylinder.rigid_body.kinematic = True
		cylinder.rigid_body.mass = 1  # kg

		# animate cylinder
		cylinder.keyframe_insert(data_path="rotation_euler", frame=1)

		iterations = 2
		duration = 5  # seconds

		cylinder.rotation_euler = (math.pi / 2, math.pi * 2 * iterations, 0.0)
		cylinder.keyframe_insert(
		    data_path="rotation_euler", frame=60 * duration * iterations
		)

		for fcurve in cylinder.animation_data.action.fcurves:
			for keyframe in fcurve.keyframe_points:
				keyframe.interpolation = "LINEAR"

		# create supports
		bpy.ops.mesh.primitive_cube_add(
		    size=2.0,
		    calc_uvs=False,
		    location=(0.6, 0, 1.88),
		    rotation=(0, 0, 0),
		    scale=(0.227, 2, 2),
		)
		support = bpy.context.active_object
		support.name = "Support"

		bpy.ops.rigidbody.objects_add(type="PASSIVE")

		# create flaps
		total_flaps = 36

		for i in range(total_flaps):
			# create hinge (empty)
			bpy.ops.object.empty_add(
			    type="PLAIN_AXES",
			    radius=0.5,
			    location=(0, 0, 0.5),
			    rotation=(0, math.pi / 2, math.pi / 2)
			)
			hinge = bpy.context.active_object
			hinge.name = "Flap Hinge " + str(i + 1)

			bpy.ops.rigidbody.constraint_add(type="HINGE")
			hinge.rigid_body_constraint.disable_collisions = False

			# create flap
			bpy.ops.mesh.primitive_cube_add(
			    size=2.0,
			    calc_uvs=False,
			    location=(0, 0, 1),
			    rotation=(0, 0, 0),
			    scale=(0.02, 1, 1),
			)
			flap = bpy.context.active_object
			flap.name = "Flap Mesh " + str(i + 1)

			bpy.ops.rigidbody.objects_add(type="ACTIVE")
			flap.rigid_body.collision_shape = "BOX"
			# flap.rigid_body.friction = 1

			# bevel flap
			# bpy.ops.object.modifier_add.bevel(
			#     offset=0.1,
			#     segments=3,
			# )
			# bpy.ops.object.modifier_add(type="BEVEL")
			# print(flap.modifiers)

			# link cylinder and flap to hinge
			hinge.rigid_body_constraint.object1 = cylinder
			hinge.rigid_body_constraint.object2 = flap

			# rotate into place
			bpy.ops.object.select_all(action="DESELECT")
			flap.select_set(True)
			hinge.select_set(True)

			bpy.ops.transform.rotate(
			    value=(math.pi * 2) / total_flaps * i,
			    orient_axis="Y",
			    center_override=(0, 0, 0),
			)

		return {"FINISHED"}