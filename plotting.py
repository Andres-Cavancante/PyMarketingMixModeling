import numpy as np
import matplotlib.pyplot as plt

class plottint:
    def __init__(self):
        pass

    def plot_polynomial_function(ind_var, dep_var, degree=1):
        coefficients = np.polyfit(ind_var, dep_var, degree)

        polynomial = np.poly1d(coefficients)

        x_values = np.linspace(min(ind_var), max(ind_var), 100)
        y_values = polynomial(x_values)

        y_pred = polynomial(ind_var)

        r_squared = r2_score(dep_var, y_pred)

        plt.figure(figsize=(8, 4))
        plt.scatter(ind_var, dep_var, label="Data Points")
        plt.plot(x_values, y_values, color="red", label=f"Degree {degree} Regression Line")
        plt.xticks(rotation=45)
        plt.legend()

        plt.text(0.05, 0.95, f'$R^2 = {r_squared:.3f}$', transform=plt.gca().transAxes,
                fontsize=12, verticalalignment='top')

        plt.tight_layout()
        plt.show()