import math

class AbstractRule:
	def _set_grammar(self,gram):
		self._grammar = gram

class UnknownLiteralError(Exception):
	def __init__(self,literal):
		self.literal = literal
		
class ConstructorRule(AbstractRule):
	def __init__(self, *args):
		self._parameters = args
		#print (self._parameters[0])
		#print (self._parameters[1])
		self._valuation = math.inf
		
	def valuation(self):
		return self._valuation
		
	def _verif_rule(self):
		try:
			self._grammar[self._parameters[0]]
		except KeyError:
			raise UnknownLiteralError(self._parameters[0])
		try:
			self._grammar[self._parameters[1]]
		except KeyError:
			raise UnknownLiteralError(self._parameters[1])
	
	#Return true if there was no update
	def _update_valuation(self):
			#print("Valuation : Constructor")
			#print("old :"+str(self._valuation))
			self._old_val = self._valuation
			self._valuation = self._calc_valuation()
			#print("new :"+str(self._valuation))
			#print(self._old_val == self._valuation)
			return (self._old_val == self._valuation)

class UnionRule(ConstructorRule):
	def __init__(self,fst,snd):
		#print ("union")
		super().__init__(fst,snd)
	def _calc_valuation(self):
		#print ("union")
		return min(self._grammar[self._parameters[0]].valuation(),
				   self._grammar[self._parameters[1]].valuation())
				   
class ProductRule(ConstructorRule):
	def __init__(self,fst,snd,cons):
		#print("product")
		super().__init__(fst,snd)
		self._constructor = cons
	def _calc_valuation(self):
		#print("product")
		return (self._grammar[self._parameters[0]].valuation() +
			   self._grammar[self._parameters[1]].valuation())

class ConstantRule(AbstractRule):
	def __init__(self,obj):
		self._object = obj
		
	#We chose to put _update_valuation here too
	#to avoid testing the presence of the function
	#every time we want to call it on a rule
	def _update_valuation(self):
		return True
	
	def valuation(self) :
		if self._object == "":
			return 0
		else :
			return 1

class EpsilonRule(ConstantRule):
	def __init__(self,obj):
		super().__init__(obj)
	
class SingletonRule(ConstantRule):
	def __init__(self,obj):
		super().__init__(obj)
	
class CircularGrammarError(Exception):
	def __init__(self,grammar,name):
		self.name = name
		self.grammar = grammar
		
def init_grammar(gram):
	for rule in gram.values() :
		rule._set_grammar(gram)
		if isinstance(rule, ConstructorRule):
			rule._verif_rule()
	
	#As long as there's a change we update again
	#(we chose to make _update_valuation available
	#to any rule)
	"""
	while True:
		test = True
		for rule in gram.values():
			test = test and next(rule._update_valuation())
		if(test):
			break;
	"""
	while not all(rule._update_valuation() for rule in gram.values()):
		pass
	for name,rule in gram.items() :
		if rule.valuation() == math.inf :
			raise CircularGrammarError(gram,name)
	
treeGram = {"Tree" : UnionRule("Node","Leaf"),
			"Node" : ProductRule("Tree","Tree",
								 lambda a, b : Node(a, b)),
			"Leaf" : SingletonRule("Leaf")}
init_grammar(treeGram)