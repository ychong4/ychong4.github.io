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
- It always works better than the normal Stochastic Gradient Descent Algorithm.

- ![](https://github.com/ychong4/ychong4.github.io/blob/master/Activity%202/DeepLearning/sgd_nomomentum.webp)
- ![](https://github.com/ychong4/ychong4.github.io/blob/master/Activity%202/DeepLearning/sgd_momentum.webp)
