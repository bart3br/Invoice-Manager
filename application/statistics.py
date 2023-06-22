import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def avg_expenses_per_month(data, year):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']
    #filtered_data = [d for d in data if d['date'].year == year]
    monthly_averages = {}
    for d in data:
        month = d['date'].month
        amount = d['amount']
        if month in monthly_averages:
            monthly_averages[month].append(amount)
        else:
            monthly_averages[month] = [amount]
            
    for month, amounts in monthly_averages.items():
        monthly_averages[month] = sum(amounts) / len(amounts)
    months = range(1, 13)
    average_amounts = [monthly_averages.get(month, 0) for month in months]

    plt.bar(months, average_amounts)
    plt.xlabel('Month')
    plt.ylabel('Average Amount')
    plt.title(f'Average Amounts for Year {year}')
    plt.xticks(months)
    plt.grid(True)
    
    fig = plt.gcf()
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    plt.close()
    return image


    
def test():
    data = [{'date': datetime(2020, 1, 1), 'amount': 100}, {'date': datetime(2020, 1, 1), 'amount': 200},
            {'date': datetime(2020, 2, 1), 'amount': 300}, {'date': datetime(2020, 2, 1), 'amount': 400},
            {'date': datetime(2020, 3, 1), 'amount': 500}, {'date': datetime(2020, 3, 1), 'amount': 600},
            {'date': datetime(2020, 4, 1), 'amount': 700}, {'date': datetime(2020, 4, 1), 'amount': 800},
            {'date': datetime(2020, 5, 1), 'amount': 900}, {'date': datetime(2020, 5, 1), 'amount': 1000}]    
    avg_expenses_per_month(data, 2020)

if __name__ == '__main__':
    pass