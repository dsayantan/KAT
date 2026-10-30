"""Builds the static KAT site into ../site. Run: python3 build.py"""
import json, random, re, os, html, sys
import gen_numeric, gen_ps, verbal, writing, official

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
SECTIONS = [("problem-solving", "Problem-Solving", "Puzzles, coding–decoding, directions, series, ranks, clocks, calendars, blood relations, syllogisms."),
            ("verbal", "Critical Thinking & Verbal Ability", "Grammar, vocabulary in context, conclusions, assumptions, flaws, strengthen/weaken, sentence order."),
            ("numeric", "Numeric Reasoning", "Percentages, ratios, profit and loss, interest, speed, work, averages, mixtures, ages.")]
MIN = 80; PER_TEST = 10; NTESTS = 3

def bank():
    r = random.Random(2027)
    ps = gen_ps.generate() + gen_ps.hand(); nu = gen_numeric.generate(50, seed=7); ve = list(verbal.V)
    out = {}
    for key, items in (("problem-solving", ps), ("verbal", ve), ("numeric", nu)):
        items = items[:]; r.shuffle(items); out[key] = items
    return out

def finalize(d, rng):
    opts = [d["ans"]] + d["wrongs"]
    assert len(set(opts)) == 4, d["q"]
    order = list(range(4)); rng.shuffle(order)
    return dict(q=d["q"], o=[opts[i] for i in order], a=order.index(0), s=d["sol"])

def esc_json(o): return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

def page(title, body, depth=0, extra_head="", scripts=""):
    p = "../" * depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><link rel="stylesheet" href="{p}assets/style.css">{extra_head}</head><body>
<header class="top"><div class="wrap"><a class="brand" href="{p}index.html">KAT Prep</a><nav>
<a href="{p}syllabus.html">Syllabus</a><a href="{p}official-sample.html">Official sample</a><a href="{p}practice-problem-solving.html">Problem-Solving</a><a href="{p}practice-verbal.html">Verbal</a><a href="{p}practice-numeric.html">Numeric</a><a href="{p}practice-writing.html">Writing</a><a href="{p}tests.html">Tests</a></nav></div></header>
<main class="wrap">{body}</main>
<div class="wrap"><footer>Unofficial practice material, not affiliated with Krea University. Questions marked “Official sample” belong to Krea; everything else is original.</footer></div>{scripts}</body></html>"""

REVEAL = '<div class="tools"><button onclick="document.querySelectorAll(\'details.a\').forEach(d=>d.open=true)">Show all answers</button><button class="ghost" onclick="document.querySelectorAll(\'details.a\').forEach(d=>d.open=false)">Hide all</button></div>'

def qhtml(i, q, label=""):
    o = "".join(f"<li>{x}</li>" for x in q["o"])
    return f'<div class="q" id="q{i}"><div class="n">Question {i}{label}</div><div>{q["q"]}</div><ol>{o}</ol><details class="a"><summary>Show answer</summary><div class="sol"><span class="ans">Answer: {"ABCD"[q["a"]]}. {q["o"][q["a"]]}</span><br>{q["s"]}</div></details></div>'

def wc(t): return len(re.findall(r"\S+", re.sub(r"<[^>]+>", " ", t.replace("<br>", " "))))

def main():
    os.makedirs(OUT, exist_ok=True)
    B = bank(); rng = random.Random(99)
    tests = [{"id": f"test-{k+1}", "n": k+1, "sections": [], "writing": None} for k in range(NTESTS)]
    practice = {}
    for key, name, desc in SECTIONS:
        items = [finalize(d, rng) for d in B[key]]
        need = PER_TEST*NTESTS
        assert len(items) >= need + 15, (key, len(items))
        for k in range(NTESTS):
            tests[k]["sections"].append({"name": name, "qs": items[k*PER_TEST:(k+1)*PER_TEST]})
        practice[key] = items[need:]
    # writing
    for k, w in enumerate(writing.W):
        assert wc(w["model"]) <= 300, (w["id"], wc(w["model"]))
        tests[k]["writing"] = dict(prompt=w["prompt"], plan=w["plan"], model=w["model"], rubric=writing.RUBRIC)
    # uniqueness across everything
    allq = [q["q"] for t in tests for s in t["sections"] for q in s["qs"]] + [q["q"] for v in practice.values() for q in v]
    assert len(allq) == len(set(allq)), "duplicate question text"
    # ---- practice pages
    for key, name, desc in SECTIONS:
        qs = practice[key]
        body = f'<div class="hero"><h1>{name}</h1><p>{desc} {len(qs)} practice questions with worked answers. These are separate from the three online tests.</p></div>{REVEAL}' + "".join(qhtml(i+1, q) for i, q in enumerate(qs))
        open(f"{OUT}/practice-{key}.html", "w").write(page(f"{name} – practice", body))
    body = '<div class="hero"><h1>Writing Skills</h1><p>Krea’s writing section asks for a reflective response in <b>not more than 300 words</b>. Plan for 4 short paragraphs. Each prompt below has planning notes; the first three also have a full model response (they are the prompts used in the three online tests, so attempt them there first).</p></div>'
    body += "<h2>Your checklist</h2><table>" + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in writing.RUBRIC) + "</table>"
    for w in writing.W + writing.BANK:
        pl = "".join(f"<li>{p}</li>" for p in w["plan"]); m = f'<p>{w["model"]}</p><p class="note">{wc(w["model"])} words.</p>' if "model" in w else ""
        body += f'<div class="q"><div class="n">Prompt {w["id"]}</div><div>{w["prompt"]}</div><details class="a"><summary>Plan{" and model response" if m else ""}</summary><div class="sol"><ul>{pl}</ul>{m}</div></details></div>'
    open(f"{OUT}/practice-writing.html", "w").write(page("Writing – practice", body))
    # ---- official sample
    body = '<div class="hero"><h1>Krea’s official sample test, solved</h1><p>The only published KAT material is the <a href="https://krea.edu.in/sias/wp-content/uploads/2023/10/Sample-Krea-Aptitude-Test-2023-24.pdf" rel="noopener">Sample Krea Aptitude Test (PDF)</a>: 15 multiple-choice questions and one essay prompt. Krea gives no answer key; the solutions below are ours. Two verbal items are ambiguous and are flagged.</p></div>' + REVEAL
    cur = None; i = 0
    for sec, q, o, a, s in official.OFF:
        i += 1
        if sec != cur: body += f'<div class="sec">{sec}</div>'; cur = sec
        body += qhtml(i, dict(q=q, o=o, a=a, s=s), " · Official sample")
    body += f'<div class="sec">Writing Skills</div><div class="q"><div class="n">Official sample</div><div>{official.PROMPT}</div><details class="a"><summary>Approach</summary><div class="sol">See the <a href="practice-writing.html">Writing page</a>; prompt W1 and W2 follow the same two ideas (a mistake you would undo, an experience you would repeat), with full model responses.</div></details></div>'
    open(f"{OUT}/official-sample.html", "w").write(page("Official sample solved", body))
    # ---- tests
    for t in tests:
        total = sum(len(s["qs"]) for s in t["sections"])
        gate = f'<div class="hero"><h1>Online Test {t["n"]}</h1><p>{total} multiple-choice questions plus one essay, {MIN} minutes, in the four-section order of the real KAT.</p></div><div id="gate" class="q"><ul><li>The clock starts when you press Begin and keeps running if you reload the page.</li><li>Change answers freely; nothing is marked until you submit. The test submits itself at time-up.</li><li>Your essay is saved in this browser as you type. It is not auto-marked; you self-assess it with a checklist.</li><li>No negative marking is applied (Krea has not published its scheme).</li><li>Suggested pacing: about 55 minutes for the {total} questions, 20 for the essay, 5 to review.</li></ul><button id="begin">Begin test</button></div>'
        gate += '<div id="result" hidden></div><div class="bar" id="runbar" hidden><div class="wrap"><span id="clock">—</span><span id="prog"></span></div></div><div id="paper" hidden></div><div class="tools"><button id="submit" hidden>Submit test</button></div>'
        data = {"id": t["id"], "minutes": MIN, "sections": t["sections"], "writing": t["writing"]}
        sc = f'<script>window.TEST={esc_json(data)}</script><script src="assets/test.js"></script>'
        open(f"{OUT}/{t['id']}.html", "w").write(page(f"Test {t['n']}", gate, scripts=sc))
    cards = "".join(f'<a class="card" href="{t["id"]}.html"><b>Online Test {t["n"]}</b><span>{sum(len(s["qs"]) for s in t["sections"])} MCQs + essay · {MIN} min</span></a>' for t in tests)
    open(f"{OUT}/tests.html", "w").write(page("Online tests", f'<div class="hero"><h1>Online tests</h1><p>Three full-length timed tests with automatic marking and worked solutions after you submit. Progress is stored only in your own browser.</p></div><div class="grid">{cards}</div>'))
    # ---- syllabus
    body = '''<div class="hero"><h1>KAT syllabus and pattern</h1><p>What Krea has actually published, and what is our inference.</p></div>
<h2>Published by Krea</h2><table><tr><th>Item</th><th>Detail</th></tr>
<tr><td>Name</td><td>Krea Assessment Test (KAT), earlier called the Krea Aptitude Test</td></tr>
<tr><td>Duration</td><td>80 minutes, taken online</td></tr>
<tr><td>Sections</td><td>1. Problem-Solving · 2. Critical Thinking &amp; Verbal Ability · 3. Numeric Reasoning · 4. Writing Skills</td></tr>
<tr><td>Writing</td><td>Reflective response, not more than 300 words</td></tr>
<tr><td>Sample</td><td><a href="https://krea.edu.in/sias/wp-content/uploads/2023/10/Sample-Krea-Aptitude-Test-2023-24.pdf" rel="noopener">Sample test PDF</a> (the 2022 and 2023–24 samples are identical) · <a href="https://krea.edu.in/sias/sias-selection-process/" rel="noopener">Selection process</a></td></tr></table>
<p class="note">Krea publishes <b>no detailed syllabus, no question count, no marking scheme and no past papers.</b> The sample itself says it is “in no way representative of the length or number of questions”.</p>
<h2>Topic map (our inference from the sample)</h2><table><tr><th>Section</th><th>Topics seen in the sample</th><th>Level</th></tr>
<tr><td>Problem-Solving</td><td>Linear seating arrangement, letter coding (fixed and alternating shifts), blood relations, direction sense</td><td>Class 8–10 reasoning</td></tr>
<tr><td>Critical Thinking &amp; Verbal</td><td>Drawing conclusions, spotting errors, rephrasing, vocabulary in context</td><td>Class 10–12 English</td></tr>
<tr><td>Numeric Reasoning</td><td>Percentage, ratio, profit and cost, percentage difference</td><td>Class 8–10 arithmetic</td></tr>
<tr><td>Writing</td><td>Reflective essay on two linked ideas</td><td>Personal, 300 words</td></tr></table>
<p>The practice sets also include nearby topics (series, ranks, clocks, calendars, syllogisms, interest, work and speed, assumptions, sentence order) because aptitude tests of this type commonly use them. Treat those as sensible preparation, not as announced content.</p>
<h2>Source note</h2><p>The brief mentioned ASOKA, SNUSAT and BITSAT English/Analytics papers as level references. Those were not downloaded for this site, so the question level was calibrated from the Krea sample and general knowledge of such tests. All questions here are original and answers to generated items are computed by code.</p>'''
    open(f"{OUT}/syllabus.html", "w").write(page("Syllabus and pattern", body))
    # ---- index
    npr = sum(len(v) for v in practice.values())
    cards = "".join(f'<a class="card" href="practice-{k}.html"><b>{n}</b><span>{len(practice[k])} practice questions with answers</span></a>' for k, n, d in SECTIONS)
    cards += '<a class="card" href="practice-writing.html"><b>Writing Skills</b><span>12 prompts, plans and model essays</span></a>'
    body = f'''<div class="hero"><h1>Krea Assessment Test (KAT) preparation</h1><p>Questions with worked answers for every section of the KAT, Krea’s official sample solved, and three timed online tests. A static site: no server, nothing to install.</p></div>
<div class="grid"><a class="card" href="syllabus.html"><b>Syllabus &amp; pattern</b><span>What Krea publishes, and what we infer</span></a><a class="card" href="official-sample.html"><b>Official sample, solved</b><span>All 15 MCQs and the essay prompt</span></a></div>
<h2>Practice, question and answer</h2><div class="grid">{cards}</div>
<h2>Online tests</h2><div class="grid">{"".join(f'<a class="card" href="{t["id"]}.html"><b>Test {t["n"]}</b><span>{PER_TEST*3} MCQs + essay · {MIN} min</span></a>' for t in tests)}</div>
<p class="note">{npr} practice MCQs + {PER_TEST*3*NTESTS} test MCQs + 15 official-sample questions. Numeric and puzzle answers are computed by the generator, not typed.</p>'''
    open(f"{OUT}/index.html", "w").write(page("KAT Preparation", body))
    open(f"{OUT}/.nojekyll", "w").close()
    print("built", npr, "practice MCQs;", {k: len(v) for k, v in practice.items()})
main()
