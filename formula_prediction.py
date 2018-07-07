class FormulaPrediction(object):
	"""A class to hold the values of predictions for a given formula"""
		
	def __init__(self, formula, predictions=None):
		"""
		Constructor.
		
		:param formula: The chemical formula to store predictions for.
		:type formula: str
		:param predictions: a dictionary holding the predicted values of a property with the property as the key
		:type predictions: dictionary
		"""
		self.formula = formula
		self.predictions = {}
		
	
	def add_prediction(self, property, predicted_values):
		"""
		Method to hold all the predicted values for one type of prediction (e.g. liquidus temp).
		
		:param property: The name of the value predicted
		:type property: str
		:param predicted_values: The values associated with a prediction
		:type predicted_values: list
		"""
		self.predictions[property] = [predicted_values]
		
		
	def update_prediction(self, property, predicted_values):
		"""
		Method to predicted values for one type of prediction (e.g. liquidus temp) that already exists
		for the object.
		
		:param property: The name of the value predicted
		:type property: str
		:param predicted_values: The values associated with a prediction
		:type predicted_values: list
		"""
		try:
			self.predictions[property].append(predicted_values)
		except KeyError:
			raise Exception("The key %s is not listed as a predicted property for %s."%(property,self.formula))
			
			
	def retrieve_predictions(self, property):
		"""
		Method that returns the predicted values for a given property
		:param property: The property to retrieve the predicted values for
		:type property: str
		:return: The predicted values
		:rtype: list
		"""
		try:
			return self.predictions[property]
		except KeyError:
			raise Exception("The key %s is not listed as a predicted property for %s."%(property,self.formula))
			
	
	def list_predicted_props(self):
		"""
		Method that returns all the properties that have predictions stored
		:return: a list of predicted properties
		:rtype: list
		"""
		return self.predictions.keys()
