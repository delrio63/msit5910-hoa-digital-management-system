import matplotlib.pyplot as plt

# Performance metrics from your test
metrics = {
    "Login": 0.000002,
    "Document Upload": 0.001323,
    "Issue Creation": 0.000027,
    "Message Posting": 0.000009
}

operations = list(metrics.keys())
latencies = list(metrics.values())

plt.figure(figsize=(10, 6))
bars = plt.bar(operations, latencies, color=["#4C72B0", "#55A868", "#C44E52", "#8172B2"])

plt.title("Latency Comparison of Core HOA System Operations", fontsize=16)
plt.xlabel("Operation", fontsize=14)
plt.ylabel("Latency (seconds)", fontsize=14)

# Add value labels on top of each bar
for bar, value in zip(bars, latencies):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.6f}",
        ha="center",
        va="bottom",
        fontsize=12
    )

plt.tight_layout()
plt.show()
