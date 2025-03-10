import sys
import os
import numpy as np
import spectral
import cv2
from spectral import open_image
from skimage.feature import graycomatrix, graycoprops
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# ✅ Read folder name from command-line arguments
# if len(sys.argv) < 2:
#     print("Error: No folder name provided.")
#     folder_name = "1600"
# else:
#     folder_name = sys.argv[1]

def prepare(folder_name):

    
    # Get the folder name from the command line
    print(f"Processing folder from PrepareData: {folder_name}")

    # ✅ Base paths
    input_dir = "../uploads"  # Ensure it matches server.py
    extracted_folder = os.path.join(input_dir, folder_name)
    print(f"Extracted folder path: {extracted_folder}")
    
    # Debug: Print current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Debug: List contents of the uploads directory
    if os.path.exists(input_dir):
        print(f"Contents of '{input_dir}': {os.listdir(input_dir)}")
    else:
        print(f"Directory '{input_dir}' does not exist.")
    
    # ✅ Ensure the folder exists
    if not os.path.exists(extracted_folder):
        raise FileNotFoundError(f"Folder '{extracted_folder}' not found!")
    else:
        print(f"Folder '{extracted_folder}' exists.")
    
    # Debug: List contents of the extracted folder
    capture_folder = extracted_folder
    if os.path.exists(capture_folder):
        print(f"Contents of '{capture_folder}': {os.listdir(capture_folder)}")
    else:
        print(f"Directory '{capture_folder}' does not exist.")
    
    # ✅ Load hyperspectral data
    hdr_file = os.path.join(capture_folder, f"{folder_name}_capture_{folder_name}.hdr")
    white_ref_file = os.path.join(capture_folder, f"{folder_name}_capture_WHITEREF_{folder_name}.hdr")
    dark_ref_file = os.path.join(capture_folder, f"{folder_name}_capture_DARKREF_{folder_name}.hdr")
    
    print(f"hdr_file path: {hdr_file}")
    print(f"white_ref_file path: {white_ref_file}")
    print(f"dark_ref_file path: {dark_ref_file}")
    
    SCraw = spectral.open_image(hdr_file).load()
    white_reference = spectral.open_image(white_ref_file).load()
    dark_reference = spectral.open_image(dark_ref_file).load()
    
    # ✅ Perform calibration
    calibrated_data = (SCraw - dark_reference) / (white_reference - dark_reference + 1e-10)
    
    # ✅ Generate binary mask using PCA
    pca = PCA(n_components=3)
    reshaped_image = calibrated_data.reshape(-1, calibrated_data.shape[2])
    pca_result = pca.fit_transform(reshaped_image)
    pca_image = pca_result.reshape(calibrated_data.shape[0], calibrated_data.shape[1], 3)
    
    pca_image_normalized = np.zeros_like(pca_image)
    for i in range(3):
        pca_image_normalized[:, :, i] = cv2.normalize(
            pca_image[:, :, i], None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    selected_channel = pca_image_normalized[:, :, 1]
    _, mask = cv2.threshold(selected_channel, 100, 255, cv2.THRESH_BINARY)
    
    mask = mask.astype(bool)
    masked_image = calibrated_data * mask[..., np.newaxis]
    
    # ✅ Extract standard deviation features
    def extract_std_features(masked_image):
        num_bands = masked_image.shape[2]
        mean_intensities, std_intensities = [], []
        contrasts, entropies, energies, homogeneities = [], [], [], []
    
        for band_idx in range(num_bands):
            band = masked_image[:, :, band_idx]
            if band.ndim != 2 or np.count_nonzero(band) == 0:
                print(f"Skipping band {band_idx}: Invalid or empty band.")
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
    
    print(f"Extracted Features for {folder_name}: {features_list}")

# python -c "from PrepareData import prepare; prepare('1600')"
