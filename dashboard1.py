import panel as pn
pn.extension()

# Define dashboard functions
import pandas as pd
import hvplot.pandas

data = pd.read_csv("StudentsPerformance.csv")

def explore_dashboard():
    # Create scatter plot with x and y selection widgets
    scatter_plot = data.hvplot.scatter(x="math score", y="reading score", width=800, height=400)
    x_select = pn.widgets.Select(name="X-Axis", options=list(data.columns), value="math score")
    y_select = pn.widgets.Select(name="Y-Axis", options=list(data.columns), value="reading score")
    
    # Define callback function to update scatter plot when x or y selection changes
    def update_scatter_plot(event):
        new_x = x_select.value
        new_y = y_select.value
        scatter_plot.x = new_x
        scatter_plot.y = new_y
    
    # Link selection widgets to callback function
    x_select.param.watch(update_scatter_plot, "value")
    y_select.param.watch(update_scatter_plot, "value")
    
    # Create dashboard layout
    layout = pn.Column(
        pn.pane.Markdown("# Explore Dashboard"),
        pn.Row(
            pn.Column(x_select),
            pn.layout.VSpacer(width=50),
            pn.Column(y_select),
        ),
        scatter_plot,
        sizing_mode="stretch_width"
    )
    
    # Return dashboard layout
    return layout

import pandas as pd
from sklearn.linear_model import LinearRegression
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import panel as pn

def analysis_dashboard():
    # Create linear regression model
    model = LinearRegression()
    X = data[["math score", "reading score"]]
    y = data["writing score"]
    model.fit(X, y)
    
    # Create scatter plot with regression line
    source = ColumnDataSource(data)
    plot = figure(width=800, height=400)
    plot.scatter(x="math score", y="writing score", source=source)
    plot.line(x="math score", y=model.predict(X), color="red", source=source)
    
    # Create dashboard layout
    layout = pn.Column(
        pn.pane.Markdown("# Analysis Dashboard"),
        pn.pane.Bokeh(plot),
        pn.pane.DataFrame(model.coef_, columns=["Coefficient"], index=["Math Score", "Reading Score"]),
        sizing_mode="stretch_width"
    )
    
    # Return dashboard layout
    return layout

def link_to_explore_dashboard(self):
    explore_dashboard().show()

pn.widgets.Button.link_to_explore_dashboard = link_to_explore_dashboard
def link_to_analysis_dashboard(self):
    analysis_dashboard().show()

pn.widgets.Button.link_to_analysis_dashboard = link_to_analysis_dashboard



# Define home page
home = pn.Column(
    pn.pane.Markdown("# Home Page"),
    pn.layout.HSpacer(height=20),
    pn.Row(
        pn.layout.VSpacer(width=20),
        pn.Column(
            pn.pane.Markdown("## Explore Dashboard"),
            pn.pane.Markdown("Click the button below to go to the Explore Dashboard"),
            pn.layout.HSpacer(height=20),
            pn.widgets.Button(name="Explore Dashboard", button_type="primary", align="center").link_to_explore_dashboard(),
            pn.layout.HSpacer(height=50),
            width=500,
            height=400
        ),
        pn.layout.VSpacer(width=20),
        pn.Column(
            pn.pane.Markdown("## Analysis Dashboard"),
            pn.pane.Markdown("Click the button below to go to the Analysis Dashboard"),
            pn.layout.HSpacer(height=20),
            pn.widgets.Button(name="Analysis Dashboard", button_type="primary", align="center").link_to_analysis_dashboard(),
            pn.layout.HSpacer(height=50),
            width=500,
            height=400
        ),
        pn.layout.VSpacer(width=20)
    ),
    sizing_mode="stretch_width"
)

# Add link functions to buttons
pn.widgets.Button.link_to_explore_dashboard = lambda self: explore_dashboard.show()
pn.widgets.Button.link_to_analysis_dashboard = lambda self: analysis_dashboard.show()


