from datetime import datetime
import json

def calculate_delay(original, delay):
    """
        Calculate the delay
    """
    original = datetime.strptime(original, '%H:%M')
    delayed = datetime.strptime(delay, '%H:%M')
    diff = delayed - original
    return diff.total_seconds() // 60

def json_test():
    result = "123"
    with open("/Users/dth/Documents/record.json", "w") as file:
        json.dump(result, file)


def main():
    # print(calculate_delay('14:30', '14:32'))
    print(datetime.date(datetime.now()))
if __name__=="__main__":
    main()