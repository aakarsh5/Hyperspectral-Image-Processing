import sys
import os
import numpy as np
import spectral
import cv2
import json
from spectral import open_image
from skimage.feature import graycomatrix, graycoprops
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def prepare(folder_name):
    # Base paths
    input_dir = "../uploads"
    extracted_folder = os.path.join(input_dir, folder_name)

    if not os.path.exists(extracted_folder):
        raise FileNotFoundError(f"Folder '{extracted_folder}' not found!")

    # Load hyperspectral data
    hdr_file = os.path.join(extracted_folder, f"{folder_name}_capture_{folder_name}.hdr")
    white_ref_file = os.path.join(extracted_folder, f"{folder_name}_capture_WHITEREF_{folder_name}.hdr")
    dark_ref_file = os.path.join(extracted_folder, f"{folder_name}_capture_DARKREF_{folder_name}.hdr")

    SCraw = spectral.open_image(hdr_file).load()
    white_reference = spectral.open_image(white_ref_file).load()
    dark_reference = spectral.open_image(dark_ref_file).load()

    # Perform calibration
    calibrated_data = (SCraw - dark_reference) / (white_reference - dark_reference + 1e-10)

    # Apply PCA to generate a binary mask
    pca = PCA(n_components=3)
    reshaped_image = calibrated_data.reshape(-1, calibrated_data.shape[2])
    pca_result = pca.fit_transform(reshaped_image)
    pca_image = pca_result.reshape(calibrated_data.shape[0], calibrated_data.shape[1], 3)

    # Normalize PCA image
    pca_image_normalized = np.zeros_like(pca_image)
    for i in range(3):
        pca_image_normalized[:, :, i] = cv2.normalize(
            pca_image[:, :, i], None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Generate binary mask
    selected_channel = pca_image_normalized[:, :, 1]
    _, mask = cv2.threshold(selected_channel, 100, 255, cv2.THRESH_BINARY)
    mask = mask.astype(bool)
    
    # Save binary mask as an image
    mask_path = os.path.join("../processed/", f"{folder_name}_binary_mask.png")
    cv2.imwrite(mask_path, (mask * 255).astype(np.uint8))
    print(f"Binary mask saved at: {mask_path}")

    # Apply mask to hyperspectral image
    masked_image = calibrated_data * mask[..., np.newaxis]

    # Feature extraction
    def extract_std_features(masked_image):
        num_bands = masked_image.shape[2]
        mean_intensities, std_intensities = [], []
        contrasts, entropies, energies, homogeneities = [], [], [], []

        for band_idx in range(num_bands):
            band = masked_image[:, :, band_idx]
            if band.ndim != 2 or np.count_nonzero(band) == 0:
                continue

            mean_intensity = np.mean(band)
            std_intensity = np.std(band)
            band_8bit = ((band - band.min()) / (band.max() - band.min()) * 255).astype(np.uint8)

            glcm = graycomatrix(band_8bit, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
            contrast = graycoprops(glcm, 'contrast')[0, 0]
            entropy = -np.sum(glcm * np.log2(glcm + (glcm == 0)))  
            energy = graycoprops(glcm, 'energy')[0, 0]
            homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]

            mean_intensities.append(mean_intensity)
            std_intensities.append(std_intensity)
            contrasts.append(contrast)
            entropies.append(entropy)
            energies.append(energy)
            homogeneities.append(homogeneity)

        features = [
            np.std(mean_intensities), np.std(std_intensities), np.std(contrasts),
            np.std(entropies), np.std(energies), np.std(homogeneities)
        ]

        scaler = StandardScaler()
        features_standardized = scaler.fit_transform(np.array(features).reshape(-1, 1)).flatten()

        return features_standardized

    features_list = extract_std_features(masked_image)

    # Save extracted features as JSON
    features_data = {
        "folder_name": folder_name,
        "features": features_list.tolist(),  # Convert NumPy array to list
        "binary_mask_path": mask_path
    }

    features_json_path = os.path.join("../processed/", f"{folder_name}_features.json")
    with open(features_json_path, "w") as json_file:
        json.dump(features_data, json_file, indent=4)

    print(f"Extracted Features saved at: {features_json_path}")

    return features_data  # Return as an object for further processing

# Example usage:
# result = prepare('1600')
# print(result)
