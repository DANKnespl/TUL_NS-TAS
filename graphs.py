import re
import matplotlib.pyplot as plt

def plotty(results, title, scale, max_time = True):
    n_values = [r["n"] for r in results]
    times = [r["time"] for r in results]
    diffs = [r["diff"] for r in results]

    n_zero = [n_values[i] for i,d in enumerate(diffs) if d==0]
    time_zero = [times[i] for i,d in enumerate(diffs) if d==0]

    n_nonzero = [n_values[i] for i,d in enumerate(diffs) if d>0]
    time_nonzero = [times[i] for i,d in enumerate(diffs) if d>0]


    

    plt.figure(figsize=(8,5))
    if max_time:
        plt.axhline(3600, color="black", linestyle="--", alpha=0.6)
    plt.plot(n_values, times, linestyle='-', color='black', alpha=0.5)

    plt.scatter(n_zero, time_zero, color='green', s=80, label='diff = 0')
    plt.scatter(n_nonzero, time_nonzero, color='red', s=80, label='diff > 0')

    plt.yscale(scale)
    plt.xlabel("N (počet rozdělovaných položek) [-]")
    plt.ylabel(f"Čas [s] (měřítko - {scale})")
    plt.title(title)
    plt.grid(False)
    plt.legend()
    plt.show()

def parse_file(filename,regex_pattern):
    results = []

    with open(filename, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        m = re.search(regex_pattern, line)
        if m:
            n = int(m.group(1))
            t = float(m.group(2))
            diff = int(m.group(3))
            
            results.append({
                "n": n,
                "time": t,
                "diff": diff
            })
        i += 1

    return results

def diff_of_diffs(bf_results, gr_results):
    bf_dict = {r["n"]: r for r in bf_results}
    gr_dict = {r["n"]: r for r in gr_results}

    combined = []

    for n in sorted(bf_dict.keys() & gr_dict.keys()):
        bf_diff = bf_dict[n]["diff"]
        gr_diff = gr_dict[n]["diff"]

        combined.append({
            "n": n,
            "quality_diff": gr_diff - bf_diff,
            "bf_diff": bf_diff,
            "gr_diff": gr_diff,
            "time_diff": gr_dict[n]["time"] - bf_dict[n]["time"],
            "bf_time": bf_dict[n]["time"],
            "gr_time": gr_dict[n]["time"]
        })

    return combined

def plot_diff_difference(data,title="Rozdíl kvality řešení heuristického algoritmu vůči optimálnímu řešení",xlabel="N (počet rozdělovaných položek) [-]",ylabel="diff(Heuristika) − diff(Hrubá síla) [-]"):
    n_values = [r["n"] for r in data]
    delta = [r["quality_diff"] for r in data]

    colors = ["green" if d == 0 else "red" for d in delta]

    plt.figure(figsize=(8,5))
    plt.axhline(0, color="black", linestyle="--", alpha=0.6)

    plt.scatter(n_values, delta, c=colors, s=80)
    plt.plot(n_values, delta, alpha=0.4)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

    import matplotlib.patches as mpatches
    plt.legend(handles=[
        mpatches.Patch(color="green", label="optimální heuristické řešení"),
        mpatches.Patch(color="red", label="neoptimální heuristické řešení")
    ])

    plt.show()

def plot_time_difference(data,title="Rozdíl výpočetního času heuristického algoritmu a metody hrubé síly",xlabel="N (počet rozdělovaných položek) [-]",ylabel="Čas(Heuristika) − Čas(Hrubá síla) [s]"):
    n_values = [r["n"] for r in data]
    delta = [r["time_diff"] for r in data]

    quality_delta = [r["quality_diff"] for r in data]
    colors = ["green" if d == 0 else "red" for d in quality_delta]

    plt.figure(figsize=(8,5))
    plt.axhline(0, color="black", linestyle="--", alpha=0.6)

    plt.scatter(n_values, delta, c=colors, s=80)
    plt.plot(n_values, delta, alpha=0.4)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

    import matplotlib.patches as mpatches
    plt.legend(handles=[
        mpatches.Patch(color="green", label="optimální heuristické řešení"),
        mpatches.Patch(color="red", label="neoptimální heuristické řešení")
    ])

    plt.show()


if __name__=="__main__":
    bf = parse_file("thieves512bf.txt",r"bruteforce\((\d*)\): (\d*\..*), diff = (\d*)")
    gr = parse_file("thieves512gr.txt",r"greedy\((\d*)\): (\d*\..*), diff = (\d*)")
    dp = parse_file("thieves512dp.txt",r"dp\((\d*)\): (\d*\..*), diff = (\d*)")
    plotty(bf, "Hrubá síla - Časová náročnost", "log")
    plotty(gr, "Hladový algoritmus - Časová náročnost", "linear")
    plotty(gr, "Hladový algoritmus - Časová náročnost", "linear",False)
    plotty(dp, "Dynamické programování - Časová náročnost", "linear",False)
    plot_diff_difference(diff_of_diffs(bf,gr),title="Rozdíl kvality řešení hladového algoritmu vůči optimálnímu řešení")
    plot_time_difference(diff_of_diffs(bf,gr),title="Rozdíl výpočetního času hladového algoritmu vůči optimálnímu řešení")
    plot_diff_difference(diff_of_diffs(bf,dp),title="Rozdíl kvality řešení dynamickým programováním vůči optimálnímu řešení")
    plot_time_difference(diff_of_diffs(dp,gr),title="Rozdíl výpočetního času dynamického programování vůči hladového algoritmu",ylabel="Čas(Hladový algoritmus) - Čas(DP) [s]")
