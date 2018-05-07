def replaceMatches(df, column, minRatio=90):
    #get a list of the unique strings
    strings = df[column].unique()

    for word in strings:
        matches = fuzzywuzz(word, strings)
        closeMatches = closeMatches = [matches[0] for matches in matches if matches[1] >= minRatio]
        rowsWithMatches = df[column].isin(closeMatches)
        df.loc[rowsWithMatches, column] = word

    newCol = df[column].unique()
    newCol.sort()
    return newCol


def fuzzywuzz(word, strings):
    return fuzzywuzzy.process.extract(word, strings, limit = 10, scorer = fuzzywuzzy.fuzz.token_sort_ratio)
