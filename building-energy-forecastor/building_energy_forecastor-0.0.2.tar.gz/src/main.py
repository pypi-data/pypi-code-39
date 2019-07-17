import pandas as pd
import src.preprocess.building_preprocess as bp
import src.model.building_model as bm


def main():

    # Get the data
    print('Your data files should be in your current repository and in .csv format.\n')
    filename = input('Enter your file\'s name:  ')
    train_raw_df = pd.read_csv('./' + filename)

    # Preprocessing
    train_df = bp.time_to_cycle(train_raw_df)
    x_train, x_test, y_train, y_test = bm.clusterisation(train_df)

    # Training and error evaluation
    reg = bm.building_regressor()
    bm.building_train(reg, x_train, y_train)
    y_hat = bm.building_prediction(reg, x_test)
    print('The mean squared logged error is:  {}\nThe closer to 0.0 the better ;)'.format(bm.error_computation(y_test, y_hat)))

    # TODO: Intervalle de confiance

    # Prediction
    print('Computing the energy consumption for tomorrow...')
    test = bp.creat_test()
    prediction = bm.building_prediction(reg, test)
    print('Result: {}'.format(prediction))

    # TODO: plot resultat avec le reste????????????????????????????????


main()





