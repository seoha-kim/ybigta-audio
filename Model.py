import torch.nn as nn
import torch.nn.functional as F


class STModel(nn.Module):
    def __init__(self):
        super(STModel, self).__init__()
        self.conv_layer = nn.Sequential(
            # Conv2d_0
            nn.Conv2d(1, 32, kernel_size=(3, 3), stride=(1, 1), padding=[0, 0]),
            nn.BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.ELU(alpha=1.0),
            nn.MaxPool2d(kernel_size=3, stride=3, padding=0, dilation=1, ceil_mode=False),
            nn.Dropout(p=0.1),

            # Conv2d_1
            nn.Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1), padding=[0, 0]),
            nn.BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.ELU(alpha=1.0),
            nn.MaxPool2d(kernel_size=4, stride=4, padding=0, dilation=1, ceil_mode=False),
            nn.Dropout(p=0.1),

            # Conv2d_2
            nn.Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=[0, 0]),
            nn.BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.ELU(alpha=1.0),
            nn.MaxPool2d(kernel_size=4, stride=4, padding=0, dilation=1, ceil_mode=False),
            nn.Dropout(p=0.1)
        )

        self.lstm_layer = nn.LSTM(128, 64, num_layers=2)

        self.fc_layer = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.Linear(in_features=64, out_features=10, bias=True)
        )


    def forward(self, x):
        out = self.conv_layer(x)
        out = self.lstm_layer(x)
        out = out.view(batch_size, -1)
        out = self.fc_layer(out)
        return out