
import panel as pn
import hvplot.pandas
import param
import pandas as pd
import seaborn as sns

# Load Data
#from bokeh.sampledata.autompg import autompg_clean as df
df = pd.read_csv("StudentsPerformance.csv")

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
    
    @param.depends('yaxis')
    
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
    def plot1(self):
        return df.hvplot.scatter(x='reading score', y='math score')
    def plot2(self):
        return df.hvplot.scatter(x='writing score', y='math score')
    def plotbox(self):
        gender_math = df[df.gender.isin(['male','female'])]
        pl = gender_math.hvplot.box("math score", by='gender', invert = True)
        return pl
        

    
    
dashboard = InteractiveDashboard()

# Layout using Template
template = pn.template.BootstrapTemplate(
    title='Dashboard Panel', 
    sidebar=[pn.Param(dashboard.param, widgets={'yaxis': pn.widgets.RadioButtonGroup})],
    main=[pn.Row(dashboard.table()),
          pn.Row(pn.Column(dashboard.plot1()), pn.Column(dashboard.plot2())),
          pn.Row(dashboard.plotbox())],
    accent_base_color="#337AFF",
    header_background="#337AFF",
)
template.servable()