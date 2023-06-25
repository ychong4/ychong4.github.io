## Optimizers  

### Gradient Descent, Stochastic Gradient Descent (SGD), Mini-batch GD
- Gradient Descent is an iterative algorithm use in loss function to find the global minima.
- The loss can be any differential loss function, such as linear loss, logistic loss, hinge loss, etc. 
- The equation is: w_new = w_old - learning_rate*(summation dl/dw), b_new = b_old - learning_rate*(summation dl/db)
- Gradient Descent uses the whole training data to update weight and bias. Suppose if we have millions of records then training becomes slow and computationally expensive.
- SGD solved the Gradient Descent problem by using only single records to update parameters, but SGD is slow to converge because it needs forward and backward propagation for every record. Also, the path to reach global minima becomes very noisy.
- Mini-batch GD overcomes the SGD drawbacks by using a batch of records to update the parameter. The path to global minima is not as smooth and Gradient Descent, but is not as noisy as Stochastic Gradient Descent.

![](https://github.com/ychong4/ychong4.github.io/blob/master/Activity%202/DeepLearning/Gradient%20descent.webp)


### SGD with momentum
- SGD with momentum applies Exponentially Weighted Averages to compute Gradient and used this Gradient to update parameter.
- In SGD with momentum, we have added momentum in a gradient function. This accelerates SGD to converge faster and reduce the oscillation.
- The learning rate is constant.
- It always works better than the normal Stochastic Gradient Descent Algorithm.

![](https://github.com/ychong4/ychong4.github.io/blob/master/Activity%202/DeepLearning/sgd_momentum.webp)

### Adagrad (Adaptive Gradient Algorithm)
- Adagrad uses different learning rates for each parameter base on iteration.
- The learning rate for sparse features parameters needs to be higher compare to the dense features parameter because the frequency of occurence of sparse features is lower.
- In Adagrad optimizer equation, the learning rate has been modified in such a way that it will automatically decrease because the summation of the previous gradient square will always keep on increasing after every time step.
- Disadvantage: Due to constantly decreasing learning rates, at some point in time step, the model will stop learning as the learning rate is almost close to 0.

### Adadelta
- Adadelta is an extension of Adagrad that attempts to solve its radically diminishing learning rates.
- Instead of summing up all the past squared gradients from 1 to "t" time steps, we restrict the window size.
- For example, computing the squared gradient of the past 10 gradients and average out. This can be achieved using Exponentially Weighted Averages over Gradient.

### Adam 
- Adam optimizer is by far the most preferred optimizers.
- The idea behind Adam optimizer is to utilize the momentum concept from "SGD with momentum" and adaptive learning rate from "Ada delta".
- Advantage: Straightforward to implement, computationally efficient, little memory requirmeents, appropritate for problems with very noisy/or sparse gradients, hyper-parameters have intuitive interpretation and typically require a little tuning.

