class HkseOmdcConnector:
    def __init__(self):
        # Save IP
        pass

    def connect():
        return False

if __name__ == "__main__":
    config = {'channel1': None, 'channel2': None}

    connector = HkseOmdcConnector(config)

    if not connector.connect():
        print("Failed to connect")
        exit(1)

    # Start reading market data in while-loop
