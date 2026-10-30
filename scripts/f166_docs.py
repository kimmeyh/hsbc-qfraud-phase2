"""Render F166's eight documents from its result file (Sprint 29 IMP-2).

    <venv python> scripts/f166_docs.py            write docs/phase2/algorithms/
    <venv python> scripts/f166_docs.py --check    exit 1 if a page differs
    <venv python> scripts/f166_docs.py --out DIR  write to DIR instead

The pages were first written by a script kept in the session scratchpad,
so they could not be regenerated or reviewed, and the PR 63 review found
a claim in its fixed text that the result does not support ("the chosen
configuration changes between seeds" on the proxy page, where `full` was
chosen on every seed). Here every such statement is computed from the
result, or checked against it: a statement whose condition the result
does not meet raises `ClaimError`, and no page is written.
`experiments/src/test_f166_docs.py` fails when a committed page differs
from what this renders.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "phase2" / "results" / "f166_ulb_algorithms.json"
DOCS = ROOT / "docs" / "phase2" / "algorithms"
FILE = "`experiments/phase2/results/f166_ulb_algorithms.json`"
sys.path.insert(0, str(ROOT / "experiments" / "src"))   # qubo_proxy

NAMES = {"hgb": "HGB", "lightgbm": "LightGBM", "xgboost": "XGBoost",
         "catboost": "CatBoost", "logreg": "Logistic regression",
         "svm": "SVM", "proxy": "CVQBoost proxy"}
# The name inside a sentence, and its possessive there.
INNER = {**NAMES, "logreg": "logistic regression", "proxy": "the proxy"}
POSSESSIVE = {"logreg": "logistic regression's", "svm": "the SVM's",
              "proxy": "the proxy's"}
FILES = {"hgb": "ULB_HGB.md", "lightgbm": "ULB_LIGHTGBM.md",
         "xgboost": "ULB_XGBOOST.md", "catboost": "ULB_CATBOOST.md",
         "logreg": "ULB_LOGISTIC_REGRESSION.md", "svm": "ULB_SVM.md",
         "proxy": "ULB_CVQBOOST_PROXY.md"}
COMPARISON = "ULB_COMPARISON.md"
BOOSTING = {"catboost", "lightgbm", "xgboost", "hgb"}
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
SETUP = {
    "hgb": "`HistGradientBoostingClassifier`, `random_state=seed`, all 30 columns",
    "lightgbm": "`LGBMClassifier`, 300 trees, `random_state=seed`, all 30 columns",
    "xgboost": "`XGBClassifier`, `random_state=seed`, all 30 columns; the library default (depth 6, rate 0.3, 100 trees) is one of the grid",
    "catboost": "`CatBoostClassifier`, 500 iterations, `random_seed=seed`, all 30 columns",
    "logreg": "`LogisticRegression`, `max_iter=2000`, all 30 columns standardized on the training fold",
    "svm": "`LinearSVC` on all training rows, scores from `decision_function`, all 30 columns standardized on the training fold",
    "proxy": "the three frozen `qubo_proxy` configurations, full-pair pool, dct learners seeded by `qubo_proxy.seeded_weak_params(seed)`, lambda 2 x n_train; each configuration uses its own top-k features",
}
ROWS = [("AUPRC", "auprc"), ("AUPRC, floor-normalized", "auprc_floor_normalized"),
        ("ROC-AUC", "auc_roc"), ("Recall at the 0.5% budget, test fold", "recall_at_budget_on_test"),
        ("Train-test AUPRC gap", "train_test_auprc_gap")]
OPS = [("max_f1_on_val", "max-F1 threshold chosen on validation"),
       ("alert_budget_0.005", "0.5% alert-budget threshold chosen on validation")]
OP_METRICS = ["precision", "recall", "specificity", "f1", "mcc", "balanced_accuracy"]
OP_LABEL = {"precision": "Precision", "recall": "Recall", "specificity": "Specificity",
            "f1": "F1", "mcc": "MCC", "balanced_accuracy": "Balanced accuracy"}
NO_DIFF = "no reliable difference"
N_PAIRS_TESTED = 6          # the entry's Bonferroni divisor, 0.05 / 6


class ClaimError(Exception):
    """A statement in the fixed text that the result does not support."""


def f4(v):
    return f"{v:.4f}"


def stat_row(label, s):
    lo, hi = s["t95"]
    return f"| {label} | {f4(s['mean'])} | {f4(s['sd'])} | {f4(lo)} to {f4(hi)} |"


def params(p):
    return ", ".join(f"{k} {v}" for k, v in sorted(p.items()))


def pair_text(p):
    w = p["wilcoxon"]["p"]
    return (f"{NAMES[p['a']]} against {NAMES[p['b']]}: mean difference "
            f"{f4(p['mean_diff'])}, Wilcoxon p {w:.4f}; reading: {p['reading']}")


def chosen_counts(rows, a):
    return collections.Counter(json.dumps(r["lanes"][a]["chosen_params"],
                                          sort_keys=True) for r in rows)


def one_choice(rows, a):
    """The configuration every seed chose, or None."""
    counts = chosen_counts(rows, a)
    return json.loads(next(iter(counts))) if len(counts) == 1 else None


def limits_line(rows, a):
    first = ("- Each validation fold holds about 95 frauds, so validation "
             "AUPRC is noisy")
    only = one_choice(rows, a)
    if only is None:
        return first + " and the chosen configuration changes between seeds."
    shown = (f"`{only['config']}`" if list(only) == ["config"]
             else params(only))
    return first + (f". Here the same configuration ({shown}) was chosen on "
                    "every seed.")


def proxy_paragraph(res, rows, n):
    import qubo_proxy as qp
    only = one_choice(rows, "proxy")
    if only is None:
        raise ClaimError("the proxy page states one configuration chosen on "
                         "every seed; the result's seeds chose more than one")
    name = only["config"]
    builds = {r["lanes"]["proxy"]["build"] for r in rows}
    par = res["proxy_build"]
    want = f"parallel, {par['workers']} workers"
    if not par["use"] or builds != {want}:
        raise ClaimError(f"the proxy page states the chosen pool was built "
                         f"with F159's parallel build; the rows record {builds}")
    cfg = qp.CONFIGS[name]
    others = [t["params"]["config"] for t in rows[0]["lanes"]["proxy"]["tried"]
              if t["params"]["config"] != name]
    return (f"The {name} configuration (k {cfg['k']}, order "
            f"{cfg['schedule']}) was chosen on every seed. Its pool was built "
            f"with F159's parallel build ({par['workers']} workers), which "
            "F159 showed gives the same pool as the serial build; "
            f"{' and '.join(others)} were built serially, so the fit seconds "
            f"of the {WORDS[len(others) + 1]} configurations are not "
            "comparable.")


def balanced_line(rows, a, n):
    k = sum(r["lanes"][a]["chosen_params"].get("class_weight") == "balanced"
            for r in rows)
    if k == 0:
        return "No seed chose `class_weight` balanced."
    return f"{k} of {n} seeds chose `class_weight` balanced."


def algo_doc(res, a):
    A, R = res["analysis"], res["rows"]
    N = A["n_seeds"]
    seeds = f"{R[0]['seed']}-{R[-1]['seed']}"
    s = A["per_algorithm"][a]
    lanes = [r["lanes"][a] for r in R]
    order = A["order_by_mean_test_auprc"]
    rank = order.index(a) + 1
    L = [f"# {NAMES[a]} on ULB: best achievable result (F166)", ""]
    L += [f"**BLUF.** Tuned on validation and scored on the test fold over "
          f"{N} seeds ({seeds}), {NAMES[a]} reaches a mean test AUPRC of "
          f"{f4(s['auprc']['mean'])} (95% t interval {f4(s['auprc']['t95'][0])} "
          f"to {f4(s['auprc']['t95'][1])}). It is number {rank} of "
          f"{len(order)} by mean test AUPRC; the ranking and which "
          "differences are reliable are on "
          f"[{COMPARISON}]({COMPARISON}).", ""]
    L += ["- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.",
          "- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "
          "\"F166\", written before any score.",
          f"- **Evidence**: {FILE} (evidence tag SIM, zero metered seconds), "
          "generator `experiments/phase2/src/f166_ulb_algorithms.py`. Every "
          "figure below comes from that file. Each seed's outcome block is "
          "in the file's rows; the per-row test scores it names are in "
          "`experiments/phase2/predictions/` (gitignored, kept on this "
          "machine), each recorded with its SHA-256.",
          "- **Data**: ULB with duplicates dropped, `data.stratified_split` "
          "(60/20/20). Tuning reads the training and validation folds; every "
          "score here is on the test fold.",
          f"- **Setup**: {SETUP[a]}.", ""]
    L += ["## Configurations tried", ""]
    tried = lanes[0]["tried"]
    L += [f"{len(tried)} configurations, named in the entry before any score. "
          "Per seed, the one with the highest validation AUPRC was kept "
          "(ties: the first listed).", ""]
    counts = chosen_counts(R, a)
    L += ["| Configuration | Seeds that chose it |", "|---|---|"]
    for t in tried:
        k = json.dumps(t["params"], sort_keys=True)
        L.append(f"| {params(t['params'])} | {counts.get(k, 0)} of {N} |")
    L.append("")
    if a == "proxy":
        L += [proxy_paragraph(res, R, N), ""]
    if a in ("logreg", "svm"):
        L += [balanced_line(R, a, N), ""]
    if a == "svm":
        won = A["svm_form"]["rbf_beats_linear_seeds"]
        kept = A["svm_form"]["kept"]
        cs = " and ".join(f"{c:g}" for c in sorted(
            g["C"] for g in res["svm_rbf_grid"]))
        L += ["## Alternative tried: an RBF kernel", "",
              f"An RBF SVM (`SVC`, `gamma=\"scale\"`, C {cs}) on a "
              f"stratified {res['rbf_rows']:,}-row subsample of the training "
              "fold, because an RBF kernel on the full fold is quadratic in "
              f"rows. The entry keeps it only if its best validation AUPRC "
              f"beats the linear form's on a majority of seeds. It did so on "
              f"{won} of {N} seeds, so the lane keeps the "
              f"**{kept}** form. Every figure in this "
              f"document is the {kept} form.", ""]
    L += ["## Test-fold results over seeds", "",
          f"Mean, SD and 95% t interval over {N} seeds, each seed at its "
          "own chosen configuration.", "",
          "| Metric | Mean | SD | 95% t interval |", "|---|---|---|---|"]
    L += [stat_row(lab, s[k]) for lab, k in ROWS]
    L.append("")
    for op, desc in OPS:
        L += [f"At the {desc}:", "",
              "| Metric | Mean | SD | 95% t interval |", "|---|---|---|---|"]
        L += [stat_row(OP_LABEL[m], s[op][m]) for m in OP_METRICS]
        L.append("")
    L += ["## Confusion counts per seed, test fold", "",
          "TP, FP, TN and FN at each validation-chosen threshold.", "",
          "| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |",
          "|---|---|---|---|"]
    for l in lanes:
        ops = {o["operating_point"]: o["confusion"] for o in l["test"]["operating_points"]}
        cells = [" / ".join(str(ops[op][k]) for k in ("tp", "fp", "tn", "fn"))
                 for op, _ in OPS]
        L.append(f"| {l['seed']} | {params(l['chosen_params'])} | {cells[0]} | {cells[1]} |")
    L.append("")
    L += ["## Limits", "",
          limits_line(R, a),
          "- One protocol and one grid per algorithm. A larger grid may do "
          "better; this is the best of the configurations named in the "
          "entry, not the best possible.",
          "- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside "
          "this part of F157.", ""]
    return "\n".join(L) + "\n"


def unestablished(order, pairs):
    """The runs of adjacent algorithms with no reliable difference between
    neighbors, each of two or more names."""
    runs, cur = [], [order[0]]
    for p in pairs:
        if p["reading"] == NO_DIFF:
            cur.append(p["b"])
        else:
            if len(cur) > 1:
                runs.append(cur)
            cur = [p["b"]]
    if len(cur) > 1:
        runs.append(cur)
    return runs


def bluf_order(order):
    """The comparison's BLUF states boosting first, then the proxy, then the
    SVM and logistic regression; check that before writing it."""
    if not (set(order[:len(BOOSTING)]) == BOOSTING
            and order[len(BOOSTING):] == ["proxy", "svm", "logreg"]):
        raise ClaimError(f"the comparison's BLUF states the boosting "
                         f"libraries, then the proxy, the SVM and logistic "
                         f"regression; the result's order is {order}")
    return (f"the {WORDS[len(BOOSTING)]} gradient-boosting libraries lead "
            "by mean test AUPRC, the CVQBoost proxy is next, then the linear "
            "SVM and logistic regression")


def names(run):
    return ", ".join(INNER[a] for a in run[:-1]) + f" and {INNER[run[-1]]}"


def comparison(res):
    A, R = res["analysis"], res["rows"]
    N = A["n_seeds"]
    seeds = f"{R[0]['seed']}-{R[-1]['seed']}"
    order = A["order_by_mean_test_auprc"]
    pairs = A["adjacent_pairs"]
    if [(p["a"], p["b"]) for p in pairs] != list(zip(order, order[1:])):
        raise ClaimError("the adjacent pairs are not the result's order")
    reliable = [p for p in pairs if p["reading"] != NO_DIFF]
    runs = unestablished(order, pairs)
    count = WORDS[len(order)]
    L = [f"# ULB: {count} algorithms compared (F166)", ""]
    L += [f"**BLUF.** Over {N} seeds ({seeds}), {bluf_order(order)}. Of the "
          f"{WORDS[len(pairs)]} adjacent pairs, {len(reliable)} differ "
          "reliably under the entry's test: "
          + "; ".join(f"{NAMES[p['a']]} above {INNER[p['b']]}" for p in reliable)
          + ". No other adjacent pair differs reliably, so the order among "
          + "; ".join(names(r) for r in runs) + " is not established.", ""]
    L += ["- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.",
          "- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "
          "\"F166\", written before any score.",
          f"- **Evidence**: {FILE} (evidence tag SIM, zero metered seconds). "
          "Every figure below comes from that file.",
          f"- **Seeds**: seed 42 took {R[0]['minutes']} minutes for all {count} "
          f"algorithms, so the entry's rule gave {N} seeds.", ""]
    L += ["## Mean test AUPRC, in order", "",
          "| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | Document |",
          "|---|---|---|---|---|---|"]
    for i, a in enumerate(order, 1):
        s = A["per_algorithm"][a]
        lo, hi = s["auprc"]["t95"]
        L.append(f"| {i} | {NAMES[a]} | {f4(s['auprc']['mean'])} | {f4(lo)} to "
                 f"{f4(hi)} | {f4(s['recall_at_budget_on_test']['mean'])} | "
                 f"[{FILES[a]}]({FILES[a]}) |")
    L.append("")
    L += ["## Adjacent pairs", "",
          f"The entry's test: with {N} seeds (8 or more), the exact two-sided "
          "Wilcoxon signed-rank test on per-seed AUPRC differences is "
          f"primary, at Bonferroni 0.05 / {N_PAIRS_TESTED}. \"A above B\" is "
          "written only when it rejects. Only adjacent pairs are tested, so a "
          f"non-adjacent statement (for example {NAMES[order[0]]} against "
          f"{INNER[order[len(BOOSTING)]]}) is not made here.", ""]
    L += [f"- {pair_text(p)}" for p in pairs]
    L.append("")
    per = A["per_algorithm"]
    gap = sorted(order, key=lambda a: per[a]["train_test_auprc_gap"]["mean"])
    top, low = gap[-1], gap[:2]
    poss = {a: POSSESSIVE.get(a, f"{NAMES[a]}'s") for a in order}
    unsure = [p for p in pairs if p["reading"] == NO_DIFF]
    near = min(unsure, key=lambda p: p["wilcoxon"]["p"])
    if near["wilcoxon"]["p"] <= 0.05 / N_PAIRS_TESTED:
        raise ClaimError("a pair read 'no reliable difference' has a p below "
                         "the Bonferroni level")
    rec = [per[a]["recall_at_budget_on_test"]["mean"] for a in order]
    auprc = [per[a]["auprc"]["mean"] for a in order]
    spread = ("narrower" if max(rec) - min(rec) < max(auprc) - min(auprc)
              else "wider")
    L += ["## Notes", "",
          f"- {poss[top][0].upper() + poss[top][1:]} train-test AUPRC gap has "
          f"the largest mean ({f4(per[top]['train_test_auprc_gap']['mean'])}); "
          f"{poss[low[0]]} and {poss[low[1]]} are the smallest "
          f"({f4(per[low[0]]['train_test_auprc_gap']['mean'])} and "
          f"{f4(per[low[1]]['train_test_auprc_gap']['mean'])}).",
          f"- {NAMES[near['a']]} against {INNER[near['b']]} has the smallest "
          f"p among the pairs read \"{NO_DIFF}\", but it is above the "
          f"Bonferroni level of 0.05 / {N_PAIRS_TESTED}, so the entry does "
          "not write \"above\".",
          "- At the 0.5% alert budget, mean recall on the test fold lies "
          f"between {f4(min(rec))} and {f4(max(rec))} for all {count}, a "
          f"{spread} spread than AUPRC's.",
          f"- The SVM lane keeps its {A['svm_form']['kept']} form; the RBF "
          f"alternative beat it on validation on "
          f"{A['svm_form']['rbf_beats_linear_seeds']} of {N} seeds "
          f"([{FILES['svm']}]({FILES['svm']})).", ""]
    return "\n".join(L)


def check_fixed_text(res: dict) -> None:
    """The fixed text states the evidence tag SIM, zero metered seconds,
    the linear SVM (`SETUP`), the Wilcoxon test as primary with 8 or more
    seeds, and a Bonferroni divisor of 6; refuse a result that differs."""
    A = res["analysis"]
    pairs = A["adjacent_pairs"]
    wrong = []
    if res.get("evidence_tag") != "SIM":
        wrong.append(f"evidence tag {res.get('evidence_tag')!r}, not SIM")
    if res.get("metered_seconds") != 0:
        wrong.append(f"metered seconds {res.get('metered_seconds')!r}, not 0")
    if A["svm_form"]["kept"] != "linear":
        wrong.append(f"SVM form {A['svm_form']['kept']!r}, not linear")
    if A["n_seeds"] < 8 or any(p["primary"] != "wilcoxon" for p in pairs):
        wrong.append("a primary test that is not Wilcoxon, or fewer than "
                     "8 seeds")
    if len(pairs) != N_PAIRS_TESTED:
        wrong.append(f"{len(pairs)} adjacent pairs, not {N_PAIRS_TESTED}")
    if wrong:
        raise ClaimError("the fixed text does not hold: " + "; ".join(wrong))


def render(res: dict) -> dict[str, str]:
    """Every page's text, keyed by file name. Raises ClaimError before
    returning anything if a statement does not hold."""
    check_fixed_text(res)
    pages = {name: algo_doc(res, a) for a, name in FILES.items()}
    pages[COMPARISON] = comparison(res)
    return pages


def differing(pages: dict[str, str], folder: Path) -> list[str]:
    def read(p):
        return p.read_text(encoding="utf-8").replace("\r\n", "\n") \
            if p.exists() else None
    return sorted(n for n, text in pages.items() if read(folder / n) != text)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--result", type=Path, default=RESULT)
    ap.add_argument("--out", type=Path, default=DOCS)
    ap.add_argument("--check", action="store_true",
                    help="compare with the pages in --out; write nothing")
    args = ap.parse_args(argv)
    pages = render(json.loads(args.result.read_text(encoding="utf-8")))
    if args.check:
        bad = differing(pages, args.out)
        for n in bad:
            print(f"DIFFERS: {args.out / n}", file=sys.stderr)
        return 1 if bad else 0
    args.out.mkdir(parents=True, exist_ok=True)
    for n, text in pages.items():
        (args.out / n).write_text(text, encoding="utf-8", newline="\n")
    print(f"written {len(pages)} to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
