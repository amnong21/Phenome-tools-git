import pandas as pd

def convert_map(df):
    '''Gets pandas df and returns a list of plots ready for Phenome Upload'''

    [rows, cols] = df.shape
    # Empty table of plots
    plots = []
    # Loop
    for row in range(1, rows+1):
        for col in range(1, cols+1):
            if pd.isna(df.iat[row-1, col-1]) == True:
                continue
            else:
                plot_name = str(df.iat[row-1, col-1])
                plot = [plot_name, plot_name, row, col]
                plots.append(plot)
    return plots