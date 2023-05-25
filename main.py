
import requests
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import webbrowser

sg.theme('PythonPlus')


def generate_share_url(leaderboard_data):
    base_url = "https://twitter.com/intent/tweet?text="
    tweet_text = "Check out the Crypto Price Prediction leaderboard!%0A%0A"

    for i, entry in enumerate(leaderboard_data):
        tweet_text += f"{i+1}. {entry[1]} - {entry[2]} - Accuracy: {entry[3]:.2f}%25%0A"

    tweet_text += "%0AJoin the game and try to beat the top scores!%0A%23CrypTool%20%23CryptoPricePrediction"
    share_url = base_url + tweet_text

    return share_url
  
def get_current_price(crypto_id):
  url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
  response = requests.get(url)
  data = response.json()
  if crypto_id in data:
    return data[crypto_id]["usd"]
  else:
    return None

def calculate_accuracy(predicted_price, actual_price):
  deviation = abs(predicted_price - actual_price)
  if actual_price == 0:
    return 0
  accuracy = max(0, 100 - (deviation / actual_price) * 100)
  return accuracy

def visualize_accuracy(prediction_history):
  usernames = [entry["Username"] for entry in prediction_history]
  accuracies = [entry["Accuracy"] for entry in prediction_history]
 
  fig, ax = plt.subplots()
  ax.bar(usernames, accuracies)
  ax.set_xlabel("Usernames")
  ax.set_ylabel("Accuracy (%)")
  ax.set_title("Prediction Accuracy per User")
  plt.xticks(rotation=45)
  plt.tight_layout()
 
  return fig

def start_game():
  layout = [
    [sg.Text("CrypTool", font=("Helvetica", 16))],
    [sg.Text("1. Predict Crypto Price"), sg.Button("Start Game")],
    [sg.Text("2. Convert between Cryptos"), sg.Button("Convert")],
    [sg.Button("Exit")]
  ]

  window = sg.Window("Main Menu", layout)

  while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
      break
    if event == "Start Game":
      crypto_choices = ["bitcoin", "ethereum", "ripple", "xrp", "cardano", "dogecoin", "polygon", "solana", "litecoin", "tron", "polkadot"]

      game_layout = [
        [sg.Text("Username:"), sg.Input(key="-USERNAME-", default_text="")],
        [sg.Text("Cryptocurrency:"), sg.Combo(crypto_choices, key="-CRYPTO-")],
        [sg.Text("Predicted Price:"), sg.Input(key="-PREDICTION-")],
        [sg.Button("Submit"), sg.Button("Visualize Accuracy"), sg.Button("Share on Twitter"), sg.Button("Back")],
        [sg.Text(size=(20, 1), key="-RESULT-")],
        [sg.Text("Leaderboard")],
        [sg.Table(values=[], headings=["Place", "Username", "Cryptocurrency", "Accuracy", "      Time      ", "Predicted Price", "Actual Price"],
             key="-LEADERBOARD-", justification="center", size=(40, 10))],
        [sg.Canvas(key="-CANVAS-", pad=(10, 10))],
      ]

      game_window = sg.Window("Crypto Price Prediction Game", game_layout)

      prediction_history = []
      leaderboard_data = []
      if event == "Share on Twitter":
        share_url = generate_share_url(leaderboard_data)
        webbrowser.open(share_url)
      while True:
        event, values = game_window.read()

        if event == sg.WINDOW_CLOSED or event == "Back":
          break

        username = values["-USERNAME-"]
        crypto_id = values["-CRYPTO-"]
        predicted_price = float(values["-PREDICTION-"])
        current_price = get_current_price(crypto_id)

        if current_price is not None:
          accuracy = calculate_accuracy(predicted_price, current_price)
          result_text = f"Current Price: ${current_price:.2f} | Accuracy: {accuracy:.2f}%"
          prediction_history.append(
            {
              "Username": username,
              "Cryptocurrency": crypto_id,
              "Predicted Price": predicted_price,
              "Actual Price": current_price,
              "Accuracy": accuracy,
              "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Add the current time of prediction
            }
          )
          leaderboard_data = [
            (i+1, entry["Username"], entry["Cryptocurrency"].capitalize(), entry["Accuracy"], entry["Time"], entry["Predicted Price"], entry["Actual Price"])
            for i, entry in enumerate(sorted(prediction_history, key=lambda x: x["Accuracy"], reverse=True)[:10])
          ] # Select top 10 entries

        else:
          result_text = "Failed to fetch price data."

        game_window["-RESULT-"].update(result_text)
        game_window["-LEADERBOARD-"].update(values=leaderboard_data)

        if event == "Visualize Accuracy":
          fig = visualize_accuracy(prediction_history)

          game_window["-CANVAS-"].TKCanvas.delete("all")

          canvas = FigureCanvasTkAgg(fig, master=game_window["-CANVAS-"].TKCanvas)
          canvas.draw()
          canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

      game_window.close()

    if event == "Convert Crypto":
      crypto_choices = ["bitcoin", "ethereum", "ripple", "xrp", "cardano", "dogecoin", "polygon", "solana", "litecoin", "tron", "polkadot"]

      convert_layout = [
        [sg.Text("Convert Crypto", font=("Helvetica", 16))],
        [sg.Text("From Cryptocurrency:"), sg.Combo(crypto_choices, key="-FROM_CRYPTO-")],
        [sg.Text("To Cryptocurrency:"), sg.Combo(crypto_choices, key="-TO_CRYPTO-")],
        [sg.Text("Amount to Convert:"), sg.Input(key="-AMOUNT-")],
        [sg.Button("Convert"), sg.Button("Back")],
        [sg.Text(size=(30, 1), key="-CONVERSION_RESULT-")]
      ]

      convert_window = sg.Window("Convert Crypto", convert_layout)

      while True:
        event, values = convert_window.read()

        if event == sg.WINDOW_CLOSED or event == "Back":
          break

        from_crypto = values["-TO_CRYPTO-"]
        to_crypto = values["-FROM_CRYPTO-"]
        amount = float(values["-AMOUNT-"])
        from_price = get_current_price(from_crypto)
        to_price = get_current_price(to_crypto)

        if from_price is not None and to_price is not None:
          converted_amount = amount / from_price * to_price
          result_text = f"{amount:.6f} {to_crypto} = {converted_amount:.6f} {from_crypto}"
        else:
          result_text = "Failed to fetch price data."
          
        if event == "Share on Twitter":
          share_url = generate_share_url(leaderboard_data)
          webbrowser.open(share_url)
        convert_window["-CONVERSION_RESULT-"].update(result_text)

      convert_window.close()

  window.close()


# Run the main menu
start_game()
