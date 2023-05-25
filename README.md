CrypTool

CrypTool is a Python application that allows users to predict cryptocurrency prices and convert between different cryptocurrencies. It utilizes the CoinGecko API to fetch real-time cryptocurrency prices and provides a leaderboard to track user predictions.

Features:

- Predict Crypto Price: Users can enter their username, select a cryptocurrency, and predict its price. The application retrieves the current price and calculates the accuracy of the prediction.

- Visualize Accuracy: Users can visualize the accuracy of predictions using a bar chart. The chart displays the usernames on the x-axis and the prediction accuracies on the y-axis.

- Convert Crypto: Users can convert between different cryptocurrencies. They can select the source and target cryptocurrencies, specify the amount to convert, and the application will calculate the converted amount based on the current prices.

- Leaderboard: The application maintains a leaderboard that displays the top 10 predictions based on accuracy. It shows the username, cryptocurrency, accuracy, prediction time, predicted price, and actual price.

Dependencies:

- requests
- PySimpleGUI
- matplotlib

Install the dependencies using pip:

pip install requests PySimpleGUI matplotlib

Usage:

Run the start_game() function to launch the application and open the main menu. From there, you can select the desired options:

- Predict Crypto Price: Enter your username, select a cryptocurrency, and predict its price.

- Convert Crypto: Convert between different cryptocurrencies by selecting the source and target cryptocurrencies and specifying the amount to convert.

- Exit: Close the application.

Known Issues:

- Occasionally, the CoinGecko API may not respond or provide inaccurate data. If you encounter any issues, please try again later.

Contributing:

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

License:

This project is licensed under the MIT License.
