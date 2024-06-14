import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv", parse_dates = ['date'], index_col = 'date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]
print(df.info())

def draw_line_plot():
    # Draw line plot\
    fig, ax = plt.subplots(figsize=(20, 6))
    ax.plot(df.index, df['value'], color='r')
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df['year'] = df.index.year
    df['month'] = df.index.month_name()
    df_bar = df.groupby(['year', 'month']).mean().reset_index()

    table = pd.pivot_table(df_bar, values='value', index='year', columns='month', dropna=False)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    table = table.reindex(columns=months)
    # Draw bar plot

    fig, ax = plt.subplots(figsize=(12,6))
    table.plot(kind='bar', ax=ax)
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title='Months')



    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig,(ax1, ax2) = plt.subplots(1, 2, figsize = (16, 9))
    sns.boxplot(x="year", y="value", data=df_box, ax=ax1).set(title = "Year-wise Box Plot (Trend)", xlabel = 'Year', ylabel = 'Page Views')
    sns.boxplot(x="month", y="value", data=df_box, ax=ax2, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct','Nov', 'Dec']).set(title = "Month-wise Box Plot (Seasonality)", xlabel = 'Month', ylabel = 'Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig