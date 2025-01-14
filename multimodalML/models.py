import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(x, self.w)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        score = nn.as_scalar(self.run(x))
        if score < 0:
            return -1
        return 1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        updated = True
        # converge when no values are updated
        while updated:
            updated = False
            for x, y in dataset.iterate_once(1):
                # we get the prediction from the dataset
                prediction = self.get_prediction(x)
                # if prediction is wrong, we update x
                if prediction != nn.as_scalar(y):
                    # w + (y*) * x -- scalar value of y times x.
                    nn.Parameter.update(self.w, x, nn.as_scalar(y))
                    updated = True

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 200
        self.learning_rate = -0.05
        self.l1Weight = nn.Parameter(1,512)
        self.l2Weight = nn.Parameter(512,1)
        self.l1Bias = nn.Parameter(1,512)
        self.l2Bias = nn.Parameter(1,1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        l1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.l1Weight), self.l1Bias))   
        l2 = nn.AddBias(nn.Linear(l1, self.l2Weight), self.l2Bias)
        return l2

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        loss = float('inf')
        while loss >= 0.02:
            for x, y in dataset.iterate_once(self.batch_size):
                lossNode = self.get_loss(x,y)
                loss = nn.as_scalar(lossNode)
                if loss >= 0.02:
                    grad_wrt_w1, grad_wrt_b1, grad_wrt_w2, grad_wrt_b2 = nn.gradients(lossNode, [self.l1Weight, self.l1Bias, self.l2Weight, self.l2Bias])
                    self.l1Weight.update(grad_wrt_w1, self.learning_rate)
                    self.l1Bias.update(grad_wrt_b1, self.learning_rate)
                    self.l2Weight.update(grad_wrt_w2, self.learning_rate)
                    self.l2Bias.update(grad_wrt_b2, self.learning_rate)

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 100
        self.learning_rate = -0.5
        self.l1Weight = nn.Parameter(784,200)
        self.l2Weight = nn.Parameter(200,10)
        self.l1Bias = nn.Parameter(1,200)
        self.l2Bias = nn.Parameter(1,10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        l1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.l1Weight), self.l1Bias))   
        l2 = nn.AddBias(nn.Linear(l1, self.l2Weight), self.l2Bias)
        return l2

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        validationAccuracy = 0
        while validationAccuracy < 0.98:
            for x, y in dataset.iterate_once(self.batch_size):
                lossNode = self.get_loss(x,y)
                grad_wrt_w1, grad_wrt_b1, grad_wrt_w2, grad_wrt_b2 = nn.gradients(lossNode, [self.l1Weight, self.l1Bias, self.l2Weight, self.l2Bias])
                self.l1Weight.update(grad_wrt_w1, self.learning_rate)
                self.l1Bias.update(grad_wrt_b1, self.learning_rate)
                self.l2Weight.update(grad_wrt_w2, self.learning_rate)
                self.l2Bias.update(grad_wrt_b2, self.learning_rate)
            validationAccuracy = dataset.get_validation_accuracy()

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 100
        self.learning_rate = -0.5
        # weights need to be size of num_chars
        self.l1Weight = nn.Parameter(self.num_chars, 300)
        self.l1Bias = nn.Parameter(1,300)
        self.l2Weight = nn.Parameter(self.num_chars, 300)
        self.l2Bias = nn.Parameter(1,300)
        self.hWeight = nn.Parameter(300, 300)
        # output needs to be the size of languages
        self.l3Weight = nn.Parameter(300,len(self.languages))
        self.l3Bias = nn.Parameter(1,len(self.languages))



    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        # for first layer dont need to switch Linear with Add(Linear)
        vector = nn.ReLU(nn.AddBias(nn.Linear(xs[0], self.l1Weight), self.l1Bias)) 
        for i in range(1, len(xs)):
            vector = nn.ReLU(nn.AddBias(nn.Add(nn.Linear(xs[i], self.l2Weight), nn.Linear(vector, self.hWeight)), self.l2Bias))
        return nn.AddBias(nn.Linear(vector, self.l3Weight), self.l3Bias)

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        validationAccuracy = 0
        while validationAccuracy < 0.84:
            for x, y in dataset.iterate_once(self.batch_size):
                lossNode = self.get_loss(x,y)
                grad_wrt_w1, grad_wrt_b1, grad_wrt_w2, grad_wrt_b2, grad_wrt_w3, grad_wrt_b3 = nn.gradients(lossNode, [self.l1Weight, self.l1Bias, self.l2Weight, self.l2Bias, self.l3Weight, self.l3Bias])
                self.l1Weight.update(grad_wrt_w1, self.learning_rate)
                self.l1Bias.update(grad_wrt_b1, self.learning_rate)
                self.l2Weight.update(grad_wrt_w2, self.learning_rate)
                self.l2Bias.update(grad_wrt_b2, self.learning_rate)
                self.l3Weight.update(grad_wrt_w3, self.learning_rate)
                self.l3Bias.update(grad_wrt_b3, self.learning_rate)
            validationAccuracy = dataset.get_validation_accuracy()

