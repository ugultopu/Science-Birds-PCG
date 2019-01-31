OBJECT_STRING = '<{} type="{}" material="{}" x="{}" y="{}" {}/>\n'
addition_x = -4
addition_y = -3.4

def get_object_string(object_type, shape_type, lateral_distance, vertical_distance, block_material = '', spining = 0):
	rotation = 'rotation="'+str(spining)+'"' if spining != -1 else ""
	return OBJECT_STRING.format(object_type,
															shape_type,
			                        block_material,
			                        round(lateral_distance+addition_x,3),
			                        round(vertical_distance+addition_y,3),
			                        rotation)
