import numpy as np

class Layer:
  def __init__(self):
    self.prev_layer = None
    self.output = None
    self.next_layer = None

  def foward(self):
    raise NotImplementedError
  
  def backward(self):
    raise NotImplementedError

class InputLayer(Layer):
  def __init__(self, size):
    self.size = size
    super().__init__()
  
  def foward(self, input_data):
    self.output = input_data

class DenseLayer(Layer):
  def __init__(self, size, activation, drop_probability=0):
    self.size = size
    self.activation = activation
    self.drop_probability = drop_probability
    self.gradient = None
    self.weights = None
    self.bias = None
    self.pre_activation = None
    super().__init__()

  def initialize_weights(self):
    weights_shape = self.prev_layer.size, self.size
    self.weights = np.random.uniform(-0.5, 0.5, weights_shape)

  def initialize_bias(self):
    bias_size = self.size
    self.bias = np.random.uniform(-0.5, 0.5, bias_size)

  def foward(self):
    self.pre_activation = (self.prev_layer.output @ self.weights) + self.bias
    self.output = self.activation(self.pre_activation)
    if self.drop_probability:
      keep_prob = 1 - self.drop_probability
      self.drop_mask = np.random.binomial(1, keep_prob, size=self.output.shape)
      self.scale = 1 / keep_prob if keep_prob > 0 else 0
      self.output *= self.drop_mask * self.scale
  
  def backward(self):
    self.gradient = (self.next_layer.gradient @ self.next_layer.weights.T) * self.activation(self.pre_activation, derivative=True)
  
  def update_weights(self, learning_rate):
    self.weights -= learning_rate * (self.prev_layer.output.T @ self.gradient)
    self.bias -= learning_rate * self.gradient.mean(axis=0)

class OutputLayer(DenseLayer):
  def __init__(self, size, activation, cost):
    self.cost = cost
    self.loss = None
    super().__init__(size, activation)

  def backward(self, target):
    self.gradient = self.cost(self.output, target, derivative=True) * self.activation(self.pre_activation, derivative=True)
  
  def calculate_loss(self, target):
    return self.cost(self.output, target)
  
  def calculate_accuracy(self, target):
    predicted = self.output
    hits = np.sum(np.argmax(predicted, axis=1) == np.argmax(target, axis=1))
    accuracy = hits / len(target)
    return accuracy
