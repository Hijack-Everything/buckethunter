
# 🚀 BucketHunter

BucketHunter is your friendly tool in discovering and analyzing cloud storage buckets! This project makes exploring AWS S3, GCP Storage, Azure Blob, DigitalOcean Spaces, and Alibaba Cloud OSS buckets simple and efficient. It even lets you peek inside accessible buckets to uncover files and valuable insights. 🔍


## ☁️ Supported Storages

BucketHunter supports discovering and analyzing buckets on the following platforms:

- **AWS S3**  
- **Azure Blob Storage**  
- **Google Cloud Storage (GCP)**  
- **DigitalOcean Spaces**  
- **Alibaba Cloud OSS**  


## 🌟 Features at a Glance

✅ **Cloud Bucket Discovery**: Detect AWS S3, GCP Storage, Azure Blob, DigitalOcean Spaces, and Alibaba Cloud OSS buckets.  
✅ **GrayHatWarfare Search**: Search cloud buckets using keywords derived from company names.  
✅ **Finding Files in Buckets**: List and analyze files stored within discovered buckets (based on permissions).  
✅ **Find Company Names**: Extract company names using two methods:  
- **Google Custom Search Engine API**: For accurate and efficient name extraction (recommended).  
- **Fallback Scraping**: A non-API method to find company names.  


## 📦 Installation

### 🛠️ Prerequisites
- **Python 3.8+**
- **pip** (Python package manager)

### ⚙️ Get Started
1. Clone the repository:
   ```bash
   git clone https://github.com/Hijack-Everything/Bucket-Hunter.git
   cd Bucket-Hunter
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## 🚦 How to Use

Run the tool with `main.py` and explore its powerful options!

### 🔧 Command-Line Options

| **Option**           | **Description**                                                                          |
|-----------------------|------------------------------------------------------------------------------------------|
| `-d, --domain`        | Analyze a single domain (e.g., `-d example.com`).                                        |
| `-l, --list`          | Analyze multiple domains from a file (e.g., `-l domains.txt`).                          |
| `-g, --grayhatwarfare`| Enable GrayHatWarfare bucket search.                                                     |
| `-a, --all`           | Perform all actions (scanning and GrayHatWarfare search).                               |
| `-cf, --config-file`  | Provide a config file for API keys to enable Google Custom Search API for finding company names (recommended). |
| `-t, --threads`       | Set the number of threads for faster bucket scanning (default: 100).                     |
| `-o, --output`        | Specify the output file name to save results in JSON format.                             |

### ⚡ Examples

1. **Analyze a Single Domain**:
   ```bash
   python main.py -d example.com
   ```

2. **Analyze Domains from a List**:
   ```bash
   python main.py -l domains.txt
   ```

3. **Use Google API for Company Name Extraction and Search GrayHatWarfare (Recommended)**:
   ```bash
   python main.py -d example.com -cf config.json -g
   ```
   _Note: Name finding is done only while searching in GrayHatWarfare with keywords._

4. **Perform All Actions**:
   ```bash
   python main.py -d example.com -a
   ```

5. **Save Results as JSON**:
   ```bash
   python main.py -d example.com -o results.json
   ```


## 💡 Behind the Scenes

BucketHunter is built with a modular architecture. Each module handles a specific task, making the tool powerful yet easy to extend. Here’s what’s under the hood:

- **`scanners/`**: Finds cloud buckets for AWS, GCP, Azure, DigitalOcean, and Alibaba Cloud.
- **`grayhatwarfare/`**: Searches GrayHatWarfare buckets.
- **`company_name/`**:
   - **Google API**: Extracts company names with efficiency using the Google Custom Search Engine API.
   - **Fallback Scraping**: Uses HTML scraping as a backup if API keys are unavailable.
- **`bucket_files/`**: Retrieves and lists files stored within buckets (if accessible).


## 🌟 Upcoming Features

🔜 **More Output Options**: Support for custom file formats such as `.csv`, `.txt`, and more.  
🔜 **Better Terminal Presentation**: Enhanced tabular and color-coded outputs for easier readability.  


## ⚠️ Known Limitations

- **False Positives in GrayHatWarfare Search**: The tool may return false positives when performing GrayHatWarfare searches, as it relies on reverse searching with company names extracted from domain keywords.


## 🌍 Contributions & Support

Have ideas for improvements or new features? Contributions are welcome! Feel free to open an issue or submit a pull request to help make BucketHunter even better.  

If you like the project, don’t forget to **star this repository** to show your support. ⭐  


## 🙌 Credits & References

A special thanks to **[GrayHatWarfare](https://grayhatwarfare.com/)** for their amazing tools and APIs.  
We highly recommend exploring their **paid APIs** for powerful and feature-rich solutions that can take your cloud storage exploration to the next level!  


## 📜 License

BucketHunter is licensed under the [MIT License](LICENSE).

## 🚀 Ready to Hunt?

Start exploring and uncover the hidden treasures of the cloud. 🕵️‍♂️
