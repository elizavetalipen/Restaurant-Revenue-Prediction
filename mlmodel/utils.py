
from PyPDF2 import PdfFileWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from category_encoders import TargetEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import PowerTransformer
from tensorflow import keras
import pandas as pd
import numpy as np
from joblib import load


def dict_to_pdf(data: dict):
    ''' This function generates pdf file from dict and applies some styling'''

    pdf_buffer = BytesIO()
    pdf_writer = PdfFileWriter()
    pdf_page = pdf_writer.addBlankPage(*letter)  

    canvas = Canvas(pdf_buffer, pagesize=letter, bottomup=0)
    x_pos = 150
    y_pos = 400
    line_spacing = 40
    canvas.setFont('Helvetica-Bold', 16)

    for key, value in data.items():
        # font color
        canvas.setFillColorRGB(0.2, 0.2, 0.2)

        canvas.drawString(x_pos, y_pos, f"{key.capitalize()}:")
        canvas.drawString(x_pos + 100, y_pos, str(value))
        y_pos -= line_spacing

    canvas.showPage() 
    canvas.save()  
    return pdf_buffer.getvalue()


def make_prediction(data:dict):
    ''''This function transforms the input data from user, 
    loads the model and calculates prediction'''

    train = pd.read_csv('trainedmodels/train.csv')
    data = pd.DataFrame.from_dict([data])

    # преобразование дат
    today = pd.to_datetime("now")
    data["Open Date"] = pd.to_datetime(data["Open Date"])
    data["NMonths"] = (today - data["Open Date"])/np.timedelta64(1, 'M')
  
    # преобразование городов
    if list(data["City"]) in list(train["City"].unique()):
        target_encoder = TargetEncoder()
        train["CityEnc"] = target_encoder.fit_transform(train["City"], train["revenue"])
        city_mean = train.groupby("City")["CityEnc"].mean().reset_index().rename(columns={"CityEnc": 'CityMean'})
        data = data.merge(city_mean, on="City", how="left")
        data["CityEnc"] = data["CityMean"].fillna(train["CityEnc"].mean())
        data.drop("CityMean", axis=1, inplace=True)
    else:
        data["CityEnc"] = 0.0

    # преобразование численных данных
    minmaxsc = MinMaxScaler()
    pcols = ["P2", "P6", "P23", "P28"]
    data[pcols+["NMonths", "CityEnc"] ] = minmaxsc.fit_transform(data[pcols+["NMonths", "CityEnc"]])

    # преобразование категориальны данных
    types_list = ["FC", "IL", "DT"]
    groups_list = ["Big Cities", "Other"]
    type_dummies = pd.get_dummies(data["Type"], columns=types_list, prefix='Type')
    group_dummies = pd.get_dummies(data["City Group"], columns=groups_list, prefix='Group')

    for t in types_list:
        if f'Type_{t}' not in type_dummies.columns:
            type_dummies[f'Type_{t}'] = 0.0
    for g in groups_list:
        if f'Group_{g}' not in group_dummies.columns:
            group_dummies[f'Group_{g}'] = 0.0

    data = pd.concat([data, type_dummies, group_dummies], axis=1)
    data.drop(["Open Date", "City", "City Group", "Type"], axis=1, inplace=True)

    # загрузка модели и выполнение предсказания
    model = keras.models.load_model('trainedmodels/model_keras.h5')
    prediction = model.predict(data.values)
    pt = PowerTransformer(method='box-cox')
    pt.fit(train["revenue"].values.reshape(-1, 1))
    prediction = pt.inverse_transform(prediction)

    return float(prediction[0][0])


  


  



