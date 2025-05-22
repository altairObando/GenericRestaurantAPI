from simpleeval import simple_eval, NameNotDefined

def evaluate_formula(formula: str, context: dict):
    try:
        return simple_eval(formula, names=context)
    except NameNotDefined as e:
        raise ValueError(f"Variable Not Found: {e}")
    except Exception as e:
        raise ValueError(f"Formula Error: {e}")