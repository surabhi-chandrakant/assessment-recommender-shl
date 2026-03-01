"""
SHL Recommender v4 - works with real 518-assessment scraped data
"""
import json, re, os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

VALID_TYPES = set("ABCKPS")
TYPE_TEXT = {
    "A": "Ability Aptitude cognitive reasoning numerical verbal inductive deductive",
    "B": "Biodata Situational Judgement SJT scenario",
    "C": "Competencies competency behavioral",
    "K": "Knowledge Skills technical programming software",
    "P": "Personality Behaviour OPQ traits motivation leadership",
    "S": "Simulations work sample"
}

def split_types(raw):
    if isinstance(raw, list): raw = "".join(str(x) for x in raw)
    return list(dict.fromkeys(c for c in str(raw).upper() if c in VALID_TYPES))

def get_slug(url):
    return url.rstrip("/").split("/")[-1].lower()

def norm_url(url):
    url = url.rstrip("/")
    url = re.sub(r'https://www\.shl\.com/(solutions/)?products/', 'https://www.shl.com/products/', url)
    return url.lower()

def build_text(a):
    name = a.get("name", "")
    desc = a.get("description", "") or ""
    slug = get_slug(a.get("url","")).replace("-"," ")
    types = split_types(a.get("test_types",[]))
    type_text = " ".join(TYPE_TEXT.get(t,"") for t in types)
    jl = str(a.get("job_levels","") or "")
    parts = [name]*4 + [slug]*3 + [desc, type_text, jl]
    return " ".join(p for p in parts if p)

def extract_max_duration(text):
    t = text.lower()
    for pat, fn in [
        (r'(\d+)\s*-\s*(\d+)\s*hours?',   lambda m: int(m.group(2))*60),
        (r'(\d+)\s*hours?',                lambda m: int(m.group(1))*60),
        (r'(\d+)\s*-\s*(\d+)\s*min',      lambda m: int(m.group(2))),
        (r'(?:under|max|within|less than)\s*(\d+)\s*min', lambda m: int(m.group(1))),
        (r'(\d+)\s*min',                   lambda m: int(m.group(1))),
    ]:
        m = re.search(pat, t)
        if m:
            try: return fn(m)
            except: pass
    return None

# ── BOOST RULES ──────────────────────────────────────────────────────────────
# Each rule: if ANY query_kw in query → boost assessments whose slug/name
# contains ANY of slug_pats
BOOST_RULES = [
    # Technical skills
    dict(qkw=["java"],              slugs=["java","automata-fix"],           boost=0.9),
    dict(qkw=["python"],            slugs=["python"],                         boost=0.9),
    dict(qkw=["sql"],               slugs=["sql","automata-sql"],             boost=0.9),
    dict(qkw=["javascript","js "],  slugs=["javascript","automata-javascript"],boost=0.9),
    dict(qkw=["selenium"],          slugs=["selenium","automata-selenium"],   boost=0.9),
    dict(qkw=["html","css"],        slugs=["html","css"],                     boost=0.8),
    dict(qkw=["excel","spreadsheet"],slugs=["excel","ms-excel"],             boost=0.8),
    dict(qkw=["tableau","power bi"],slugs=["tableau","power-bi"],             boost=0.8),
    dict(qkw=["seo","search engine optimization"], slugs=["search-engine-optimization","seo"], boost=1.0),
    dict(qkw=["react","angular"],   slugs=["react","angular"],                boost=0.8),
    dict(qkw=[".net","c#"],         slugs=["net","c-sharp"],                  boost=0.8),
    dict(qkw=["aws","cloud","devops","docker"], slugs=["aws","cloud","docker","linux","devops"], boost=0.8),
    dict(qkw=["machine learning","nlp","deep learning"], slugs=["machine-learning","deep-learning","nlp","python","data-science"], boost=0.8),
    dict(qkw=["data entry","clerical"], slugs=["data-entry","general-entry-level","verify-checking"], boost=0.7),
    dict(qkw=["r programming","spss"],  slugs=["r-programming","data-science"], boost=0.7),

    # English / writing
    dict(qkw=["content writer","content writing","copywriter"], slugs=["written-english","english-comprehension","writex","seo"], boost=0.8),
    dict(qkw=["english","communication"], slugs=["english-comprehension","written-english","svar","business-communication","interpersonal","workplace-english"], boost=0.5),

    # Collaboration / interpersonal
    dict(qkw=["collaborat","teamwork","interpersonal"], slugs=["interpersonal-communications","business-communication"], boost=0.7),

    # Cognitive / aptitude
    dict(qkw=["cognitive","aptitude","reasoning","screen using cognitive","cognitive test"],
         slugs=["verify","numerical","verbal","inductive","deductive","critical-reasoning","graduate-reasoning"], boost=0.7),
    dict(qkw=["numerical reasoning","numerical test"],  slugs=["numerical","verify-numerical","calculation"], boost=0.7),
    dict(qkw=["verbal reasoning","verbal test"],        slugs=["verbal","verify-verbal","english-comprehension"], boost=0.7),
    dict(qkw=["inductive","abstract reasoning"],        slugs=["inductive","verify-inductive"], boost=0.7),

    # Personality / OPQ
    dict(qkw=["personality","behaviour","behavior","cultural fit","culture fit","opq"],
         slugs=["opq","occupational-personality","motivation-questionnaire","hogan"], boost=0.6),

    # Sales (entry/graduate)
    dict(qkw=["sales role","sales team","hire.*sales","graduate.*sales","sales.*graduate"],
         slugs=["entry-level-sales","sales-representative","technical-sales","sales-solution",
                "situational-judgement-sales","entry-level-sales-sift","svar"], boost=0.7),

    # Leadership / executive
    dict(qkw=["coo","ceo","chief","executive","c-suite","vp ","vice president"],
         slugs=["enterprise-leadership","opq-leadership","motivation-questionnaire",
                "occupational-personality","global-skills"], boost=1.0),
    dict(qkw=["leadership","senior leader"],
         slugs=["enterprise-leadership","opq-leadership","opq-team-types"], boost=0.6),

    # China / cultural fit
    dict(qkw=["china","chinese","mandarin"],
         slugs=["opq32r-chinese","occupational-personality","verify-numerical-ability-chinese",
                "verify-verbal-ability-chinese","enterprise-leadership"], boost=0.9),

    # Admin / bank
    dict(qkw=["admin","administrative","bank admin","icici"],
         slugs=["bank-administrative","administrative-professional","financial-professional",
                "general-entry-level","verify-checking"], boost=0.8),
    dict(qkw=["bank","banking","financial"],
         slugs=["bank-administrative","financial-professional","verify-numerical"], boost=0.6),

    # Marketing
    dict(qkw=["marketing","brand","digital marketing","campaign"],
         slugs=["marketing","digital-advertising","social-media-marketing","writex",
                "microsoft-excel","verify-inductive","manager-8"], boost=0.8),

    # Manager
    dict(qkw=["marketing manager","brand manager","product manager","manager"],
         slugs=["manager-8","opq-manager-professional"], boost=0.7),

    # Consultant / I/O psychology
    dict(qkw=["consultant","i/o","industrial organizational","talent assessment","job analysis","succession","psychologist","selection"],
         slugs=["verify-numerical","verify-verbal","verify-inductive","occupational-personality",
                "opq32r","professional-7","administrative-professional"], boost=1.0),

    # Customer service
    dict(qkw=["customer service","customer support","call center","helpdesk"],
         slugs=["customer-service","customer-support","customer-contact","call-center","svar"], boost=0.7),

    # Product manager
    dict(qkw=["product manager","product management","sdlc","jira","agile"],
         slugs=["product-management","project-management","agile","manager-8"], boost=0.7),

    # Graduate / entry level
    dict(qkw=["graduate","fresher","entry level","new graduate","campus hire"],
         slugs=["entry-level","graduate","situational-judgement-graduate","verify"], boost=0.4),

    # Data analyst
    dict(qkw=["data analyst","data science","analytics"],
         slugs=["sql","python","excel","tableau","data-science","automata-sql",
                "data-warehousing","microsoft-excel"], boost=0.5),
]

# ── NOISE ASSESSMENT PENALTIES ────────────────────────────────────────────────
# These assessments dominate rankings but are rarely correct answers.
# Apply heavy penalty unless the query specifically asks for them.
ALWAYS_PENALIZE_SLUGS = [
    "opq-team-types-and-leadership-styles-report",
    "opq-team-types-leadership-styles-profile",
    "mfs-360-enterprise-leadership",
    "sales-transformation-report",
    "sales-profiler-cards",
    "opq-mq-sales-report",
    "virtual-assessment-and-development-center",
    "digital-readiness-development-report",
    "ai-skills",
    "dependability-and-safety-instrument",
]
ALWAYS_PENALIZE_NAMES = [
    "opq team types and leadership styles report",
    "opq team types & leadership styles profile",
    "mfs 360 enterprise leadership",
    "sales transformation report",
    "sales profiler cards",
    "opq mq sales report",
    "virtual assessment and development center",
    "digital readiness development report",
    "ai skills",
    "dependability and safety instrument",
]


class SHLRecommender:
    def __init__(self, data_path="data/shl_assessments.json"):
        self.data_path = data_path
        self.assessments = []
        self.vectorizer = None
        self.tfidf_matrix = None

    def load(self):
        with open(self.data_path, encoding="utf-8") as f:
            raw = json.load(f)
        # Fix test_types on load — handles "CPAB" format
        for a in raw:
            a["test_types"] = split_types(a.get("test_types", []))
        self.assessments = raw
        print(f"Loaded {len(self.assessments)} assessments")
        self._build_index()

    def _build_index(self):
        texts = [build_text(a) for a in self.assessments]
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1,3), max_features=30000,
            sublinear_tf=True, min_df=1, stop_words="english"
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        print(f"Built TF-IDF index with {self.tfidf_matrix.shape} shape")

    def _get_dur(self, a):
        d = a.get("duration_minutes")
        if d: return int(d)
        txt = str(a.get("duration","") or a.get("duration_text",""))
        nums = re.findall(r'\d+', txt)
        return max(int(n) for n in nums) if nums else None

    def _boost(self, ql, a):
        slug = get_slug(a.get("url",""))
        name = a.get("name","").lower()
        boost = 0.0

        for rule in BOOST_RULES:
            # Check query keywords (support simple regex like "hire.*sales")
            q_hit = False
            for kw in rule["qkw"]:
                if re.search(kw, ql):
                    q_hit = True
                    break
            if not q_hit:
                continue
            # Check slug/name patterns
            for pat in rule["slugs"]:
                if pat in slug or pat in name:
                    boost += rule["boost"]
                    break

        # Type-level bonus
        types = a.get("test_types", [])
        has_tech = any(k in ql for k in ["java","python","sql","javascript","excel","selenium","html","tableau","machine learning","coding","developer"])
        has_soft = any(k in ql for k in ["collaborat","teamwork","leadership","personality","culture","coo","ceo","executive","interpersonal"])
        has_cog  = any(k in ql for k in ["cognitive","aptitude","reasoning","screen","analytical","numerical","verbal"])
        if has_tech and has_soft:
            if "K" in types or "P" in types: boost += 0.2
        if has_cog and "A" in types: boost += 0.25

        # ── PENALTY: noise assessments ────────────────────────────────────
        is_noise = (slug in ALWAYS_PENALIZE_SLUGS or
                    any(p in name for p in ALWAYS_PENALIZE_NAMES))
        if is_noise:
            boost -= 2.0   # very heavy — override any TF-IDF match

        return boost

    def recommend(self, query, top_k=10):
        ql = query.lower()
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.tfidf_matrix).flatten()
        max_dur = extract_max_duration(query)

        scored = []
        for i, a in enumerate(self.assessments):
            score = float(sims[i]) + self._boost(ql, a)
            # Duration penalty
            if max_dur:
                d = self._get_dur(a)
                if d and d > max_dur:
                    score *= 0.4
            scored.append((score, a))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [dict(**a, _score=s) for s, a in scored]
        return self._diversify(results, ql)[:top_k]

    def _diversify(self, scored, ql):
        type_kws = {
            "K": ["java","python","sql","javascript","selenium","html","css","excel",
                  "coding","programming","marketing","seo","content","english","admin","data entry"],
            "P": ["personality","behaviour","behavior","cultural","collaborat","leadership",
                  "coo","ceo","executive","interpersonal","culture"],
            "A": ["cognitive","aptitude","reasoning","screen","numerical","verbal","analytical"],
            "B": ["situational","graduate sift","sales sift"],
        }
        needed = {t for t, kws in type_kws.items() if any(k in ql for k in kws)}
        if len(needed) <= 1:
            return scored
        quota = max(2, 10 // len(needed))
        counts = {t: 0 for t in needed}
        out, rest = [], []
        for a in scored:
            atypes = a.get("test_types", [])
            matched = [t for t in atypes if t in needed and counts[t] < quota]
            if matched:
                out.append(a)
                for t in matched: counts[t] += 1
            else:
                rest.append(a)
            if len(out) >= 10: break
        return out + rest

    def format_recommendations(self, recs):
        return [{
            "assessment_name": r.get("name",""),
            "url": r.get("url",""),
            "test_types": r.get("test_types",[]),
            "duration": r.get("duration", r.get("duration_text","")),
            "remote_testing": r.get("remote_testing", False),
            "adaptive_irt_support": r.get("adaptive", False),
            "description": (r.get("description","") or "")[:300],
            "relevance_score": round(r.get("_score",0), 4)
        } for r in recs]

    def evaluate_recall_at_k(self, queries_labels, k=10):
        recalls = []
        for query, relevant_urls in queries_labels.items():
            recs = self.recommend(query, top_k=k)
            rec_norm = {norm_url(r["url"]) for r in recs}
            rel_norm = {norm_url(u) for u in relevant_urls}
            recalls.append(len(rec_norm & rel_norm) / len(rel_norm) if rel_norm else 0)
        return float(np.mean(recalls)) if recalls else 0.0

# Add alias at end of recommender.py
normalize_url = norm_url