from ensemble_uq import EnsembleCalculator

def main():
    # Replace with your actual calculators
    calculators = [None] * 3

    ensemble_calc = EnsembleCalculator(calculators, bias_strength=1.0)
    print("EnsembleCalculator initialized with", ensemble_calc.M, "calculators.")

if __name__ == "__main__":
    main()
