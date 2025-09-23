from Exceptions import ConstraintException

####### NUMBERS #######
def constraintPositiveNumber(number: int):
	if number < 0:
		raise ConstraintException('Number cannot be negative.')

def constraintPositiveNumberInclusive(number: int):
	if number <= 0:
		raise ConstraintException('Number cannot be negative or zero.')
	
####### TEXT #######
def constraintNotEmptyText(text: str):
	if len(text.strip()) == 0:
		raise ConstraintException('Text cannot be empty.')

