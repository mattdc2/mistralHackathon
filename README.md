# Mistral Driver

The goal of this project is to find a way to use Mistral as an autonomous driving simulator. 
The project is divided into two parts: the first part is to create a simple autonomous driving simulator using pygame and the second part is to use Mistral as the autonomous driving simulator.

## Getting Started

Clone the repository and run the following command to install the required packages.

```
pip install -r requirements.txt
```

To use Mistral as the autonomous driving simulator, you need to provide a Mistral API key. You can get the API key by signing up on the Mistral website.

Create a .env file in the root directory and add the following line to the file.
```
MISTRAL_API_KEY=<your_mistral_api_key>
```

## Running the simulator

You can use two modes to run the simulator: manual and autonomous.

```
python main.py --mode=autonomous
```

