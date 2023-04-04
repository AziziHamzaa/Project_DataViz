import panel as pn
pn.extension()

# Create the links to the two dashboards
#explore_link = pn.pane.HTML("<a href='/dash1'>Explore Dashboard</a>")
#analysis_link = pn.pane.HTML("<a href='/dash2'>Analysis Dashboard</a>")

button1 = pn.widgets.Button(name='Explore Dashboard', margin=(25, 0), button_type='primary', width=200, height=50, align='center', icon='fas fa-chart-bar')
button1.js_on_click(args={'url': '/dash1'}, code="window.location.href = url;")
button2 = pn.widgets.Button(name='Analysis Dashboard', margin=(25, 0), button_type='primary', width=200, height=50, align='center', icon='fas fa-chart-pie')
button2.js_on_click(args={'url': '/dash2'}, code="window.location.href = url;")



# Create the home page layout
home_page = pn.Column(
    pn.pane.Markdown("# Welcome to my Dashboard", align="center"),
    pn.layout.HSpacer(height=50),
    pn.pane.Markdown("Click on the links below to access the dashboards : ", align='center'),
    
    pn.Row(
        pn.layout.HSpacer(width=20),
        pn.layout.VSpacer(),
        
        button1,
        pn.layout.HSpacer(),
        button2,
        
        pn.layout.VSpacer(),
        pn.layout.HSpacer(width=20)
    ),
    sizing_mode='stretch_width',
    
)

home_page.servable()
