import itertools, random, time

def bruteforce(items):
    def check(split, total):
        return abs(total - 2 * sum(split))
    
    n = len(items)
    total = sum(items)
    best_diff = float("inf")
    best_split = None
    for i in range(n // 2+1):
        for combo in itertools.combinations(range(n), i):
            combo_values = [items[i] for i in combo]

            
            diff = check(combo_values,total)
            if(diff==0):
                return combo_values, 0
            if best_diff > diff:
                best_diff = diff
                best_split = combo_values
        
    return best_split, best_diff

def greedy(items):
    items_sorted = sorted(items, reverse=True)
    
    set0, set1 = [], []
    sum0, sum1 = 0, 0

    for item in items_sorted:
        if sum0 <= sum1:
            set0.append(item)
            sum0 += item
        else:
            set1.append(item)
            sum1 += item
    diff = abs(sum0 - sum1)
    return set1, diff



def bf_run():
    f=open("thieves512bf.txt","a")
    for length in range(50):
        random.seed(512)
        lst = []
        for i in range(length): 
            lst.append(random.randint(1,100))
        print(lst)
        f.write(str(lst)+"\n")
        t1 = time.time()
        split,diff = bruteforce(lst)
        t2 = time.time()
        print(split)
        f.write(str(split)+"\n")
        print(f"bruteforce({length}): {t2-t1}, diff = {diff}\n")
        f.write(f"bruteforce({length}): {t2-t1}, diff = {diff}\n\n")
        if t2-t1 > 3600:
            break
    f.close()

def greedy_run():
    f=open("thieves512gr.txt","a")
    for length in range(36):
        random.seed(512)
        lst = []
        for i in range(length): 
            lst.append(random.randint(1,100))
        print(lst)
        f.write(str(lst)+"\n")
        t1 = time.time()
        split,diff = greedy(lst)
        t2 = time.time()
        print(split)
        f.write(str(split)+"\n")
        print(f"greedy({length}): {t2-t1}, diff = {diff}\n")
        f.write(f"greedy({length}): {t2-t1}, diff = {diff}\n\n")
        if t2-t1 > 3600:
            break
    f.close()


def dp_run():
    f=open("thieves512dp.txt","a")
    for length in range(36):
        random.seed(512)
        lst = []
        for i in range(length): 
            lst.append(random.randint(1,100))
        print(lst)
        f.write(str(lst)+"\n")
        t1 = time.time()
        split,diff = dp_partition(lst)
        t2 = time.time()
        print(split)
        f.write(str(split)+"\n")
        print(f"dp({length}): {t2-t1}, diff = {diff}\n")
        f.write(f"dp({length}): {t2-t1}, diff = {diff}\n\n")
        if t2-t1 > 3600:
            break
    f.close()

def dp_partition(items):
    total = sum(items)
    target = total // 2
    n = len(items)

    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True

    for i in range(1, n + 1):
        for s in range(target + 1):
            dp[i][s] = dp[i - 1][s]
            if s >= items[i - 1]:
                dp[i][s] = dp[i][s] or dp[i - 1][s - items[i - 1]]

    for s in range(target, -1, -1):
        if dp[n][s]:
            best_sum = s
            break

    split = []
    i, s = n, best_sum
    while i > 0 and s >= 0:
        if s >= items[i - 1] and dp[i - 1][s - items[i - 1]]:
            split.append(items[i - 1])
            s -= items[i - 1]
        i -= 1

    diff = abs(total - 2 * best_sum)
    return split, diff

if __name__ == "__main__":
    #bf_run()
    greedy_run()
    dp_run()