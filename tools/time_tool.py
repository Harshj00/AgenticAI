from datetime import datetime

def excecute(argument: dict):
    now = datetime.now()
    return now.strftime("%d-%m-%Y %I:%M:%S %p")


if __name__ == "__main__":
    print("time tool\n")
    print(
        excecute(
            {
                
            }
        )
    )

