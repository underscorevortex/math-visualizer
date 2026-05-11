import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import *

st.set_page_config(page_title="Math Visualizer", page_icon="📐", layout="wide")

st.title("📐 Interactive Math Visualizer")
st.markdown("Visualize mathematical concepts interactively.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Function Grapher",
    "📉 Derivative",
    "∫ Integral",
    "🔢 Taylor Series",
    "🌐 3D Surface"
])

x = symbols('x')

# TAB 1 - Function Grapher
with tab1:
    st.header("Function Grapher")
    func_input = st.text_input("Enter a function of x:", "x**2 + 2*x + 1")
    x_min = st.slider("X min", -20, 0, -10)
    x_max = st.slider("X max", 0, 20, 10)

    try:
        expr = sympify(func_input)
        f = lambdify(x, expr, "numpy")
        x_vals = np.linspace(x_min, x_max, 500)
        y_vals = f(x_vals)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x_vals, y_vals, color='cyan', linewidth=2)
        ax.axhline(0, color='white', linewidth=0.5)
        ax.axvline(0, color='white', linewidth=0.5)
        ax.set_facecolor('#0e1117')
        fig.patch.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        ax.spines[:].set_color('gray')
        ax.set_title(f"f(x) = {func_input}", color='white')
        ax.set_xlabel("x", color='white')
        ax.set_ylabel("f(x)", color='white')
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)

        st.markdown(f"**Simplified:** `{simplify(expr)}`")
    except Exception as e:
        st.error(f"Invalid function! Try something like: x**2 + 3*x - 5")

# TAB 2 - Derivative
with tab2:
    st.header("Derivative Visualizer")
    func_input2 = st.text_input("Enter a function of x:", "x**3 - 3*x", key="deriv")
    point = st.slider("Point to show tangent line", -10.0, 10.0, 0.0, 0.1)
    x_min2 = st.slider("X min", -20, 0, -5, key="dmin")
    x_max2 = st.slider("X max", 0, 20, 5, key="dmax")

    try:
        expr2 = sympify(func_input2)
        deriv = diff(expr2, x)
        f2 = lambdify(x, expr2, "numpy")
        df = lambdify(x, deriv, "numpy")

        x_vals2 = np.linspace(x_min2, x_max2, 500)
        y_vals2 = f2(x_vals2)

        slope = float(df(point))
        y_at_point = float(f2(point))
        tangent = slope * (x_vals2 - point) + y_at_point

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(x_vals2, y_vals2, color='cyan', linewidth=2, label=f"f(x) = {func_input2}")
        ax2.plot(x_vals2, tangent, color='orange', linewidth=1.5, linestyle='--', label=f"Tangent at x={point}")
        ax2.scatter([point], [y_at_point], color='red', zorder=5, s=100)
        ax2.set_facecolor('#0e1117')
        fig2.patch.set_facecolor('#0e1117')
        ax2.tick_params(colors='white')
        ax2.spines[:].set_color('gray')
        ax2.set_title(f"Derivative of {func_input2}", color='white')
        ax2.set_xlabel("x", color='white')
        ax2.set_ylabel("f(x)", color='white')
        ax2.legend(facecolor='#0e1117', labelcolor='white')
        ax2.grid(True, alpha=0.2)
        ax2.set_ylim(-50, 50)
        st.pyplot(fig2)

        st.markdown(f"**f'(x) =** `{deriv}`")
        st.markdown(f"**Slope at x={point}:** `{slope:.4f}`")
    except Exception as e:
        st.error("Invalid function!")

# TAB 3 - Integral
with tab3:
    st.header("Integral Visualizer")
    func_input3 = st.text_input("Enter a function of x:", "x**2", key="integ")
    a = st.slider("Lower bound (a)", -10.0, 10.0, 0.0, 0.1)
    b = st.slider("Upper bound (b)", -10.0, 10.0, 3.0, 0.1)

    try:
        expr3 = sympify(func_input3)
        f3 = lambdify(x, expr3, "numpy")
        x_vals3 = np.linspace(-10, 10, 500)
        y_vals3 = f3(x_vals3)

        x_fill = np.linspace(a, b, 500)
        y_fill = f3(x_fill)

        area = float(integrate(expr3, (x, a, b)))

        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.plot(x_vals3, y_vals3, color='cyan', linewidth=2)
        ax3.fill_between(x_fill, y_fill, alpha=0.4, color='orange', label=f"Area = {area:.4f}")
        ax3.axhline(0, color='white', linewidth=0.5)
        ax3.set_facecolor('#0e1117')
        fig3.patch.set_facecolor('#0e1117')
        ax3.tick_params(colors='white')
        ax3.spines[:].set_color('gray')
        ax3.set_title(f"Integral of {func_input3}", color='white')
        ax3.set_xlabel("x", color='white')
        ax3.set_ylabel("f(x)", color='white')
        ax3.legend(facecolor='#0e1117', labelcolor='white')
        ax3.grid(True, alpha=0.2)
        ax3.set_ylim(-50, 50)
        st.pyplot(fig3)

        st.markdown(f"**∫f(x)dx =** `{integrate(expr3, x)}`")
        st.markdown(f"**Definite integral from {a} to {b} =** `{area:.6f}`")
    except Exception as e:
        st.error("Invalid function!")

# TAB 4 - Taylor Series
with tab4:
    st.header("Taylor Series Approximation")
    func_input4 = st.text_input("Enter a function:", "sin(x)", key="taylor")
    order = st.slider("Polynomial order", 1, 15, 5)
    x_min4 = st.slider("X min", -20, 0, -10, key="tmin")
    x_max4 = st.slider("X max", 0, 20, 10, key="tmax")

    try:
        expr4 = sympify(func_input4)
        taylor = series(expr4, x, 0, order).removeO()
        f4 = lambdify(x, expr4, "numpy")
        t4 = lambdify(x, taylor, "numpy")

        x_vals4 = np.linspace(x_min4, x_max4, 500)
        y_orig = f4(x_vals4)
        y_taylor = t4(x_vals4)

        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.plot(x_vals4, y_orig, color='cyan', linewidth=2, label=f"f(x) = {func_input4}")
        ax4.plot(x_vals4, y_taylor, color='orange', linewidth=2, linestyle='--', label=f"Taylor order {order}")
        ax4.set_facecolor('#0e1117')
        fig4.patch.set_facecolor('#0e1117')
        ax4.tick_params(colors='white')
        ax4.spines[:].set_color('gray')
        ax4.set_title(f"Taylor Series of {func_input4}", color='white')
        ax4.set_xlabel("x", color='white')
        ax4.set_ylabel("f(x)", color='white')
        ax4.legend(facecolor='#0e1117', labelcolor='white')
        ax4.grid(True, alpha=0.2)
        ax4.set_ylim(-5, 5)
        st.pyplot(fig4)

        st.markdown(f"**Taylor expansion:** `{taylor}`")
    except Exception as e:
        st.error("Invalid function!")

# TAB 5 - 3D Surface
with tab5:
    st.header("3D Surface Plotter")
    func_input5 = st.text_input("Enter a function of x and y:", "sin(sqrt(x**2 + y**2))", key="surf")

    try:
        from sympy import symbols as sym
        xs, ys = sym('x y')
        expr5 = sympify(func_input5)
        f5 = lambdify((xs, ys), expr5, "numpy")

        x_vals5 = np.linspace(-10, 10, 100)
        y_vals5 = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x_vals5, y_vals5)
        Z = f5(X, Y)

        fig5 = plt.figure(figsize=(10, 7))
        ax5 = fig5.add_subplot(111, projection='3d')
        ax5.plot_surface(X, Y, Z, cmap='plasma', alpha=0.9)
        ax5.set_facecolor('#0e1117')
        fig5.patch.set_facecolor('#0e1117')
        ax5.tick_params(colors='white')
        ax5.set_title(f"z = {func_input5}", color='white')
        ax5.set_xlabel("x", color='white')
        ax5.set_ylabel("y", color='white')
        ax5.set_zlabel("z", color='white')
        st.pyplot(fig5)
    except Exception as e:
        st.error("Invalid function! Try: sin(sqrt(x**2 + y**2))")