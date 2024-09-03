# LSTM Time series neural network model

## Overview

- LSTM, long short-term memory, is a type of recurrent neural network (RNN) that is capable of learning long-term dependencies.
- It is developed to overcome the limitations of traditional RNNs, such as the vanishing gradient problem, which makes it difficult for RNNs to learn from long sequences.

**Data Dictionary**

| Variable | Definition |
| --- | --- |
| timestamp | Date and minute |
| open | Price at the beginning of the minute |
| high | Highest price within the minute |
| low | Lowest price within the minute |
| close | Price at the end of the minute |
| volume| Trading volume (amount) |
| close_time | Closing timestamp |
| quote_asset_volume| Trading volume (value) |
| number_of_trades | Number of trades |
| taker_buy_base_asset_volume| Taker buy volume (amount) |
| taker_buy_quote_asset_volume | Taker buy volume (value) |
| ignore | Unused field |

</br>

## Section 1. Data Transformation

The original dataset is in 1-minute interbal. We created 5min, hourly, daily, weekly, and monthly datasets.

</br>
The dataset length is shown below:
- 5_min dataset length: 740725
- Hourly dataset length: 61728
- Daily dataset length: 2573
- Weekly dataset length: 368
- Monthly dataset length: 86

</br>
Also, we created a moving ave

