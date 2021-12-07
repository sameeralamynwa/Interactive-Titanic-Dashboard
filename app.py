import pandas as pd # importing pandas
import plotly.express as px # importing plotly.express for visualizing the dataset
import streamlit as st # importing streamlit which is used for web apps


# Streamlit supports a wide range of characters including emojis
st.set_page_config(page_title = "Titanic Dashboard", page_icon = "🚢", layout = "wide")

# Streamlit cache decorator so that we do not have to read the csv file again and again
@st.cache
def read_data():
    df = pd.read_csv("train.csv")

    df['Sex'].replace({
        "male" : "Male",
        "female" : "Female"
    }, inplace = True)

    df['Embarked'].replace({
        "S" : "Southampton",
        "C" : "Cherbourg",
        "Q" : "Queenstown"
    }, inplace = True)

    return df


df = read_data()

# A sidebar to for all the filters.
st.sidebar.header("Apply Filters ")

embarked = st.sidebar.multiselect(
    "Embarked ",
    options = df["Embarked"].unique(),
    default = df["Embarked"].unique(),
)

pclass = st.sidebar.multiselect(
    "Passenger Class ",
    options = df["Pclass"].unique(),
    default = df["Pclass"].unique(),
)

sex = st.sidebar.multiselect(
    "Sex:  ",
    options = df["Sex"].unique(),
    default = df["Sex"].unique(),
)

# Using the query method with all the three filters that we have in our dataset.
df_selection = df.query(
    "Embarked == @embarked & Pclass == @pclass & Sex == @sex"
)

st.title("🚢 Titanic Dashboard") # Title of our web app

st.markdown("##") # Used to separate paragraphs

# df_selection is used because it queries only from those attributes that are checked in the filters
total_deaths = df_selection['Survived'].sum()
median_age = df_selection['Age'].median() # 50 percent of people above/below this age abroad 
total_survival = len(df_selection['Survived']) - total_deaths

# Plotting three graphs horizontally.
left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Deaths 💀")
    st.subheader(f" {total_deaths}")
with middle_column:
    st.subheader("Median Age Aboard 👦")
    st.subheader(f" {median_age}")
with right_column:
    st.subheader("Total Survivals 👫")
    st.subheader(f" {total_survival}")

st.markdown("---") # Used to separate paragraphs

box_plot = px.box(df_selection, 
    y = "Age", 
    x = "Pclass",
    title = "<b>Age and Passengers' Class</b>"
)

# Using update_layout method to give the manual xlabels and ylabels
box_plot.update_layout(
    xaxis_title_text = "Class",
    yaxis_title_text = "Age",
)

# use_container_width is made True so that it does not occupy the whole space
left_column.plotly_chart(box_plot, use_container_width = True)

pie_chart = px.pie(names = df_selection["Embarked"].unique(), 
    values = df_selection.groupby("Embarked")["Embarked"].count(), 
    hole = 0.5,
    title="<b>Embarked</b>"
)

middle_column.plotly_chart(pie_chart, use_container_width = True)

group_plot = px.histogram(df_selection, 
    x = "Survived",
    color = "Sex", 
    barmode = 'group',
    title="<b>Survival by Sex</b>"
)

# Using update_layout method to give the manual xlabels and ylabels
group_plot.update_layout(
    xaxis_title_text = "Survived",
    yaxis_title_text = "Frequency"
)

right_column.plotly_chart(group_plot,use_container_width = True)

# df_selection is used because it queries only from those attributes that are checked in the filters
age_by_survival = (
    df_selection.groupby(by=["Age"]).sum()[["Survived"]].sort_values(by="Survived")
)

fig_age_survival = px.bar(
    age_by_survival,
    x = "Survived",
    y = age_by_survival.index,
    orientation = "h",
    title="<b>Survival by Age</b>",
    color_discrete_sequence = ["#0083B8"] * len(age_by_survival),
    template = "plotly_white",
)

# Using update_layout method to give the manual xlabels and ylabels
fig_age_survival.update_layout(
    plot_bgcolor = "rgb(0, 0, 26)",
    xaxis = (dict(showgrid=False))
)

# use_container_width is made True so that it does not occupy the whole space
left_column.plotly_chart(fig_age_survival, use_container_width = True)

pie_chart = px.pie(names = ["Survived", "Dead"],
    values = df.groupby("Survived")["Survived"].count(), 
    hole = 0.5,
    title="<b>Dead and Survived</b>",
    labels = ["Survived", "Dead"],
)

middle_column.plotly_chart(pie_chart, use_container_width = True)

plot = px.histogram(df_selection, 
    x = "Pclass",
    color = "Sex", 
    barmode = 'group',
    title = "<b>Siblings Aboard</b>",
)

plot.update_layout(
    xaxis_title_text = "Passenger Class",
    yaxis_title_text = "Frequency",
)

right_column.plotly_chart(plot, use_container_width = True);

line_plot = px.line(df_selection, 
    x = "Fare",
    y = ["Fare_Tax", "Food Charges", "Luggage Charges"], # Plotting multiple lines for one x
    title = "<b>Different Fares</b>",
)

# Using update_layout method to give the manual xlabels and ylabels
line_plot.update_layout(
    yaxis_title_text = "Amount",
)   

st.plotly_chart(line_plot, use_container_width = True)
