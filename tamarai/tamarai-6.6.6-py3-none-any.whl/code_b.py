from sklearn import tree


def food_ai(original_a, original_b, new):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(original_a, original_b)
    return clf.predict(new)
