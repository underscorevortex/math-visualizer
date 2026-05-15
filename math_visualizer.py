import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import *

st.set_page_config(page_title="Math Visualizer", page_icon="📐", layout="wide")

st.title("📐 Interactive Math Visualizer")
st.markdown("Hover, zoom, and pan all graphs interactively.")

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

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines',
            line=dict(color='cyan', width=2), name=f"f(x) = {func_input}"))
        fig.add_hline(y=0, line_color='gray', line_width=0.5)
        fig.add_vline(x=0, line_color='gray', line_width=0.5)
        fig.update_layout(
            title=f"f(x) = {func_input}",
            paper_bgcolor='#0e1117', plot_bgcolor='#0e1117',
            font=dict(color='white'),
            xaxis=dict(gridcolor='#333', title='x'),
            yaxis=dict(gridcolor='#333', title='f(x)'),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"**Simplified:** `{simplify(expr)}`")
    except:
        st.error("Invalid function! Try: x**2 + 3*x - 5")

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

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=x_vals2, y=y_vals2, mode='lines',
            line=dict(color='cyan', width=2), name=f"f(x) = {func_input2}"))
        fig2.add_trace(go.Scatter(x=x_vals2, y=tangent, mode='lines',
            line=dict(color='orange', width=1.5, dash='dash'),
            name=f"Tangent at x={point}"))
        fig2.add_trace(go.Scatter(x=[point], y=[y_at_point], mode='markers',
            marker=dict(color='red', size=10), name='Point'))
        fig2.update_layout(
            title=f"Derivative of {func_input2}",
            paper_bgcolor='#0e1117', plot_bgcolor='#0e1117',
            font=dict(color='white'),
            xaxis=dict(gridcolor='#333', title='x'),
            yaxis=dict(gridcolor='#333', title='f(x)', range=[-50, 50]),
            hovermode='x unified'
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(f"**f'(x) =** `{deriv}`")
        st.markdown(f"**Slope at x={point}:** `{slope:.4f}`")
    except:
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

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=x_vals3, y=y_vals3, mode='lines',
            line=dict(color='cyan', width=2), name=f"f(x) = {func_input3}"))
        fig3.add_trace(go.Scatter(
            x=np.concatenate([x_fill, x_fill[::-1]]),
            y=np.concatenate([y_fill, np.zeros(len(y_fill))]),
            fill='toself', fillcolor='rgba(255,165,0,0.3)',
            line=dict(color='orange'), name=f"Area = {area:.4f}"))
        fig3.update_layout(
            title=f"Integral of {func_input3}",
            paper_bgcolor='#0e1117', plot_bgcolor='#0e1117',
            font=dict(color='white'),
            xaxis=dict(gridcolor='#333', title='x'),
            yaxis=dict(gridcolor='#333', title='f(x)', range=[-50, 50]),
            hovermode='x unified'
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown(f"**∫f(x)dx =** `{integrate(expr3, x)}`")
        st.markdown(f"**Definite integral from {a} to {b} =** `{area:.6f}`")
    except:
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

        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=x_vals4, y=y_orig, mode='lines',
            line=dict(color='cyan', width=2), name=f"f(x) = {func_input4}"))
        fig4.add_trace(go.Scatter(x=x_vals4, y=y_taylor, mode='lines',
            line=dict(color='orange', width=2, dash='dash'),
            name=f"Taylor order {order}"))
        fig4.update_layout(
            title=f"Taylor Series of {func_input4}",
            paper_bgcolor='#0e1117', plot_bgcolor='#0e1117',
            font=dict(color='white'),
            xaxis=dict(gridcolor='#333', title='x'),
            yaxis=dict(gridcolor='#333', title='f(x)', range=[-5, 5]),
            hovermode='x unified'
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown(f"**Taylor expansion:** `{taylor}`")
    except:
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

        fig5 = go.Figure(data=[go.Surface(
            x=X, y=Y, z=Z,
            colorscale='plasma',
            contours=dict(z=dict(show=True, usecolormap=True))
        )])
        fig5.update_layout(
            title=f"z = {func_input5}",
            paper_bgcolor='#0e1117',
            font=dict(color='white'),
            scene=dict(
                xaxis=dict(gridcolor='gray', title='x'),
                yaxis=dict(gridcolor='gray', title='y'),
                zaxis=dict(gridcolor='gray', title='z'),
                bgcolor='#0e1117'
            )
        )
        st.plotly_chart(fig5, use_container_width=True)
    except:
        st.error("Invalid function! Try: sin(sqrt(x**2 + y**2))")
