import numpy as np

from cs294_129.layers import *
from cs294_129.fast_layers import *
from cs294_129.layer_utils import *


class ThreeLayerConvNet(object):
  """
  A three-layer convolutional network with the following architecture:

  conv - relu - 2x2 max pool - affine - relu - affine - softmax

  The network operates on minibatches of data that have shape (N, C, H, W)
  consisting of N images, each with height H and width W and with C input
  channels.
  """

  def __init__(self, input_dim=(3, 32, 32), num_filters=32, filter_size=7,
               hidden_dim=100, num_classes=10, weight_scale=1e-3, reg=0.0,
               dtype=np.float32):
    """
    Initialize a new network.

    Inputs:
    - input_dim: Tuple (C, H, W) giving size of input data
    - num_filters: Number of filters to use in the convolutional layer
    - filter_size: Size of filters to use in the convolutional layer
    - hidden_dim: Number of units to use in the fully-connected hidden layer
    - num_classes: Number of scores to produce from the final affine layer.
    - weight_scale: Scalar giving standard deviation for random initialization
      of weights.
    - reg: Scalar giving L2 regularization strength
    - dtype: numpy datatype to use for computation.
    """
    self.params = {}
    self.reg = reg
    self.dtype = dtype

    ############################################################################
    # TODO: Initialize weights and biases for the three-layer convolutional    #
    # network. Weights should be initialized from a Gaussian with standard     #
    # deviation equal to weight_scale; biases should be initialized to zero.   #
    # All weights and biases should be stored in the dictionary self.params.   #
    # Store weights and biases for the convolutional layer using the keys 'W1' #
    # and 'b1'; use keys 'W2' and 'b2' for the weights and biases of the       #
    # hidden affine layer, and keys 'W3' and 'b3' for the weights and biases   #
    # of the output affine layer.                                              #
    ############################################################################
    C, H, W = input_dim

    # Conv Layer
    F = num_filters
    filter_height = filter_size
    filter_width = filter_size
    stride_conv = 1
    p = (filter_size - 1)/2
    Hc = (H + 2 * p - filter_height) /stride_conv + 1
    Wc = (W + 2 * p - filter_width) /stride_conv + 1
    b1 = np.zeros(F)
    W1 = np.random.randn(F, C, filter_height, filter_width) * weight_scale
    print(weight_scale)
    # Max Pool Layer
    p_w = 2
    p_h = 2
    p_s = 2
    Hp = (Hc - p_h) / p_s + 1
    Wp = (Wc - p_w) / p_s + 1

    # affine layer
    Hh = hidden_dim
    b2 = np.zeros(Hh)
    W2 = np.random.randn(F*Hp*Wp, Hh) * weight_scale

    # output
    b3 = np.zeros(num_classes)
    W3 = np.random.randn(Hh, num_classes) * weight_scale

    self.params.update({'W1': W1, 'W2': W2, 'W3': W3, 'b1': b1, 'b2': b2, 'b3': b3})
    ############################################################################
    #                             END OF YOUR CODE                             #
    ############################################################################

    for k, v in self.params.iteritems():
      self.params[k] = v.astype(dtype)


  def loss(self, X, y=None):
    """
    Evaluate loss and gradient for the three-layer convolutional network.

    Input / output: Same API as TwoLayerNet in fc_net.py.
    """
    W1, b1 = self.params['W1'], self.params['b1']
    W2, b2 = self.params['W2'], self.params['b2']
    W3, b3 = self.params['W3'], self.params['b3']

    # pass conv_param to the forward pass for the convolutional layer
    filter_size = W1.shape[2]
    conv_param = {'stride': 1, 'pad': (filter_size - 1) / 2}

    # pass pool_param to the forward pass for the max-pooling layer
    pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

    scores = None
    ############################################################################
    # TODO: Implement the forward pass for the three-layer convolutional net,  #
    # computing the class scores for X and storing them in the scores          #
    # variable.                                                                #
    ############################################################################
    x = X
    w = W1
    b = b1
    # convolution
    conv_x, cache_conv_x = conv_relu_pool_forward(x, w, b, conv_param, pool_param)
    N, F, Hp, Wp = conv_x.shape
    # Affine layer
    x = conv_x.reshape((N, F*Hp*Wp))
    w = W2
    b = b2
    hidden_layer, cache_hidden_layer = affine_relu_forward(x, w, b)
    N, Hh = hidden_layer.shape
    # Output layer
    x = hidden_layer
    w = W3
    b = b3
    scores, cache_scores = affine_forward(x, w, b)
    # print(scores.shape, y.shape)


    ############################################################################
    #                             END OF YOUR CODE                             #
    ############################################################################

    if y is None:
      return scores
    #print(scores)
    loss, grads = 0, {}
    ############################################################################
    # TODO: Implement the backward pass for the three-layer convolutional net, #
    # storing the loss and gradients in the loss and grads variables. Compute  #
    # data loss using softmax, and make sure that grads[k] holds the gradients #
    # for self.params[k]. Don't forget to add L2 regularization!               #
    ############################################################################
    data_loss, dscores = softmax_loss(scores, y)
    #print(data_loss)
    reg_loss = 0.5 * self.reg *(np.sum(W1**2) + np.sum(W2**2) + np.sum(W3**2))
    loss = data_loss + reg_loss
    #print(loss)


    # Backpropagation
    dx3, dW3, db3 = affine_backward(dscores, cache_scores)
    dW3 += self.reg * W3 # Adding effect of regularization

    dx2, dW2, db2 = affine_relu_backward(dx3, cache_hidden_layer)
    dW2 += self.reg * W2

    dx2 = dx2.reshape(N, F, Hp, Wp)
    dx1, dW1, db1 = conv_relu_pool_backward(dx2, cache_conv_x)

    dW1 += self.reg * W1


    grads.update({'W1': dW1, 'W2': dW2, 'W3': dW3, 'b1': db1, 'b2': db2, 'b3': db3})


    ############################################################################
    #                             END OF YOUR CODE                             #
    ############################################################################

    return loss, grads


pass
