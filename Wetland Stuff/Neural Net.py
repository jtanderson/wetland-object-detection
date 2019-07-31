#In a neural network these are the variables we are concerned about:
#x= input layer
#hidden layers
#y = output layer
#W = weights
#b = biases
#o = Active function for each layer

#An output of a 2 layer Neural Network looks like
#y=o((W2)(o)((W1)(x) - (b1)) + (b2))

#Weights and Balances determine our y output
#Finding the right values for the weights and biases is called "training"
#Each training iteration consists of:
    #Calculating predicted y = feedforward
    #Updating Weights and Biases = backpropagation 



class NeuralNetwork:
    def_init_(self,x,y):
        self.input =x
        self.weights1 =np.random.rand(self.input.shape[1],4)
        self.weights2 =np.random.rand(4,1)
        self.y =y
        self.output =np.zeros(self.y.shape)
        
        
        def feedforward(self):
            self.layer1 = sigmoid(np.dot(self.input, self.weights1))
            self.output = sigmoid(np.dot(self.layer1, self.weights2))
            
        #application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        def backprop(self):
            d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) * sigmoid_derivative(self.output)))
            d_weights1 = np.dot(self.input.T, (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1)))
            
            #update the weights with the derivative (slope) of the loss function
            self.weights1 += d_weights1
            self.weights2 += d_weights2
