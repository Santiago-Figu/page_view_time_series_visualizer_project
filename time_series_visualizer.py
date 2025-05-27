import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
n=5
file_path = os.path.join(os.getcwd(),"data", "fcc-forum-pageviews.csv")
df = pd.read_csv(filepath_or_buffer=file_path, delimiter=",")
df= df.set_index('date')

# Clean data
# Clean the data by filtering out days when the page views were in the top 2.5% of the dataset 
# or bottom 2.5% of the dataset.
# Note: La desviación estándar asume una distribución simétrica (como la normal), 
# pero si los datos están sesgados, los percentiles funcionan mejor. 
# Ejemplo: Si hay muchos valores extremos, la desviación estándar los incluiría, 
# mientras que los percentiles los eliminan directamente.

#calculo de percentiles
# print(f"count: {df.count()}")

low_percentil = df['value'].quantile(0.025) # percentil 2.5% / bottom 2.5%

high_percentil = df['value'].quantile(0.975) # percentil 97.5% / top 2.5%

print(f"low: {low_percentil}")
print(f"high: {high_percentil}")
df = df[(df['value'] >= low_percentil) & (df['value'] <= high_percentil)]
# print(f"count: {df.count()}")


def draw_line_plot():
    # Draw line plot
    # print(f"Line plot {df.head(n)}")

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize=12)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylabel('Page Views', fontsize=10)

    ax.xaxis.set_major_locator(plt.MaxNLocator(8))  # ~8 marcas en eje X (como en la imagen)

    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    plt.grid(False)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.index = pd.to_datetime(df_bar.index)

    #group data and calculate averages
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')
    df_bar = df_bar.groupby(['year', 'month']).mean().reset_index()

    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)
    df_bar = df_bar.sort_values(['year', 'month'])

    # reshaped DataFrame organized by given index / column values.
    df_bar = df_bar.pivot(index='year', columns='month', values='value')

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Bar configuration
    bar_width = 0.07
    years = df_bar.index.astype(str)
    x = range(len(years))

    # Draw bars for each month
    for i, month in enumerate(month_order):
        ax.bar(
            [pos + i * bar_width for pos in x],  # calculate positions in axe x for each year
            df_bar[month],
            width=bar_width,
            label=month
        )

    # styles
    ax.set_xlabel('Years', fontsize=12)
    ax.set_ylabel('Average Page Views', fontsize=12)
    ax.set_xticks([pos + (len(month_order)/2 * bar_width - bar_width/2) for pos in x])
    ax.set_xticklabels(years)
    ax.legend(title='Months', loc='upper left')

    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_bar_plot_2():
    # Copy and modify data for monthly bar plot
    print(f"df {df.head(n)}")
    df_bar = df.copy()
    df_bar.index= pd.to_datetime(df_bar.index)
    
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')
    

    df_bar = df_bar.groupby(['year', 'month']).mean().reset_index()
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)
    df_bar = df_bar.sort_values(['year', 'month'])

    plt.figure(figsize=(12, 6))
    graph = sns.barplot(
        data=df_bar,
        x='year',
        y='value',
        hue='month',
        palette='tab10'
    )

    # plt.title('Average Page Views per Month', fontsize=14)
    plt.xlabel('Years', fontsize=12)
    plt.ylabel('Average Page Views', fontsize=12)
    # plt.xticks(rotation=45, ha='right')
    # loc values = 'best', 'upper right', 'upper left', 'lower left', 
    # 'lower right', 'right', 'center left', 'center right',
    # 'lower center', 'upper center', 'center'
    plt.legend(title='Months', loc='upper left')
    # plt.legend(title='Months', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    # plt.show()
    fig = graph.figure
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    plt.close()
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()

    # df_box.reset_index(inplace=True)
    # df_box['year'] = [d.year for d in df_box.date]
    # df_box['month'] = [d.strftime('%b') for d in df_box.date]

    #In order to use the proposed logic, I had to adapt the code to use the index, 
    # because the 'date' column was set as an index (instruction: Consider setting index column to 'date')

    df_box.index= pd.to_datetime(df_box.index)
    df_box['year'] = [d.year for d in df_box.index]
    df_box['month'] = [d.strftime('%b') for d in df_box.index]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1, hue='year', legend=False, palette='tab10')
    ax1.set_title('Year-wise Box Plot (Trend)', fontsize=14)
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Page Views', fontsize=12)
    
    # Month-wise Box Plot (Seasonality)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=ax2, hue='month', legend=False, palette='tab10')
    ax2.set_title('Month-wise Box Plot (Seasonality)', fontsize=14)
    ax2.set_xlabel('Month', fontsize=12)
    ax2.set_ylabel('Page Views', fontsize=12)

    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
