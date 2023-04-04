import panel as pn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from bokeh.plotting import figure
import hvplot.pandas
import param
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


pn.extension(sizing_mode="stretch_width")


ACCENT_COLOR = pn.template.FastListTemplate.accent_base_color

df = pd.read_csv("StudentsPerformance.csv")
df['total score'] = round((df['math score']+df['reading score']+df['writing score']) / 3, 1) 

class InteractiveDashboard(param.Parameterized):

    n_clusters = param.Integer(1, bounds=(1, 10),label = "Number Of Clusters - KMeans")
    y_select = param.Selector(label="Linear Regression Target", objects=['total score', 'math score', 'writing score', 'reading score'])
    x1_select = param.Selector(label="Scatter X1 Select", objects= ['math score', 'writing score', 'reading score', 'total score'])
    x2_select = param.Selector(label="Scatter X2 Select", objects= ['writing score', 'math score','reading score', 'total score'])
    @param.depends('y_select','x1_select','x2_select','n_clusters')
    def linear_regression(self):
        model = LinearRegression()
        X = df[[self.x1_select, self.x2_select]]
        y = df[self.y_select]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model.fit(X_train, y_train)

        
        score = model.score(X_test, y_test)*100
        layout = pn.indicators.Number(
            name="Test score",
            value=score,
            format="{value}%",
            colors=[(85.0, "#E2F313"), (95.0, "#A4DA1E"), (100, "#3E848C")],
        )
        return layout
    def plot_scatter(self):
        scatter_plot = df.hvplot.scatter(x = self.x1_select , y = self.y_select , color = "#3E848C", title = "Scatter Plot", width=800, height=400)
        return scatter_plot
    def heatmap(self):
        scaler = StandardScaler()
        X = scaler.fit_transform(df[['math score', 'reading score', 'writing score', 'total score']])
        similarity_matrix = np.corrcoef(X.T)
        heatmap = pd.DataFrame(similarity_matrix, columns=['math score', 'reading score', 'writing score', 'total score'], index=['math score', 'reading score', 'writing score', 'total score']).hvplot.heatmap(title='Similarity Matrix',cmap = "summer",width=850)
        return pn.Column(heatmap)
    def clustering(self):
        scaler = StandardScaler()
        X = scaler.fit_transform(df[['math score', 'reading score', 'writing score']])

        # Create a KMeans model with 3 clusters
        kmeans = KMeans(n_clusters=self.n_clusters)
        kmeans.fit(X)
        labels = kmeans.labels_
        scatter = df.hvplot.scatter(x='math score', y='reading score', c=labels,cmap = "summer", title='Clustering Analysis - KMeans',width=850)
        
        # Comparing Clustering Results

        sse = []
        for k in range(1, 11):
            X = scaler.fit_transform(df[['math score', 'reading score', 'writing score']])
            kmeans = KMeans(n_clusters = k)
            kmeans.fit(X)
        #Computing the sum of squared error for each
            sse.append(kmeans.inertia_)
        
        clust_df = pd.DataFrame(sse, columns=["Sum of Squared Error"])
        clust_df['Number of clusters'] = clust_df.index.map(lambda x:x+1)

        line = clust_df.hvplot.line('Number of clusters','Sum of Squared Error',width=850, color = "#3E848C", title='Clustering Evaluation - KMeans')

        return pn.Column(scatter, line)

dashboard = InteractiveDashboard()

# Layout using Template
template = pn.template.FastListTemplate(
    title = 'Analysis Dashboard', 
    sidebar=[
             pn.pane.Markdown("## Settings"),
             pn.Param(dashboard.param,widgets={'y_select': pn.widgets.Select,'x1_select': pn.widgets.Select,'x2_select': pn.widgets.Select,'n_clusters': pn.widgets.IntSlider})],
    
    main=[
            pn.Row(dashboard.heatmap),
            pn.Row(pn.Column("## Training Linear Regression Model To Predict Either Writing, Math Or Reading Scores.",
            dashboard.plot_scatter,
            dashboard.linear_regression)),
            pn.Row(dashboard.clustering),
          ],
    sidebar_width=310,
    accent_base_color="#3E848C",
    header_background="#3E848C",

)
template.servable()