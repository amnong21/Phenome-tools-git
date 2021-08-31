import pandas as pd
import difflib

def check_variables(variables_list, data):
    
    columns = data.columns

    decisions = pd.DataFrame(None, index=data.columns, columns=['Exact', 'Suggestion 1', 'Suggestion 2',
                                                            'Change'])
    decisions.at[:, 'Suggestion 1'] = ""
    decisions.at[:, 'Suggestion 2'] = ""
    decisions.at[:, 'Change'] = ""

    for variable in decisions.index:

        if variable.lower() in variables_list:
            decisions.at[variable, 'Exact'] = True
        else:
            decisions.at[variable, 'Exact'] = False
            suggestions = difflib.get_close_matches(variable, variables_list, 2, 0.5)
            decisions.at[variable, 'Suggestion 1'] = "(No suggestions)"
            if len(suggestions) > 0:
                decisions.at[variable, 'Suggestion 1'] = suggestions[0]
                decisions.at[variable, 'Change'] = suggestions[0]
            if len(suggestions) > 1:
                decisions.at[variable, 'Suggestion 2'] = suggestions[1]

    
    changes = decisions[decisions['Change'].notnull()].filter(['index', 'Change']).to_dict()
    replace_dict = changes['Change']
    # print('-'*40)
    # print(replace_dict)
    # print('-'*40)

    # data.rename(columns=replace_dict, inplace=True)
    
    return decisions