[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Wuud-5WI)
# Topics in CS - Project 5: AI (Final Project for Fall Semester)

Welcome to your final project for the AI unit! This assignment serves as your final exam and challenges you to design, train, evaluate, and present an AI system of your choice.

You will use skills from computer vision, audio processing, natural language processing, or reinforcement learning to build a complete, end-to-end AI project.

---

## Project Requirements

### 1. Custom Dataset (Required)
You must create **your own dataset**. Examples include:
- Images you photograph (faces, gestures, objects, ASL letters, etc.)
- Audio recordings (spoken commands, noises, instruments)
- Text you write or collect manually
- Gameplay or simulation data (for RL)

Your dataset must include:
- At least **100 labeled samples**, OR  
- At least **30 minutes of gameplay/data** if working with reinforcement learning

You must include a short description of:
- How you collected your dataset  
- Potential sources of bias  
- How the dataset might impact model performance

Place your dataset inside a folder named `data/`.

---

### 2. Model Training (Required)
You must train **three separate models or three training configurations**.

Each training run must include:
- A clear description of the hyperparameters used  
- A graph showing performance  
  - ML examples: loss vs. epochs, accuracy vs. epochs, confusion matrix  
  - RL examples: reward per episode, cumulative reward, exploration vs. exploitation curve

Changes between runs may include:
- Learning rate  
- Batch size  
- Number of layers  
- Optimizer  
- Data augmentation  
- RL-specific: reward structure, discount factor (γ), exploration rate (ε), etc.

Save all graphs in a folder named `graphs/`.

---

### 3. Performance Graphs
Each of your three training runs must include at least one graph. Requirements:
- Labeled axes  
- Clearly readable  
- Shows trends over training  

For ML:
- Loss curves  
- Accuracy curves  
- Confusion matrices  

For RL:
- Episode reward  
- Moving average of reward  
- Exploration vs. exploitation indicators  

---

### 4. Reflection & Analysis
At the end of this README, include a reflection section with:
- Which training run performed best and why  
- What hyperparameters mattered most  
- What surprised you  
- How your dataset quality affected results  
- What you would do differently with more time  

---

## Deliverables

Your repository must include:

project_root/
 - data/ -  store your data sets here
 - src/ -  store all code here
 - graphs/ - store all output graphs here
 - models/ -  export your model into this folder
```python
#Code to save/ load a Tensorflow Model

#Save
model.save("name.keras")

#Load
model = keras.models.load_model("model.keras")
```

 - README.md - this file

## Suggested Project Areas

### Computer Vision
- Facial expression classifier  
- Hand gesture detector  
- Object recognizer  
- Your own “mini-MNIST” with custom drawings  

### Audio
- Speech command classifier  
- Environmental sound classifier  
- Music note or instrument detector  

### NLP
- Sentiment classifier on text you write  
- Topic classifier  
- Custom prompt/response dataset  

### Reinforcement Learning
- Game-playing agent (CartPole, Pong, maze, etc.)  
- RL agent with custom reward and punishment rules  
- Exploration vs. exploitation tuning experiments  

---

## Timeline

### Week 1 — Proposal + Data Collection
- Choose project and get approval  
- Begin collecting dataset  
- Set up initial code structure  

### Week 2 — Model Development
- Build baseline model  
- First training run  
- Adjust preprocessing or pipeline  

### Week 3 — Complete Training Runs
- Perform all three training runs  
- Save graphs and results  
- Tune hyperparameters  

### Week 4 — Finalization
- Analyze results  
- Finish README  
- Prepare optional demo video  
- Submit final project  

---

## Evaluation Rubric (Summary)

| Category | Points |
|---------|--------|
| Dataset Quality & Documentation | 40 |
| Model Development & Code | 40 |
| Three Training Runs + Graphs | 60 |
| Final Reflection & Analysis | 40 |
| Organization & Clarity | 20 |
| **Total** | **200 points** |

---

## Final Submission Checklist

- [ ] Custom dataset created and documented  
- [ ] Three training runs completed  
- [ ] Graphs for each run  
- [ ] Code for training and inference included  
- [ ] Explanation of hyperparameter changes  
- [ ] Reflection section written  
- [ ] README clearly organized  

---

## Reflection - Complete this once you have finished!

**Best performing model/run and why:**  
*The best run was game number 145 with a score of 63. It has played the game enough time that it has explored the environment and learned that it gets a reward when "eating" an apple. It also had learned to avoid the walls and somewhat avoid itself.*  

**Most important hyperparameters and effects:**  
*The most important hyperparameters and effects are exploration rate and the reward/penalty shaping behavior. The exploration rate is important because it controls the trade-off between exploring new actiona and exploiting known good ones. The reward/penalty shaping behavior is important because it strengthens behaviors followed by positive reinforcements, while those followed by punishments are weakened. This helps guide the agent.*  

**Dataset limitations or biases:**  
*A limitation is that there is no time limit. This allows the agent to exploit instead of explore its environment. The agent can move in a circle, without getting any food and still not be punished.*  

**Unexpected results:**  
*I expected the snake to get better as time went on and it got better at the game. Instead, each good run was followed by a horrible one. The average score did slighty increase per game, but even after over 200 games the average score was only 16.*  

**What you would improve with more time:**  
*If I had more time I would add a time limit. This would force the snake to explore the environment more, making it better at the game.*  
