
import pickle

with open("kernel3.pkl", 'rb') as file:
    model = pickle.load(file)

# model = pickle.load(open("model.pkl"))

foo = ['40','0','0','144','122.5','123']

# foo = [40,0,0,144,122.5,123]

prediction = model.predict([list(map(float,foo))]) 

print(prediction)
    