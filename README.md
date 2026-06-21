# AI-Driven Parking Intelligence for Congestion-Aware Enforcement



**"How can AI-driven parking intelligence detect illegal parking hotspots and quantify their impact on traffic flow to enable targeted enforcement?"**

---

# Dataset Description

The dataset consists of historical parking violation records collected across Bengaluru.

Key attributes used in the analysis include:

* Latitude
* Longitude
* Violation Type
* Created Timestamp
* Junction Name
* Police Station

Some of parking-related violations present in the dataset include:

* Wrong Parking
* No Parking
* Double Parking
* Parking in a Main Road
* Parking on Footpath
* Parking Near Road Crossing
* Parking Near Bus Stop / School / Hospital

---

# Methodology

## Step 1: Data Cleaning and Preprocessing

The violation type field contained multiple violations stored as string representations of lists.

Example:

```text
["WRONG PARKING","PARKING IN A MAIN ROAD"]
```

These entries were converted into Python lists for easier processing and analysis.

We then filtered the dataset to retain only parking-related violations, removing records unrelated to parking congestion.

---

## Step 2: Spatial Hotspot Detection

To identify recurring illegal parking zones, geographical clustering was performed using DBSCAN (Density-Based Spatial Clustering of Applications with Noise).

### Why DBSCAN?

Unlike K-Means, DBSCAN:

* Does not require specifying the number of clusters beforehand.
* Can detect irregularly shaped hotspots.
* Naturally identifies noise points.
* Works well with spatial coordinates.

Input Features:

* Latitude
* Longitude

Output:

Each violation record was assigned:

* A hotspot cluster ID
* Or a noise label (-1)

This allowed us to automatically identify high-density parking violation regions across the city.

---

## Step 3: Hotspot Ranking

After clustering, each hotspot was ranked based on the total number of parking violations occurring within it.

For every hotspot, we calculated:

* Number of violations
* Geographic center coordinates

This produced a city-wide hotspot map highlighting areas with recurring parking violations.

---

## Step 4: Temporal Analysis

Understanding when violations occur is equally important as understanding where they occur.

Timestamps were converted to Indian Standard Time (IST) and the hour of occurrence was extracted.

For every hotspot, we determined:

* Peak violation hour
* Most active enforcement window

This enables authorities to deploy personnel during the hours when violations are most likely to occur.

Example:

| Hotspot   | Peak Hour   |
| --------- | ----------- |
| Cluster 2 | 18:00–19:00 |
| Cluster 3 | 09:00–10:00 |

---

## Step 5: Congestion Severity Feature Engineering

To quantify how disruptive a hotspot is, we engineered several congestion-related features.

### 1. Total Violations

Measures hotspot size and frequency of offenses.

Higher value indicates larger enforcement demand.

---

### 2. Main Road Ratio

Percentage of violations involving:

* Parking in a Main Road

Vehicles parked on main roads directly reduce roadway capacity and slow traffic movement.

---

### 3. Double Parking Ratio

Percentage of violations involving:

* Double Parking

Double parking often blocks entire lanes and causes significant bottlenecks.

---

### 4. Junction Ratio

Percentage of violations occurring near intersections and junctions.

Parking near junctions disrupts:

* Turning movements
* Signal efficiency
* Intersection throughput

This was found to be the strongest contributor to congestion severity.

---

### 5. Peak Hour Concentration

Measures how concentrated violations are during a hotspot's busiest hour.

Higher concentration indicates recurring congestion bursts.

---

### 6. Active Days

Measures how frequently the hotspot reappears across multiple days.

This distinguishes recurring problem areas from one-time incidents.

---

# Learning Congestion Severity

Rather than assigning arbitrary weights, we used a Random Forest model to estimate the relative importance of hotspot characteristics.

The model identified the following feature importance values:

| Feature              | Importance |
| -------------------- | ---------- |
| Junction Ratio       | 70.1%      |
| Main Road Ratio      | 20.1%      |
| Double Parking Ratio | 7.9%       |
| Peak Fraction        | 0.9%       |
| Active Days          | 0.9%       |

### Key Insight

Violations occurring near junctions were found to have the highest contribution toward congestion risk, followed by parking on major roads and double parking.

---

# Parking-Induced Congestion Risk Index (PICRI)

To prioritize enforcement, we developed a custom metric called:

## PICRI

(Parking-Induced Congestion Risk Index)

PICRI combines two dimensions:

### Exposure

Represents the scale of the problem.

Based on:

* Total violations within the hotspot

### Severity

Represents how disruptive the violations are.

Based on:

* Junction Ratio
* Main Road Ratio
* Double Parking Ratio
* Peak Hour Concentration
* Active Days

Severity is calculated using the learned feature importance values.

---

## Final Impact Score

The final hotspot priority score is calculated by combining:

* Exposure
* Severity

This score enables enforcement teams to identify:

* Which hotspots are most problematic
* When intervention is needed
* Which locations should be prioritized first

---

# Outputs Generated

The system produces:

### Hotspot Heatmap

Visual representation of illegal parking density across the city.

### Ranked Hotspots

Prioritized list of enforcement zones.

### Peak Violation Windows

Time-based recommendations for deployment.

### Congestion Severity Scores

Assessment of how disruptive each hotspot is.

### PICRI Rankings

Final enforcement priority list.

# Conclusion

This project demonstrates how spatial clustering, temporal analytics, and machine learning can be combined to transform raw parking violation records into actionable enforcement intelligence.

By identifying parking hotspots, estimating their congestion severity, and generating a Parking-Induced Congestion Risk Index (PICRI), the system enables data-driven, targeted enforcement strategies that can significantly improve urban traffic management.
