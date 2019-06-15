from collections import defaultdict, Counter

userHistory = defaultdict(list)


def log_answer(userId, selectedTrueFact):
        userHistory[userId].append(selectedTrueFact)


def get_true_ratio_for_user(userID):
        history = userHistory[userID]
        trueCount = Counter(history)[True]
        return divide(trueCount, len(history))


def divide(a, b):
        if b == 0:
                return 0
        else:
                return a/b