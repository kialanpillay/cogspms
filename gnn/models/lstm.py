import torch
import torch.nn as nn


class LSTM(nn.Module):
    """
    A baseline 100-layer LSTM model with a single output layer for univariate predictions
    """

    def __init__(self, input_size=1, hidden_layers=100, output_size=1):
        """
        Parameters
        ----------
        input_size : int, optional
            Input layer dimension
        hidden_layers : int, optional
            Number of hidden layers
        output_size : int, optional
            Output layer dimension
        """
        super().__init__()
        self.hidden_layers = hidden_layers

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_layers)

        self.linear = nn.Linear(hidden_layers, output_size)

        self.hidden_cell = (torch.zeros(1, 1, self.hidden_layers),
                            torch.zeros(1, 1, self.hidden_layers))

    def forward(self, in_seq):
        lstm_out, self.hidden_cell = self.lstm(in_seq.view(len(in_seq), 1, -1), self.hidden_cell)
        forecast = self.linear(lstm_out.view(len(in_seq), -1))
        return forecast
