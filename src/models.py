import torch
import torch.nn as nn
import torch.nn.functional as F


class GeneratorNetwork(nn.Module):
    """the same model as the one given in original [N.Umetani et al., 2017] article
    """
    def __init__(self):
        super(GeneratorNetwork, self).__init__()
        self.linear1 = nn.Linear(6165, 1000)
        self.linear2 = nn.Linear(1000, 10)
        self.linear3 = nn.Linear(10, 1000)
        self.linear4 = nn.Linear(1000, 6165)

    def forward(self, x):
       y = F.sigmoid(self.linear1(x))
       y = F.sigmoid(self.linear2(y))
       y = F.sigmoid(self.linear3(y))
       y = F.sigmoid(self.linear4(y))
       return y