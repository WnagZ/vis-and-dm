import math

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import re

app = dash.Dash(__name__)
df = pd.read_csv('filled_data.csv')
income_bins = [0, 10000, 20000, 30000, 50000, 70000]
income_labels = ['0-10000', '10000-20000', '30000-50000', '50000-70000', '70000+']
df['Grouped_Annual_Income'] = pd.cut(df['Annual_Income'], bins=income_bins, labels=income_labels)

age_bins = [0, 20, 35, 50, 75]
age_labels = ['0-20', '20-35', '35-50', '50-75']
df['Grouped_Age'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)

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

loan_options = []
loan_types = ['Payday Loan', 'Auto Loan', 'Home Equity Loan', 'Mortgage Loan', 'Student Loan', 'Personal Loan',
              'Loan Not Specified', 'Debt Consolidation Loan', 'Credit-Builder Loan']
loan_types.sort()
for loan_type in loan_types:
    loan_options.append({'label': loan_type, 'value': loan_type})

# Options for the category filter dropdown
category_options = [
    {'label': 'Occupation', 'value': 'Occupation'},
    {'label': 'Age Group', 'value': 'Grouped_Age'},
    {'label': 'Income Group', 'value': 'Grouped_Annual_Income'},
    {'label': 'Loan Type', 'value': 'Loan_Type'}
]

fields = ['Credit_Utilization_Ratio', 'Total_EMI_per_month', 'Outstanding_Debt',
              'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment']

app.layout = html.Div([
    # Left block
    html.Div([
        # Occupation name at the top
        html.H3(id='left-occupation-name'),

        # Four dropdowns for the left side
        html.Label('Select Left Side Category'),
        dcc.Dropdown(
            id='left-side-category-dropdown',
            options=category_options,
            value=category_options[0]['value']
        ),

        html.Label('Select Left Side Label'),
        dcc.Dropdown(
            id='left-side-label-dropdown',
            multi=False,
            value=df[category_options[0]['value']].unique().tolist()
        ),

        html.Label('Select Left Side Second Category'),
        dcc.Dropdown(
            id='left-side-second-category-dropdown',
            options=category_options[1:],
            value=category_options[1]['value']
        ),

        html.Label('Select Left Side Second Label'),
        dcc.Dropdown(
            id='left-side-second-label-dropdown',
            multi=False,
            value=df[category_options[1]['value']].unique().tolist()
        ),

        html.Label('Select Left Side Field'),
        dcc.Dropdown(
            id='left-side-field-dropdown',
            options=[{'label': field, 'value': field} for field in fields],
            value=fields[0]
        ),

        # Scatterpolar graph for left side
        dcc.Graph(id='scatterpolar-left'),

    ], style={'width': '33%', 'display': 'inline-block'}),

    # Middle block
    html.Div([
        html.H1("Dynamic Dropdowns with Plotly Dash"),
        # Category Dropdown
        html.Label('Select Category'),
        dcc.Dropdown(
            id='category-dropdown',
            options=category_options,
            value='Occupation'
        ),

        # Dynamic Dropdowns for the first and second occupations
        html.Label('Select First Occupation'),
        dcc.Dropdown(
            id='first-occupation-dropdown',
            options=occupation_options,
            multi=False,
            value=occupation_options[0]['value']
        ),

        html.Label('vs \n'),

        html.Label('Select Second Occupation'),
        dcc.Dropdown(
            id='second-occupation-dropdown',
            options=occupation_options,
            multi=False,
            value=occupation_options[1]['value']
        ),

        # Scatterpolar graph for displaying selected values
        dcc.Graph(id='scatterpolar-middle'),

        # Pcp graph for displaying selected values
        dcc.Graph(id='pcp'),
    ], style={'width': '33%', 'display': 'inline-block'}),

    # Right block
    html.Div([
        # Occupation name at the top
        html.H3(id='right-occupation-name'),

        # Four dropdowns for the right side
        html.Label('Select Right Side Category'),
        dcc.Dropdown(
            id='right-side-category-dropdown',
            options=category_options,
            value=category_options[0]['value']
        ),

        html.Label('Select Right Side Label'),
        dcc.Dropdown(
            id='right-side-label-dropdown',
            multi=False,
            value=df[category_options[0]['value']].unique().tolist()
        ),

        html.Label('Select Right Side Second Category'),
        dcc.Dropdown(
            id='right-side-second-category-dropdown',
            options=category_options[1:],
            value=category_options[1]['value']
        ),

        html.Label('Select Right Side Second Label'),
        dcc.Dropdown(
            id='right-side-second-label-dropdown',
            multi=False,
            value=df[category_options[1]['value']].unique().tolist()
        ),

        html.Label('Select Right Side Field'),
        dcc.Dropdown(
            id='right-side-field-dropdown',
            options=[{'label': field, 'value': field} for field in fields],
            value=fields[0]
        ),

        # Scatterpolar graph for right side
        dcc.Graph(id='scatterpolar-right'),

    ], style={'width': '33%', 'display': 'inline-block'}),

])


# Callback to dynamically update the options of the first occupation dropdown
@app.callback(
    [Output('first-occupation-dropdown', 'options'),
     Output('first-occupation-dropdown', 'value')],
    [Input('category-dropdown', 'value')]
)
def update_first_occupation_dropdown_options(selected_category):
    if selected_category == 'Occupation':
        options = occupation_options
    elif selected_category == 'Grouped_Age':
        options = age_options
    elif selected_category == 'Grouped_Annual_Income':
        options = income_options
    elif selected_category == 'Loan_Type':
        options = loan_options
    else:
        options = []
    # Pre-select the first option for the first occupation dropdown
    values = [options[0]['value']] if options else []
    return options, values

# Callback to dynamically update the options of the second occupation dropdown
@app.callback(
    [Output('second-occupation-dropdown', 'options'),
     Output('second-occupation-dropdown', 'value')],
    [Input('category-dropdown', 'value')]
)
def update_second_occupation_dropdown_options(selected_category):
    if selected_category == 'Occupation':
        options = occupation_options
    elif selected_category == 'Grouped_Age':
        options = age_options
    elif selected_category == 'Grouped_Annual_Income':
        options = income_options
    else:
        options = []
    # Pre-select the second option for the second occupation dropdown
    values = [options[1]['value']] if len(options) > 1 else []
    return options, values

# Callback to dynamically update the options for the left side label dropdown based on the selected category
@app.callback(
    [Output('left-side-label-dropdown', 'options'),
     Output('left-side-label-dropdown', 'value')],
    [Input('left-side-category-dropdown', 'value')]
)
def update_left_side_label_options(selected_category):
    options = [{'label': label, 'value': label} for label in df[selected_category].dropna().unique()]
    values = options[0]['value'] if options else []
    return options, values

# Callback to dynamically update the options for the right side label dropdown based on the selected category
@app.callback(
    [Output('right-side-label-dropdown', 'options'),
     Output('right-side-label-dropdown', 'value')],
    [Input('right-side-category-dropdown', 'value')]
)
def update_right_side_label_options(selected_category):
    options = [{'label': label, 'value': label} for label in df[selected_category].dropna().unique()]
    values = options[0]['value'] if options else []
    return options, values


# Callback to dynamically update the options for the left side second label dropdown based on the selected category
@app.callback(
    [Output('left-side-second-label-dropdown', 'options'),
     Output('left-side-second-label-dropdown', 'value')],
    [Input('left-side-second-category-dropdown', 'value')]
)
def update_left_side_second_label_options(selected_category):
    options = [{'label': label, 'value': label} for label in df[selected_category].dropna().unique()]
    values = options[0]['value'] if options else []
    return options, values

# Callback to dynamically update the options for the right side second label dropdown based on the selected category
@app.callback(
    [Output('right-side-second-label-dropdown', 'options'),
     Output('right-side-second-label-dropdown', 'value')],
    [Input('right-side-second-category-dropdown', 'value')]
)
def update_right_side_second_label_options(selected_category):
    options = [{'label': label, 'value': label} for label in df[selected_category].dropna().unique()]
    values = options[0]['value'] if options else []
    return options, values


# Callbacks for updating the occupation names in the left and right side blocks
@app.callback(
    [Output('left-occupation-name', 'children'),
     Output('right-occupation-name', 'children')],
    [Input('first-occupation-dropdown', 'value'),
     Input('second-occupation-dropdown', 'value')]
)
def update_occupation_names(first_occupation, second_occupation):
    return f'{first_occupation} (Left Side)', f'{second_occupation} (Right Side)'


# Callback to update the scatterpolar graph for the left side
@app.callback(
    Output('scatterpolar-left', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('left-side-category-dropdown', 'value'),
     Input('left-side-label-dropdown', 'value'),
     Input('left-side-second-category-dropdown', 'value'),
     Input('left-side-second-label-dropdown', 'value'),
     Input('left-side-field-dropdown', 'value')]
)
def update_scatterpolar_left(main_category, selected_category, selected_label, second_category, second_label, selected_field):
    # Get unique labels for the main category selected in the middle
    main_category_labels = df[main_category].unique()

    # Filter the database based on left-side category labels and second category labels
    filtered_data = df[(df[selected_category] == selected_label) & (df[second_category] == second_label)]

    # Create traces for the selected field
    values = []
    for label in main_category_labels:
        label_data = filtered_data[filtered_data[main_category] == label]
        mean_value = label_data[selected_field].mean()
        if not math.isnan(mean_value):
            values.append(math.log(round(mean_value)))
        else:
            values.append(None)

    # Pad 'r' values with None to match the length of 'theta' values
    while len(values) < len(main_category_labels):
        values.append(None)

    trace = go.Scatterpolar(
        r=values,
        theta=main_category_labels,
        name=selected_field
    )

    layout = go.Layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    return go.Figure(data=[trace], layout=layout)


# Callback to update the scatterpolar graph for the left side
@app.callback(
    Output('scatterpolar-right', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('right-side-category-dropdown', 'value'),
     Input('right-side-label-dropdown', 'value'),
     Input('right-side-second-category-dropdown', 'value'),
     Input('right-side-second-label-dropdown', 'value'),
     Input('right-side-field-dropdown', 'value')]
)
def update_scatterpolar_right(main_category, selected_category, selected_label, second_category, second_label, selected_field):
    # Get unique labels for the main category selected in the middle
    main_category_labels = df[main_category].unique()

    # Filter the database based on left-side category labels and second category labels
    filtered_data = df[(df[selected_category] == selected_label) & (df[second_category] == second_label)]

    # Create traces for the selected field
    values = []
    for label in main_category_labels:
        label_data = filtered_data[filtered_data[main_category] == label]
        mean_value = label_data[selected_field].mean()
        if not math.isnan(mean_value):
            values.append(math.log(round(mean_value)))
        else:
            values.append(None)

    # Pad 'r' values with None to match the length of 'theta' values
    while len(values) < len(main_category_labels):
        values.append(None)

    trace = go.Scatterpolar(
        r=values,
        theta=main_category_labels,
        name=selected_field
    )

    layout = go.Layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    return go.Figure(data=[trace], layout=layout)


# Callback to update the output div based on the selected occupations
@app.callback(
    [Output('scatterpolar-middle', 'figure'),
     Output('pcp', 'figure')],
    [Input('first-occupation-dropdown', 'value'),
     Input('second-occupation-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_output(first_occupation, second_occupation, selected_category):
    # Convert single selected values to lists
    selected_values = [first_occupation] if isinstance(first_occupation, str) else first_occupation
    selected_values += [second_occupation] if isinstance(second_occupation, str) else second_occupation
    fields = ['Credit_Utilization_Ratio', 'Total_EMI_per_month', 'Outstanding_Debt',
              'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment']

    # Making fig1 scatterpolar
    fig1 = go.Figure()
    dimensions = []
    for value in selected_values:
        mean_table = []
        for field in fields:
            if selected_category == 'Loan_Type':
                masked_df = df[df[value] == 1]
            else:
                masked_df = df[df[selected_category] == value]
            calculated_mean = masked_df[field].mean()
            if not math.isnan(calculated_mean):
                mean_table.append(math.log(round(calculated_mean)))
            else:
                mean_table.append(0)
        fig1.add_trace(go.Scatterpolar(
            r=mean_table,
            theta=fields,
            name=value
        ))

    #Making fig2 pcp with go.parcoods
    if selected_category == 'Loan_Type':
        fig2 = go.Figure()
    else:
        for field in fields:
            if selected_category == 'Loan_Type':
                masked_field = pd.DataFrame(columns=[field])
                for value in selected_values:
                    new_values = df[df[value] == 1][field]
                    pd.concat(masked_field[field], new_values)
                    print(masked_field.head())
            else:
                masked_field = df[df[selected_category].isin(selected_values)][field]
            dimensions.append(
                dict(range=[masked_field.min(), masked_field.max()], label=field.replace("_", " "), values=masked_field))

        if selected_category == 'Loan_Type':
            fig2 = go.Figure(data=
            go.Parcoords(
                line=dict(color=range(len(selected_values)),
                          showscale=True),
                dimensions=dimensions,
            ))
        else:
            fig2 = go.Figure(data=
            go.Parcoords(
                line=dict(color=df[selected_category].astype('category').cat.codes,
                          showscale=True),
                dimensions=dimensions,
            ))
        fig2.update_xaxes(tickangle=-90)
    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
