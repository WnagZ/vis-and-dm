import math

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__)
df = pd.read_csv('filled_data.csv')
income_bins = [0, 10000, 20000, 30000, 50000, 70000]
income_labels = ['0-10000', '10000-20000', '30000-50000', '50000-70000', '70000+']
df['Grouped_Annual_Income'] = pd.cut(df['Annual_Income'], bins=income_bins, labels=income_labels)

income_bins = [0, 20, 35, 50, 75]
income_labels = ['0-20', '20-35', '35-50', '50-75']
df['Grouped_Age'] = pd.cut(df['Age'], bins=income_bins, labels=income_labels)

# Sample data for each dropdown
occupation_options = []
occupations = df['Occupation'].dropna().unique().tolist()
occupations.sort()
for occupation in occupations:
    if not pd.isna(occupation):
        occupation_options.append({'label': occupation, 'value': occupation})

age_options = []

age_groups = df['Grouped_Age'].dropna().unique().tolist()
age_groups.sort()
for age_group in age_groups:
    if not pd.isna(age_group):
        age_options.append({'label': age_group, 'value': age_group})

income_options = []
income_groups = df['Grouped_Annual_Income'].dropna().unique().tolist()
income_groups.sort()

for income_group in income_groups:
    if not pd.isna(income_group):
        income_options.append({'label': income_group, 'value': income_group})

# Options for the category filter dropdown
category_options = [
    {'label': 'Occupation', 'value': 'Occupation'},
    {'label': 'Age Group', 'value': 'Grouped_Age'},
    {'label': 'Income Group', 'value': 'Grouped_Annual_Income'}
]

app.layout = html.Div([
    #Left block
    html.Div([

    ], style={'width': '33%', 'display': 'inline-block'}),

    #Middle block
    html.Div([
        html.H1("Dynamic Dropdowns with Plotly Dash"),
            # Category Dropdown
            html.Label('Select Category'),
            dcc.Dropdown(
                id='category-dropdown',
                options=category_options,
                value='Occupation'
            ),

            # Dynamic Dropdown based on Category selection
            html.Label('Select Filter'),
            dcc.Dropdown(
                id='dynamic-dropdown',
                multi=True,
                value=df['Occupation'].unique().tolist()
            ),

            # Scatterpolar graph for displaying selected values
            dcc.Graph(id='scatterpolar'),

            # Parcoods graph for displaying selected values
            dcc.Graph(id='parcoods'),
    ], style={'width': '33%', 'display': 'inline-block'}),

    # Right block
    html.Div([

    ], style={'width': '33%', 'display': 'inline-block'}),

])


# Callback to dynamically update the options of the second dropdown based on the selected category
@app.callback(
    [Output('dynamic-dropdown', 'options'),
     Output('dynamic-dropdown', 'value')],
    [Input('category-dropdown', 'value')]
)
def update_dynamic_dropdown_options(selected_category):
    if selected_category == 'Occupation':
        options = occupation_options
    elif selected_category == 'Grouped_Age':
        options = age_options
    elif selected_category == 'Grouped_Annual_Income':
        options = income_options
    else:
        options = []
    # Pre-select all options for the dynamic dropdown
    values = [option['value'] for option in options]
    return options, values


# Callback to update the output div based on the second dropdown selection
@app.callback(
    [Output('scatterpolar', 'figure'),
     Output('parcoods', 'figure')],
    [Input('dynamic-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_output(selected_values, selected_category):

    categories = ['Credit_Utilization_Ratio', 'Total_EMI_per_month', 'Outstanding_Debt',
                  'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment']
    pcp_list = []
    fig = go.Figure()
    for y in selected_values:
        meantable = []
        for x in categories:
            small_df = df[df[selected_category] == y]
            calculated_mean = small_df[x].mean()
            meantable.append(math.log(round(calculated_mean)))
        fig.add_trace(go.Scatterpolar(
            r=meantable,
            theta=categories,
            name=y
        ))

    # fig2 = go.Figure(data=
    # go.Parcoords(
    #     line_color='blue',
    #     dimensions=pcp_list
    # ))
    fig2 = go.Figure()
    return fig, fig2
    # return f"You have selected: {', '.join(selected_values)}"

if __name__ == '__main__':
    app.run_server(debug=True)
