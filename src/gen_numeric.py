"""Numeric Reasoning: templated questions whose answers are COMPUTED, never typed."""
import random, math

def f(x):
    if isinstance(x, float) and abs(x - round(x)) < 1e-9: x = int(round(x))
    if isinstance(x, float): return ("%.2f" % x).rstrip("0").rstrip(".")
    return f"{x:,}" if abs(x) >= 10000 else str(x)

def T(q, ans, wrongs, sol, fmt="{}"):
    return dict(q=q, ans=fmt.format(f(ans)), wrongs=[fmt.format(f(w)) for w in wrongs], sol=sol)

def t_present(r):
    n = r.choice([240, 360, 450, 600, 800, 960]); a = r.choice([x for x in (30, 48, 60, 72, 90, 120, 150, 160, 192) if x < n and (100*(n-x)) % n == 0] or [n//5])
    p = (n-a)*100/n
    return T(f"A school has {n} students. Today {a} are absent. What percentage of the students are present?", p,
             [a*100/n, p+5, p-10], f"Present = {n} − {a} = {n-a}. Percentage = {n-a}/{n} × 100 = {f(p)}%. (Trap: {f(a*100/n)}% is the <i>absent</i> share.)", "{}%")

def t_change(r):
    a = r.choice([40, 50, 80, 120, 200, 250]); k = r.choice([10, 20, 25, 30, 40, 50]); b = a*(100+k)//100
    return T(f"The price of a book rises from ₹{a} to ₹{b}. By what percentage has the price increased?", k,
             [k+5, round(100*(b-a)/b, 2), k*2], f"Increase = {b} − {a} = {b-a}. % increase = {b-a}/{a} × 100 = {k}%. Always divide by the <i>original</i> value.", "{}%")

def t_succ(r):
    M = r.choice([1000, 1500, 2000, 2500, 4000]); d1, d2 = r.choice([(20, 10), (10, 10), (20, 20), (25, 20), (50, 10), (30, 10)])
    sp = M*(100-d1)/100*(100-d2)/100
    return T(f"A jacket marked ₹{M} is sold at successive discounts of {d1}% and {d2}%. Find the selling price.", sp,
             [M*(100-d1-d2)/100, M*(100-(d1+d2)/2)/100, sp+M/50],
             f"After {d1}%: {f(M*(100-d1)/100)}. After a further {d2}%: {f(M*(100-d1)/100)} × {(100-d2)/100} = {f(sp)}. Successive discounts multiply; they do not add (adding would give {f(M*(100-d1-d2)/100)}).", "₹{}")

def t_profit(r):
    cp = r.choice([200, 250, 400, 500, 800, 1200]); p = r.choice([10, 20, 25, 40, 5, 15])
    sp = cp*(100+p)/100
    if r.random() < .5:
        return T(f"An article bought for ₹{cp} is sold at a profit of {p}%. Find the selling price.", sp, [cp+p, cp*(100-p)/100, cp*p/100], f"SP = CP × (100 + {p})/100 = {cp} × {(100+p)/100} = ₹{f(sp)}.", "₹{}")
    return T(f"An article is sold for ₹{f(sp)} at a profit of {p}%. Find its cost price.", cp, [sp*(100-p)/100, sp-p, sp*100/(100+p)+p], f"SP = CP × {100+p}/100, so CP = {f(sp)} × 100/{100+p} = ₹{cp}. (Trap: subtracting {p}% from SP gives {f(sp*(100-p)/100)}, because the profit is a percentage of CP, not SP.)", "₹{}")

def t_reverse_pct(r):
    x = r.choice([10, 20, 25, 50, 100, 40])
    ans = x*100/(100+x)
    return T(f"Company A's revenue is {x}% more than Company B's. By what percentage is B's revenue less than A's?", ans, [x, x/2, 100*x/(100-x) if x < 100 else 50],
             f"Let B = 100, so A = {100+x}. B is less than A by {x}/{100+x} × 100 = {f(ans)}%. The base changes, so the percentages are not equal.", "{}%")

def t_ratio(r):
    a, b, c = r.choice([(2, 3, 5), (1, 2, 3), (3, 4, 5), (2, 5, 3), (4, 5, 6)]); u = r.choice([40, 60, 80, 120, 150, 200]); tot = (a+b+c)*u
    return T(f"₹{tot} is divided among A, B and C in the ratio {a}:{b}:{c}. How much does B receive?", b*u, [a*u, c*u, tot*b//(a+b)],
             f"Total parts = {a+b+c}; one part = {tot}/{a+b+c} = {u}. B = {b} × {u} = ₹{b*u}.", "₹{}")

def t_si(r):
    P = r.choice([2000, 4000, 5000, 8000, 10000]); R = r.choice([5, 6, 8, 10]); t = r.choice([2, 3, 4, 5]); si = P*R*t//100
    return T(f"Find the simple interest on ₹{P} at {R}% per annum for {t} years.", si, [P+si, si*2, P*R//100], f"SI = P × R × T/100 = {P} × {R} × {t}/100 = ₹{si}.", "₹{}")

def t_ci(r):
    P, R = r.choice([(10000, 10), (5000, 20), (8000, 5), (2500, 20), (20000, 10), (4000, 25)])
    ci = P*(1+R/100)**2 - P; si = P*R*2/100
    return T(f"Find the compound interest on ₹{P} for 2 years at {R}% per annum, compounded yearly.", ci, [si, ci+P*R/100, P*(1+R/100)**2],
             f"Amount = {P} × (1 + {R}/100)² = {f(P*(1+R/100)**2)}. CI = Amount − P = ₹{f(ci)}. (Simple interest would be {f(si)}; the extra {f(ci-si)} is interest on interest.)", "₹{}")

def t_avgspeed(r):
    a, b = r.choice([(40, 60), (30, 60), (60, 90), (20, 30), (50, 75), (24, 40), (45, 90)])
    ans = 2*a*b/(a+b)
    return T(f"A car goes from P to Q at {a} km/h and returns along the same road at {b} km/h. What is its average speed for the whole trip?", ans, [(a+b)/2, ans+2, a*b/(a+b)],
             f"For equal distances, average speed = 2ab/(a+b) = 2 × {a} × {b}/{a+b} = {f(ans)} km/h. The simple mean {f((a+b)/2)} is wrong because more time is spent at the slower speed.", "{} km/h")

def t_work(r):
    a, b = r.choice([(12, 24), (10, 15), (20, 30), (15, 30), (6, 12), (9, 18), (30, 60), (8, 24)])
    ans = a*b/(a+b)
    return T(f"A can finish a job in {a} days and B in {b} days. Working together, in how many days will they finish it?", ans, [(a+b)/2, a+b, b-a],
             f"Work per day together: 1/{a} + 1/{b} = {a+b}/{a*b}. Time = {a*b}/{a+b} = {f(ans)} days.", "{} days")

def t_avg_add(r):
    n = r.choice([4, 5, 6, 9]); m = r.choice([30, 40, 50, 60]); k = r.choice([6, 8, 10]); x = m + k*(n+1)
    return T(f"The average of {n} numbers is {m}. When one more number is included the average becomes {m+k}. What is the new number?", x, [m+k, x-m, k*(n+1)],
             f"Old total = {n} × {m} = {n*m}. New total = {n+1} × {m+k} = {(n+1)*(m+k)}. New number = {(n+1)*(m+k)} − {n*m} = {x}.")

def t_age(r):
    a, b = r.choice([(2, 5), (3, 4), (1, 3), (2, 7), (3, 8)]); u = r.choice([4, 5, 6, 7]); y = r.choice([5, 10]); S = (a+b)*u + 2*y
    return T(f"The present ages of Rahul and Meera are in the ratio {a}:{b}. After {y} years the sum of their ages will be {S}. What is Rahul's present age?", a*u, [b*u, a*u+y, S//(a+b)*a],
             f"Sum now = {S} − 2 × {y} = {(a+b)*u}. One part = {(a+b)*u}/{a+b} = {u}. Rahul = {a} × {u} = {a*u} years.", "{} years")

def t_mixture(r):
    a, b = r.choice([(3, 1), (4, 1), (5, 1), (2, 1), (3, 2)]); x = (a+b)*r.choice([6, 8, 10]); milk = x*a//(a+b); water = x - milk
    add = milk - water
    return T(f"A {x}-litre mixture has milk and water in the ratio {a}:{b}. How much water must be added to make the ratio 1:1?", add, [water, milk, add*2],
             f"Milk = {milk} L, water = {water} L. For equal parts water must also be {milk} L, so add {milk} − {water} = {add} L.", "{} litres")

def t_train(r):
    v = r.choice([36, 54, 72, 90, 108]); t = r.choice([6, 8, 10, 12, 15]); L = v*5//18*t if (v*5) % 18 == 0 else None
    if L is None: return t_train(r)
    return T(f"A train running at {v} km/h passes a pole in {t} seconds. What is its length?", L, [v*t, L+v, L*18//5],
             f"Speed = {v} × 5/18 = {v*5//18} m/s. Length = speed × time = {v*5//18} × {t} = {L} m.", "{} m")

def t_markup(r):
    m, d = r.choice([(40, 10), (50, 20), (25, 20), (60, 25), (20, 10), (30, 10), (80, 25)])
    p = (100+m)*(100-d)/100 - 100
    return T(f"A shopkeeper marks goods {m}% above cost and then allows a discount of {d}%. What is his profit or loss percent?", p, [m-d, abs(p)+3, m*d/100],
             f"Take CP = 100. Marked = {100+m}. SP = {100+m} × {(100-d)/100} = {f(p+100)}. Profit = {f(p)}%." + (" (Not m − d = %d.)" % (m-d)), "{}%")

def t_cistern(r):
    a, b = r.choice([(10, 15), (12, 20), (6, 12), (20, 30)])
    ans = a*b/(b-a)
    return T(f"A tap fills a tank in {a} hours; a leak at the bottom empties the full tank in {b} hours. If both work together, in how many hours is the empty tank filled?", ans, [a+ (b-a)/2, b-a, a*b/(a+b)],
             f"Net rate = 1/{a} − 1/{b} = {b-a}/{a*b} of the tank per hour → time = {a*b}/{b-a} = {f(ans)} hours.", "{} hours")

def t_pct_of_pct(r):
    n = r.choice([2000, 4000, 5000, 8000]); p, q = r.choice([(20, 50), (40, 25), (10, 30), (50, 40), (25, 20)])
    ans = n*p*q/10000
    return T(f"In a town of {n} people, {p}% are children and {q}% of the children are girls. How many girls are there?", ans, [n*(p+q)/100, n*p/100, n*q/100],
             f"Children = {p}% of {n} = {f(n*p/100)}. Girls = {q}% of that = {f(ans)}.")

def t_speed_meet(r):
    a, b, t = r.choice([(40, 60, 3), (30, 50, 2), (45, 55, 4), (25, 35, 5), (60, 40, 2)])
    d = (a+b)*t
    return T(f"Two cars start at the same time from towns that are {d} km apart and drive towards each other at {a} km/h and {b} km/h. After how many hours do they meet?", t, [d/max(a, b), d/a, d/(b-a) if b != a else 1],
             f"They close the gap at {a} + {b} = {a+b} km/h, so time = {d}/{a+b} = {t} hours.", "{} hours")

TEMPLATES = [t_present, t_change, t_succ, t_profit, t_reverse_pct, t_ratio, t_si, t_ci, t_avgspeed, t_work, t_avg_add,
             t_age, t_mixture, t_train, t_markup, t_cistern, t_pct_of_pct, t_speed_meet]

def generate(n, seed=7):
    r = random.Random(seed); out = []; seen = set(); i = 0
    while len(out) < n and i < 5000:
        t = TEMPLATES[i % len(TEMPLATES)]; i += 1
        d = t(r)
        if d["q"] in seen: continue
        opts = [d["ans"]] + d["wrongs"]
        # unique options; top up if a distractor collided with the answer
        wr = []
        for w in d["wrongs"]:
            if w != d["ans"] and w not in wr: wr.append(w)
        k = 1
        while len(wr) < 3:
            try:
                base = float(d["ans"].replace("%", "").replace("₹", "").replace(",", "").split()[0]) ; 
            except Exception: break
            cand = d["ans"].replace(d["ans"].replace("%", "").replace("₹", "").replace(",", "").split()[0], f(base+k*max(1, round(base*0.1))))
            if cand != d["ans"] and cand not in wr: wr.append(cand)
            k += 1
        d["wrongs"] = wr[:3]; seen.add(d["q"]); out.append(d)
    return out
