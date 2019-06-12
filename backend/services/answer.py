from collections import defaultdict

userHistory = defaultdict(list)

def log_answer(userId, selectedTrueFact):
        userHistory[userId].append(selectedTrueFact)