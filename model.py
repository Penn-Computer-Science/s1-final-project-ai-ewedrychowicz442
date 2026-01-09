import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module): #defines a class for the linear Q-network
    def __init__(self, input_size, hidden_size, output_size): #defines a function for initializing the linear Q-network
        super().__init__() #calls the parent class's init function
        self.linear1 = nn.Linear(input_size, hidden_size) #defines the first linear layer
        self.linear2 = nn.Linear(hidden_size, output_size) #defines the second linear layer

    def forward(self, x): #defines the forward function
        x = F.relu(self.linear1(x)) #applies the ReLU activation function to the output of the first linear layer
        x = self.linear2(x) #passes the output through the second linear layer
        return x
    
    def save(self, file_name = 'model.pth'): #defines a function for saving the model
        model_folder_path = './model' #sets the model folder path
        if not os.path.exists(model_folder_path): #checks if the model folder path exists
            os.makedirs(model_folder_path) #creates the model folder path if it does not exist

        file_name = os.path.join(model_folder_path, file_name) #joins the model folder path and file name
        torch.save(self.state_dict(), file_name) #saves the model state dictionary to the file name


class QTrainer: #defines a class for the Q-trainer
    def __init__(self, model, lr, gamma): #defines a function for initializing the Q-trainer
        self.lr = lr 
        self.gamma = gamma 
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr) #defines the optimizer
        self.criterion = nn.MSELoss() #defines the loss function

    def train_step(self, state, action, reward, next_state, done): #defines a function for training the model
        state = torch.tensor(state, dtype = torch.float) #converts the state to a tensor
        next_state = torch.tensor(next_state, dtype = torch.float) #converts the next state to a tensor
        action = torch.tensor(action, dtype = torch.long) #converts the action to a tensor
        reward = torch.tensor(reward, dtype = torch.float) #converts the reward to a tensor
        #(n, x)

        if len(state.shape) == 1: #if the state shape is 1
            #(1, x)
            state = torch.unsqueeze(state, 0) #unsqueezes the state tensor
            next_state = torch.unsqueeze(next_state, 0) #unsqueezes the next state tensor
            action = torch.unsqueeze(action, 0) #unsqueezes the action tensor
            reward = torch.unsqueeze(reward, 0) #unsqueezes the reward tensor
            done = (done, ) #makes done a tuple

        #1: predicted Q values with current state
        pred = self.model(state) #gets the predicted Q values from the model

        target = pred.clone() #clones the predicted Q values
        for idx in range(len(done)): #loops through the length of done
            Q_new = reward[idx] #sets Q_new to the reward at the current index
            if not done[idx]: #if the game is not done at the current index
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx])) #calculates the new Q value

            target[idx][torch.argmax(action).item()] = Q_new #updates the target Q value for the action taken

        #2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        #pred.clone()
        #preds(argmax(action)) = Q_new
        self.optimizer.zero_grad() #zeros the gradients
        loss = self.criterion(target, pred) #calculates the loss
        loss.backward() #calculates the gradients of the loss function with respect to all the model's parameters

        self.optimizer.step() #updates the model's parameters based on the computed gradients
        
