import torch

## Option 1

dist = torch.cdist(x, y, p=2)

## Option 2

n = x.size(0)
m = y.size(0)
d = x.size(1)

x = x.unsqueeze(1).expand(n, m, d)
y = y.unsqueeze(0).expand(n, m, d)
Then calculate dist[i,j] = ||x[i,:]-y[j,:]||^2 in the following way:

dist = torch.pow(x - y, 2).sum(2) 
