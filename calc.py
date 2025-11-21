import importer

if __name__ == "__main__":
    while True:
        try:
            expr = input("calc> ")
            if expr.lower() == "exit":
                break
            if not expr.strip():
                continue

            result = importer.evaluate(expr)
            print(result)

        except Exception as e:
            print("Error:", e)
