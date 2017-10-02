import os

if __name__ == "__main__":
    try:
        os.system("python bot_impl.py")
    except Exception as e:
        print(str(e))
        os.system("python main.py")
