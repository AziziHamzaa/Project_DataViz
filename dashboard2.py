
import panel as pn
import hvplot.pandas
import param
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go

# Load Data

df = pd.read_csv("StudentsPerformance.csv")
#df.rename(columns={"gender": "gender", "race/ethnicity": "race_ethnicity", "parental level of education": "parental_level_of_education","lunch": "lunch", "test preparation course": "test_preparation_course", "math score": "math_score","reading score": "reading_score","writing score": "writing_score"},inplace=True)
# Adding Total Score Attribute to each student
df['total score'] = round((df['math score']+df['reading score']+df['writing score']) / 3, 1)




ACCENT_COLOR = pn.template.FastListTemplate.accent_base_color
# create a self-contained dashboard class
class InteractiveDashboard(param.Parameterized):

    #cylinders =  param.Integer(label='Cylinders', default=4, bounds=(4, 8))
    """
    mfr = param.ListSelector(
        label='MFR',
        default=['ford', 'chevrolet', 'honda', 'toyota', 'audi'], 
        objects=['ford', 'chevrolet', 'honda', 'toyota', 'audi'], precedence=0.5)
    """
    yaxis = param.Selector(label='Y axis', objects=['math score', 'writing score', 'reading score'])
    #select = param.Select(name='Select', options=['math score', 'writing score', 'reading score'])
    x_select = param.Selector(label="x_select", objects=list(df.columns))
    y_select = param.Selector(label="y_select", objects=list(df.columns))
    
    
    @param.depends('yaxis','x_select','y_select')
    
    def table(self):
        df_filters = {
                'gender': {'type': 'input', 'func': 'like', 'placeholder': 'Enter gender'},
                'race/ethnicity': {'func':'like','placeholder': 'Enter Race'},
                'parental level of education': {'type': 'input', 'func': 'like', 'placeholder': 'Enter parental level of education'},
                'lunch': {'type': 'input', 'func': 'like', 'placeholder': 'Enter lunch'},
                'test preparation course': {'type': 'input', 'func': 'like', 'placeholder': 'none/completed'},
                'math score': {'type': 'number', 'func': '>=', 'placeholder': 'Enter minimum score'},
                'reading score': {'type': 'number', 'func': '>=', 'placeholder': 'Enter minimum score'},
                'writing score': {'type': 'number', 'func': '>=', 'placeholder': 'Enter minimum score'}
            }
        df_widget = pn.widgets.Tabulator(df, layout='fit_columns', page_size = 10, sizing_mode='stretch_width' ,header_filters=df_filters)
        return df_widget
    def plot_scatter(self):
        scatter_plot = df.hvplot.scatter(x = self.x_select , y = self.y_select , color = ACCENT_COLOR, title = "Scatter Plot", width=800, height=400)
        return scatter_plot
    def plotbox(self):
        gender_math = df[df.gender.isin(['male','female'])]
        pl = gender_math.hvplot.box(self.yaxis, by='gender', invert = True, color = ACCENT_COLOR, title = "Box Plot")
        return pl
    def countBarPlot(self,column):
        table = df[[column,"gender"]].value_counts()
        pl = table.hvplot.bar(by = column, staked = True)
        return pl



    def dataPreccessing(self):
        pass

    #    return 

    def heatmap(self):
        return df.hvplot.heatmap(colorbar=True)
    
    

        return fig
dashboard = InteractiveDashboard()

# Layout using Template
template = pn.template.FastListTemplate(
    title='Dashboard-Panel Students Performance', 
    sidebar=[
             pn.pane.Markdown("## Settings"),
             pn.Param(dashboard.param,widgets={'yaxis': pn.widgets.Select,'y_select': pn.widgets.Select,'x_select': pn.widgets.Select})],
    
    main=[
          pn.Row(dashboard.table),
          #pn.Row(dashboard.df_widget.controls(jslink=True), dashboard.df_widget),
          pn.Row(pn.Column("## Scatter Plot",dashboard.plot_scatter)),
          pn.Row(pn.Column("Score and Gender",dashboard.plotbox)),
          pn.pane.Markdown("## Counts plot for various numuric features according gender"),
          pn.Row(pn.Column(dashboard.countBarPlot('test preparation course'),dashboard.countBarPlot("lunch"),dashboard.countBarPlot('parental level of education'),dashboard.countBarPlot("race/ethnicity")))],
    
    #accent_base_color="#337AFF",
    #header_background="#337AFF",
)
template.servable()
