# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
from datetime import datetime
import locale
import plotly.graph_objects as go


time_format = '%d. %B %Y  %H:%M'
locale.setlocale(locale.LC_TIME, 'de_DE')
time_second_group = datetime.strptime('16. Mai 2023 00:00', time_format)

def calculate_points(student_answer_list, right_answer, pos_percentage, neg_percentage):
     points_temp = 0
    
     for answer in student_answer_list:
        answer = answer.replace("\n", "")
        if answer[0] == " ":
            answer = answer.strip()
        if answer in right_answer:
            points_temp += (2*pos_percentage)
        else:
            points_temp -= (2*neg_percentage)
     return round(points_temp,2) if points_temp > 0 else 0

def calculate_mean(data):
    mean_first_test_group = 0
    count_frist_group = 0
    mean_second_test_group = 0
    count_second_group = 0
    for entry in data:
        time = datetime.strptime(entry['Beendet'], time_format)
        if time < time_second_group:
            mean_first_test_group += entry['points']
            count_frist_group +=1
        else:
            mean_second_test_group += entry['points']
            count_second_group += 1

    mean_first_test_group /= count_frist_group
    mean_second_test_group /= count_second_group
    return mean_first_test_group, mean_second_test_group

def create_histograms(data, quiz_nr):
    values_first_group = [d['points'] for d in data if datetime.strptime(d['Beendet'], time_format) < time_second_group]
    values_second_group = [d['points'] for d in data if datetime.strptime(d['Beendet'], time_format) > time_second_group]

    fig_first_group = go.Figure(data=[go.Histogram(x=values_first_group, histnorm='percent')])
    fig_first_group.update_layout(
        title={
            'text': f"Points Distribution of first testgroup of Quiz {quiz_nr}",
            'x': 0.5,
            'y': 0.9,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            title='Points',
            range=[0, 10]
        ),
        yaxis=dict(
            title='Percentage of answers',
        )
    )

    fig_second_group = go.Figure(data=[go.Histogram(x=values_second_group, histnorm='percent')])
    fig_second_group.update_layout(
        title={
            'text': f"Points Distribution of second testgroup of Quiz {quiz_nr}",
            'x': 0.5,
            'y': 0.9,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            title='Points',
            range=[0, 10]
        ),
        yaxis=dict(
            title='Percentage of answers',
        )
    )
    return fig_first_group, fig_second_group

#------- Quiz 1 -------#
#calculate points
data_1 = pd.read_csv('lek1_pre.csv').to_dict('records')
for i,d in enumerate(data_1):
    p = {'points':0, 'a1':0, 'a2':0, 'a3':0, 'a4':0, 'a5':0}
    d = {**p, **d}
    d.update({**p, **d})

    d['points'] += calculate_points(d['Antwort 1'].split(';'), d['Richtige Antwort 1'],0.333333, 1)
    d['a1'] = calculate_points(d['Antwort 1'].split(';'), d['Richtige Antwort 1'],0.333333, 1)
    d['points'] += calculate_points(d['Antwort 2'].split(';'), d['Richtige Antwort 2'],0.5, 0.5)
    d['a2'] = calculate_points(d['Antwort 2'].split(';'), d['Richtige Antwort 2'],0.5, 0.5)
    d['points'] += calculate_points(d['Antwort 3'].split(';'), d['Richtige Antwort 3'],0.5, 0.5)
    d['a3'] = calculate_points(d['Antwort 3'].split(';'), d['Richtige Antwort 3'],0.5, 0.5)
    d['points'] += calculate_points(d['Antwort 4'].split(';'), d['Richtige Antwort 4'],1, 0.333333)
    d['a4'] = calculate_points(d['Antwort 4'].split(';'), d['Richtige Antwort 4'],1, 0.333333)
    d['points'] += calculate_points(d['Antwort 5'].split(';'), d['Richtige Antwort 5'],1, 0.333333)
    d['a5'] = calculate_points(d['Antwort 5'].split(';'), d['Richtige Antwort 5'],1, 0.333333)

    data_1[i] = d

#mean
mean_first_group_quiz_1,mean_second_group_quiz_1 = calculate_mean(data=data_1)

#total tries
total_tries_quiz_1 = len(data_1)

#create Histograms
fig_first_group, fig_second_group = create_histograms(data_1, 1)


#------- Quiz 2 -------#
#calculate points
data_2 = pd.read_csv('lek2_pre.csv').to_dict('records')
for i,d in enumerate(data_2):
    p = {'points':0, 'a1':0, 'a2':0, 'a3':0, 'a4':0, 'a5':0}
    d = {**p, **d}
    d.update({**p, **d})

    d['points'] += calculate_points(d['Antwort 1'].split(';'), d['Richtige Antwort 1'], 0.333333, 1)
    d['a1'] = calculate_points(d['Antwort 1'].split(';'), d['Richtige Antwort 1'], 0.333333, 1)

    d['points'] += calculate_points(d['Antwort 2'].split(';'), d['Richtige Antwort 2'], 1, 0.333333)
    d['a2'] = calculate_points(d['Antwort 2'].split(';'), d['Richtige Antwort 2'], 1, 0.333333)

    d['points'] += calculate_points(d['Antwort 3'].split(';'), d['Richtige Antwort 3'],1,0.333333)
    d['a3'] = calculate_points(d['Antwort 3'].split(';'), d['Richtige Antwort 3'],1, 0.333333)

    d['points'] += calculate_points(d['Antwort 4'].split(';'), d['Richtige Antwort 4'],1, 0.333333)
    d['a4'] = calculate_points(d['Antwort 4'].split(';'), d['Richtige Antwort 4'],1, 0.333333)

    d['points'] += calculate_points(d['Antwort 5'].split(';'), d['Richtige Antwort 5'],1, 0.333333)
    d['a5'] = calculate_points(d['Antwort 5'].split(';'), d['Richtige Antwort 5'],1, 0.333333)

    data_2[i] = d

#mean
mean_first_group_quiz_2,mean_second_group_quiz_2 = calculate_mean(data=data_2)

#create Histograms
fig_first_group_2, fig_second_group_2 = create_histograms(data_2, 2)

#total tries
total_tries_quiz_2 = len(data_2)

#------- Quiz 3 -------#
#calculate points
data_3 = pd.read_csv('lek3_pre.csv').to_dict('records')
for i,d in enumerate(data_3):
    p = {'points':0, 'a1':0, 'a2':0, 'a3':0, 'a4':0, 'a5':0}
    d = {**p, **d}
    d.update({**p, **d})

    d['points'] += calculate_points(d['Antwort 1'].split(';'), d['Richtige Antwort 1'], 1, 0.333333)
    d['a1'] = calculate_points(d['Antwort 1'].split(';'), d['Richtige Antwort 1'], 1, 0.333333)
    d['points'] += calculate_points(d['Antwort 2'].split(';'), d['Richtige Antwort 2'], 1, 0.333333)
    d['a2'] = calculate_points(d['Antwort 2'].split(';'), d['Richtige Antwort 2'], 1, 0.333333)
    d['points'] += calculate_points(d['Antwort 3'].split(';'), d['Richtige Antwort 3'],1,0.333333)
    d['a3'] = calculate_points(d['Antwort 3'].split(';'), d['Richtige Antwort 3'],1, 0.333333)
    d['points'] += calculate_points(d['Antwort 4'].split(';'), d['Richtige Antwort 4'],1, 0.333333)
    d['a4'] = calculate_points(d['Antwort 4'].split(';'), d['Richtige Antwort 4'],1, 0.333333)
    d['points'] += calculate_points(d['Antwort 5'].split(';'), d['Richtige Antwort 5'],0.5, 0.5)
    d['a5'] = calculate_points(d['Antwort 5'].split(';'), d['Richtige Antwort 5'],0.5, 0.5)

    data_3[i] = d

#mean
mean_first_group_quiz_3,mean_second_group_quiz_3 = calculate_mean(data=data_3)

#create Histograms
fig_first_group_3, fig_second_group_3 = create_histograms(data_3, 3)

#total tries
total_tries_quiz_3 = len(data_3)



#------- Quiz 4 -------#
#calculate points
data_4 = pd.read_csv('lek4_pre.csv').to_dict('records')
for i,d in enumerate(data_4):
    p = {'points':0, 'a1':0, 'a2':0, 'a3':0, 'a4':0, 'a5':0}
    d = {**p, **d}
    d.update({**p, **d})

    d['points'] += calculate_points(d['Antwort 1'].split(';'), d['Richtige Antwort 1'], 1, 0.333333)
    d['a1'] = calculate_points(d['Antwort 1'].split(';'), d['Richtige Antwort 1'], 1, 0.333333)

    d['points'] += calculate_points(d['Antwort 2'].split(';'), d['Richtige Antwort 2'], 1, 0.5)
    d['a2'] = calculate_points(d['Antwort 2'].split(';'), d['Richtige Antwort 2'], 1, 0.5)

    d['points'] += calculate_points(d['Antwort 3'].split(';'), d['Richtige Antwort 3'],1,0.333333)
    d['a3'] = calculate_points(d['Antwort 3'].split(';'), d['Richtige Antwort 3'],1, 0.333333)

    d['points'] += calculate_points(d['Antwort 4'].split(';'), d['Richtige Antwort 4'],1, 0.333333)
    d['a4'] = calculate_points(d['Antwort 4'].split(';'), d['Richtige Antwort 4'],1, 0.333333)

    d['points'] += calculate_points(d['Antwort 5'].split(';'), d['Richtige Antwort 5'],1, 0.333333)
    d['a5'] = calculate_points(d['Antwort 5'].split(';'), d['Richtige Antwort 5'],1, 0.333333)

    data_4[i] = d

#mean
mean_first_group_quiz_4,mean_second_group_quiz_4 = calculate_mean(data=data_4)

#create Histograms
fig_first_group_4, fig_second_group_4 = create_histograms(data_4, 4)

# Initialize the app
app = Dash(__name__)

#total tries
total_tries_quiz_4 = len(data_4)

# App layout
app.layout = html.Div([
    html.Div(children='Testgruppe mit Overlays Durchschnitt Quiz 1:  ' + str(round(mean_first_group_quiz_1, 2))),
    html.Div(children='Testgruppe ohne Overlays Durchschnitt Quiz 1: ' + str(round(mean_second_group_quiz_1, 2))),
    html.Div(children='Total tries Quiz 1: ' + str(round(total_tries_quiz_1, 2))),
    dash_table.DataTable(data=data_1, page_size=10),
    html.Div([dcc.Graph(figure=fig_first_group, style={'width': '50%'}),
    dcc.Graph(figure=fig_second_group, style={'width': '50%'})], style={'display':'flex'}),
    #second quiz
    html.Div(children='Testgruppe mit Overlays Durchschnitt Quiz 2:  ' + str(round(mean_first_group_quiz_2, 2))),
    html.Div(children='Testgruppe ohne Overlays Durchschnitt Quiz 2: ' + str(round(mean_second_group_quiz_2, 2))),
    html.Div(children='Total tries Quiz 2: ' + str(round(total_tries_quiz_2, 2))),
    dash_table.DataTable(data=data_2, page_size=10),
    html.Div([dcc.Graph(figure=fig_first_group_2, style={'width': '50%'}),
    dcc.Graph(figure=fig_second_group_2, style={'width': '50%'})], style={'display':'flex'}),
    #third Quiz
    html.Div(children='Testgruppe mit Overlays Durchschnitt Quiz 3:  ' + str(round(mean_first_group_quiz_3, 2))),
    html.Div(children='Testgruppe ohne Overlays Durchschnitt Quiz 3: ' + str(round(mean_second_group_quiz_3, 2))),
    html.Div(children='Total tries Quiz 3: ' + str(round(total_tries_quiz_3, 2))),
    dash_table.DataTable(data=data_3, page_size=10),
    html.Div([dcc.Graph(figure=fig_first_group_3, style={'width': '50%'}),
    dcc.Graph(figure=fig_second_group_3, style={'width': '50%'})], style={'display':'flex'}),
    #fourth Quiz
    html.Div(children='Testgruppe mit Overlays Durchschnitt Quiz 4:  ' + str(round(mean_first_group_quiz_4, 2))),
    html.Div(children='Testgruppe ohne Overlays Durchschnitt Quiz 4: ' + str(round(mean_second_group_quiz_4, 2))),
    html.Div(children='Total tries Quiz 4: ' + str(round(total_tries_quiz_4, 2))),
    dash_table.DataTable(data=data_4, page_size=10),
    html.Div([dcc.Graph(figure=fig_first_group_4, style={'width': '50%'}),
    dcc.Graph(figure=fig_second_group_4, style={'width': '50%'})], style={'display':'flex'}),
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
