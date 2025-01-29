import React from "react";
import "./Home.css";

const Home = () => {
  return (
    <div className="home">
      <header className="home-header">
        <h1>Welcome to Pesticide Detection</h1>
        <p>
          Your ultimate solution for detecting pesticide residues on apples
          using advanced hyperspectral imaging technology.
        </p>
      </header>
      <section className="home-features">
        <h2>Features</h2>
        <ul>
          <li>Fast and accurate pesticide residue detection.</li>
          <li>Detailed analysis and visualization of results.</li>
          <li>Helps ensure safe and healthy produce.</li>
          <li>Supports multiple pesticide types and concentrations.</li>
        </ul>
      </section>
      <section className="home-about">
        <h2>About Our Technology</h2>
        <p>
          Our platform leverages cutting-edge hyperspectral imaging technology
          to analyze the surface of apples and detect pesticide residues with
          high precision. This ensures that you can monitor and maintain the
          quality of your produce effectively.
        </p>
      </section>
      <section className="home-process">
        <h2>Process Explanation</h2>
        <ol>
          <li>
            <strong>Step 1: Capturing Hyperspectral Images</strong>
            <p>
              We begin by taking hyperspectral images of apples using advanced
              cameras that capture a wide range of wavelengths beyond human
              vision.
            </p>
          </li>
          <li>
            <strong>Step 2: Preprocessing the Data</strong>
            <p>
              The raw hyperspectral data is preprocessed to remove noise,
              correct lighting variations, and normalize the spectral signatures
              for accurate analysis.
            </p>
          </li>
          <li>
            <strong>Step 3: Feature Extraction</strong>
            <p>
              Key spectral features are extracted from the hyperspectral data,
              focusing on specific wavelengths that indicate the presence of
              pesticide residues.
            </p>
          </li>
          <li>
            <strong>Step 4: Pesticide Detection</strong>
            <p>
              A machine learning model analyzes the extracted features to
              classify whether the apple's surface contains pesticide residues
              and their concentration levels.
            </p>
          </li>
          <li>
            <strong>Step 5: Visualization of Results</strong>
            <p>
              The detection results are presented visually, highlighting areas
              on the apple where pesticide residues are detected, along with a
              detailed report.
            </p>
          </li>
        </ol>
      </section>
      <footer className="home-footer">
        <p>Empowering farmers and consumers for a healthier tomorrow.</p>
      </footer>
    </div>
  );
};

export default Home;
