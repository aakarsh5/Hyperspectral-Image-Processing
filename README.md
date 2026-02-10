#  Pesticide Residue Detection Using Hyperspectral Image Processing

## Project Overview

This project focuses on detecting and analyzing **pesticide residues on apple surfaces** using **hyperspectral image processing**. Hyperspectral imaging captures rich **spectral and spatial information**, enabling the identification of chemical residues that are not visible in standard RGB images.

The project aims to **classify and analyze pesticide concentration levels** using hyperspectral data acquired over multiple days.

---

## Objectives

- Capture hyperspectral images using a **Specim IQ hyperspectral camera**
- Preprocess hyperspectral images to remove noise and redundant spectral bands
- Extract spectral signatures associated with pesticide residues
- Analyze residue concentration variations over time
- Build machine learning / deep learning models for residue detection
- Differentiate between **low** and **high** pesticide concentration samples

---

## Dataset Description

- **Fruit:** Apples  
- **Imaging Device:** Specim IQ Hyperspectral Camera  
- **Spectral Range:** Visible–Near Infrared (VNIR)  
- **Classes:**
  - No pesticide (baseline)
  - Low pesticide concentration
  - High pesticide concentration
- **Data Collection Period:** 7 days  
- **Total Samples:** Multiple apples captured daily  

Each hyperspectral image folder contains:
- `capture/`
- `metadata/`
- `results/`
- PNG preview image
- `manifest.json`
- `validate.json`

---

## Tech Stack

- **Programming Language:** Python  
- **Libraries & Tools:**
  - NumPy
  - SciPy
  - OpenCV
  - scikit-learn
  - matplotlib
  - Spectral Python (SPy)
  - TensorFlow / PyTorch (optional)
- **IDE:** Visual Studio Code  

---

##  Methodology

1. **Data Acquisition**
   - Capture hyperspectral images using Specim IQ

2. **Preprocessing**
   - Noise removal
   - Spectral band selection
   - Normalization
   - Smoothing

3. **Feature Extraction**
   - Pixel-wise spectral signatures
   - Mean reflectance curves
   - PCA / dimensionality reduction

4. **Modeling**
   - Machine Learning (SVM, Random Forest)
   - Deep Learning (CNN / 3D-CNN – optional)

5. **Evaluation**
   - Accuracy
   - Precision
   - Recall
   - Confusion Matrix

---
