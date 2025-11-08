from .Exceptions import ConstraintException


####### NUMBERS #######
def constraintPositiveNumber(number: int) -> None:
	if number < 0:
		raise ConstraintException('Number cannot be negative.')


def constraintPositiveNumberInclusive(number: int) -> None:
	if number <= 0:
		raise ConstraintException('Number cannot be negative or zero.')


def constraintPourcentageNumber(number: float) -> None:
	if number < 0 or number > 1:
		raise ConstraintException('Pourcentage number cannot be negative or >1.')


def constraintPourcentageNumberExclusive(number: float) -> None:
	if number <= 0 or number > 1:
		raise ConstraintException('Pourcentage number cannot be negative or 0 or >1.')


####### TEXT #######
def constraintNotEmptyText(text: str) -> None:
	if len(text.strip()) == 0:
		raise ConstraintException('Text cannot be empty.')
