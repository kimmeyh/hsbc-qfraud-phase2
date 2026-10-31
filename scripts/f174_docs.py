"""Render F174's eight IEEE-CIS documents from its result file (F174
acceptance; the pattern of `scripts/f166_docs.py`, Sprint 29 IMP-2).

    <venv python> scripts/f174_docs.py            write docs/phase2/algorithms/
    <venv python> scripts/f174_docs.py --check    exit 1 if a page differs
    <venv python> scripts/f174_docs.py --out DIR  write to DIR instead

One page per algorithm and a comparison page, beside F166's ULB pages.
The helpers that do not name a dataset are F166's, imported. Every
statement in the fixed text is computed from the result or checked
against it; one the result does not support raises `ClaimError` and no
page is written. `experiments/src/test_f174_docs.py` tests the checks.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import f166_docs as fd  # noqa: E402  (F166's helpers; not edited)

RESULT = ROOT / "experiments" / "phase2" / "results" / "f174_ieee_algorithms.json"
DOCS = fd.DOCS
FILE = "`experiments/phase2/results/f174_ieee_algorithms.json`"
NAMES, INNER, POSSESSIVE, WORDS = fd.NAMES, fd.INNER, fd.POSSESSIVE, fd.WORDS
FILES = {a: n.replace("ULB_", "IEEE_") for a, n in fd.FILES.items()}
COMPARISON = "IEEE_COMPARISON.md"
ClaimError = fd.ClaimError
NO_DIFF = fd.NO_DIFF
N_PAIRS_TESTED = fd.N_PAIRS_TESTED
IMPUTED = {"logreg", "svm"}
SETUP = {
    "hgb": "`HistGradientBoostingClassifier`, `random_state=seed`, every column the fold keeps",
    "lightgbm": "`LGBMClassifier`, 300 trees, `random_state=seed`, every column the fold keeps",
    "xgboost": "`XGBClassifier`, `random_state=seed`, every column the fold keeps; the library default (depth 6, rate 0.3, 100 trees) is one of the grid",
    "catboost": "`CatBoostClassifier`, 500 iterations, `random_seed=seed`, every column the fold keeps",
    "logreg": "`LogisticRegression`, `max_iter=2000`, missing values imputed with the training months' medians, then standardized on them",
    "svm": "`LinearSVC` on all training rows, scores from `decision_function`, missing values imputed with the training months' medians, then standardized on them",
    "proxy": "the three frozen `qubo_proxy` configurations, full-pair pool built serially, dct learners seeded by `qubo_proxy.seeded_weak_params(seed)`; each configuration uses its own top-k features, ranked by mutual information on a 50,000-row subsample of the training months",
}


def fold_line(res) -> str:
    v, t = res["folds"]["validation"], res["folds"]["test"]
    return (f"- **Data**: IEEE-CIS with exact duplicates dropped "
            f"({res['folds']['exact_duplicates_removed']:,} rows), F105's month "
            f"folds and F152's item-4 controls. Tuning fits months "
            f"{months(v['train_months'])} and chooses on month {v['eval_month']} "
            f"({v['n_eval']:,} rows); the chosen configuration is fitted again "
            f"on months {months(t['train_months'])} and scored once on month "
            f"{t['eval_month']} ({t['n_eval']:,} rows). Every score here is on "
            f"month {t['eval_month']}.")


def months(ms) -> str:
    return f"{ms[0]}-{ms[-1]}" if len(ms) > 1 else str(ms[0])


def val_frauds(res) -> int:
    v = res["folds"]["validation"]
    return round(v["n_eval"] * v["prevalence_eval"])


def limits_line(res, rows, a) -> str:
    first = (f"- The validation month holds about {val_frauds(res):,} frauds, "
             "so validation AUPRC is less noisy than on ULB")
    only = fd.one_choice(rows, a)
    if only is None:
        return first + "; the chosen configuration changes between seeds."
    shown = f"`{only['config']}`" if list(only) == ["config"] else fd.params(only)
    return first + (f". Here the same configuration ({shown}) was chosen on "
                    "every seed.")


def proxy_paragraph(rows) -> str:
    builds = {r["lanes"]["proxy"]["build"] for r in rows}
    if builds != {"serial"}:
        raise ClaimError(f"the proxy page states every pool was built "
                         f"serially; the rows record {builds}")
    k = sorted({len(r["lanes"]["proxy"]["features"]) for r in rows})
    n = sorted({r["lanes"]["proxy"]["n_learners"] for r in rows})
    feats = str(k[0]) if len(k) == 1 else f"{k[0]} to {k[-1]}"
    held = str(n[0]) if len(n) == 1 else f"{n[0]} to {n[-1]}"
    return (f"Every pool was built serially. The chosen configuration's pool "
            f"used {feats} features and held {held} learners.")


def algo_doc(res, a) -> str:
    A, R = res["analysis"], res["rows"]
    N = A["n_seeds"]
    seeds = f"{R[0]['seed']}-{R[-1]['seed']}"
    s = A["per_algorithm"][a]
    lanes = [r["lanes"][a] for r in R]
    order = A["order_by_mean_test_auprc"]
    rank = order.index(a) + 1
    L = [f"# {NAMES[a]} on IEEE-CIS: best achievable result (F174)", ""]
    L += [f"**BLUF.** Tuned on month {res['folds']['validation']['eval_month']} "
          f"and scored on month {res['folds']['test']['eval_month']} over {N} "
          f"seeds ({seeds}), {NAMES[a]} reaches a mean test AUPRC of "
          f"{fd.f4(s['auprc']['mean'])} (95% t interval "
          f"{fd.f4(s['auprc']['t95'][0])} to {fd.f4(s['auprc']['t95'][1])}). "
          f"It is number {rank} of {len(order)} by mean test AUPRC; the "
          "ranking and which differences are reliable are on "
          f"[{COMPARISON}]({COMPARISON}). The ULB page for the same algorithm "
          f"is [{fd.FILES[a]}]({fd.FILES[a]}).", ""]
    L += ["- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.",
          "- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "
          "\"F174\", written before any score.",
          f"- **Evidence**: {FILE} (evidence tag SIM, zero metered seconds), "
          "generator `experiments/phase2/src/f174_ieee_algorithms.py`. Every "
          "figure below comes from that file. Each seed's outcome block is "
          "in the file's rows; the per-row test scores it names are in "
          "`experiments/phase2/predictions/` (gitignored, kept on this "
          "machine), each recorded with its SHA-256.",
          fold_line(res),
          f"- **Setup**: {SETUP[a]}.", ""]
    tried = lanes[0]["tried"]
    counts = fd.chosen_counts(R, a)
    L += ["## Configurations tried", "",
          f"{len(tried)} configurations, F166's grid, imported unchanged. Per "
          "seed, the one with the highest validation AUPRC was kept (ties: "
          "the first listed).", "",
          "| Configuration | Seeds that chose it |", "|---|---|"]
    for t in tried:
        k = json.dumps(t["params"], sort_keys=True)
        L.append(f"| {fd.params(t['params'])} | {counts.get(k, 0)} of {N} |")
    L.append("")
    if a == "proxy":
        L += [proxy_paragraph(R), ""]
    if a in IMPUTED:
        L += [fd.balanced_line(R, a, N), ""]
    if a == "svm":
        won, kept = A["svm_form"]["rbf_beats_linear_seeds"], A["svm_form"]["kept"]
        cs = " and ".join(f"{c:g}" for c in sorted(g["C"] for g in res["svm_rbf_grid"]))
        L += ["## Alternative tried: an RBF kernel", "",
              f"An RBF SVM (`SVC`, `gamma=\"scale\"`, C {cs}) on a stratified "
              f"{res['rbf_rows']:,}-row subsample of the tuning months, because "
              "an RBF kernel on every row is quadratic in rows. The entry keeps "
              "it only if its best validation AUPRC beats the linear form's on "
              f"a majority of seeds. It did so on {won} of {N} seeds, so the "
              f"lane keeps the **{kept}** form. Every figure in this document "
              f"is the {kept} form.", ""]
    L += ["## Test-month results over seeds", "",
          f"Mean, SD and 95% t interval over {N} seeds, each seed at its own "
          "chosen configuration.", "",
          "| Metric | Mean | SD | 95% t interval |", "|---|---|---|---|"]
    L += [fd.stat_row(lab, s[k]) for lab, k in fd.ROWS]
    L.append("")
    for op, desc in fd.OPS:
        L += [f"At the {desc.replace('validation', 'the validation month')}:", "",
              "| Metric | Mean | SD | 95% t interval |", "|---|---|---|---|"]
        L += [fd.stat_row(fd.OP_LABEL[m], s[op][m]) for m in fd.OP_METRICS]
        L.append("")
    L += ["## Confusion counts per seed, test month", "",
          "TP, FP, TN and FN at each threshold chosen on the validation month.", "",
          "| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |",
          "|---|---|---|---|"]
    for ln in lanes:
        ops = {o["operating_point"]: o["confusion"] for o in ln["test"]["operating_points"]}
        cells = [" / ".join(str(ops[op][k]) for k in ("tp", "fp", "tn", "fn"))
                 for op, _ in fd.OPS]
        L.append(f"| {ln['seed']} | {fd.params(ln['chosen_params'])} | {cells[0]} | {cells[1]} |")
    L.append("")
    L += ["## Limits", "",
          limits_line(res, R, a),
          "- One protocol and one grid per algorithm, F166's. A larger grid "
          "may do better; this is the best of the configurations named in "
          "the entry, not the best possible.",
          "- One test month. Month-to-month drift is outside this result; "
          "F152 scores months 4-6.",
          "- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside "
          "this part of F157.", ""]
    return "\n".join(L) + "\n"


def comparison(res) -> str:
    A, R = res["analysis"], res["rows"]
    N = A["n_seeds"]
    seeds = f"{R[0]['seed']}-{R[-1]['seed']}"
    order = A["order_by_mean_test_auprc"]
    pairs = A["adjacent_pairs"]
    if [(p["a"], p["b"]) for p in pairs] != list(zip(order, order[1:])):
        raise ClaimError("the adjacent pairs are not the result's order")
    reliable = [p for p in pairs if p["reading"] != NO_DIFF]
    runs = fd.unestablished(order, pairs)
    count = WORDS[len(order)]
    bluf = (f"**BLUF.** Over {N} seeds ({seeds}), the order by mean test "
            f"AUPRC is {fd.names(order)}. Of the {WORDS[len(pairs)]} adjacent "
            f"pairs, {len(reliable)} "
            f"{'differs' if len(reliable) == 1 else 'differ'} reliably under "
            "the entry's test")
    if reliable:
        bluf += ": " + "; ".join(f"{NAMES[p['a']]} above {INNER[p['b']]}"
                                 for p in reliable)
    bluf += "."
    if runs:
        bluf += (" No other adjacent pair differs reliably, so the order "
                 "among " + "; ".join(fd.names(r) for r in runs)
                 + " is not established.")
    L = [f"# IEEE-CIS: {count} algorithms compared (F174)", "", bluf, ""]
    L += ["- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.",
          "- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "
          "\"F174\", written before any score.",
          f"- **Evidence**: {FILE} (evidence tag SIM, zero metered seconds). "
          "Every figure below comes from that file.",
          f"- **Seeds**: {N}, as Sprint 30 Decision D5 set, with no time cap. "
          f"Seed 42 took {R[0]['minutes']} minutes for all {count} algorithms.",
          f"- **ULB**: the same algorithms and grids on ULB are on "
          f"[{fd.COMPARISON}]({fd.COMPARISON}).", ""]
    L += ["## Mean test AUPRC, in order", "",
          "| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | Document |",
          "|---|---|---|---|---|---|"]
    for i, a in enumerate(order, 1):
        s = A["per_algorithm"][a]
        lo, hi = s["auprc"]["t95"]
        L.append(f"| {i} | {NAMES[a]} | {fd.f4(s['auprc']['mean'])} | {fd.f4(lo)} "
                 f"to {fd.f4(hi)} | {fd.f4(s['recall_at_budget_on_test']['mean'])} "
                 f"| [{FILES[a]}]({FILES[a]}) |")
    L.append("")
    L += ["## Adjacent pairs", "",
          f"The entry's test: with {N} seeds (8 or more), the exact two-sided "
          "Wilcoxon signed-rank test on per-seed AUPRC differences is primary, "
          f"at Bonferroni 0.05 / {N_PAIRS_TESTED}. \"A above B\" is written "
          "only when it rejects. Only adjacent pairs are tested, so a "
          "non-adjacent statement is not made here.", ""]
    L += [f"- {fd.pair_text(p)}" for p in pairs]
    L.append("")
    per = A["per_algorithm"]
    rec = [per[a]["recall_at_budget_on_test"]["mean"] for a in order]
    L += ["## Notes", "",
          "- At the 0.5% alert budget, mean recall on the test month lies "
          f"between {fd.f4(min(rec))} and {fd.f4(max(rec))}. The month's fraud "
          f"rate is {res['folds']['test']['prevalence_eval']:.2%}, so a 0.5% "
          "budget cannot flag most frauds (F171).",
          f"- The SVM lane keeps its {A['svm_form']['kept']} form; the RBF "
          f"alternative beat it on validation on "
          f"{A['svm_form']['rbf_beats_linear_seeds']} of {N} seeds "
          f"([{FILES['svm']}]({FILES['svm']})).", ""]
    return "\n".join(L)


def check_fixed_text(res: dict) -> None:
    """The fixed text states IEEE-CIS, the evidence tag SIM, zero metered
    seconds, the linear SVM, the Wilcoxon test as primary with 8 or more
    seeds, a Bonferroni divisor of 6 and a complete run."""
    A = res["analysis"]
    pairs = A["adjacent_pairs"]
    wrong = []
    if res.get("dataset") != "ieee_cis":
        wrong.append(f"dataset {res.get('dataset')!r}, not ieee_cis")
    if res.get("evidence_tag") != "SIM":
        wrong.append(f"evidence tag {res.get('evidence_tag')!r}, not SIM")
    if res.get("metered_seconds") != 0:
        wrong.append(f"metered seconds {res.get('metered_seconds')!r}, not 0")
    if not res.get("complete"):
        wrong.append("the run is not complete")
    if A["svm_form"]["kept"] != "linear":
        wrong.append(f"SVM form {A['svm_form']['kept']!r}, not linear")
    if A["n_seeds"] < 8 or any(p["primary"] != "wilcoxon" for p in pairs):
        wrong.append("a primary test that is not Wilcoxon, or fewer than 8 seeds")
    if len(pairs) != N_PAIRS_TESTED:
        wrong.append(f"{len(pairs)} adjacent pairs, not {N_PAIRS_TESTED}")
    if wrong:
        raise ClaimError("the fixed text does not hold: " + "; ".join(wrong))


def render(res: dict) -> dict[str, str]:
    check_fixed_text(res)
    pages = {name: algo_doc(res, a) for a, name in FILES.items()}
    pages[COMPARISON] = comparison(res)
    return pages


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--result", type=Path, default=RESULT)
    ap.add_argument("--out", type=Path, default=DOCS)
    ap.add_argument("--check", action="store_true",
                    help="compare with the pages in --out; write nothing")
    args = ap.parse_args(argv)
    pages = render(json.loads(args.result.read_text(encoding="utf-8")))
    if args.check:
        bad = fd.differing(pages, args.out)
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
