from collections import Counter


TRUTH = ["normal", "normal", "normal", "normal", "fraud", "fraud", "review", "review"]
PREDICTED = ["normal", "normal", "normal", "fraud", "normal", "fraud", "review", "normal"]
LABELS = ["normal", "fraud", "review"]


def safe_divide(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def per_class_scores(truth: list[str], predicted: list[str]) -> dict[str, dict[str, float]]:
    scores = {}
    for label in LABELS:
        tp = sum(actual == label and guess == label for actual, guess in zip(truth, predicted))
        fp = sum(actual != label and guess == label for actual, guess in zip(truth, predicted))
        fn = sum(actual == label and guess != label for actual, guess in zip(truth, predicted))
        precision = safe_divide(tp, tp + fp)
        recall = safe_divide(tp, tp + fn)
        f1 = safe_divide(2 * tp, 2 * tp + fp + fn)
        scores[label] = {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}
    return scores


scores = per_class_scores(TRUTH, PREDICTED)
support = Counter(TRUTH)
accuracy = sum(actual == guess for actual, guess in zip(TRUTH, PREDICTED)) / len(TRUTH)
macro_f1 = sum(item["f1"] for item in scores.values()) / len(LABELS)
weighted_f1 = sum(scores[label]["f1"] * support[label] for label in LABELS) / len(TRUTH)
total_tp = sum(item["tp"] for item in scores.values())
total_fp = sum(item["fp"] for item in scores.values())
total_fn = sum(item["fn"] for item in scores.values())
micro_f1 = safe_divide(2 * total_tp, 2 * total_tp + total_fp + total_fn)

print(f"accuracy:    {accuracy:.3f}")
print(f"micro F1:    {micro_f1:.3f}")
print(f"macro F1:    {macro_f1:.3f}")
print(f"weighted F1: {weighted_f1:.3f}")
for label, item in scores.items():
    print(f"{label:>6}: P={item['precision']:.3f} R={item['recall']:.3f} F1={item['f1']:.3f} support={support[label]}")

assert round(accuracy, 3) == 0.625
assert micro_f1 == accuracy  # True for this single-label multiclass task when every class is included.
assert round(macro_f1, 3) == 0.611
assert round(weighted_f1, 3) == 0.625
