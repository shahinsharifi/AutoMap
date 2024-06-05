# Detecting, Classifying, and Mapping Retail Storefronts

This repository contains the implementation of the paper "Detecting, classifying, and mapping retail storefronts using street-level imagery" by Shahin Sharifi Noorian, Sihang Qiu, Achilleas Psyllidis, Alessandro Bozzon, and Geert-Jan Houben. The paper was presented at the 2020 International Conference on Multimedia Retrieval.

The project introduces a novel method for automatically detecting, geo-locating, and classifying retail stores and related commercial functions, on the basis of storefronts extracted from street-level imagery. It presents a deep learning approach that takes storefronts from street-level imagery as input, and directly provides the geo-location and type of commercial function as output.

## Repository Structure

The repository is structured as follows:

- [``crowdsourcing/``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Fcrowdsourcing%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/crowdsourcing/"): Contains the Angular project for crowdsourcing.
- [``input/``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Finput%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/input/"): Directory for input data.
- [``labels/``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Flabels%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/labels/"): Contains label files like `categories.txt` and [``google_label.txt``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Flabels%2Fgoogle_label.txt%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/labels/google_label.txt").
- [``location_estimator/``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Flocation_estimator%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/location_estimator/"): Contains Python scripts for location estimation.
- [``main_video.py``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Fmain_video.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/main_video.py"): Main script for video processing.
- [``main.py``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/main.py"): Main script for image processing.
- [``model_weights``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Fmodel_weights%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/model_weights"): Directory for model weights.
- [``shop_detector/``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Fshop_detector%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/shop_detector/"): Contains Python scripts for shop detection.
- [``shop_recognizer/``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Fshop_recognizer%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/shop_recognizer/"): Contains Python scripts for shop recognition.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Angular CLI 8.3.21 or higher

### Installation

1. Clone the repository.
2. Install Python dependencies: `pip install -r requirements.txt`.
3. Navigate to the [``crowdsourcing/``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Fcrowdsourcing%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/crowdsourcing/") directory and install Angular dependencies: `npm install`.

### Usage

#### Image Processing

Run `python main.py` to start the image processing.

#### Video Processing

Run `python main_video.py` to start the video processing.

#### Crowdsourcing

Navigate to the [``crowdsourcing/``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Fcrowdsourcing%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/crowdsourcing/") directory.

1. Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.
2. Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Testing

Navigate to the [``crowdsourcing/``](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fshahin%2FDocuments%2FPhD%2FCode%2FAutoMap%2Fcrowdsourcing%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/shahin/Documents/PhD/Code/AutoMap/crowdsourcing/") directory.

- Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).
- Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Citation

If you use this code in your research, please cite the paper:

```bibtex
@inproceedings{sharifi2020detecting,
  title={Detecting, classifying, and mapping retail storefronts using street-level imagery},
  author={Sharifi Noorian, Shahin and Qiu, Sihang and Psyllidis, Achilleas and Bozzon, Alessandro and Houben, Geert-Jan},
  booktitle={Proceedings of the 2020 international conference on multimedia retrieval},
  pages={495--501},
  year={2020}
}
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.