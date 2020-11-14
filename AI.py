import requests

def CheckSpam(message):
    if len(message) > 700:
        message = message[:700]

    # This function will pass your text to the machine learning model
    # and return the top result with the highest confidence
    def classify(text):
        key = str(open("AI_API_KEY.txt", "r", encoding="utf-8").readline())
        url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/classify"

        response = requests.get(url, params={"data": text})

        if response.ok:
            responseData = response.json()
            topMatch = responseData[0]
            return topMatch
        else:
            response.raise_for_status()

    # CHANGE THIS to something you want your machine learning model to classify
    demo = classify(str(message))

    class_name = demo["class_name"]
    confidence = demo["confidence"]

    if (class_name == "Spam"):
        # CHANGE THIS to do something different with the result
        return confidence
    else:
        return 0