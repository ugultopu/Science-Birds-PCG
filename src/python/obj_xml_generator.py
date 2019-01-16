OBJECT_STRING = '<{} type="{}" material="{}" x="{}" y="{}" {}/>\n'

def get_object_string(object_type, shape_type, lateral_distance, vertical_distance, block_material = '', spining = 0):
	rotation = 'rotation="'+str(spining)+'"' if spining != -1 else ""
	return OBJECT_STRING.format(object_type,
															shape_type,
			                        block_material,
			                        round(lateral_distance,3),
			                        round(vertical_distance,3),
			                        rotation)
