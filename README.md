# CAB

CAB is a Python program that can detect arbitrage and output a router for it. The router consists of multiple buy and sell processes from different exchanges. Users have the choice to follow the instructions and execute transactions, generating potential profit. Its features include:
- The Arbitrage Strategy Computation
- API Options
- Transaction Link Filters
- History Export

## Run the Executable
To run the executable version of the application, you can either download the source code and run the python files yourself or run the precompiled exe file in the .zip file provided in the releases page.

To run the precompiled file, download the .zip file from the releases page and extract it. Run the `main.exe` file in order to start the program.

To view the source code, see below.

## Installation
To install CAB, you need to have python 3.10.x

Head over to the releases page and download the latest release.

Open a terminal to the directory that you downloaded the release to and run the command `pip install -r requirements.txt --user`

To run the program, run the command `python main.py`

## Usage

To begin using CAB, select a crypto exchange. Once an exchange has been selected, then click "Retrieve Data" to
retrieve data from the API and diplay profitable links for that API.

![selectapi](https://user-images.githubusercontent.com/79658547/183536131-98f30020-ce86-4ecd-be1a-83e723dc926d.png)
![home](https://user-images.githubusercontent.com/79658547/183536159-0e8efbfa-7813-459d-a9bd-83018aebc380.png)


Visit the History tab to view all of the links generated this session. You can sort the history by Time, Exchange, and Profitability, Ascending or Descending.

![history](https://user-images.githubusercontent.com/79658547/183536172-40665075-19ed-4d45-8f51-ba80ffbb1762.png)


You can export the history into your Downloads folder for future use. The exported file will be saved as `history.xlsx`.

![exporthistory](https://user-images.githubusercontent.com/79658547/183536179-d8db1eda-9687-4850-b3ab-87de6128fef0.png)

You can also switch between light and dark mode for the application.
![lightmode](https://user-images.githubusercontent.com/79658547/183536230-728074cb-ec03-412f-afdd-23e6dda505fe.png)
![darkmode](https://user-images.githubusercontent.com/79658547/183536236-07337a88-e19c-417a-83dd-afd47d2c1fc7.png)
![darkmode2](https://user-images.githubusercontent.com/79658547/183536249-45bc7f6e-7229-49d2-b426-611b5b98e3f0.png)
