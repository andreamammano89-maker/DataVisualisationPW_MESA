# =============================================================================
# AIRBNB PROFESSIONALIZATION ANALYSIS
# Rome vs Copenhagen — Data Cleaning & EDA
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# =============================================================================
# 0. SETUP
# =============================================================================

# Metti i tuoi CSV nella stessa cartella di questo script, oppure cambia i path
PATH_ROME = "listings_rome.csv"
PATH_CPH  = "listings_copenhagen.csv"

# Palette coerente per tutto il progetto
PALETTE = {"Casual": "#4C9BE8", "Semi-Pro": "#F5A623", "Professional": "#E84C4C"}
CITY_COLORS = {"Rome": "#E84C4C", "Copenhagen": "#4C9BE8"}

# =============================================================================
# 1. CARICAMENTO
# =============================================================================

rome = pd.read_csv(PATH_ROME, low_memory=False)
cph  = pd.read_csv(PATH_CPH,  low_memory=False)

rome["city"] = "Rome"
cph["city"]  = "Copenhagen"

print(f"Rome:       {len(rome):,} listings, {rome.shape[1]} colonne")
print(f"Copenhagen: {len(cph):,} listings, {cph.shape[1]} colonne")

# =============================================================================
# 2. SELEZIONE COLONNE UTILI
# =============================================================================
# Tieni solo ciò che serve — riduce rumore e memoria

COLS = [
    "id", "city",
    "host_id", "host_name", "host_since",
    "host_listings_count",          # quanti listing ha quell'host in totale
    "host_is_superhost",
    "neighbourhood_cleansed",       # quartiere normalizzato
    "latitude", "longitude",
    "room_type",
    "price",                        # stringa tipo "$120.00" → va pulita
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "calculated_host_listings_count",  # calcolato da Inside Airbnb, più affidabile
    "availability_365",
    "last_review",
]

# Tieni solo le colonne che esistono in entrambi i dataset
common_cols = [c for c in COLS if c in rome.columns and c in cph.columns]
rome = rome[common_cols].copy()
cph  = cph[common_cols].copy()

# Unisci in un unico dataframe
df = pd.concat([rome, cph], ignore_index=True)
print(f"\nDataset unificato: {len(df):,} righe")

# =============================================================================
# 3. PULIZIA
# =============================================================================

# --- 3a. Prezzo ---
# Il campo price arriva come "$1,234.00" — rimuovi simboli e converti
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace(r"[\$,]", "", regex=True)
    .str.strip()
    .replace("", np.nan)
    .astype(float)
)

# Rimuovi outlier di prezzo: sotto $5 o sopra $2000 sono quasi sempre errori
price_before = len(df)
df = df[(df["price"] >= 5) & (df["price"] <= 2000)]
print(f"Rimossi {price_before - len(df)} listing con prezzo anomalo")

# --- 3b. Valori mancanti ---
print("\nValori mancanti (%):")
missing = df.isnull().mean().mul(100).round(1).sort_values(ascending=False)
print(missing[missing > 0])

# reviews_per_month mancante = listing senza recensioni → imputa 0
df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

# host_listings_count: usa calculated_host_listings_count se disponibile
if "calculated_host_listings_count" in df.columns:
    df["host_listings_count"] = df["calculated_host_listings_count"].fillna(
        df["host_listings_count"]
    )

df["host_listings_count"] = df["host_listings_count"].fillna(1).astype(int)

# --- 3c. host_is_superhost ---
df["host_is_superhost"] = df["host_is_superhost"].map({"t": True, "f": False})

# --- 3d. Duplicati ---
dupes = df.duplicated(subset=["id", "city"]).sum()
print(f"\nDuplicati rimossi: {dupes}")
df = df.drop_duplicates(subset=["id", "city"])

# =============================================================================
# 4. FEATURE ENGINEERING
# =============================================================================

# --- 4a. Segmentazione host (questa è la colonna CORE del progetto) ---
# Soglia di default: 1 = Casual, 2-5 = Semi-Pro, >5 = Professional
# Il JS simulator permetterà di cambiarla interattivamente

def segment_host(n, threshold_pro=5, threshold_semi=2):
    if n < threshold_semi:
        return "Casual"
    elif n <= threshold_pro:
        return "Semi-Pro"
    else:
        return "Professional"

df["host_segment"] = df["host_listings_count"].apply(segment_host)

# --- 4b. Stima revenue mensile (Inside Airbnb methodology) ---
# IMPORTANTE: questa è una STIMA, non dati reali — dichiaralo nel paper
# Formula: price × minimum_nights × reviews_per_month × fattore_occupancy
# Inside Airbnb usa 0.72 come occupancy assumption (72%)
OCCUPANCY_FACTOR = 0.72
df["estimated_monthly_revenue"] = (
    df["price"] * df["minimum_nights"] * df["reviews_per_month"] * OCCUPANCY_FACTOR
).clip(upper=50000)  # cap a 50k/mese per rimuovere outlier estremi

# --- 4c. Flag: listing probabilmente non residenziale ---
# Alta disponibilità + molte recensioni → uso prevalentemente turistico
df["likely_commercial"] = (
    (df["availability_365"] > 180) &
    (df["reviews_per_month"] > 1)
).astype(int)

# =============================================================================
# 5. STATISTICHE DESCRITTIVE
# =============================================================================

print("\n" + "="*60)
print("STATISTICHE PER CITTÀ")
print("="*60)

summary = df.groupby("city").agg(
    total_listings       = ("id", "count"),
    unique_hosts         = ("host_id", "nunique"),
    avg_listings_per_host= ("host_listings_count", "mean"),
    median_price         = ("price", "median"),
    pct_professional     = ("host_segment", lambda x: (x == "Professional").mean() * 100),
    pct_casual           = ("host_segment", lambda x: (x == "Casual").mean() * 100),
).round(2)

print(summary.T)

# Quota di mercato dei Professional (listing)
print("\n--- Quota listing dei Professional ---")
mkt = df.groupby(["city", "host_segment"]).size().div(
    df.groupby("city").size(), level="city"
).mul(100).round(1)
print(mkt)

# =============================================================================
# 6. VISUALIZZAZIONI (per il paper — white/black hat e EDA)
# =============================================================================

# Stile coerente per tutto il progetto
plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})

# --- FIG 1: Distribuzione listing per host (log scale) ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=False)

for ax, (city, group) in zip(axes, df.groupby("city")):
    host_counts = group.groupby("host_id")["host_listings_count"].first()
    ax.hist(host_counts, bins=50, color=CITY_COLORS[city], edgecolor="white", linewidth=0.5)
    ax.set_yscale("log")
    ax.set_title(f"{city}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Numero di listing per host")
    ax.set_ylabel("Numero di host (log)")
    ax.axvline(5, color="gray", linestyle="--", linewidth=1, label="Soglia Professional (5)")
    ax.legend(fontsize=8)

fig.suptitle("Distribuzione listing per host — mercato fortemente skewed", fontsize=14)
plt.tight_layout()
plt.savefig("fig1_distribution.png", bbox_inches="tight")
plt.show()
print("Salvato: fig1_distribution.png")

# --- FIG 2: Composizione host per città (stacked bar) ---
seg_pct = (
    df.groupby(["city", "host_segment"])
    .size()
    .div(df.groupby("city").size(), level="city")
    .mul(100)
    .unstack("host_segment")
    .reindex(columns=["Casual", "Semi-Pro", "Professional"])
)

fig, ax = plt.subplots(figsize=(7, 4))
seg_pct.plot(kind="bar", stacked=True, color=list(PALETTE.values()), ax=ax, edgecolor="white")
ax.set_xlabel("")
ax.set_ylabel("% degli host")
ax.set_title("Segmentazione host per città", fontsize=13, fontweight="bold")
ax.legend(title="Categoria host", bbox_to_anchor=(1.02, 1))
ax.set_xticklabels(seg_pct.index, rotation=0)
plt.tight_layout()
plt.savefig("fig2_host_segments.png", bbox_inches="tight")
plt.show()
print("Salvato: fig2_host_segments.png")

# --- FIG 3: Concentrazione mercato — top 10% host vs resto ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, (city, group) in zip(axes, df.groupby("city")):
    host_listings = (
        group.groupby("host_id")["id"]
        .count()
        .sort_values(ascending=False)
        .reset_index()
    )
    host_listings["cumulative_share"] = (
        host_listings["id"].cumsum() / host_listings["id"].sum() * 100
    )
    host_listings["host_rank_pct"] = (
        np.arange(1, len(host_listings) + 1) / len(host_listings) * 100
    )

    ax.plot(
        host_listings["host_rank_pct"],
        host_listings["cumulative_share"],
        color=CITY_COLORS[city], linewidth=2
    )
    ax.plot([0, 100], [0, 100], color="gray", linestyle="--", linewidth=1, label="Distribuzione perfetta")

    # Evidenzia top 10%
    top10 = host_listings[host_listings["host_rank_pct"] <= 10]["cumulative_share"].max()
    ax.axvline(10, color="red", linestyle=":", linewidth=1)
    ax.axhline(top10, color="red", linestyle=":", linewidth=1)
    ax.annotate(
        f"Top 10% host\ncontrolla {top10:.0f}% listing",
        xy=(10, top10), xytext=(30, top10 - 20),
        arrowprops=dict(arrowstyle="->", color="red"),
        fontsize=9, color="red"
    )

    ax.set_title(f"{city} — Curva di Lorenz (listing)", fontsize=12, fontweight="bold")
    ax.set_xlabel("% host (dal più grande)")
    ax.set_ylabel("% listing cumulativa")
    ax.legend(fontsize=8)

fig.suptitle("Concentrazione del mercato: pochi host, molti listing", fontsize=14)
plt.tight_layout()
plt.savefig("fig3_lorenz.png", bbox_inches="tight")
plt.show()
print("Salvato: fig3_lorenz.png")

# --- FIG 4 (WHITE HAT): Revenue mediana per segmento ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, (city, group) in zip(axes, df.groupby("city")):
    med_rev = group.groupby("host_segment")["estimated_monthly_revenue"].median().reindex(
        ["Casual", "Semi-Pro", "Professional"]
    )
    bars = ax.bar(med_rev.index, med_rev.values,
                  color=[PALETTE[s] for s in med_rev.index], edgecolor="white")
    ax.set_title(f"{city} — Revenue mediana per segmento\n(WHITE HAT: mediana)", fontsize=11)
    ax.set_ylabel("Revenue mensile stimata (€)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
    for bar, val in zip(bars, med_rev.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f"€{val:,.0f}", ha="center", va="bottom", fontsize=9)

fig.suptitle("WHITE HAT — Distribuzione reale: la mediana racconta la storia vera", fontsize=13)
plt.tight_layout()
plt.savefig("fig4_whitehat_revenue.png", bbox_inches="tight")
plt.show()
print("Salvato: fig4_whitehat_revenue.png")

# --- FIG 5 (BLACK HAT): Revenue MEDIA — manipolazione ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, (city, group) in zip(axes, df.groupby("city")):
    mean_rev = group.groupby("host_segment")["estimated_monthly_revenue"].mean().reindex(
        ["Casual", "Semi-Pro", "Professional"]
    )
    bars = ax.bar(mean_rev.index, mean_rev.values,
                  color=[PALETTE[s] for s in mean_rev.index], edgecolor="white")
    ax.set_title(f"{city} — Revenue MEDIA per segmento\n(BLACK HAT: gonfiata dagli outlier)", fontsize=11)
    ax.set_ylabel("Revenue mensile stimata (€)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
    for bar, val in zip(bars, mean_rev.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f"€{val:,.0f}", ha="center", va="bottom", fontsize=9)

fig.suptitle("BLACK HAT — Usare la media crea l'illusione che tutti guadagnino molto", fontsize=13,
             color="#cc0000")
plt.tight_layout()
plt.savefig("fig5_blackhat_revenue.png", bbox_inches="tight")
plt.show()
print("Salvato: fig5_blackhat_revenue.png")

# =============================================================================
# 7. EXPORT PER TABLEAU
# =============================================================================

# CSV pulito unificato — importalo direttamente in Tableau
df.to_csv("airbnb_clean_combined.csv", index=False)
print(f"\nExport Tableau: airbnb_clean_combined.csv ({len(df):,} righe)")

# CSV aggregato per host — utile per scatter plot e analisi concentrazione
host_agg = df.groupby(["host_id", "city"]).agg(
    host_name         = ("host_name", "first"),
    host_segment      = ("host_segment", "first"),
    n_listings        = ("id", "count"),
    avg_price         = ("price", "mean"),
    total_est_revenue = ("estimated_monthly_revenue", "sum"),
    avg_availability  = ("availability_365", "mean"),
    n_reviews         = ("number_of_reviews", "sum"),
).round(2).reset_index()

host_agg.to_csv("airbnb_host_aggregated.csv", index=False)
print(f"Export Tableau: airbnb_host_aggregated.csv ({len(host_agg):,} host unici)")

print("\n✅ Pipeline completata.")