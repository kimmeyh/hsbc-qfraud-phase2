"""Render the F157 SPECTRA part's pages from its result file (the pattern
of `scripts/f166_docs.py` and `scripts/f174_docs.py`).

    <venv python> scripts/f157_spectra_docs.py            write docs/phase2/algorithms/
    <venv python> scripts/f157_spectra_docs.py --check    exit 1 if a page differs
    <venv python> scripts/f157_spectra_docs.py --out DIR  write to DIR instead

Per dataset: one page per algorithm and one comparison page, as the entry
("F157 SPECTRA part", `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6) sets. F166's helpers are imported. Every statement in the
fixed text is computed from the result or checked against it; one the
result does not support raises `ClaimError` and no page is written.
`experiments/src/test_f157_spectra_docs.py` tests the checks.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import f166_docs as fd  # noqa: E402  (F166's helpers)

# The D14 amendment's result: every row, with the kept SVM form scored. The
# first result (`FIRST`) is kept as recorded; its linear SVM rows are in
# this file as `svm_linear`.
RESULT = (ROOT / "experiments" / "phase2" / "results"
          / "f157_spectra_algorithms_rbf.json")
DOCS = fd.DOCS
FILE = "`experiments/phase2/results/f157_spectra_algorithms_rbf.json`"
FIRST = "`experiments/phase2/results/f157_spectra_algorithms.json`"
AMENDED = ("- **Amendment**: the SVM lane is the form the entry's rule keeps, "
           "scored on the test fold under the entry's amendment of "
           "2026-11-05 (Sprint 31 D14 option 1). The first result, "
           f"{FIRST}, is kept as recorded; it scored the linear form only.")
GENERATOR = "`experiments/phase2/src/f157_spectra_algorithms.py`"
NAMES, INNER, POSSESSIVE, WORDS = fd.NAMES, fd.INNER, fd.POSSESSIVE, fd.WORDS
ClaimError = fd.ClaimError
NO_DIFF = fd.NO_DIFF
N_PAIRS_TESTED = fd.N_PAIRS_TESTED
DATASETS = ("energy_steel", "oilgas_gasturbine", "telecom_churn",
            "maintenance_ai4i")
SUFFIX = {"hgb": "HGB", "lightgbm": "LIGHTGBM", "xgboost": "XGBOOST",
          "catboost": "CATBOOST", "logreg": "LOGISTIC_REGRESSION",
          "svm": "SVM", "proxy": "CVQBOOST_PROXY"}
CARD = ("- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: "
        "F166's algorithms and grids on SPECTRA's four datasets.")
ENTRY = ("- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` "
         "section 6, \"F157 SPECTRA part\", written before any score.")


def page(ds: str, a: str) -> str:
    return f"{ds.upper()}_{SUFFIX[a]}.md"


def comparison_page(ds: str) -> str:
    return f"{ds.upper()}_COMPARISON.md"


def rows_of(res: dict, ds: str) -> list[dict]:
    rows = sorted((r for r in res["rows"] if r["dataset"] == ds),
                  key=lambda r: r["seed"])
    if not rows:
        raise ClaimError(f"no rows for {ds}")
    return rows


def test_size(rows: list[dict]) -> tuple[int, int]:
    """Test rows and test positives, from the first lane's confusion
    counts; refused if they differ between lanes of a seed."""
    sizes = set()
    for r in rows:
        for ln in r["lanes"].values():
            c = ln["test"]["operating_points"][0]["confusion"]
            sizes.add((r["seed"], sum(c.values()), c["tp"] + c["fn"]))
    by_seed = {}
    for seed, n, pos in sizes:
        by_seed.setdefault(seed, set()).add((n, pos))
    if any(len(v) > 1 for v in by_seed.values()):
        raise ClaimError("the lanes of one seed score different test rows")
    ns = sorted({n for v in by_seed.values() for n, _ in v})
    ps = sorted({p for v in by_seed.values() for _, p in v})
    return ns, ps


def span(vals, fmt="{:,}") -> str:
    lo, hi = min(vals), max(vals)
    return fmt.format(lo) if lo == hi else f"{fmt.format(lo)} to {fmt.format(hi)}"


def data_line(res: dict, ds: str, rows: list[dict]) -> str:
    ns, ps = test_size(rows)
    k = sorted({len(r["features"]) for r in rows})
    return (f"- **Data**: SPECTRA `{ds}`, label `{res['label']}`, "
            f"{res['protocol']['split']}. Tuning reads the training and "
            f"validation folds; every score here is on the test fold "
            f"({span(ns)} rows, {span(ps)} positives per seed; "
            f"{span(k)} feature columns).")


def svm_form_line(A: dict, n: int) -> str:
    won, kept = A["svm_form"]["rbf_beats_linear_seeds"], A["svm_form"]["kept"]
    if not A.get("svm_lane_is_kept_form") or A.get("svm_lane_form") != kept:
        raise ClaimError(f"the rule keeps the {kept} SVM and the lane scored "
                         f"{A.get('svm_lane_form')!r}")
    head = (f"The entry keeps the RBF form only if its best validation AUPRC "
            f"beats the linear form's on a majority of seeds. It did so on "
            f"{won} of {n} seeds, so the entry's rule keeps the **{kept}** "
            "form.")
    if kept == "linear":
        return head + " Every SVM figure here is the linear form."
    return (head + " Every SVM figure here, its place in the order and its "
            "adjacent pairs are the RBF form's, scored on the test fold under "
            "the D14 amendment. The linear form is reported on the SVM page, "
            "not ranked.")


def degenerate_seeds(rows: list[dict], fold: str = "val") -> list[int]:
    """Seeds whose RBF AUPRC equals the test fold's positive rate to 4
    places: on validation the best recorded RBF fit (`fold="val"`; the
    result does not record the validation fold's rate), on test the
    scored RBF lane (`fold="test"`). That is the AUPRC of scores that
    carry no ranking."""
    out = []
    for r in rows:
        prev = r["lanes"]["svm"]["test"]["prevalence"]
        v = (r["svm_rbf_alternative"]["best_val_auprc"] if fold == "val"
             else r["lanes"]["svm"]["test"]["auprc"])
        if round(v, 4) == round(prev, 4):
            out.append(r["seed"])
    return out


def seeds_text(seeds: list[int]) -> str:
    return (f"seed{'s' if len(seeds) > 1 else ''} "
            f"{', '.join(str(x) for x in seeds)}")


def linear_paragraph(rows: list[dict]) -> str:
    """The linear form's test AUPRC, the form the rule did not keep."""
    import statistics
    lin = [r["lanes"].get("svm_linear") for r in rows]
    if any(x is None for x in lin):
        raise ClaimError("a seed has no svm_linear lane")
    v = [x["test"]["auprc"] for x in lin]
    return (f"The linear form (`LinearSVC`, all training rows, F166's grid), "
            f"which the rule did not keep: mean test AUPRC "
            f"{fd.f4(statistics.mean(v))} over {len(v)} seeds, from {fd.f4(min(v))} "
            f"to {fd.f4(max(v))} (the SVM figures of {FIRST}). It is not ranked.")


def pocket_line(A: dict, a: str) -> str | None:
    p = A["pocket"].get(a)
    if not p or not p.get("in_pocket") or not p.get("out_of_pocket"):
        return None
    i, o = p["in_pocket"], p["out_of_pocket"]
    return (f"Secondary, as the entry reports it: test AUPRC inside the "
            f"pocket (`in_pocket` = 1) {fd.f4(i['mean'])} (95% t interval "
            f"{fd.f4(i['t95'][0])} to {fd.f4(i['t95'][1])}, {i['n']} seeds) "
            f"and outside it {fd.f4(o['mean'])} ({fd.f4(o['t95'][0])} to "
            f"{fd.f4(o['t95'][1])}, {o['n']} seeds).")


def proxy_paragraph(rows: list[dict]) -> str:
    builds = {r["lanes"]["proxy"]["build"] for r in rows}
    if builds != {"serial"}:
        raise ClaimError(f"the proxy page states every pool was built "
                         f"serially; the rows record {builds}")
    only = fd.one_choice(rows, "proxy")
    chose = (f"The `{only['config']}` configuration was chosen on every seed"
             if only else "The chosen configuration changes between seeds")
    held = span(sorted({r["lanes"]["proxy"]["n_learners"] for r in rows}))
    feats = span(sorted({len(r["lanes"]["proxy"]["features"]) for r in rows}))
    return (f"{chose}. Every pool was built serially; the chosen pool used "
            f"{feats} features and held {held} learners.")


def algo_doc(res: dict, ds: str, a: str) -> str:
    A, R = res["analysis"][ds], rows_of(res, ds)
    N = A["n_seeds"]
    seeds = f"{R[0]['seed']}-{R[-1]['seed']}"
    s = A["per_algorithm"][a]
    lanes = [r["lanes"][a] for r in R]
    order = A["order_by_mean_test_auprc"]
    comp = comparison_page(ds)
    L = [f"# {NAMES[a]} on SPECTRA {ds}: best achievable result (F157)", ""]
    L += [f"**BLUF.** Tuned on validation and scored on the test fold over "
          f"{N} seeds ({seeds}), {NAMES[a]} reaches a mean test AUPRC of "
          f"{fd.f4(s['auprc']['mean'])} (95% t interval "
          f"{fd.f4(s['auprc']['t95'][0])} to {fd.f4(s['auprc']['t95'][1])}). "
          f"It is number {order.index(a) + 1} of {len(order)} by mean test "
          f"AUPRC; the ranking and which differences are reliable are on "
          f"[{comp}]({comp}).", ""]
    L += [CARD, ENTRY, AMENDED,
          f"- **Evidence**: {FILE} (evidence tag SIM, zero metered seconds), "
          f"generator {GENERATOR}. Every figure below comes from that file. "
          "Each seed's outcome block is in the file's rows; the per-row test "
          "scores it names are in `experiments/phase2/predictions/` "
          "(gitignored, kept on this machine), each recorded with its "
          "SHA-256.",
          data_line(res, ds, R), ""]
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
    if a == "logreg" or (a == "svm" and A["svm_lane_form"] == "linear"):
        L += [fd.balanced_line(R, a, N), ""]
    if a == "svm":
        L += ["## The SVM's form", "",
              f"The RBF SVM is fitted on a stratified subsample of at most "
              f"{res['rbf_rows']:,} training rows (the whole fold when "
              "smaller). " + svm_form_line(A, N), "",
              linear_paragraph(R), ""]
        flat = degenerate_seeds(R)
        if flat:
            L += [f"On {seeds_text(flat)} the RBF form's best validation "
                  "AUPRC equals the test fold's positive rate to four places, "
                  "which is what a score with no ranking gets. They count as "
                  "linear wins, so they do not add to the RBF majority.", ""]
            if any(r["svm_rbf_alternative"]["beats_linear_on_validation"]
                   for r in R if r["seed"] in flat):
                raise ClaimError("a seed with a no-ranking RBF score is "
                                 "recorded as an RBF win")
            flat_test = degenerate_seeds(R, "test")
            ranked = [x for x in flat if x not in flat_test]
            if flat_test:
                L += [f"On {seeds_text(flat_test)} the scored RBF lane's test "
                      "AUPRC is also the positive rate: no ranking there "
                      "either, and those seeds are scored as they are, as "
                      "the amendment sets.", ""]
            if ranked:
                L += [f"On {seeds_text(ranked)} the RBF scores carry no "
                      "ranking on validation but do on test. **Not "
                      "explained**: the same fit gives constant scores on one "
                      "fold and ranked scores on the other. A cause in this "
                      "dataset's features (the date columns parsed per fold, "
                      "which raise a format warning) is a guess, not tested.",
                      ""]
    L += ["## Test-fold results over seeds", "",
          f"Mean, SD and 95% t interval over {N} seeds, each seed at its "
          "own chosen configuration.", "",
          "| Metric | Mean | SD | 95% t interval |", "|---|---|---|---|"]
    L += [fd.stat_row(lab, s[k]) for lab, k in fd.ROWS]
    L.append("")
    pk = pocket_line(A, a)
    if pk:
        L += [pk, ""]
    for op, desc in fd.OPS:
        L += [f"At the {desc}:", "",
              "| Metric | Mean | SD | 95% t interval |", "|---|---|---|---|"]
        L += [fd.stat_row(fd.OP_LABEL[m], s[op][m]) for m in fd.OP_METRICS]
        L.append("")
    L += ["## Confusion counts per seed, test fold", "",
          "TP, FP, TN and FN at each validation-chosen threshold, and at "
          "the test fold's own 0.5% budget (the comparison page's recall).", "",
          "| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |",
          "|---|---|---|---|---|"]
    for ln in lanes:
        ops = {o["operating_point"]: o["confusion"]
               for o in ln["test"]["operating_points"]}
        cells = [fd.counts_cell(ops[op]) for op, _ in fd.OPS]
        L.append(f"| {ln['seed']} | {fd.params(ln['chosen_params'])} | "
                 f"{cells[0]} | {cells[1]} | "
                 f"{fd.counts_cell(fd.at_budget(ln)['confusion'])} |")
    L.append("")
    L += ["## Limits", "",
          "- One protocol and one grid per algorithm, F166's. A larger grid "
          "may do better; this is the best of the configurations named in "
          "the entry, not the best possible.",
          "- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside "
          "this part of F157.", ""]
    return "\n".join(L) + "\n"


def comparison(res: dict, ds: str) -> str:
    A, R = res["analysis"][ds], rows_of(res, ds)
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
    svm_form_line(A, N)  # refuses a lane that is not the kept form
    plan = res["seed_plans"][ds]
    L = [f"# SPECTRA {ds}: {count} algorithms compared (F157)", "", bluf, ""]
    L += [CARD, ENTRY, AMENDED,
          f"- **Evidence**: {FILE} (evidence tag SIM, zero metered seconds). "
          "Every figure below comes from that file.",
          f"- **Seeds**: seed 42 took {plan['t42_minutes']} minutes for all "
          f"{count} algorithms, so the entry's rule gave {N} seeds.",
          data_line(res, ds, R), ""]
    L += ["## Mean test AUPRC, in order", "", fd.counts_intro("test fold", N), "",
          "| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | TP | FP | TN | FN | Document |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for i, a in enumerate(order, 1):
        s = A["per_algorithm"][a]
        lo, hi = s["auprc"]["t95"]
        tp, fp, tn, fn = fd.count_ranges([r["lanes"][a] for r in R])
        L.append(f"| {i} | {NAMES[a]} | {fd.f4(s['auprc']['mean'])} | "
                 f"{fd.f4(lo)} to {fd.f4(hi)} | "
                 f"{fd.f4(s['recall_at_budget_on_test']['mean'])} | {tp} | "
                 f"{fp} | {tn} | {fn} | [{page(ds, a)}]({page(ds, a)}) |")
    L.append("")
    L += ["## Adjacent pairs", "",
          f"The entry's test (F166's): with {N} seeds (8 or more), the exact "
          "two-sided Wilcoxon signed-rank test on per-seed AUPRC differences "
          f"is primary, at Bonferroni 0.05 / {N_PAIRS_TESTED}. \"A above B\" "
          "is written only when it rejects. Only adjacent pairs are tested, "
          "so a non-adjacent statement is not made here.", ""]
    L += [f"- {fd.pair_text(p)}" for p in pairs]
    L.append("")
    L += ["## In and out of the pocket (secondary)", "",
          "Test AUPRC inside the pocket (`in_pocket` = 1) and outside it, "
          "mean over seeds, as the entry reports it.", "",
          "| Algorithm | In the pocket | Out of the pocket |", "|---|---|---|"]
    for a in order:
        p = A["pocket"].get(a) or {}
        cell = (lambda q: f"{fd.f4(q['mean'])} ({q['n']} seeds)"
                if q else "not scored")
        L.append(f"| {NAMES[a]} | {cell(p.get('in_pocket'))} | "
                 f"{cell(p.get('out_of_pocket'))} |")
    L.append("")
    rec = [A["per_algorithm"][a]["recall_at_budget_on_test"]["mean"]
           for a in order]
    over = fd.over_budget_line(R, order, "test fold")
    L += ["## Notes", "",
          f"- At the test fold's own 0.5% alert budget, mean recall lies "
          f"between {fd.f4(min(rec))} and {fd.f4(max(rec))}. The budget is "
          "set for fraud rates; these datasets' positive rates are far "
          "higher, so the budget can catch only a small share of their "
          "positives.",
          *([over] if over else []),
          "- " + svm_form_line(A, N) + f" ([{page(ds, 'svm')}]"
          f"({page(ds, 'svm')}))", ""]
    return "\n".join(L)


def check_fixed_text(res: dict) -> None:
    """The fixed text states the SPECTRA part, the evidence tag SIM, zero
    metered seconds, a complete run, the four datasets, and per dataset
    the Wilcoxon test as primary with 8 or more seeds and a Bonferroni
    divisor of 6."""
    wrong = []
    if res.get("part") != "SPECTRA":
        wrong.append(f"part {res.get('part')!r}, not SPECTRA")
    if res.get("evidence_tag") != "SIM":
        wrong.append(f"evidence tag {res.get('evidence_tag')!r}, not SIM")
    if res.get("metered_seconds") != 0:
        wrong.append(f"metered seconds {res.get('metered_seconds')!r}, not 0")
    if not res.get("complete"):
        wrong.append("the run is not complete")
    if tuple(res.get("datasets", ())) != DATASETS:
        wrong.append(f"datasets {res.get('datasets')}, not {list(DATASETS)}")
    for ds in DATASETS:
        A = (res.get("analysis") or {}).get(ds)
        if A is None:
            wrong.append(f"no analysis for {ds}")
            continue
        pairs = A["adjacent_pairs"]
        if A["n_seeds"] < 8 or any(p["primary"] != "wilcoxon" for p in pairs):
            wrong.append(f"{ds}: a primary test that is not Wilcoxon, or "
                         "fewer than 8 seeds")
        if len(pairs) != N_PAIRS_TESTED:
            wrong.append(f"{ds}: {len(pairs)} adjacent pairs, not "
                         f"{N_PAIRS_TESTED}")
    if wrong:
        raise ClaimError("the fixed text does not hold: " + "; ".join(wrong))


def render(res: dict) -> dict[str, str]:
    check_fixed_text(res)
    pages = {}
    for ds in DATASETS:
        for a in SUFFIX:
            pages[page(ds, a)] = algo_doc(res, ds, a)
        pages[comparison_page(ds)] = comparison(res, ds)
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
