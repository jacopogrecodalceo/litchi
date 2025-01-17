def db2amp(db):
	max_val = 0
	min_val = -33
	return (db - min_val) / (max_val - min_val)

def amp2db(amp):
    max_val = 0
    min_val = -33
    return amp * (max_val - min_val) + min_val

def find_nearest(target, values):
    return min(values, key=lambda x: abs(x - target))

