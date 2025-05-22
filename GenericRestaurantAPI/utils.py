from simpleeval import simple_eval, NameNotDefined
from decimal import Decimal

def evaluate_formula(formula: str, context: dict):
    try:
        # Agregar Decimal al contexto de evaluación
        result = simple_eval(formula, names=context, functions={
            "Decimal": Decimal,
        })
        return result
    except NameNotDefined as e:
        raise ValueError(f"Variable Not Found: {e}")
    except Exception as e:
        raise ValueError(f"Formula Error: {e}")