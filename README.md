# Market Strength Prediction with Machine Learning

This project explores building a machine learning model to predict market strength using various technical indicators. While technical indicators alone may not be ideal for this task, it serves as a practical exercise for applying machine learning concepts.

## Motivation

As a beginner in machine learning , this project aims to demonstrate my skills .

## TODO

* **Refine Feature Engineering:** Implement more meaningful alpha .
* **Hyperparameter Optimization:** Conduct a grid search or other optimization techniques to find the optimal model hyperparameters.
* **Real-World Testing:** Evaluate the model's performance in a live trading environment or through backtesting with realistic market simulations.

## Technical Indicators

The following indicators, sourced from TradingView, are used as features:

* **PrasiGanFanFib:** [https://www.tradingview.com/script/TvkU7Pav-PrasiGanFanFib/](https://www.tradingview.com/script/TvkU7Pav-PrasiGanFanFib/) (Extrema points are extracted)
* **Gann High Low:** [https://www.tradingview.com/script/XNQSLIYb-Gann-High-Low/](https://www.tradingview.com/script/XNQSLIYb-Gann-High-Low/)
* **RSI (14/7):** [https://www.tradingview.com/support/solutions/43000502338/](https://www.tradingview.com/support/solutions/43000502338/)
* **Gann Swing Chart (One Bar):** [https://www.tradingview.com/script/R7VWnhIV-Gann-Swing-Chart-One-Bar/](https://www.tradingview.com/script/R7VWnhIV-Gann-Swing-Chart-One-Bar/) (Used to determine up/down day )
