import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):

	return ''.join(random.choice(chars) for x in range(size))