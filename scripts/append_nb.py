import json

with open('data_processing.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Data Cleaning\n",
            "We need to clean the `price` column (removing the `$` sign and converting to float), handle NaN values in important columns, and drop listings that do not make sense (e.g., price = 0, or extreme outliers)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Price comes as a string with '$' and ','. Let's clean it.\n",
            "listings_df['price'] = listings_df['price'].astype(str).replace({'\\\\$': '', ',': ''}, regex=True).astype(float)\n",
            "\n",
            "# Drop rows where price is missing or 0\n",
            "listings_df = listings_df.dropna(subset=['price'])\n",
            "listings_df = listings_df[listings_df['price'] > 0]\n",
            "\n",
            "# Handle other missing values: reviews_per_month to 0\n",
            "listings_df['reviews_per_month'] = listings_df['reviews_per_month'].fillna(0)\n",
            "\n",
            "# Drop irrelevant columns or columns with mostly nulls\n",
            "columns_to_drop = ['neighbourhood_group', 'license']\n",
            "listings_df = listings_df.drop(columns=columns_to_drop, errors='ignore')\n",
            "\n",
            "print(f\"Cleaned dataset shape: {listings_df.shape}\")\n",
            "listings_df.describe()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Exploratory Data Analysis\n",
            "Let's check the price distribution and the top neighborhoods with the most Airbnbs. We'll also spatial join with the GeoJSON to view the map."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Price Distribution (Filtered to < 1000 for visibility)\n",
            "plt.figure(figsize=(10, 6))\n",
            "sns.histplot(listings_df[listings_df['price'] < 1000]['price'], bins=50, kde=True, color='teal')\n",
            "plt.title('Distribution of Airbnb Prices in Milan (Under 1000€)')\n",
            "plt.xlabel('Price (€)')\n",
            "plt.ylabel('Count')\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Top 10 Neighbourhoods by number of listings\n",
            "top_neighbourhoods = listings_df['neighbourhood'].value_counts().head(10)\n",
            "\n",
            "plt.figure(figsize=(12, 6))\n",
            "sns.barplot(y=top_neighbourhoods.index, x=top_neighbourhoods.values, palette='viridis')\n",
            "plt.title('Top 10 Milan Neighbourhoods by Number of Airbnb Listings')\n",
            "plt.xlabel('Number of Listings')\n",
            "plt.ylabel('Neighbourhood')\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Calculate average price per neighbourhood and merge with GeoPandas\n",
            "avg_price_df = listings_df.groupby('neighbourhood')['price'].mean().reset_index()\n",
            "avg_price_df.columns = ['neighbourhood', 'avg_price']\n",
            "\n",
            "# Assume neighborhoods_gdf has a 'neighborhood' or 'NIL_NM' column depending on the Milan open data structure.\n",
            "# Inside Airbnb geojson usually uses 'neighbourhood'\n",
            "map_df = neighborhoods_gdf.merge(avg_price_df, on='neighbourhood', how='left')\n",
            "\n",
            "fig, ax = plt.subplots(1, 1, figsize=(10, 10))\n",
            "map_df.plot(column='avg_price', cmap='OrRd', ax=ax, legend=True, \n",
            "            legend_kwds={'label': \"Average Price (€)\", 'orientation': \"vertical\"},\n",
            "            missing_kwds={\"color\": \"lightgrey\", \"label\": \"No Data\"})\n",
            "plt.title('Average Airbnb Price per Neighbourhood in Milan')\n",
            "ax.set_axis_off()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Target Question check: Professional vs Casual Hosts\n",
            "Let's see the split of hosts with a single listing vs hosts with multiple listings."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Count hosts\n",
            "hosts_listings_count = listings_df[['host_id', 'calculated_host_listings_count']].drop_duplicates()\n",
            "\n",
            "def categorize_host(listings_count):\n",
            "    if listings_count == 1:\n",
            "        return 'Single-listing (Casual)'\n",
            "    elif listings_count <= 3:\n",
            "        return '2-3 listings'\n",
            "    else:\n",
            "        return '4+ listings (Professional)'\n",
            "\n",
            "hosts_listings_count['host_type'] = hosts_listings_count['calculated_host_listings_count'].apply(categorize_host)\n",
            "\n",
            "host_counts = hosts_listings_count['host_type'].value_counts()\n",
            "\n",
            "plt.figure(figsize=(8, 8))\n",
            "plt.pie(host_counts, labels=host_counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'], startangle=90)\n",
            "plt.title('Proportion of Host Types in Milan')\n",
            "plt.show()"
        ]
    }
]

nb['cells'].extend(new_cells)

with open('data_processing.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
