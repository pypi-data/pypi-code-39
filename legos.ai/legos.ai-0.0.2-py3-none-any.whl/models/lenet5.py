from torch import nn

class LeNet5(nn.Module):
    '''
    input: (1, 28, 28)
    conv1: (6, 28, 28) -> (6, 14, 14)
    conv2: (16, 10, 10) -> (16, 5, 5)
    fc1: (120, )
    fc2: (84, )
    fc3: (10, )
    '''
    def __init__(self):
        super(LeNet5, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 6, 5, stride=1, padding=2),
            nn.AvgPool2d(2, 2),
            nn.Tanh()
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(6, 16, 5),
            nn.AvgPool2d(2, 2),
            nn.Tanh()
        )
        self.fc1 = nn.Sequential(
            nn.Linear(5 * 5 * 16, 120),
            nn.Tanh()
        )
        self.fc2 = nn.Sequential(
            nn.Linear(120, 10),
            nn.Tanh()
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.fc2(x)
        return x