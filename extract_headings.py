import os, sys, json, re
import fitz                             # PyMuPDF
import pandas as pd
import joblib

# 1) Load model & encoder
model = joblib.load('heading_classifier.pkl')
le    = joblib.load('label_encoder.pkl')

def extract_lines_with_features(pdf_path):
    doc = fitz.open(pdf_path)
    all_lines = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = " ".join(span["text"] for span in line["spans"]).strip()
                if not text: continue
                span = line["spans"][0]
                all_lines.append({
                    "text":       text,
                    "font_size":  round(span["size"], 1),
                    "bold":       1 if span["flags"] & 2 else 0,
                    "x":          round(span["bbox"][0], 1),
                    "y":          round(span["bbox"][1], 1),
                    "page":       page_num + 1    # ensure 1‑based
                })
    doc.close()
    return all_lines

def extract_title_from_page1(lines):
    p1 = [l for l in lines if l["page"] == 1]
    if not p1:
        # fallback: first line of document
        return lines[0]["text"] if lines else "Untitled"
    max_fs = max(l["font_size"] for l in p1)
    # take any block ≥ 85% of max instead of 90%
    cands = [l for l in p1 if l["font_size"] >= 0.85 * max_fs]
    if not cands:
        return lines[0]["text"]
    cands.sort(key=lambda l: (l["y"], l["x"]))
    return " ".join(l["text"] for l in cands)

def classify_and_build_outline(lines):
    # 1) Predict all levels using basic features
    feats = ["font_size", "bold", "x", "y", "page"]
    preds = []
    for L in lines:
        row = [L[f] for f in feats]
        lvl = le.inverse_transform([model.predict([row])[0]])[0]
        preds.append({**L, "level": lvl})

    # 2) Title with fallback
    title = extract_title_from_page1(lines)

    # 3) Outline filter: include H1–H4
    outline = [p for p in preds if p["level"] in ("H1","H2","H3","H4")]

    # 4) Sort by page & y, then drop extras
    outline.sort(key=lambda r: (r["page"], r["y"]))
    clean = [{"level":o["level"], "text":o["text"], "page":o["page"]} for o in outline]

    # 5) If outline is empty, try:
    #     any numbered lines as H1
    if not clean:
        for p in lines:
            if re.match(r'^\d+(\.\d+)*\s', p["text"]):
                clean.append({"level":"H1","text":p["text"],"page":p["page"]})
        clean = clean[:1]  # just the first
    return title, clean

def process_pdf(inp, outp):
    lines = extract_lines_with_features(inp)
    title, outline = classify_and_build_outline(lines)
    with open(outp, "w") as f:
        json.dump({"title": title, "outline": outline}, f, indent=2)
    print(f"Wrote {outp}")

if __name__ == "__main__":
    if len(sys.argv)==3:
        process_pdf(sys.argv[1], sys.argv[2])
        sys.exit()
    IN, OUT = "input","output"
    os.makedirs(OUT, exist_ok=True)
    for fn in sorted(os.listdir(IN)):
        if fn.lower().endswith(".pdf"):
            process_pdf(os.path.join(IN,fn),
                        os.path.join(OUT,fn[:-4]+".json"))
