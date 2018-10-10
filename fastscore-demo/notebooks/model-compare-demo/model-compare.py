# fastscore.schema.0: double
# fastscore.schema.2: double
# fastscore.slot.1: in-use
# fastscore.module-attached: ModelCompareClass

import numpy as np
from ModelCompareClass.ModelCompare import ModelCompare

mc = ModelCompare()
scores = [{}] #TODO: Change 2 to get number of models from user.
scores.append({})
		
def action(datum, i, seq_num):
	global mc
	global scores
	if i == 2 or i == 0:
		scores[i/2][seq_num] = datum	
	if all(seq_num in score for score in scores):
		mc.update(scores[0][seq_num], scores[1][seq_num])
#	if i == 4 and datum == '#':
		yield mc.to_dict()
