class Event():
	"""Event structure"""
	def __init__(self, user="", msg="", target="", event_type=""):
		self.user = user
		self.msg = msg
		self.target = target
		self.event_type = event_type
