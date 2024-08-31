from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

def training(pre_path):
    model_name = "example"
    file_name_to_save = "models/Classification/"+model_name+"_model.sav"

    #PreProcessing
    dataframe_new = pd.read_csv(pre_path)

    #Spliting Classes and Features
    x = dataframe_new.iloc[:,2:13]
    y = dataframe_new.iloc[:,13:14]
    x.drop(["X_GPS","Y_GPS"],axis=1,inplace=True)
    x_dataset = x.values
    y_dataset = y.values

    #Spliting Dataset
    train_x,test_x,train_y,test_y = train_test_split(x_dataset,y_dataset, test_size=0.3, random_state=42, shuffle=True)

    #Model ANN Code
    classifier = MLPClassifier(hidden_layer_sizes=(100,50,25), max_iter=150,activation = 'relu',solver='adam',random_state=1)
    classifier.fit(train_x, train_y)
    # Model Decision Tree
    # classifier = tree.DecisionTreeClassifier()
    # classifier.fit(train_x, train_y)
    # Model KNN
    # classifier = KNeighborsClassifier(n_neighbors=8, metric='minkowski', p=2 )
    # classifier.fit(train_x, train_y)
    # Model Gaussian
    # classifier = GaussianNB()
    # classifier.fit(train_x, train_y)

    joblib.dump(classifier, file_name_to_save)
    pred_y = classifier.predict(test_x)
    print(classification_report(test_y, pred_y))
