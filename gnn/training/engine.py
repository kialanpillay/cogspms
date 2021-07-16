import torch


class Engine:
    def __init__(self, model, loss, optim, clip, step_size, horizon, scaler, device, cl=True):
        self.scaler = scaler
        self.model = model.to(device)
        self.optim = optim
        self.loss = loss
        self.clip = clip
        self.step = step_size
        self.iter = 1
        self.task_level = 1
        self.seq_out_len = horizon
        self.cl = cl

    def train(self, model_input, target, idx=None):
        self.optim.zero_grad()
        forecast = self.model(model_input, idx=idx).transpose(1,3)
        target = torch.unsqueeze(target, dim=1)
        if self.iter % self.step == 0 and self.task_level <= self.seq_out_len:
            self.task_level += 1
        if self.cl:
            loss = self.loss(forecast[:, :, :, :self.task_level], target[:, :, :, :self.task_level])
        else:
            loss = self.loss(forecast, target)
        loss.backward()

        if self.clip is not None:
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.clip)

        self.optim.step()
        self.iter += 1
        return loss.item()
