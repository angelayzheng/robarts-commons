import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Robarts Commons Study Rooms Analysis 2025-2026
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup and Colour Palettes
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import datetime as dt

    rooms = pd.read_csv('data/2025-2026.csv', sep=',', header=0, na_filter=False)
    rooms['Date'] = pd.to_datetime(rooms['Date'])
    return dt, mo, pd, rooms


@app.cell
def _():
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import random

    sns.set_theme(style='ticks')

    palette = ['#A3D2CA', '#7AAAAD', '#50828F', '#C4A5D3', '#8F69A2', '#5A2C70', '#804C83', '#A66C96', '#DFB6B2', '#FFD8BE']
    sns.color_palette(palette)
    return palette, plt, random, sns, ticker


@app.cell
def _(palette, random, sns):
    random.shuffle(palette)
    sns.set_palette(palette)
    sns.color_palette(palette)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Figures
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Figure 0. Distribution by Status
    """)
    return


@app.cell
def _(plt, rooms, sns, ticker):
    statuses = ['Not visited', 'Visited', 'Picture taken']

    fig0 = sns.countplot(data=rooms, x='Status', order=statuses, hue='Status', legend=False)

    fig0.set_title('Distribution of Room Status')
    plt.xlabel('Status', labelpad=15)
    plt.ylabel('Count')

    fig0.minorticks_on()
    fig0.xaxis.set_minor_locator(ticker.FixedLocator([0, 1, 2])) 
    fig0.yaxis.set_major_locator(ticker.MultipleLocator(2))
    fig0.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    fig0.grid(which='minor', linestyle='--')

    plt.ylim(0, 18)

    # fig0.get_figure().savefig('figures/2025-2026/00_status-distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Figure 1. Distribution by Floor
    """)
    return


@app.cell
def _(plt, rooms, sns):
    fig1 = sns.countplot(data=rooms[rooms['Status'] != 'Not visited'], x='Floor', hue='Floor', legend=False)

    fig1.set_title('Distribution of Visited Study Rooms by Floor')
    plt.ylabel('Count')

    # fig1.get_figure().savefig('figures/2025-2026/01_floor-distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Figure 2. Distribution by Room Letter
    """)
    return


@app.cell
def _(plt, rooms, sns, ticker):
    letters = list(set(rooms['Letter']))
    letters.sort()

    fig2 = sns.countplot(data=rooms[rooms['Status'] != 'Not visited'], x='Letter', order=letters, hue='Letter', legend=False)

    fig2.set_title('Distribution of Visited Study Rooms by Room Letter')
    plt.xlabel('Room Letter', labelpad=15)
    plt.ylabel('Count')

    fig2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # fig2.get_figure().savefig('figures/2025-2026/02_letter-distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Figure 3. Distribution by Author
    """)
    return


@app.cell
def _(plt, rooms, sns, ticker):
    filtered = rooms[(rooms['Status'] != 'Not visited') & (rooms['Author'] != '')]

    counts = filtered['Author'].value_counts()
    order = sorted(
        [a for a in counts.index if a != 'N/A'],
        key=lambda a: (-counts[a], a)
    )
    if 'N/A' in counts.index:
        order.append('N/A')

    fig3 = sns.countplot(data=rooms[rooms['Status'] != 'Not visited'][rooms['Author'] != ''], x='Author', order=order, hue='Author', legend=False)

    fig3.set_title('Distribution of Visited Study Rooms by Author')
    plt.ylabel('Count')

    fig3.set_xticklabels(fig3.get_xticklabels(), rotation=45, ha='right')
    fig3.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # fig3.get_figure().savefig('figures/2025-2026/03_author-distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Figure 4. Distribution by Month
    """)
    return


@app.cell
def _(plt, rooms, sns):
    filtered_date = rooms.copy()
    filtered_date['Date'] = filtered_date['Date'][filtered_date['Date'].notna()].dt.month_name()
    months = ['September', 'October', 'November', 'December', 'January', 'February', 'March', 'April']

    fig4 = sns.countplot(data=filtered_date, x='Date', order=months, hue='Date', legend=False)

    fig4.set_title('Distribution of Visited Study Rooms by Month')
    plt.ylabel('Count')

    fig4.set_xticklabels(fig4.get_xticklabels(), rotation=45, ha='right')

    # fig4.get_figure().savefig('figures/2025-2026/04_month-distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Figure 5. Timeline
    """)
    return


@app.cell
def _(dt, pd, plt, rooms, sns):
    import matplotlib.dates as mdates

    timeline_data = rooms[rooms['Date'].notna()][['ID', 'Date']].copy()

    timeline_data.sort_values(by=['Date', 'ID'], ascending=[True, True], inplace=True)
    timeline_data['Cumulative'] = timeline_data['Date'].rank(ascending=True, method='first').astype(int)

    print(timeline_data)

    new_data = pd.DataFrame([{'ID': '', 'Date': dt.datetime(2025, 10, 1), 'Cumulative': 0},
                             {'ID': '', 'Date': dt.datetime(2025, 11, 8), 'Cumulative': 0},
                             {'ID': '', 'Date': dt.datetime(2026, 7, 1), 'Cumulative': 15}])
    timeline_data = pd.concat([timeline_data, new_data], ignore_index=True)

    sns.set_theme(style='whitegrid')
    fig5 = sns.lineplot(data=timeline_data, x='Date', y='Cumulative', color='#5A2C70', legend=False, errorbar=None)

    fig5.set_title('Timeline of Visited Study Rooms')
    plt.xlabel('Date', labelpad=15)
    plt.ylabel('Count')

    plt.xlim(dt.datetime(2025, 10, 1), dt.datetime(2026, 5, 1))
    plt.ylim(-0.1, 16)

    fig5.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    fig5.xaxis.set_major_locator(mdates.MonthLocator())

    # fig5.get_figure().savefig('figures/2025-2026/05_timeline.png', dpi=300, bbox_inches='tight')
    plt.show()
    return


if __name__ == "__main__":
    app.run()
