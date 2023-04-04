
import panel as pn
import hvplot.pandas
import holoviews as hv
import param
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# Load Data

df = pd.read_csv("StudentsPerformance.csv")
#df.rename(columns={"gender": "gender", "race/ethnicity": "race_ethnicity", "parental level of education": "parental_level_of_education","lunch": "lunch", "test preparation course": "test_preparation_course", "math score": "math_score","reading score": "reading_score","writing score": "writing_score"},inplace=True)
# Adding Total Score Attribute to each student
df['total score'] = round((df['math score']+df['reading score']+df['writing score']) / 3, 1)
pn.extension('tabulator', css_files=[pn.io.resources.CSS_URLS['font-awesome']])



pn.widgets.Tabulator.theme = 'simple'
# create a self-contained dashboard class
class InteractiveDashboard(param.Parameterized):

    
    yaxis = param.Selector(label='Box Plot Selector', objects=['math score', 'writing score', 'reading score'])
    x_select = param.Selector(label="X Selector Scatter", objects=['writing score', 'math score', 'reading score','total score'])
    y_select = param.Selector(label="y Selector Scatter", objects=['math score', 'writing score', 'reading score','total score'])
    
    
    @param.depends('yaxis','x_select','y_select')
    
    
    def table(self):
        
        df_widget = pn.widgets.Tabulator(df, layout='fit_data_table', page_size = 10, sizing_mode='stretch_width' )#,header_filters=df_filters)
        
        return df_widget
    def plot_scatter(self):
        scatter_plot = df.hvplot.scatter(x = self.x_select , y = self.y_select , color = "#74a9cf", title = "Scatter Plot", width=800, height=400)
        return scatter_plot
    def plotbox(self):
        gender_math = df[df.gender.isin(['male','female'])]
        pl = gender_math.hvplot.box(self.yaxis, by='gender', invert = True, color = "#74a9cf", title = "Box Plot")
        return pl
    def countBarPlot(self,column):
        table = df[[column,"gender"]].value_counts()
        pl = table.hvplot.bar(by = column, cmap="PuBu",stacked=True, rot=90, width=800, legend='top_left', title="Count Plot")
        return pl


    def plot_score_relations(self):
        ethnicity = df.groupby('race/ethnicity')[['math score','reading score','writing score','total score']].mean().sort_values(by='total score')
        education = df.groupby('parental level of education')[['math score','reading score','writing score','total score']].mean().sort_values(by='total score')
        lunch = df.groupby('lunch')[['math score','reading score','writing score','total score']].mean().sort_values(by='total score')
        course = df.groupby('test preparation course')[['math score','reading score','writing score','total score']].mean().sort_values(by='total score')

        fig = (
            ethnicity.hvplot.bar(cmap="PuBu",y='total score', xlabel='Race/Ethnicity', ylabel='Average of total score', 
                                width=400, height=400, title='Relation between Race/Ethnicity and\n High Scores') +
            education.hvplot.bar(cmap="PuBu",y='total score', xlabel='Parental Education', ylabel='Average of total score', 
                                width=400, height=400, title='Relation between Parental Education\n and High Scores', rot=10) +
            lunch.hvplot.bar(cmap="PuBu",y='total score', xlabel='Lunch Type', ylabel='Average of total score', 
                            width=400, height=400, title='Relation between Lunch Type\n and High Scores') +
            course.hvplot.bar(cmap="PuBu",y='total score', xlabel='Test Prep Course', ylabel='Average of total score', 
                            width=400, height=400, title='Relation between Test Prep Course \n and High Scores')
        ).cols(2)
        
        return fig
    def corr_heatmap(self):
    # calculate correlation matrix
        corr = df.corr()

        # plot heatmap of correlation matrix
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
        ax.set_title('Correlation Matrix Heatmap')
    
        return fig



dashboard = InteractiveDashboard()

# Layout using Template
template = pn.template.VanillaTemplate(
    title = 'Explore Dashboard', 
    sidebar=[
             pn.pane.Markdown("## Settings"),
             pn.Param(dashboard.param,widgets={'yaxis': pn.widgets.Select,'y_select': pn.widgets.Select,'x_select': pn.widgets.Select})],
    
    main=[
          
          pn.Row(dashboard.table),
          pn.Row(pn.Column("## Scatter Plot", dashboard.plot_scatter)),
          pn.Row(pn.Column("Score and Gender", dashboard.plotbox)),
          pn.pane.Markdown("## Counts plot for various numuric features according gender"),
          pn.Row(pn.Column(dashboard.countBarPlot('test preparation course'),dashboard.countBarPlot("lunch"),dashboard.countBarPlot('parental level of education'),dashboard.countBarPlot("race/ethnicity"))),
          pn.Row(dashboard.plot_score_relations),
          pn.Row(dashboard.corr_heatmap)
          
          
          ],
    #3E848C
    accent_base_color="#74a9cf",
    header_background="#74a9cf",
    sidebar_width=310,
)
template.servable()
