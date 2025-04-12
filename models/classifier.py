import torch
import torch.nn as nn
import torch.nn.functional as F

class ClassifierRegressor(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes, regression=False):
        super(ClassifierRegressor, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.output = nn.Linear(hidden_size, 1 if regression else num_classes)
        self.regression = regression

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.output(x)
        return x if self.regression else F.log_softmax(x, dim=1)
