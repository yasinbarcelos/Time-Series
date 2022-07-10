import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score

def u1(f,y):
    '''The function takes in two pandas series, one with the actual values and one with the predicted
    values, and returns the u1 score
    
    Parameters
    ----------
    f
        the predicted values
    y
        the actual values
    
    Returns
    -------
        the value of the u1 score.
    
    '''
    y = y.reset_index(drop=True).values.flatten()
    f = f.reset_index(drop=True).values.flatten()
    df = pd.DataFrame({'f_i':f, 'y_i': y})
    df['(y_i - f_i)^2'] = np.square(df['y_i'] - df['f_i'])
    df['y_i^2'] = np.square(df['y_i'])
    df['f_i^2'] = np.square(df['f_i'])
    return (np.sqrt(np.mean(df['(y_i - f_i)^2'])))/(np.sqrt(np.mean(df['y_i^2']))+np.sqrt(np.mean(df['f_i^2'])))

def u2(f,y):
    '''> The function takes in two pandas series, one of the actual values and one of the forecasted
    values, and returns the U2 score
    
    Parameters
    ----------
    f
        forecast
    y
        actual values
    
    Returns
    -------
        the square root of the sum of the numerator divided by the sum of the denominator.
    
    '''
    y = y.reset_index(drop=True).values.flatten()
    f = f.reset_index(drop=True).values.flatten()
    df = pd.DataFrame({'f_i+1':f, 'y_i+1': y})
    df['y_i'] = df['y_i+1'].shift(periods=1)
    df['numerator'] = np.square((df['f_i+1'] - df['y_i+1']) / df['y_i'])
    df['denominator'] = np.square((df['y_i+1'] - df['y_i']) / df['y_i'])
    df.dropna(inplace=True)
    return np.sqrt(np.sum(df['numerator'])/np.sum(df['denominator']))


def prediction_of_change_in_direction(y_true, y_pred):
    '''It takes the difference between each element in the array and the next element in the array, and
    then multiplies the two arrays together. If the result is positive, it adds 1 to the result. It then
    divides the result by the length of the array and multiplies by 100 to get a percentage
    
    Parameters
    ----------
    y_true
        The actual values of the target variable
    y_pred
        The predicted values
    
    Returns
    -------
        The percentage of times the model predicted the correct direction of change.
    
    '''
    y_true = np.asarray(y_true).reshape(-1)
    y_pred = np.asarray(y_pred).reshape(-1)

    true_sub = np.subtract(y_true[0:(len(y_true) - 1)], y_true[1:(len(y_true))])
    pred_sub = np.subtract(y_pred[0:(len(y_pred) - 1)], y_pred[1:(len(y_pred))])

    mult = true_sub * pred_sub
    result = 0
    for m in mult:
        if m > 0:
            result = result + 1

    return (100 * (result / len(y_true)))

def evaluate_all(actual_df,predicted_df):    
    '''It calculates the MSE, MAE, RMSE, MAPE, POCID, R2, Theil's U1 and Theil's U2
    
    Parameters
    ----------
    actual_df
        The actual values of the time series
    predicted_df
        The predicted values
    
    Returns
    -------
        the values of the metrics.
    
    '''

    mse = mean_squared_error(actual, predicted)
    print('MSE: (Mean Squared Error) '+str(mse))

    mae = mean_absolute_error(actual, predicted)
    print('MAE: Mean Absolute Error '+str(mae))

    rmse = np.sqrt(mean_squared_error(actual, predicted))    
    print('RMSE: (Root Mean Square Error): '+str(rmse))

    mape = np.mean(np.abs(predicted - actual)/np.abs(actual))
    print('MAPE (Mean Absolute Percentage Error): '+str(mape))

    pocid = np.mean((np.sign(actual[1:] - actual[:-1]) == np.sign(predicted[1:] - predicted[:-1])).astype(int))
    print('POCID (Prediction of Change in Direction): '+str(pocid))

    r2 = r2_score(actual,predicted) 
    print('R2 (Coeficiente de Determinação): '+str(r2))

    theilsu1 = u1(predicted_df,actual_df)
    print('Theil’s U1 : '+str(theilsu1))

    theilsu2 = u2(predicted_df,actual_df)
    print('Theil’s U2 : '+str(theilsu2))

    return mse,mae,rmse,mape,pocid,r2,theilsu1,theilsu2